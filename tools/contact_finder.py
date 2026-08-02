#!/usr/bin/env python3
"""
Contact Finder - Locate Writers, Collaborators, and Potential Partners
Searches GitHub for like-minded writers in your field
Generates email suggestions using pattern matching

Usage:
    python3 automation_scripts/contact_finder.py \\
      --search "disability writing" \\
      --type writers \\
      --limit 10
"""

import json
import requests
from datetime import datetime
from pathlib import Path
import argparse
from urllib.parse import quote

class ContactFinder:
    def __init__(self):
        self.contacts_file = Path('contact_network/potential_contacts.json')
        self.contacts_file.parent.mkdir(exist_ok=True)

    def search_github_writers(self, search_term, language='markdown', limit=20):
        """Find GitHub users with relevant content"""
        url = "https://api.github.com/search/users"
        params = {
            'q': f"{search_term} type:user",
            'per_page': limit,
            'sort': 'followers'
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            contacts = []
            for user in data.get('items', []):
                contacts.append({
                    'platform': 'GitHub',
                    'name': user.get('login'),
                    'profile': user.get('html_url'),
                    'bio': user.get('bio', ''),
                    'followers': user.get('followers', 0),
                    'found_date': datetime.now().isoformat(),
                    'status': 'not_contacted',
                    'potential_email': self.guess_email(user.get('login'))
                })
            return contacts
        except Exception as e:
            print(f"❌ GitHub search error: {e}")
            return []

    def guess_email(self, username):
        """Try to guess email from username"""
        patterns = [
            f"{username}@gmail.com",
            f"{username}@protonmail.com",
            f"hello@{username}.com",
            f"contact@{username}.com"
        ]
        return patterns[0]

    def search_by_topic(self, topic):
        """Find writers discussing specific topic"""
        github_writers = self.search_github_writers(topic, limit=15)
        contacts = github_writers
        if contacts:
            self.save_contacts(contacts)
        return contacts

    def save_contacts(self, contacts):
        """Save contacts to JSON"""
        existing = {}
        if self.contacts_file.exists():
            with open(self.contacts_file, 'r') as f:
                existing = {c['profile']: c for c in json.load(f)}

        for contact in contacts:
            existing[contact['profile']] = contact

        with open(self.contacts_file, 'w') as f:
            json.dump(list(existing.values()), f, indent=2, ensure_ascii=False)

    def generate_outreach_email(self, contact, subject_topic):
        """Generate personalized email template"""
        email_template = f"""
Subject: Collaboration on {subject_topic}

Hi {contact['name']},

I noticed your work on {subject_topic} on {contact['platform']}.

I'm writing about [YOUR TOPIC] and believe our perspectives align.

Would you be open to:
- Guest post collaboration
- Writing partnership on [SPECIFIC PROJECT]
- Sharing resources/insights

Looking forward to connecting.

Best,
[Your Name]
"""
        return email_template.strip()

def main():
    parser = argparse.ArgumentParser(
        description='Find writers and potential collaborators'
    )
    parser.add_argument('--search', help='Topic to search for writers')
    parser.add_argument('--type', choices=['writers', 'developers', 'collaborators'],
                       default='writers', help='Type of contact')
    parser.add_argument('--limit', type=int, default=15, help='Max contacts to find')

    args = parser.parse_args()

    finder = ContactFinder()

    if args.search:
        print(f"\n\U0001f50d Finding {args.type} interested in: {args.search}")
        contacts = finder.search_by_topic(args.search)

        if contacts:
            print(f"✅ Found {len(contacts)} potential contacts\n")
            for c in contacts[:5]:
                print(f"   • {c['name']} ({c['platform']})")
                print(f"     Profile: {c['profile']}")
                print(f"     Email guess: {c['potential_email']}\n")

            if contacts:
                email = finder.generate_outreach_email(contacts[0], args.search)
                print("\U0001f4e7 Sample outreach email:\n")
                print(email)
        else:
            print(f"❌ No contacts found for '{args.search}'")
    else:
        print("❌ Use --search to find contacts")

if __name__ == '__main__':
    main()
