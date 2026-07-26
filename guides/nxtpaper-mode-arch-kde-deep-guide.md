# NXTPaper Mode on Arch Linux + KDE Plasma
## Deep Guide — Every Scenario Covered

> **Goal:** One-click warm sepia screen, readable contrast font, grainy off-white background — like the TCL NXTPaper display — on a normal laptop running Arch + KDE Plasma.

---

## How to Read This Guide

Each section uses a consistent format:

- **IF** → your condition or situation
- **THEN** → exactly what to do
- **BEWARE** → the real traps that will silently break things

Work through the sections in order. Do not skip Phase 0 and Phase 1 — they determine every decision that follows.

---

## Phase 0 — Diagnose Your Environment First

Run these three commands before doing anything else. The entire guide branches based on their output.

```bash
echo "SESSION: $XDG_SESSION_TYPE"
lspci | grep -i vga
xrandr --listmonitors 2>/dev/null || echo "xrandr unavailable (Wayland)"
```

---

### 0.1 — Identify Your Display Server

**IF** the output says `wayland`

**THEN** you are on Wayland. xrandr gamma **does not work** and never will on Wayland, by design. This is confirmed as a known unfixed issue in the official KDE bug tracker (bug #481591, marked WONTFIX for xrandr compatibility). Your color filter path is Night Color via `kwriteconfig6` + ICC profile as fallback. Skip ahead to Phase 2-B.

**BEWARE** — On Wayland, even `xrandr` itself launches silently via XWayland compatibility shim. It will *run without error* but the gamma flag is completely ignored. You will think it worked. Nothing will have changed. There is no error message.

---

**IF** the output says `x11`

**THEN** you have full xrandr gamma control. The simplest and most precise filter path. Continue to Phase 1.

**BEWARE** — If you log into KDE and never explicitly chose X11 or Wayland at the SDDM login screen, modern Arch KDE defaults to **Wayland** as of Plasma 6. Check again with `echo $XDG_SESSION_TYPE` from inside a terminal, not from a tty.

---

### 0.2 — Identify Your GPU

**IF** `lspci | grep -i vga` returns `NVIDIA`

**THEN** you have an additional complication. Night Color (the Wayland color temperature tool) was **completely broken on NVIDIA + Wayland** until NVIDIA driver version 545+ and Plasma 6.0. Before those versions, night color applied nothing, with no error. Verify your driver:

```bash
nvidia-smi --query-gpu=driver_version --format=csv,noheader
```

If the driver is below 545, Night Color on Wayland is silently broken. Your only reliable option is to switch to X11 session for this feature.

**BEWARE** — The Night Color settings panel will appear to work (slider moves, values save) but zero visual change will occur on screen. This is the most common silent failure in this entire setup.

---

**IF** `lspci | grep -i vga` returns `Intel` or `AMD`

**THEN** both X11 xrandr and Wayland Night Color should work correctly. Continue normally.

---

### 0.3 — Count Your Monitors

**IF** `xrandr --listmonitors` shows more than one monitor (e.g., `eDP-1` and `HDMI-1`)

**THEN** you must apply the gamma filter to **every connected output**, not just one. A script that targets only the primary display will leave external monitors at normal color, making the effect jarring.

**BEWARE** — The `xrandr` command requires the exact output name. Output names on laptops are inconsistent across sessions. Common names: `eDP-1`, `eDP1`, `LVDS-1`. External monitors: `HDMI-1`, `HDMI-A-1`, `DisplayPort-0`, `DP-1`. A docking station can rename outputs between sessions. Build the detection dynamically (shown in Phase 3).

---

## Phase 1 — Install Dependencies

```bash
sudo pacman -S xorg-xrandr imagemagick --needed
```

**IF** you are only on Wayland and will not use xrandr at all

**THEN** `xorg-xrandr` is not required. Only `imagemagick` is needed for the wallpaper generation step.

**BEWARE** — On Arch, the `convert` command has been renamed to `magick` in ImageMagick 7+. If you run `convert` and get "command not found", use `magick` instead. Both are tested in the script below with an automatic fallback.

---

## Phase 2-A — Screen Color Filter (X11 Path)

### How xrandr gamma works

The `--gamma R:G:B` flag adjusts the gamma ramp for each color channel independently. Default is `1.0:1.0:1.0`. To produce a warm sepia/paper tone:

- Red stays at `1.0` (full)
- Green is reduced (reduces green cast)
- Blue is reduced most (removes cold blue light)
- `--brightness` reduces overall luminance slightly

**Sepia intensity table:**

| Effect | Red | Green | Blue | Brightness |
|---|---|---|---|---|
| Barely warm | 1.0 | 0.95 | 0.85 | 0.95 |
| Warm (mild NXTPaper) | 1.0 | 0.90 | 0.78 | 0.90 |
| **Paper (target)** | **1.0** | **0.85** | **0.70** | **0.88** |
| E-ink aggressive | 1.0 | 0.78 | 0.60 | 0.85 |

**Test live before committing:**

```bash
# Get your output name first
xrandr | grep " connected" | awk '{print $1}'

# Apply test (replace eDP-1 with your output name)
xrandr --output eDP-1 --gamma 1.0:0.85:0.70 --brightness 0.88
```

**Reset if it looks wrong:**

```bash
xrandr --output eDP-1 --gamma 1.0:1.0:1.0 --brightness 1.0
```

**IF** you have multiple monitors

**THEN** apply to each one individually in the same command chain:

```bash
xrandr --output eDP-1 --gamma 1.0:0.85:0.70 --brightness 0.88 \
       --output HDMI-1 --gamma 1.0:0.85:0.70 --brightness 0.88
```

**BEWARE** — xrandr gamma changes are **not persistent**. They reset on every login. The toggle script handles active sessions, but if you want it on immediately at login, add the enable command to **System Settings → Autostart** (see Phase 5).

**BEWARE** — xrandr gamma does not affect screenshots. The color filter is applied at the GPU output stage, after screen capture. Screenshots will look normal/uncorrected. This is expected behavior, not a bug.

---

## Phase 2-B — Screen Color Filter (Wayland Path)

On Wayland, the only system-level color shift tool available without a hardware colorimeter is **KWin Night Color**, configured via `kwriteconfig6`.

### How Night Color configuration works on Plasma 6

Night Color is controlled by the `[NightColor]` group in `~/.config/kwinrc`. The key parameters:

```
Mode = Constant       (always on, regardless of time/location)
NightTemperature = X  (color temperature in Kelvin, lower = warmer)
Active = true
```

**Temperature reference for NXTPaper feel:**

| Feel | Temperature (K) |
|---|---|
| Neutral (off) | 6500 |
| Slightly warm | 5000 |
| Warm reading mode | 4000 |
| **NXTPaper paper feel** | **3200** |
| Deep amber | 2700 |
| Candle-like | 2000 |

**Apply via terminal:**

```bash
kwriteconfig6 --file kwinrc --group NightColor --key Mode "Constant"
kwriteconfig6 --file kwinrc --group NightColor --key NightTemperature "3200"
kwriteconfig6 --file kwinrc --group NightColor --key Active "true"
dbus-send --type=signal --dest=org.kde.KWin /ColorCorrect \
    org.kde.kwin.ColorCorrect.nightColorSettingsChanged
```

**IF** the dbus signal command fails or does nothing

**THEN** try the alternative reload:

```bash
qdbus6 org.kde.KWin /ColorCorrect refreshConfig 2>/dev/null
```

**IF** even that fails

**THEN** log out and back in. The `kwinrc` file is written correctly; KWin simply needs a session restart to pick it up. This is a known KWin configuration reload reliability issue.

**BEWARE** — The `qdbus` inhibit/preview approach (often found in older forum posts) will **not work** for persistent toggling. KWin's inhibition model requires the DBus client to stay alive as a running process. When `qdbus` exits, the inhibition is dropped immediately and Night Color reverts. The `kwriteconfig6` approach writes the setting permanently and survives process exit, which is what you want.

**BEWARE** — Night Color on Wayland is a full-screen compositor effect. It applies uniformly to every pixel. Unlike xrandr, you cannot apply it differently per-monitor on KDE Plasma 6. If you have two monitors and need independent color on each, X11 is the only current option.

**BEWARE** — If you had Night Color previously configured to trigger at specific times of day, setting `Mode = Constant` will override that. The toggle script saves and restores the original mode (see Phase 3).

---

### Wayland Fallback: ICC Profile Method (Advanced)

If Night Color is broken on your system (e.g., NVIDIA + old driver), an ICC profile embedded with a warm gamma curve can be applied through KWin's display settings.

**IF** you want a permanent Wayland color shift without Night Color

**THEN** install `argyllcms` and create a warm-tinted profile using `colprof`, or use a pre-made warm sRGB profile from the community. Save it to `~/.config/color/icc/devices/display/warm.icc` and assign it in **System Settings → Display & Monitor → Color Profile**.

**BEWARE** — Assigning an ICC profile this way is **not toggleable** without going back into System Settings. It is persistent, not on/off scriptable. Use it for a permanent "always warm" setup, not for toggling.

**BEWARE** — The ICC profile method in Plasma Wayland does NOT affect applications that declare their own color management (like Krita, Darktable, or professional photo editors). Those apps manage their own color pipeline. This only affects the compositor-level output for non-color-managed apps.

---

## Phase 3 — Generate the Grainy Paper Wallpaper

Run once. Generates the static background file.

```bash
# Detect screen resolution
RESOLUTION=$(xrandr 2>/dev/null | grep '\*' | awk '{print $1}' | head -1)
# Fallback if xrandr unavailable
RESOLUTION=${RESOLUTION:-1920x1080}

# Choose ImageMagick binary (v7 uses 'magick', v6 uses 'convert')
IM_BIN=$(command -v magick 2>/dev/null || command -v convert 2>/dev/null)

"$IM_BIN" -size "$RESOLUTION" xc:"#F5ECD7" \
  +noise Gaussian -attenuate 0.22 \
  -colorspace sRGB \
  ~/Pictures/nxtpaper_bg.png

echo "Wallpaper created: ~/Pictures/nxtpaper_bg.png"
```

**Color palette options for the base tone:**

| Style | Hex | Feel |
|---|---|---|
| Warm cream | `#F5ECD7` | NXTPaper default |
| Aged paper | `#EDE0C8` | Antique book |
| Warm white | `#FAF6F0` | Clean minimal |
| Cool paper | `#F0F0E8` | Newspaper-like |

**Grain intensity guide:**

- `-attenuate 0.10` → barely visible grain (smooth)
- `-attenuate 0.22` → subtle but present (recommended)
- `-attenuate 0.40` → clearly grainy, film-like
- `-attenuate 0.60` → heavy, visible noise

**BEWARE** — `plasma-apply-wallpaperimage` has a documented caching bug: if you call it with the **same filename** as the currently set wallpaper, Plasma assumes nothing changed and skips the update. The toggle script works around this by copying the file to a temp path with a unique name before each apply.

**BEWARE** — If `~/Pictures/` does not exist yet, the `magick` command will fail silently with a path error. Create it first: `mkdir -p ~/Pictures`.

---

## Phase 4 — Font Rendering for Ink-Like Contrast

This is separate from the toggle and recommended as a permanent system setting.

### The goal

NXTPaper's readability comes from high contrast, sharp font edges. On a normal LCD, this means:

- Sub-pixel rendering set to **RGB** (matches most laptop LCDs)
- Hinting set to **Slight** (preserves letter shapes while improving crispness)
- LCD filter set to **lcddefault** (reduces color fringing on sub-pixel rendering)

### Apply in KDE System Settings

Go to **System Settings → Appearance → Fonts → Configure...**

Set:
- Anti-aliasing: **Enabled**
- Sub-pixel rendering: **RGB**
- Hinting: **Slight**

### Apply via terminal (requires logout/login to take full effect)

```bash
kwriteconfig6 --file kcmfonts --group General \
    --key antiAliasing "1"
kwriteconfig6 --file kcmfonts --group General \
    --key subPixelType "rgb"
kwriteconfig6 --file kcmfonts --group General \
    --key hinting "slight"
```

### Apply at the fontconfig system level (affects all apps including GTK)

Create or edit `/etc/fonts/local.conf`:

```xml
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <match target="font">
    <edit name="lcdfilter" mode="assign">
      <const>lcddefault</const>
    </edit>
  </match>
  <match target="font">
    <edit name="hinting" mode="assign">
      <bool>true</bool>
    </edit>
    <edit name="hintstyle" mode="assign">
      <const>hintslight</const>
    </edit>
    <edit name="antialias" mode="assign">
      <bool>true</bool>
    </edit>
    <edit name="rgba" mode="assign">
      <const>rgb</const>
    </edit>
  </match>
</fontconfig>
```

Then rebuild the font cache:

```bash
fc-cache -fv
```

**IF** your laptop screen has a BGR (Blue-Green-Red) pixel layout instead of RGB (uncommon but exists on some Dell/Lenovo panels)

**THEN** set `subPixelType` to `bgr` in KDE and `<const>bgr</const>` in fontconfig. Wrong sub-pixel order causes colored halos around text that looks worse than no sub-pixel rendering at all.

**IF** you are on Wayland

**THEN** sub-pixel rendering hints from fontconfig are largely ignored by the Wayland compositor, which handles font rendering independently. KDE's own font rendering on Wayland uses Qt's font pipeline. The KDE system settings values still apply to Qt apps. GTK apps under Wayland have their own fontconfig pipeline, so the `/etc/fonts/local.conf` still matters for them.

**BEWARE** — Changing font settings in KDE System Settings can trigger a known Plasma bug where the "Exclude from anti-aliasing" checkbox enables itself automatically and breaks rendering for everything below a certain pixel size. If your fonts suddenly look aliased after visiting the font settings, go back and uncheck that box.

**BEWARE** — `kwriteconfig6` writes to `~/.config/kcmfonts` but the change does not apply to the running session. A logout/login is required. The color filter toggle does not need a logout; the font setting does.

---

## Phase 5 — The Toggle Script

Create the file:

```bash
mkdir -p ~/.local/bin
nano ~/.local/bin/nxtpaper
```

Paste the full script:

```bash
#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# nxtpaper — NXTPaper Mode Toggle for Arch Linux + KDE Plasma
# Works on both X11 and Wayland sessions
# ═══════════════════════════════════════════════════════════════

# ─── USER CONFIG ─────────────────────────────────────────────
WALLPAPER_ON="$HOME/Pictures/nxtpaper_bg.png"
WALLPAPER_OFF=""          # Set to a path to restore a specific wallpaper
                          # Leave empty to skip restoring on disable
SEPIA_GAMMA="1.0:0.85:0.70"
SEPIA_BRIGHTNESS="0.88"
SEPIA_TEMP="3200"         # Night Color temperature for Wayland (Kelvin)
# ─────────────────────────────────────────────────────────────

STATE_FILE="$HOME/.local/share/nxtpaper.state"
BACKUP_FILE="$HOME/.local/share/nxtpaper_nightcolor.backup"
mkdir -p "$(dirname "$STATE_FILE")"

# Detect ImageMagick binary (v7 = magick, v6 = convert)
IM_BIN=$(command -v magick 2>/dev/null || command -v convert 2>/dev/null)

# Detect all connected outputs on X11
get_outputs() {
    xrandr 2>/dev/null | awk '/ connected/{print $1}'
}

# Apply sepia gamma to all connected outputs
apply_gamma_all() {
    local outputs
    outputs=$(get_outputs)
    if [ -z "$outputs" ]; then
        echo "[nxtpaper] WARNING: No xrandr outputs found."
        return 1
    fi
    local cmd="xrandr"
    while IFS= read -r output; do
        cmd+=" --output $output --gamma $SEPIA_GAMMA --brightness $SEPIA_BRIGHTNESS"
    done <<< "$outputs"
    eval "$cmd"
}

# Reset gamma on all connected outputs
reset_gamma_all() {
    local outputs
    outputs=$(get_outputs)
    local cmd="xrandr"
    while IFS= read -r output; do
        cmd+=" --output $output --gamma 1.0:1.0:1.0 --brightness 1.0"
    done <<< "$outputs"
    eval "$cmd"
}

# Save current Night Color config before overwriting
backup_nightcolor() {
    local mode temp active
    mode=$(kreadconfig6 --file kwinrc --group NightColor --key Mode 2>/dev/null)
    temp=$(kreadconfig6 --file kwinrc --group NightColor --key NightTemperature 2>/dev/null)
    active=$(kreadconfig6 --file kwinrc --group NightColor --key Active 2>/dev/null)
    printf "Mode=%s\nNightTemperature=%s\nActive=%s\n" \
        "${mode:-Automatic}" "${temp:-4500}" "${active:-false}" > "$BACKUP_FILE"
}

# Restore Night Color from backup
restore_nightcolor() {
    if [ ! -f "$BACKUP_FILE" ]; then
        # No backup: just disable Night Color
        kwriteconfig6 --file kwinrc --group NightColor --key Active "false"
    else
        local mode temp active
        mode=$(grep '^Mode=' "$BACKUP_FILE" | cut -d= -f2)
        temp=$(grep '^NightTemperature=' "$BACKUP_FILE" | cut -d= -f2)
        active=$(grep '^Active=' "$BACKUP_FILE" | cut -d= -f2)
        kwriteconfig6 --file kwinrc --group NightColor --key Mode "${mode:-Automatic}"
        kwriteconfig6 --file kwinrc --group NightColor --key NightTemperature "${temp:-4500}"
        kwriteconfig6 --file kwinrc --group NightColor --key Active "${active:-false}"
        rm -f "$BACKUP_FILE"
    fi
    # Signal KWin to reload
    dbus-send --type=signal --dest=org.kde.KWin /ColorCorrect \
        org.kde.kwin.ColorCorrect.nightColorSettingsChanged 2>/dev/null || \
    qdbus6 org.kde.KWin /ColorCorrect refreshConfig 2>/dev/null || true
}

# Apply wallpaper — copies to temp path to bypass Plasma's filename cache
apply_wallpaper() {
    local src="$1"
    if [ ! -f "$src" ]; then
        echo "[nxtpaper] Wallpaper file not found: $src"
        return 1
    fi
    local tmp
    tmp="/tmp/nxtpaper_wall_$(date +%s).png"
    cp "$src" "$tmp"
    plasma-apply-wallpaperimage "$tmp" 2>/dev/null && rm -f "$tmp" || \
        echo "[nxtpaper] WARNING: plasma-apply-wallpaperimage failed."
}

# ─── ENABLE ───────────────────────────────────────────────────
enable_nxtpaper() {
    echo "[nxtpaper] Enabling NXTPaper mode..."

    # Color filter
    if [ "$XDG_SESSION_TYPE" = "x11" ]; then
        if ! command -v xrandr &>/dev/null; then
            echo "[nxtpaper] ERROR: xrandr not found. Install xorg-xrandr."
            exit 1
        fi
        apply_gamma_all
    else
        # Wayland: Night Color via kwinrc
        backup_nightcolor
        kwriteconfig6 --file kwinrc --group NightColor --key Mode "Constant"
        kwriteconfig6 --file kwinrc --group NightColor --key NightTemperature "$SEPIA_TEMP"
        kwriteconfig6 --file kwinrc --group NightColor --key Active "true"
        dbus-send --type=signal --dest=org.kde.KWin /ColorCorrect \
            org.kde.kwin.ColorCorrect.nightColorSettingsChanged 2>/dev/null || \
        qdbus6 org.kde.KWin /ColorCorrect refreshConfig 2>/dev/null || true
    fi

    # Wallpaper
    if [ -f "$WALLPAPER_ON" ]; then
        apply_wallpaper "$WALLPAPER_ON"
    else
        echo "[nxtpaper] NOTE: Wallpaper file not found at $WALLPAPER_ON"
        echo "           Run the wallpaper generation command first."
    fi

    echo "on" > "$STATE_FILE"

    # Notification (fails silently if libnotify not installed)
    notify-send "NXTPaper Mode" "ON — warm sepia filter active" \
        --icon=preferences-desktop-display --expire-time=2500 2>/dev/null || true
}

# ─── DISABLE ──────────────────────────────────────────────────
disable_nxtpaper() {
    echo "[nxtpaper] Disabling NXTPaper mode..."

    # Color filter
    if [ "$XDG_SESSION_TYPE" = "x11" ]; then
        reset_gamma_all
    else
        restore_nightcolor
    fi

    # Wallpaper
    if [ -n "$WALLPAPER_OFF" ] && [ -f "$WALLPAPER_OFF" ]; then
        apply_wallpaper "$WALLPAPER_OFF"
    fi

    echo "off" > "$STATE_FILE"

    notify-send "NXTPaper Mode" "OFF — normal display restored" \
        --icon=preferences-desktop-display --expire-time=2500 2>/dev/null || true
}

# ─── STATUS ───────────────────────────────────────────────────
status_nxtpaper() {
    local state
    state=$(cat "$STATE_FILE" 2>/dev/null || echo "off")
    echo "NXTPaper mode is currently: $state"
    echo "Session type: $XDG_SESSION_TYPE"
    if [ "$XDG_SESSION_TYPE" = "x11" ]; then
        echo "Connected outputs:"
        get_outputs | sed 's/^/  /'
    fi
}

# ─── MAIN ─────────────────────────────────────────────────────
case "${1:-toggle}" in
    on)      enable_nxtpaper ;;
    off)     disable_nxtpaper ;;
    status)  status_nxtpaper ;;
    toggle)
        current=$(cat "$STATE_FILE" 2>/dev/null || echo "off")
        if [ "$current" = "on" ]; then
            disable_nxtpaper
        else
            enable_nxtpaper
        fi
        ;;
    *)
        echo "Usage: nxtpaper [on|off|toggle|status]"
        exit 1
        ;;
esac
```

Make it executable:

```bash
chmod +x ~/.local/bin/nxtpaper
```

Ensure `~/.local/bin` is in your PATH (it usually is on Arch, but verify):

```bash
echo $PATH | grep -q "$HOME/.local/bin" && echo "PATH OK" || \
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

---

## Phase 6 — Bind to One Click

### Option A — Keyboard shortcut (fastest)

Go to **System Settings → Keyboard → Shortcuts → Custom Shortcuts → Edit → New → Command/URL**

- Name: `NXTPaper Toggle`
- Trigger: Assign any key (e.g. `Meta+P`)
- Action: `~/.local/bin/nxtpaper toggle`

**BEWARE** — KDE custom shortcuts require an **absolute path** or the command must be in PATH. Using `~` in the command field does not expand in all KDE versions. Use the full path: `/home/yourusername/.local/bin/nxtpaper toggle`

### Option B — Panel button widget

Right-click panel → **Add Widgets** → search for **Quick Launch** or **Application Launcher**. Create a `.desktop` file:

```bash
cat > ~/.local/share/applications/nxtpaper.desktop << 'EOF'
[Desktop Entry]
Name=NXTPaper Toggle
Comment=Toggle warm sepia screen mode
Exec=/home/YOURUSERNAME/.local/bin/nxtpaper toggle
Icon=preferences-desktop-display
Type=Application
Categories=Utility;
EOF
```

Replace `YOURUSERNAME` with your actual username. Then pin the app to the panel or taskbar.

### Option C — KRunner

Press `Alt+F2`, type `nxtpaper`, press Enter. Works immediately if `~/.local/bin` is in PATH.

---

## Phase 7 — Persistence Across Reboots (X11 Only)

xrandr settings reset on every login. The Wayland Night Color settings are already persistent in `kwinrc` and survive reboot. For X11, add an autostart entry:

**Method 1 — KDE Autostart:**

Go to **System Settings → Autostart → Add Application**, point it to `~/.local/bin/nxtpaper on`

**BEWARE** — Only add this if you want NXTPaper mode ON at every login. If you want it optional, don't add the autostart entry and rely on the toggle shortcut instead.

**Method 2 — .xprofile (X11 only):**

```bash
echo '~/.local/bin/nxtpaper on' >> ~/.xprofile
```

This runs at the start of every X11 session regardless of desktop environment. Safe for Arch.

**BEWARE** — If you add the autostart and also try to toggle off during the session, the next login will turn it back on silently. Either remove the autostart entry when you want NXTPaper off permanently, or make the autostart read the state file:

```bash
# Smarter autostart — only re-enables if it was on when you logged out
~/.local/bin/nxtpaper on
```

Actually, the script already respects the state file for `toggle`. For autostart, explicitly using `on` forces it on regardless. Use `toggle` in autostart if you want it to restore the last state:

```bash
# This restores whatever state was active when you last logged out
~/.local/bin/nxtpaper toggle  # will turn ON if state says off, and vice versa
```

For "restore last state" behavior, change the autostart command to:

```bash
bash -c 'STATE=$(cat ~/.local/share/nxtpaper.state 2>/dev/null); [ "$STATE" = "on" ] && ~/.local/bin/nxtpaper on'
```

---

## Phase 8 — Generating the Wallpaper (Full Command Reference)

### Standard (recommended):

```bash
magick -size 1920x1080 xc:"#F5ECD7" \
  +noise Gaussian -attenuate 0.22 \
  -colorspace sRGB \
  ~/Pictures/nxtpaper_bg.png
```

### Auto-detect resolution:

```bash
# X11
RES=$(xrandr | grep '\*' | awk '{print $1}' | head -1)
# Wayland — read from KScreen config
RES=${RES:-$(kscreen-doctor -o 2>/dev/null | grep -oP '\d+x\d+' | head -1)}
RES=${RES:-1920x1080}
magick -size "$RES" xc:"#F5ECD7" +noise Gaussian -attenuate 0.22 \
  -colorspace sRGB ~/Pictures/nxtpaper_bg.png
```

### Multiple resolutions (for multi-monitor):

```bash
# Generate for each connected screen at its native size
xrandr | grep '\*' | awk '{print $1}' | while read -r res; do
    safe_res=$(echo "$res" | tr 'x' '_')
    magick -size "$res" xc:"#F5ECD7" +noise Gaussian -attenuate 0.22 \
      -colorspace sRGB ~/Pictures/nxtpaper_bg_"${safe_res}".png
done
```

**BEWARE** — `plasma-apply-wallpaperimage` sets the same wallpaper on all monitors. There is no CLI flag to target a specific monitor. Setting per-monitor wallpaper requires a qdbus `evaluateScript` call with JavaScript, which is significantly more complex and breaks between Plasma versions.

---

## Phase 9 — Troubleshooting Decision Tree

### "Nothing changed when I ran the script"

```
Is your session X11 or Wayland?  →  echo $XDG_SESSION_TYPE
    │
    ├─ x11 → Did xrandr find your output?  →  xrandr | grep connected
    │            │
    │            ├─ Output found → Check gamma values in xrandr output:
    │            │                 xrandr --verbose | grep -A5 "connected"
    │            │
    │            └─ No outputs → Are you running in a VM?
    │                            VMs often don't expose xrandr gamma.
    │                            No workaround for this.
    │
    └─ wayland → Is Night Color actually applying?
                    Open System Settings → Display → Night Color
                    Is "Constant" selected and temperature showing 3200?
                    │
                    ├─ Yes but still not working → NVIDIA driver check:
                    │                              nvidia-smi --query-gpu=driver_version
                    │                              Need driver 545+
                    │
                    └─ Settings not saving → Run kwriteconfig6 commands again,
                                             then log out and back in.
```

### "Wallpaper didn't change"

```
Does the file exist?  →  ls -la ~/Pictures/nxtpaper_bg.png
    │
    ├─ No → Re-run the magick command to generate it
    │
    └─ Yes → Is plasma-apply-wallpaperimage available?
                 which plasma-apply-wallpaperimage
                 │
                 ├─ Not found → Install plasma-workspace (should already be present)
                 │
                 └─ Found → Is Plasma shell running?
                                qdbus6 | grep plasmashell
                                │
                                └─ If not running, plasma-apply-wallpaperimage
                                   will fail silently. Log into a full KDE session.
```

### "Font rendering looks worse after changes"

```
Did you visit System Settings → Fonts?
    │
    └─ Yes → Check if "Exclude from anti-aliasing" checkbox
             enabled itself automatically (known KDE bug).
             Uncheck it. Also verify sub-pixel is set to RGB not BGR.
```

### "Script toggled ON but I want to reset everything to defaults manually"

```bash
# X11 manual reset
xrandr --output eDP-1 --gamma 1.0:1.0:1.0 --brightness 1.0

# Wayland manual reset
kwriteconfig6 --file kwinrc --group NightColor --key Active "false"
dbus-send --type=signal --dest=org.kde.KWin /ColorCorrect \
    org.kde.kwin.ColorCorrect.nightColorSettingsChanged

# Reset state file
echo "off" > ~/.local/share/nxtpaper.state
```

---

## Summary Table

| Feature | X11 | Wayland (Intel/AMD) | Wayland (NVIDIA old) |
|---|---|---|---|
| Sepia gamma filter | ✅ xrandr | ⚠️ Night Color only | ❌ Broken until driver 545+ |
| Per-monitor color | ✅ Yes | ❌ No | ❌ No |
| Gamma persists reboot | ❌ Need autostart | ✅ Saved in kwinrc | — |
| Precise warm tones | ✅ Full R:G:B control | ⚠️ Temperature only | — |
| Wallpaper toggle | ✅ | ✅ | ✅ |
| Font rendering changes | ✅ Immediate effect | ⚠️ Logout required | ⚠️ Logout required |
| Screenshot affected | ❌ Not captured | ✅ Captured | — |

---

## Quick-Start Checklist

```
[ ] 1. Run: echo $XDG_SESSION_TYPE  → know your session
[ ] 2. Run: lspci | grep -i vga     → know your GPU
[ ] 3. Run: mkdir -p ~/Pictures
[ ] 4. Run the magick wallpaper command for your resolution
[ ] 5. Create ~/.local/bin/nxtpaper from Phase 5
[ ] 6. chmod +x ~/.local/bin/nxtpaper
[ ] 7. Test: nxtpaper on
[ ] 8. Test: nxtpaper off
[ ] 9. Test: nxtpaper status
[ ] 10. Bind to shortcut in KDE System Settings
[ ] 11. (Optional) Apply font rendering changes from Phase 4
[ ] 12. (X11 only, optional) Add to KDE Autostart
```

> **Navigation:** [[_AI_AGENT_RULES/_INDEX]]
