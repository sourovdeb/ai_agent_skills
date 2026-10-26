#!/bin/bash
set -e

SKILLS_DIR="$(cd "$(dirname "$0")" && pwd)/skills"
ERRORS=0
WARNINGS=0

validate_skill() {
    local skill_dir="$1"
    local skill_name=$(basename "$skill_dir")
    local skill_file="$skill_dir/SKILL.md"

    echo "=== Validating: $skill_name ==="

    if [ ! -f "$skill_file" ]; then
        echo "  ERROR: SKILL.md not found"
        ERRORS=$((ERRORS + 1))
        return
    fi

    if ! head -1 "$skill_file" | grep -q "^---$"; then
        echo "  ERROR: SKILL.md must start with YAML frontmatter (---)"
        ERRORS=$((ERRORS + 1))
    fi

    local name=$(grep -m1 "^name:" "$skill_file" | sed 's/^name: *//' | tr -d '"'"'"'')
    if [ -z "$name" ]; then
        echo "  ERROR: Missing 'name' field in frontmatter"
        ERRORS=$((ERRORS + 1))
    elif [ "$name" != "$skill_name" ]; then
        echo "  ERROR: name '$name' doesn't match directory name '$skill_name'"
        ERRORS=$((ERRORS + 1))
    elif ! echo "$name" | grep -qE '^[a-z0-9-]+$'; then
        echo "  ERROR: name '$name' must be lowercase letters, numbers, hyphens only"
        ERRORS=$((ERRORS + 1))
    elif echo "$name" | grep -qE '(^[-])|([-]$)|(--)'; then
        echo "  ERROR: name '$name' has invalid hyphen usage"
        ERRORS=$((ERRORS + 1))
    else
        echo "  OK: name = $name"
    fi

    local desc=$(grep -m1 "^description:" "$skill_file" | sed 's/^description: *//')
    if [ -z "$desc" ]; then
        echo "  ERROR: Missing 'description' field in frontmatter"
        ERRORS=$((ERRORS + 1))
    elif [ ${#desc} -gt 1024 ]; then
        echo "  ERROR: description is ${#desc} chars (max 1024)"
        ERRORS=$((ERRORS + 1))
    else
        echo "  OK: description (${#desc} chars)"
    fi

    local lines=$(wc -l < "$skill_file")
    if [ "$lines" -gt 500 ]; then
        echo "  WARNING: SKILL.md is $lines lines (recommended: < 500)"
        WARNINGS=$((WARNINGS + 1))
    else
        echo "  OK: $lines lines"
    fi

    # Only check actual markdown links: [text](references/file.md)
    local refs=$(grep -oE '\]\(references/[^)]+\)' "$skill_file" | sed 's/^](//' | sed 's/)$//' | sort -u)
    for ref in $refs; do
        if [ ! -f "$skill_dir/$ref" ]; then
            echo "  WARNING: Referenced file not found: $ref"
            WARNINGS=$((WARNINGS + 1))
        else
            echo "  OK: reference exists: $ref"
        fi
    done

    echo ""
}

echo "Validating skills in $SKILLS_DIR"
echo ""

for skill_dir in "$SKILLS_DIR"/*/; do
    validate_skill "$skill_dir"
done

echo "=========================================="
echo "Validation complete:"
echo "  Errors: $ERRORS"
echo "  Warnings: $WARNINGS"
echo "=========================================="

if [ "$ERRORS" -gt 0 ]; then
    exit 1
fi
