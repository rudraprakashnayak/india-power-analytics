# Git Setup and Push Instructions

## Step 1: Initialize Git Repository

Open your terminal/command prompt and navigate to the project folder:

```bash
cd C:\Users\rudra\CascadeProjects\india-power-analytics
```

Initialize the git repository:

```bash
git init
```

## Step 2: Add Files to Git

Add all files (respecting .gitignore):

```bash
git add .
```

Verify what will be committed:

```bash
git status
```

## Step 3: Create Initial Commit

```bash
git commit -m "Initial commit: India Power Consumption Analytics project

- Added synthetic power consumption dataset (500 rows)
- Created SQL schema and analytical queries
- Added Excel and Power BI build guides
- Set up project structure for GitHub portfolio"
```

## Step 4: Create Empty GitHub Repository

1. Go to https://github.com and sign in
2. Click the **+** icon → **New repository**
3. Repository name: `india-power-analytics`
4. Description: "End-to-end analytics project analyzing power consumption across Indian states using Excel, SQL, and Power BI"
5. Make it **Public** (for portfolio visibility)
6. **Do NOT** initialize with README, .gitignore, or license (we already have these)
7. Click **Create repository**

## Step 5: Link Local Repo to GitHub

Copy the repository URL from GitHub (it will look like: `https://github.com/YOUR_USERNAME/india-power-analytics.git`)

Then run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/india-power-analytics.git
```

## Step 6: Push to GitHub

⚠️ **PAUSE HERE**: Confirm you've created the empty GitHub repository before running the push command.

```bash
git branch -M main
git push -u origin main
```

## Step 7: Verify

Go to your GitHub repository page and verify all files are uploaded:
- data/ folder with CSV files
- sql/ folder with SQL scripts
- docs/ folder with guides
- screenshots/ folder (empty initially)
- README.md
- .gitignore

## Troubleshooting

### If push fails with authentication error:
```bash
git config --global credential.helper store
git push -u origin main
```
Then enter your GitHub username and personal access token (not password).

### If you need to change the remote URL:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/india-power-analytics.git
```

### If you accidentally committed .pbix file:
```bash
git rm --cached your-report.pbix
git commit -m "Remove .pbix file"
git push
```
