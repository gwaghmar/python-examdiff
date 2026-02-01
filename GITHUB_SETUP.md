# GitHub Repository Setup Guide

This guide will help you create and upload this project to GitHub.

## Step 1: Create GitHub Repository

### Option A: Using GitHub Web Interface

1. Go to [GitHub](https://github.com) and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Repository name: `python-examdiff`
4. Description: `Professional file and directory comparison tool for Windows - An enhanced ExamDiff Pro clone with modern GUI, syntax highlighting, and advanced diff features`
5. Visibility: **Public** (or Private if you prefer)
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click **"Create repository"**

### Option B: Using GitHub CLI (if installed)

```bash
gh repo create python-examdiff --public --description "Professional file and directory comparison tool for Windows"
```

## Step 2: Initialize Git Repository (if not already done)

```bash
cd "C:\Users\govin\Downloads\drive-download-20260131T235116Z-3-001\EXAMDIFF"
git init
```

## Step 3: Add All Files

```bash
git add .
```

## Step 4: Create Initial Commit

```bash
git commit -m "Initial commit: Python ExamDiff Pro - Professional file comparison tool"
```

## Step 5: Connect to GitHub Repository

Replace `YOUR_USERNAME` with your GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/python-examdiff.git
```

## Step 6: Push to GitHub

```bash
git branch -M main
git push -u origin main
```

## Step 7: Update README URLs

After creating the repository, update the following files with your actual GitHub username:

1. **README.md**: Replace `YOUR_USERNAME` with your GitHub username
2. **pyproject.toml**: Replace `YOUR_USERNAME` with your GitHub username

## Step 8: Add Screenshots (Optional but Recommended)

1. Take screenshots of the application:
   - Main window showing file comparison
   - Directory comparison view
   - Syntax highlighting example
   - Three-way merge interface
   - HTML report output

2. Save screenshots to `docs/screenshots/` with these names:
   - `main-window.png`
   - `directory-view.png`
   - `syntax-highlighting.png`
   - `three-way-merge.png`
   - `html-report.png`

3. Commit and push:
   ```bash
   git add docs/screenshots/*.png
   git commit -m "docs: add application screenshots"
   git push
   ```

## Step 9: Create a Release (Optional)

1. Go to your repository on GitHub
2. Click **"Releases"** → **"Create a new release"**
3. Tag version: `v1.0.0`
4. Release title: `Python ExamDiff Pro v1.0.0`
5. Description: Copy from README.md features section
6. Upload the `PythonExamDiff.exe` file if you have it
7. Click **"Publish release"**

## Troubleshooting

### Authentication Issues

If you get authentication errors:

1. **Use Personal Access Token**:
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Generate a new token with `repo` permissions
   - Use token as password when pushing

2. **Or use SSH**:
   ```bash
   git remote set-url origin git@github.com:YOUR_USERNAME/python-examdiff.git
   ```

### Large Files

If you have large files (like the .exe), consider:
- Using [Git LFS](https://git-lfs.github.com/)
- Or excluding them from the repository (they're already in .gitignore)

## Next Steps

After uploading:

1. ✅ Add screenshots to `docs/screenshots/`
2. ✅ Update README.md with your GitHub username
3. ✅ Update pyproject.toml with your GitHub username
4. ✅ Enable GitHub Actions (CI will run automatically)
5. ✅ Add topics/tags to your repository: `python`, `diff`, `file-comparison`, `windows`, `gui`, `tkinter`
6. ✅ Create a nice repository description
7. ✅ Pin the repository to your profile (optional)

## Repository Topics (Tags)

Add these topics to your repository for better discoverability:
- `python`
- `diff`
- `file-comparison`
- `directory-comparison`
- `windows`
- `gui`
- `tkinter`
- `customtkinter`
- `myers-algorithm`
- `syntax-highlighting`
- `merge-tool`

---

**Your repository is now ready!** 🎉
