"""MCP stdio server for the local-software-launcher plugin.

Exposes tools to launch (programmatic double-click), resolve, search, list,
inspect, and stop installed Windows software, and to list mounted drives.
Pure standard library - no third-party dependencies.
"""

import ctypes
import json
import os
import shutil
import string
import subprocess
import sys
import winreg

SERVER_NAME = "local-software-launcher"
SERVER_VERSION = "1.0.0"

# ------------------------------------------------------------- win32 plumbing

_kernel32 = ctypes.windll.kernel32


# ---------------------------------------------------------------- resolution

def _start_menu_dirs():
    dirs = []
    program_data = os.environ.get("ProgramData")
    app_data = os.environ.get("APPDATA")
    if program_data:
        dirs.append(os.path.join(program_data, "Microsoft", "Windows", "Start Menu", "Programs"))
    if app_data:
        dirs.append(os.path.join(app_data, "Microsoft", "Windows", "Start Menu", "Programs"))
    return [d for d in dirs if os.path.isdir(d)]


def _app_paths(name):
    exe = name if name.lower().endswith(".exe") else name + ".exe"
    key_path = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\" + exe
    for root in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        try:
            with winreg.OpenKey(root, key_path) as key:
                value, _ = winreg.QueryValueEx(key, "")
                if value:
                    return value
        except OSError:
            continue
    return None


def _shortcuts(name, limit=5):
    wanted = name.lower()
    if not wanted.endswith(".lnk"):
        wanted += ".lnk"
    hits = []
    for base in _start_menu_dirs():
        for _dirpath, _dirnames, filenames in os.walk(base):
            for fname in filenames:
                if fname.lower() == wanted:
                    hits.append(os.path.join(base, fname))
                    if len(hits) >= limit:
                        return hits
    return hits


def resolve_program(name):
    matches = []
    which = shutil.which(name)
    if which:
        matches.append({"source": "PATH", "path": which})
    app_path = _app_paths(name)
    if app_path:
        matches.append({"source": "AppPaths", "path": app_path})
    for lnk in _shortcuts(name):
        matches.append({"source": "StartMenu", "path": lnk})
    return matches


def _default_search_roots():
    roots = [
        os.environ.get("ProgramFiles", r"C:\Program Files"),
        os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs"),
        r"E:\tools",
        r"E:\apps",
    ]
    return roots


# --------------------------------------------------------------------- tools

def _popen_detached(target, args=None):
    """Start an executable without waiting for it; return its pid."""
    proc = subprocess.Popen(
        [target] + list(args or []),
        close_fds=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
    )
    return proc.pid


def tool_launch(program, args=None):
    if not isinstance(program, str) or not program.strip():
        raise RuntimeError("'program' must be a non-empty string")
    if "://" in program:
        os.startfile(program)
        return {"launched": program, "pid": None, "resolvedVia": "direct",
                "method": "os.startfile"}
    matches = [{"source": "direct", "path": program}] if os.path.exists(program) \
        else resolve_program(program)
    if not matches:
        raise RuntimeError(
            "program not found: %s (tried direct path, PATH, App Paths registry, "
            "Start Menu shortcuts; use 'search' for a broader lookup)" % program)
    path = matches[0]["path"]
    if path.lower().endswith(".exe"):
        pid = _popen_detached(path, args)
        return {"launched": path, "pid": pid, "resolvedVia": matches[0]["source"],
                "method": "Popen", "otherMatches": matches[1:]}
    os.startfile(path)
    return {"launched": path, "pid": None, "resolvedVia": matches[0]["source"],
            "method": "os.startfile", "otherMatches": matches[1:]}


def tool_search(query, roots=None, limit=25, max_depth=6):
    if not isinstance(query, str) or not query.strip():
        raise RuntimeError("'query' must be a non-empty string")
    needle = query.lower()
    hits = []
    for root in (roots if roots else _default_search_roots()):
        if not os.path.isdir(root):
            continue
        base_depth = root.rstrip("\\").count("\\")
        for dirpath, dirnames, filenames in os.walk(root):
            depth = dirpath.rstrip("\\").count("\\") - base_depth
            if depth >= max_depth:
                dirnames[:] = []
            for fname in filenames:
                low = fname.lower()
                if needle in low and low.endswith((".exe", ".lnk")):
                    hits.append(os.path.join(dirpath, fname))
                    if len(hits) >= int(limit):
                        return {"query": query, "count": len(hits), "matches": hits}
    return {"query": query, "count": len(hits), "matches": hits}


def tool_list_apps(query=None):
    names = set()
    for base in _start_menu_dirs():
        for _dirpath, _dirnames, filenames in os.walk(base):
            for fname in filenames:
                if fname.lower().endswith(".lnk"):
                    names.add(os.path.splitext(fname)[0])
    apps = sorted(names, key=str.lower)
    if query:
        needle = query.lower()
        apps = [a for a in apps if needle in a.lower()]
    return {"count": len(apps), "apps": apps[:300]}


_DRIVE_TYPES = {0: "UNKNOWN", 1: "NO_ROOT_DIR", 2: "REMOVABLE", 3: "FIXED",
                4: "REMOTE", 5: "CDROM", 6: "RAMDISK"}


