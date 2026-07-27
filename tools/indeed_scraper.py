#!/usr/bin/env python3
"""
Indeed Job Scraper - Free & Lightweight
Scrapes Indeed for teaching/writing/tech jobs without API key
Stores results in job_leads/indeed_leads.json for tracking

Usage:
    python3 automation_scripts/indeed_scraper.py \\
      --keywords "English teacher" \\
      --location "France" \\
      --max-pages 5

Dependencies: pip install requests beautifulsoup4
"""

import json
import requests
from datetime import datetime
from pathlib import Path
import argparse
import time
from urllib.parse import quote

class IndeedScraper:
    def __init__(self):
        self.base_url = "https://fr.indeed.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.jobs_file = Path('job_leads/indeed_leads.json')
        self.jobs_file.parent.mkdir(exist_ok=True)

    def search_jobs(self, keywords, location, max_pages=3):
        """Scrape Indeed for jobs"""
        jobs = []

        for page in range(max_pages):
            start = page * 15
            url = f"{self.base_url}/jobs?q={quote(keywords)}&l={quote(location)}&start={start}"

            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()

                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                job_cards = soup.find_all('div', class_='job_seen_beacon')

                if not job_cards:
                    print(f"⚠️  No jobs found on page {page + 1}")
                    break

                for card in job_cards:
                    try:
                        job_title_elem = card.find('h2', class_='jobTitle')
                        company_elem = card.find('span', class_='companyName')
                        location_elem = card.find('div', class_='companyLocation')
                        salary_elem = card.find('div', class_='salary-snippet')
                        snippet_elem = card.find('div', class_='job-snippet')

                        if not job_title_elem:
                            continue

                        job_link = job_title_elem.find('a')
                        job_id = job_link.get('data-jk', '') if job_link else ''

                        job = {
                            'id': job_id,
                            'title': job_title_elem.get_text(strip=True),
                            'company': company_elem.get_text(strip=True) if company_elem else 'Unknown',
                            'location': location_elem.get_text(strip=True) if location_elem else location,
                            'salary': salary_elem.get_text(strip=True) if salary_elem else 'Not specified',
                            'description': snippet_elem.get_text(strip=True)[:300] if snippet_elem else '',
                            'url': f"{self.base_url}/viewjob?jk={job_id}",
                            'posted_date': datetime.now().isoformat(),
                            'status': 'new',
                            'applied': False
                        }
                        jobs.append(job)
                    except Exception as e:
                        print(f"⚠️  Error parsing job card: {e}")
                        continue

                print(f"✅ Page {page + 1}: Found {len(job_cards)} jobs")
                time.sleep(2)

            except requests.RequestException as e:
                print(f"❌ Error fetching page {page + 1}: {e}")
                break

        return jobs

    def save_jobs(self, jobs):
        """Save to JSON, avoiding duplicates"""
        existing = {}
        if self.jobs_file.exists():
            with open(self.jobs_file, 'r') as f:
                existing = {job['id']: job for job in json.load(f)}

        for job in jobs:
            if job['id'] not in existing:
                existing[job['id']] = job
            else:
                existing[job['id']]['posted_date'] = job['posted_date']

        with open(self.jobs_file, 'w') as f:
            json.dump(list(existing.values()), f, indent=2, ensure_ascii=False)

        return len(jobs)

    def filter_relevant(self, keywords_filter=None):
        """Filter jobs matching specific keywords"""
        if not self.jobs_file.exists():
            return []

        with open(self.jobs_file, 'r') as f:
            all_jobs = json.load(f)

        if not keywords_filter:
            return all_jobs

        keywords_lower = [k.lower() for k in keywords_filter]
        return [
            job for job in all_jobs
            if any(k in job['title'].lower() or k in job['description'].lower()
                   for k in keywords_lower)
        ]

def main():
    parser = argparse.ArgumentParser(
        description='Scrape Indeed for jobs without API key'
    )
    parser.add_argument('--keywords', default='English teacher', help='Job search keywords')
    parser.add_argument('--location', default='France', help='Location')
    parser.add_argument('--max-pages', type=int, default=3, help='Max pages to scrape')

    args = parser.parse_args()
    scraper = IndeedScraper()

    print(f"\n\U0001f50d Scraping Indeed for: {args.keywords} in {args.location}")
    jobs = scraper.search_jobs(
        keywords=args.keywords,
        location=args.location,
        max_pages=args.max_pages
    )

    if jobs:
        saved = scraper.save_jobs(jobs)
        print(f"\n✅ Saved {saved} new jobs to job_leads/indeed_leads.json")
        print(f"   Total unique jobs: {len(scraper.filter_relevant())}")
    else:
        print("❌ No jobs found")

if __name__ == '__main__':
    main()
