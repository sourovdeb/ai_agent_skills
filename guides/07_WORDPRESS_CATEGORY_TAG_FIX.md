# WordPress Category and Tag Fix Guide

## Common Problems and How to Fix Them

### Problem 1: Posts Assigned to "Uncategorized"

This happens when:
- No category was specified in the API call
- The category name didn't match an existing category
- The default category was never changed from "Uncategorized"

**Fix via WordPress Admin:**
1. Go to `Posts → Categories`
2. Find "Uncategorized" → click Edit
3. Change the name to your default (e.g., "ELT Masterclass")
4. Update the slug too

**Fix via REST API (Python script):**

Save as `scripts/wordpress_category_fixer.py`:

```python
import requests
import base64
import json

# Configuration - use environment variables
WP_URL   = 'https://sourovdeb.com'
WP_USER  = 'your-username'
WP_PASS  = 'your-application-password'  # From Users > Profile > Application Passwords

headers = {
    'Authorization': 'Basic ' + base64.b64encode(f'{WP_USER}:{WP_PASS}'.encode()).decode(),
    'Content-Type': 'application/json'
}

def get_all_posts(status='any', per_page=100):
    posts = []
    page = 1
    while True:
        resp = requests.get(
            f'{WP_URL}/wp-json/wp/v2/posts',
            headers=headers,
            params={'status': status, 'per_page': per_page, 'page': page}
        )
        if resp.status_code != 200:
            break
        batch = resp.json()
        if not batch:
            break
        posts.extend(batch)
        page += 1
        if len(batch) < per_page:
            break
    return posts

def get_category_id(name):
    resp = requests.get(f'{WP_URL}/wp-json/wp/v2/categories', headers=headers,
                        params={'search': name, 'per_page': 10})
    cats = resp.json()
    for cat in cats:
        if cat['name'].lower() == name.lower():
            return cat['id']
    # Create it if it doesn't exist
    create = requests.post(f'{WP_URL}/wp-json/wp/v2/categories',
                           headers=headers, json={'name': name})
    return create.json()['id']

def fix_uncategorized_posts(new_category='ELT Masterclass'):
    """Move all Uncategorized posts to a proper category."""
    # Get the Uncategorized category ID (usually 1)
    resp = requests.get(f'{WP_URL}/wp-json/wp/v2/categories',
                        headers=headers, params={'slug': 'uncategorized'})
    uncat_id = resp.json()[0]['id'] if resp.json() else 1
    
    new_cat_id = get_category_id(new_category)
    print(f'Moving Uncategorized (ID:{uncat_id}) -> {new_category} (ID:{new_cat_id})')
    
    posts = get_all_posts()
    fixed = 0
    for post in posts:
        if uncat_id in post.get('categories', []):
            # Guess category from title
            guessed = guess_category(post['title']['rendered'])
            cat_id = get_category_id(guessed)
            requests.post(
                f'{WP_URL}/wp-json/wp/v2/posts/{post["id"]}',
                headers=headers,
                json={'categories': [cat_id]}
            )
            print(f'  Fixed: "{post["title"]["rendered"]}" -> {guessed}')
            fixed += 1
    print(f'Done. Fixed {fixed} posts.')

def guess_category(title):
    t = title.lower()
    if any(w in t for w in ['grammar', 'tense', 'verb', 'noun', 'adjective']):
        return 'Grammar'
    if any(w in t for w in ['listen', 'audio', 'phonetic', 'pronunciation']):
        return 'Listening & Phonology'
    if any(w in t for w in ['speak', 'fluency', 'conversation', 'oral']):
        return 'Speaking'
    if any(w in t for w in ['read', 'comprehension', 'text']):
        return 'Reading'
    if any(w in t for w in ['writ', 'essay', 'paragraph', 'composition']):
        return 'Writing'
    if any(w in t for w in ['celta', 'lesson', 'teaching', 'teacher']):
        return 'CELTA'
    if any(w in t for w in ['vocabular', 'word', 'idiom', 'phrase']):
        return 'Vocabulary'
    return 'ELT Masterclass'

def fix_empty_tags(posts=None):
    """Add tags to posts that have none."""
    if posts is None:
        posts = get_all_posts()
    fixed = 0
    for post in posts:
        if not post.get('tags'):
            title = post['title']['rendered']
            new_tags = suggest_tags(title)
            if new_tags:
                tag_ids = [get_or_create_tag(t) for t in new_tags]
                requests.post(
                    f'{WP_URL}/wp-json/wp/v2/posts/{post["id"]}',
                    headers=headers,
                    json={'tags': tag_ids}
                )
                print(f'  Tagged: "{title}" -> {new_tags}')
                fixed += 1
    print(f'Tagged {fixed} posts.')

def get_or_create_tag(name):
    resp = requests.get(f'{WP_URL}/wp-json/wp/v2/tags',
                        headers=headers, params={'search': name})
    tags = resp.json()
    for tag in tags:
        if tag['name'].lower() == name.lower():
            return tag['id']
    create = requests.post(f'{WP_URL}/wp-json/wp/v2/tags',
                           headers=headers, json={'name': name})
    return create.json()['id']

def suggest_tags(title):
    keywords = ['grammar', 'listening', 'speaking', 'reading', 'writing',
                'vocabulary', 'pronunciation', 'CELTA', 'ELT', 'fluency',
                'comprehension', 'tense', 'idiom', 'phrasal verb', 'lesson plan']
    t = title.lower()
    return [kw for kw in keywords if kw.lower() in t][:5]

def audit_wordpress():
    """Print a health report of your WordPress posts."""
    posts = get_all_posts()
    print(f'\n=== WordPress Health Report ===')
    print(f'Total posts: {len(posts)}')
    
    no_tags      = [p for p in posts if not p.get('tags')]
    no_category  = [p for p in posts if not p.get('categories') or p['categories'] == [1]]
    no_excerpt   = [p for p in posts if not p.get('excerpt', {}).get('rendered', '').strip()]
    
    print(f'Posts without tags:       {len(no_tags)}')
    print(f'Posts in Uncategorized:   {len(no_category)}')
    print(f'Posts without excerpt:    {len(no_excerpt)}')
    print()
    
    if no_tags:
        print('Posts needing tags:')
        for p in no_tags[:10]:
            print(f'  - {p["title"]["rendered"]}')
    return posts

if __name__ == '__main__':
    print('WordPress Category & Tag Fixer')
    print('1. Audit (report only, no changes)')
    print('2. Fix uncategorized posts')
    print('3. Add tags to untagged posts')
    print('4. Fix everything')
    choice = input('Choose (1-4): ')
    
    if choice == '1':
        audit_wordpress()
    elif choice == '2':
        fix_uncategorized_posts()
    elif choice == '3':
        fix_empty_tags()
    elif choice == '4':
        posts = audit_wordpress()
        fix_uncategorized_posts()
        fix_empty_tags(posts)
```

