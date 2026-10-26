#!/bin/bash
set -e

SKILLS_DIR="$(cd "$(dirname "$0")" && pwd)/skills"

usage() {
    echo "Usage: $0 [--global | --project | --vibe-global | --vibe-project | --claude-global | --claude-project]"
    echo ""
    echo "Options:"
    echo "  --global          Install to ~/.agents/skills/ (all agents)"
    echo "  --project         Install to ./.agents/skills/ (project-level)"
    echo "  --vibe-global     Install to ~/.vibe/skills/ (Mistral Vibe user-level)"
    echo "  --vibe-project    Install to ./.vibe/skills/ (Mistral Vibe project-level)"
    echo "  --claude-global   Install to ~/.claude/skills/ (Claude Code user-level)"
    echo "  --claude-project  Install to ./.claude/skills/ (Claude Code project-level)"
    echo "  --list            List available skills"
    echo "  --help            Show this help"
    exit 1
}

list_skills() {
    echo "Available skills:"
    for skill in "$SKILLS_DIR"/*/; do
        name=$(basename "$skill")
        desc=$(grep -m1 "^description:" "$skill/SKILL.md" | sed 's/^description: *//' | cut -c1-80)
        echo "  $name — $desc..."
    done
}

install_skills() {
    local target_dir="$1"
    echo "Installing skills to $target_dir"
    mkdir -p "$target_dir"
    for skill in "$SKILLS_DIR"/*/; do
        name=$(basename "$skill")
        echo "  Installing: $name"
        cp -r "$skill" "$target_dir/"
    done
    echo ""
    echo "Done! Installed skills:"
    ls -1 "$target_dir"
    echo ""
    echo "Restart your agent or run /reload to pick up the new skills."
}

case "${1:-}" in
    --global)
        install_skills "$HOME/.agents/skills"
        ;;
    --project)
        install_skills "./.agents/skills"
        ;;
    --vibe-global)
        install_skills "$HOME/.vibe/skills"
        ;;
    --vibe-project)
        install_skills "./.vibe/skills"
        ;;
    --claude-global)
        install_skills "$HOME/.claude/skills"
        ;;
    --claude-project)
        install_skills "./.claude/skills"
        ;;
    --list)
        list_skills
        ;;
    --help|"")
        usage
        ;;
    *)
        echo "Unknown option: $1"
        usage
        ;;
esac
