#!/bin/bash
# Daily Automation Runner
# Run all scrapers, cleanups, and checks in one command
# Usage: bash tools/run_daily.sh

set -e

echo "╔════════════════════════════════════════╗"
echo "║  Daily Automation Runner                ║"
echo "║  $(date '+%Y-%m-%d %H:%M')              ║"
echo "╚════════════════════════════════════════╝"

cd "$(dirname "$0")/.."

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. JOB SCRAPING
echo -e "\n${BLUE}1. Scraping Indeed for jobs...${NC}"
python3 tools/indeed_scraper.py \
  --keywords "English teacher" \
  --location "France" \
  --max-pages 3

job_count=$(jq 'length' job_leads/indeed_leads.json 2>/dev/null || echo "0")
echo -e "${GREEN}   ✓ Total jobs tracked: $job_count${NC}"

# 2. CONTACT FINDING
echo -e "\n${BLUE}2. Finding potential collaborators...${NC}"
python3 tools/contact_finder.py \
  --search "disability writing" \
  --type writers \
  --limit 10

contact_count=$(jq 'length' contact_network/potential_contacts.json 2>/dev/null || echo "0")
echo -e "${GREEN}   ✓ Total contacts: $contact_count${NC}"

# 3. ESSAY COUNT
echo -e "\n${BLUE}3. Checking essay stats...${NC}"
essay_count=$(ls daily_essays/*.md 2>/dev/null | wc -l)
word_count=0
for file in daily_essays/*.md; do
  if [ -f "$file" ]; then
    words=$(wc -w < "$file")
    word_count=$((word_count + words))
  fi
done
echo -e "${GREEN}   ✓ Essays written: $essay_count${NC}"
echo -e "${GREEN}   ✓ Total words: $word_count${NC}"

# 4. GIT STATUS
echo -e "\n${BLUE}4. Git status...${NC}"
uncommitted=$(git status --short | wc -l)
if [ $uncommitted -gt 0 ]; then
  echo -e "${YELLOW}   ⚠ Uncommitted changes: $uncommitted${NC}"
else
  echo -e "${GREEN}   ✓ All changes committed${NC}"
fi

# 5. SUMMARY
echo -e "\n${BLUE}═══════════════════════════════════════${NC}"
echo -e "${GREEN}Today's Summary:${NC}"
echo -e "   \U0001f4dd Essays: $essay_count"
echo -e "   \U0001f4bc Jobs tracked: $job_count"
echo -e "   \U0001f465 Contacts: $contact_count"
echo -e "   \U0001f4ca Total words: $word_count"
echo -e "   \U0001f500 Git status: $([ $uncommitted -eq 0 ] && echo '✓ Clean' || echo '✗ Needs commit')${NC}"

echo -e "\n${GREEN}✓ Automation complete!${NC}\n"