**Run it:**
```bash
pip install requests
python3 scripts/wordpress_category_fixer.py
```

---

## Setting Up WordPress Application Password

The script above uses a WordPress Application Password (more secure than your main password):

1. Log into WordPress admin
2. Go to **Users → Your Profile**
3. Scroll down to **Application Passwords**
4. Type a name: `category-fixer`
5. Click **Add New Application Password**
6. Copy the password (format: `xxxx xxxx xxxx xxxx xxxx xxxx`)
7. Remove the spaces when using it in scripts

---

## Preventing Future Category/Tag Problems

### In Your sourov-ai-controller.php Plugin

Add this validation at the top of your post creation function:

```php
// In your plugin: default category fallback
$category = sanitize_text_field($data['category'] ?? 'ELT Masterclass');
$cat_id   = get_cat_ID($category);
if (!$cat_id) {
    // Create the category if it doesn't exist
    $cat_id = wp_insert_category(['cat_name' => $category]);
}
if (!$cat_id) {
    $cat_id = get_cat_ID('ELT Masterclass') ?: 1; // fallback to default
}
```

### In Google Sheets

Use data validation on the Category column:
1. Select column C
2. Click **Data → Data validation**
3. Choose **Dropdown (from a range)** or **Dropdown**
4. Add your categories: `ELT Masterclass, Grammar, Listening & Phonology, Speaking, Reading, Writing, CELTA, Vocabulary`
5. Now you can only pick from the list — no typos, no mismatches