def tool_list_drives():
    bitmask = _kernel32.GetLogicalDrives()
    drives = []
    for index, letter in enumerate(string.ascii_uppercase):
        if not (bitmask & (1 << index)):
            continue
        root = letter + ":\\"
        dtype = _kernel32.GetDriveTypeW(root)
        free = ctypes.c_ulonglong(0)
        total = ctypes.c_ulonglong(0)
        has_space = _kernel32.GetDiskFreeSpaceExW(
            root, ctypes.byref(free), ctypes.byref(total), None)
        entry = {"drive": root, "type": _DRIVE_TYPES.get(dtype, str(dtype))}
        if has_space:
            entry["freeBytes"] = free.value
            entry["totalBytes"] = total.value
        drives.append(entry)
    return {"drives": drives}


def tool_status(pid):
    proc = subprocess.run(
        ["tasklist", "/FI", "PID eq %d" % pid, "/FO", "CSV", "/NH"],
        capture_output=True, text=True, errors="replace")
    running = False
    process_name = None
    for line in proc.stdout.splitlines():
        fields = [f.strip('"') for f in line.split('","')]
        if len(fields) > 1 and fields[1] == str(pid):
            running = True
            process_name = fields[0]
            break
    return {"pid": pid, "running": running, "processName": process_name}


def tool_stop(pid):
    proc = subprocess.run(
        ["taskkill", "/PID", str(pid), "/T", "/F"],
        capture_output=True, text=True, errors="replace")
    return {"pid": pid, "exitCode": proc.returncode,
            "output": (proc.stdout or proc.stderr).strip()[:400]}


# ------------------------------------------------------------ MCP tool specs

_TOOLS = [
    {
        "name": "launch",
        "description": "Launch a local program, file, Start Menu shortcut, document, or URL by name or path - the programmatic equivalent of double-clicking it. Executables return the new process id immediately; shortcuts, documents, and URLs launch via shell association without a pid.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "program": {"type": "string", "description": "Program name (notepad, winword), absolute path, .lnk shortcut, document path, or URL"},
                "args": {"type": "array", "items": {"type": "string"}, "description": "Optional command-line arguments (executables only)"}
            },
            "required": ["program"]
        }
    },
    {
        "name": "resolve",
        "description": "Find where an installed program lives. Searches PATH, the App Paths registry, and Start Menu shortcuts; returns all matches with their source.",
        "inputSchema": {
            "type": "object",
            "properties": {"name": {"type": "string", "description": "Program name, with or without .exe"}},
            "required": ["name"]
        }
    },
    {
        "name": "search",
        "description": "Bounded search for executables and shortcuts by name substring under Program Files, Local Programs, E:\\tools, and E:\\apps (or custom roots). Depth- and result-limited.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Case-insensitive substring of the file name"},
                "roots": {"type": "array", "items": {"type": "string"}, "description": "Optional directories to search instead of the defaults"},
                "limit": {"type": "integer", "description": "Max matches (default 25)"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "list_apps",
        "description": "List installed apps by their Start Menu shortcut names, optionally filtered by a substring.",
        "inputSchema": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "Optional case-insensitive substring filter"}}
        }
    },
    {
        "name": "list_drives",
        "description": "List mounted drives with type (fixed/removable/cdrom/remote) and free/total bytes.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "status",
        "description": "Check whether a process id is still running, and report its process name.",
        "inputSchema": {
            "type": "object",
            "properties": {"pid": {"type": "integer"}},
            "required": ["pid"]
        }
    },
    {
        "name": "stop",
        "description": "Force-stop a process tree by process id (taskkill /T /F). Returns the taskkill exit code.",
        "inputSchema": {
            "type": "object",
            "properties": {"pid": {"type": "integer"}},
            "required": ["pid"]
        }
    }
]


# ----------------------------------------------------------------- dispatch

def _require_int(args, key):
    value = args.get(key)
    if value is None:
        raise RuntimeError("missing required integer argument: %s" % key)
    return int(value)


def _call_tool(name, args):
    if name == "launch":
        return tool_launch(args.get("program"), args.get("args"))
    if name == "resolve":
        target = args.get("name") or args.get("program")
        if not target:
            raise RuntimeError("resolve requires 'name'")
        return {"matches": resolve_program(target)}
    if name == "search":
        return tool_search(args.get("query"), args.get("roots"),
                           args.get("limit", 25))
    if name == "list_apps":
        return tool_list_apps(args.get("query"))
    if name == "list_drives":
        return tool_list_drives()
    if name == "status":
        return tool_status(_require_int(args, "pid"))
    if name == "stop":
        return tool_stop(_require_int(args, "pid"))
    raise RuntimeError("unknown tool: %s" % name)


def _handle(request):
    method = request.get("method", "")
    request_id = request.get("id")
    if method == "initialize":
        params = request.get("params") or {}
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": params.get("protocolVersion", "2024-11-05"),
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            },
        }
    if method == "ping":
        return {"jsonrpc": "2.0", "id": request_id, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": _TOOLS}}
    if method == "tools/call":
        params = request.get("params") or {}
        try:
            result = _call_tool(params.get("name"), params.get("arguments") or {})
            payload = json.dumps(result, ensure_ascii=True)
            return {"jsonrpc": "2.0", "id": request_id,
                    "result": {"content": [{"type": "text", "text": payload}]}}
        except Exception as exc:
            return {"jsonrpc": "2.0", "id": request_id,
                    "result": {"isError": True,
                               "content": [{"type": "text",
                                            "text": "error: %s" % exc}]}}
    if method == "logging/setLevel":
        return {"jsonrpc": "2.0", "id": request_id, "result": {}}
    if request_id is None:
        return None
    return {"jsonrpc": "2.0", "id": request_id,
            "error": {"code": -32601, "message": "method not found: %s" % method}}


def main():
    try:
        sys.stdin.reconfigure(encoding="utf-8", errors="replace")
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            continue
        response = _handle(request)
        if response is not None:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
