#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-/mnt/sourov-database/Sourov_Personal_Documents}"
REMOTE_URL="${2:-https://github.com/sourovdeb/my_professional_documents.git}"
BRANCH="${3:-main}"

info() { printf '%s\n' "$*"; }
warn() { printf 'WARN: %s\n' "$*" >&2; }
err() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

ensure_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    err "Required command '$1' is not installed. Please install it and re-run this script."
  fi
}

extract_archive() {
  local archive="$1"
  local base target parent stem
  base="$(basename "$archive")"
  parent="$(dirname "$archive")"
  stem="${base%.*}"
  target="$parent/${stem}_extracted"

  if [[ "$archive" == *"_extracted"* || "$archive" == *"_extracted_"* ]]; then
    warn "Skipping archive inside extracted output: $archive"
    return 0
  fi

  if [ -d "$target" ] && [ "$(find "$target" -mindepth 1 | wc -l)" -gt 0 ]; then
    info "Archive already extracted, skipping: $archive -> $target"
    return 0
  fi

  mkdir -p "$target"
  case "${archive,,}" in
    *.zip)
      ensure_cmd unzip
      info "Extracting ZIP: $archive -> $target"
      unzip -n -qq "$archive" -d "$target"
      ;;
    *.tar)
      ensure_cmd tar
      info "Extracting TAR: $archive -> $target"
      tar -xf "$archive" -C "$target"
      ;;
    *.tar.gz|*.tgz)
      ensure_cmd tar
      info "Extracting TAR.GZ: $archive -> $target"
      tar -xzf "$archive" -C "$target"
      ;;
    *.tar.bz2|*.tbz2)
      ensure_cmd tar
      info "Extracting TAR.BZ2: $archive -> $target"
      tar -xjf "$archive" -C "$target"
      ;;
    *.tar.xz|*.txz)
      ensure_cmd tar
      info "Extracting TAR.XZ: $archive -> $target"
      tar -xJf "$archive" -C "$target"
      ;;
    *.7z)
      ensure_cmd 7z
      info "Extracting 7Z: $archive -> $target"
      7z x -y -o"$target" "$archive" >/dev/null
      ;;
    *.rar)
      ensure_cmd unrar
      info "Extracting RAR: $archive -> $target"
      unrar x -o- "$archive" "$target" >/dev/null
      ;;
    *)
      warn "Skipping unsupported archive type: $archive"
      rm -rf "$target"
      return 1
      ;;
  esac
}

git_setup_and_push() {
  cd "$ROOT_DIR"

  if [ ! -d .git ]; then
    info "Initializing new git repository in '$ROOT_DIR'"
    git init -b "$BRANCH"
    git remote add origin "$REMOTE_URL"
  else
    info "Using existing git repository in '$ROOT_DIR'"
    git checkout "$BRANCH" 2>/dev/null || git checkout -b "$BRANCH"
    if git remote get-url origin >/dev/null 2>&1; then
      local current_remote
      current_remote="$(git remote get-url origin)"
      if [ "$current_remote" != "$REMOTE_URL" ]; then
        info "Updating origin remote URL from '$current_remote' to '$REMOTE_URL'"
        git remote set-url origin "$REMOTE_URL"
      fi
    else
      git remote add origin "$REMOTE_URL"
    fi
  fi

  ensure_git_identity

  git add -A
  if git diff --cached --quiet; then
    info "No changes to commit."
  else
    git commit -m "Update personal documents and extracted archives $(date -u '+%Y-%m-%d %H:%M UTC')"
  fi

  info "About to push branch '$BRANCH' to origin ($REMOTE_URL)"
  if [ -t 0 ]; then
    git status --short
    read -rp "Push to origin/$BRANCH now? [y/N]: " reply
    case "$reply" in
      [Yy]*)
        git push -u origin "$BRANCH"
        ;;
      *)
        info "Push aborted by user.";
        ;;
    esac
  else
    git push -u origin "$BRANCH"
  fi
}

enable_git_identity() {
  local name email

  if git config --local user.name >/dev/null 2>&1 && git config --local user.email >/dev/null 2>&1; then
    return 0
  fi

  name="${GIT_AUTHOR_NAME:-${GIT_COMMITTER_NAME:-${USER:-${LOGNAME:-Sourov}}}}"
  email="${GIT_AUTHOR_EMAIL:-${GIT_COMMITTER_EMAIL:-${USER:-sourov}@localhost}}"

  if [ -z "$name" ] || [ -z "$email" ]; then
    return 1
  fi

  git config user.name "$name"
  git config user.email "$email"
}

ensure_git_identity() {
  if git config user.name >/dev/null 2>&1 && git config user.email >/dev/null 2>&1; then
    return 0
  fi

  if enable_git_identity; then
    info "Set local git identity: $(git config user.name) <$(git config user.email)>"
    return 0
  fi

  if [ -t 0 ]; then
    info "Git identity is not configured for this repo."
    default_name="${GIT_AUTHOR_NAME:-${GIT_COMMITTER_NAME:-${USER:-${LOGNAME:-}}}}"
    default_email="${GIT_AUTHOR_EMAIL:-${GIT_COMMITTER_EMAIL:-}}"
    read -rp "Enter git user.name [${default_name}]: " input_name
    read -rp "Enter git user.email [${default_email}]: " input_email
    name="${input_name:-$default_name}"
    email="${input_email:-$default_email}"
    if [ -n "$name" ] && [ -n "$email" ]; then
      git config user.name "$name"
      git config user.email "$email"
      info "Set local git identity: $name <$email>"
      return 0
    fi
  fi

  err "Git identity is missing. Run 'git config --global user.name \"Your Name\"' and 'git config --global user.email \"you@example.com\"', or set GIT_AUTHOR_NAME/GIT_AUTHOR_EMAIL in the environment."
}

main() {
  if [ ! -d "$ROOT_DIR" ]; then
    err "Root directory does not exist: $ROOT_DIR"
  fi

  info "Scanning for archives under: $ROOT_DIR"
  mapfile -t archives < <(find "$ROOT_DIR" \( -path '*/.git' -o -path '*/.git/*' -o -path '*/*_extracted' -o -path '*/*_extracted/*' \) -prune -o -type f \( -iname '*.zip' -o -iname '*.tar' -o -iname '*.tar.gz' -o -iname '*.tgz' -o -iname '*.tar.bz2' -o -iname '*.tbz2' -o -iname '*.tar.xz' -o -iname '*.txz' -o -iname '*.7z' -o -iname '*.rar' \) -print | sort)

  if [ ${#archives[@]} -eq 0 ]; then
    info "No archive files found in $ROOT_DIR"
  else
    for archive in "${archives[@]}"; do
      if ! extract_archive "$archive"; then
        warn "Failed to extract $archive"
      fi
    done
  fi

  git_setup_and_push
}

main "$@"
