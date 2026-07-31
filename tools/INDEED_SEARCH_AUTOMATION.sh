#!/bin/bash

# INDEED JOB SEARCH AUTOMATION
# Searches Indeed for relevant jobs and exports to CSV + markdown
# Usage: ./INDEED_SEARCH_AUTOMATION.sh
# Cron: Run daily at 8 AM: 0 8 * * * /path/to/INDEED_SEARCH_AUTOMATION.sh

SEARCH_DATE=$(date +"%Y-%m-%d")
REPORT_FILE="job_search_report_${SEARCH_DATE}.md"
OUTPUT_DIR="../job_search"

declare -a SEARCH_QUERIES=(
    "remote writing"
    "technical writer remote"
    "content writer France"
    "documentation specialist remote"
    "UX writer remote"
    "English teacher online"
    "freelance translator English"
    "automation engineer remote"
)

mkdir -p "${OUTPUT_DIR}"
echo "# Indeed Job Search Report - ${SEARCH_DATE}" > "${OUTPUT_DIR}/${REPORT_FILE}"
echo "" >> "${OUTPUT_DIR}/${REPORT_FILE}"
echo "Generated at $(date)" >> "${OUTPUT_DIR}/${REPORT_FILE}"
echo "" >> "${OUTPUT_DIR}/${REPORT_FILE}"

for query in "${SEARCH_QUERIES[@]}"; do
    echo "Searching: $query"
    echo "" >> "${OUTPUT_DIR}/${REPORT_FILE}"
    echo "## Search Query: $query" >> "${OUTPUT_DIR}/${REPORT_FILE}"
    echo "" >> "${OUTPUT_DIR}/${REPORT_FILE}"
    echo "- URL: https://www.indeed.com/jobs?q=${query// /+}&l=remote" >> "${OUTPUT_DIR}/${REPORT_FILE}"
    echo "" >> "${OUTPUT_DIR}/${REPORT_FILE}"
done

echo "✓ Job search report generated: ${OUTPUT_DIR}/${REPORT_FILE}"
echo "Review the report and visit the URLs to find current listings."
