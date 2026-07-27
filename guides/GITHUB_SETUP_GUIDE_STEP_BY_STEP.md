# GITHUB SETUP GUIDE — STEP BY STEP
## Create & Upload a Repository
**Time:** 30–45 minutes | **Cost:** Free | **Difficulty:** Beginner-friendly

---

## WHAT YOU'LL END UP WITH

A GitHub repository (online code storage) containing all your documents, organized into folders, with version control and backup.

---

## PREREQUISITES (Check These First)

### 1. GitHub Account
- **Do you have one?**
  - ✅ Yes → Skip to Step 1
  - ❌ No → Go to github.com/signup → Create account (free)

### 2. Git Installed on Your Computer
- **Windows:** Download from git-scm.com → Run installer → Accept defaults
- **Mac:** Download from git-scm.com → Run installer → Accept defaults
- **Linux:** `sudo apt-get install git`

**Test if Git is installed:**
```bash
git --version
# Should see: git version 2.x.x
```

---

## STEP 1: CREATE REPOSITORY ON GITHUB.COM

### 1A. Log In to GitHub
1. Go to github.com
2. Click "Sign in"
3. Enter email + password

### 1B. Create New Repository
1. Click "+" icon (top right)
2. Select "New repository"

### 1C. Fill in Repository Details
```
Repository name: your-repo-name
Description: Brief description
Visibility:
   ⭕ Private (only you can see) — RECOMMENDED for personal data
   ⭕ Public (anyone can see) — for open source/sharing

☑ Add a README file (YES, check this)
☑ Add .gitignore (YES, select 'Python' or 'Node')
```

### 1D. Click "Create Repository"

---

## STEP 2: CLONE REPOSITORY TO YOUR COMPUTER

### 2A. Get the Repository URL
1. On GitHub repo page, click green button "Code"
2. Under "HTTPS", click copy icon
3. URL format: `https://github.com/YOUR_USERNAME/your-repo-name.git`

### 2B. Open Terminal/Command Prompt
**Windows:** `Win` key + type "cmd" → Enter  
**Mac:** `Cmd` + `Space` → Type "Terminal" → Enter  
**Linux:** Right-click desktop → "Open Terminal Here"

### 2C. Navigate to Where You Want to Store Files
```bash
cd ~/Documents
```

### 2D. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/your-repo-name.git
```

### 2E. Enter the Repository Folder
```bash
cd your-repo-name
```

---

## STEP 3: CREATE FOLDER STRUCTURE

```bash
mkdir docs guides tools skills projects
```

---

## STEP 4: COPY FILES INTO FOLDERS

Copy your files into the correct folders using your file manager or terminal:

```bash
cp /path/to/your/file.md ./docs/
cp /path/to/script.py ./tools/
```

---

## STEP 5: UPDATE .gitignore

Open `.gitignore` and add:

```
# Sensitive files
.env
credentials.json
*.xml
credentials/

# OS files
.DS_Store
Thumbs.db

# Large files
*.iso
*.zip
*.tar.gz
```

---

## STEP 6: UPLOAD TO GITHUB

### 6A. Check Status
```bash
git status
```

### 6B. Add All Files
```bash
git add .
```

### 6C. Create Commit
```bash
git commit -m "Initial commit: Add project files"
```

### 6D. Push to GitHub
```bash
git push origin main
```

---

## STEP 7: VERIFY ON GITHUB.COM

1. Go to github.com
2. Log in
3. Click on your repository
4. You should see all files and folders

---

## TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| `git: command not found` | Git not installed — download from git-scm.com |
| `fatal: could not read Username` | Use HTTPS URL, not SSH |
| `Permission denied (publickey)` | Set up SSH keys or use HTTPS |
| File too large | Use Git LFS for files >100MB |

---

## ONGOING MAINTENANCE

```bash
# Making changes:
git add .
git commit -m "Description of change"
git push origin main

# Updating from multiple devices:
git pull origin main
```

---

## FINAL CHECKLIST

- [ ] GitHub account created
- [ ] Git installed on computer
- [ ] Repository created on GitHub
- [ ] Repository cloned to computer
- [ ] Folder structure created
- [ ] Files copied into correct folders
- [ ] .gitignore customized
- [ ] README.md customized
- [ ] Files added and committed
- [ ] Pushed to GitHub
- [ ] Verified on github.com
