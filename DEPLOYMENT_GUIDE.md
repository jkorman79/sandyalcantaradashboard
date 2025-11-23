# Deployment Guide: Making Your Dashboard Public

This guide will help you deploy your Sandy Alcantara Performance Analysis Dashboard to Streamlit Community Cloud so you can share it publicly.

## Option 1: Streamlit Community Cloud (Recommended - FREE & EASIEST)

### Step 1: Create a GitHub Account (if you don't have one)
1. Go to https://github.com
2. Sign up for a free account

### Step 2: Create a New Repository
1. Click the "+" icon in the top right → "New repository"
2. Name it something like `sandy-alcantara-dashboard` or `mlb-pitching-analysis`
3. Make it **Public** (required for free Streamlit hosting)
4. **Don't** initialize with README, .gitignore, or license (we already have files)
5. Click "Create repository"

### Step 3: Push Your Code to GitHub

Open your terminal in the project folder and run:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Create your first commit
git commit -m "Initial commit: Sandy Alcantara Performance Dashboard"

# Add your GitHub repository as remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4: Deploy to Streamlit Community Cloud

1. Go to https://share.streamlit.io/
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository and branch (usually `main`)
5. Set the **Main file path** to: `dashboard.py`
6. Click "Deploy"

**That's it!** Your dashboard will be live at a URL like:
`https://YOUR_USERNAME-REPO_NAME.streamlit.app`

### Step 5: Share Your Dashboard

Once deployed, you can:
- Share the public URL with anyone
- Add it to your portfolio
- The dashboard will automatically update when you push changes to GitHub

---

## Option 2: Alternative Hosting Options

### Railway (railway.app)
- Free tier available
- Easy deployment from GitHub
- Good for production apps

### Render (render.com)
- Free tier available
- Automatic deployments from GitHub
- Good alternative to Streamlit Cloud

### Heroku
- More complex setup
- Requires credit card (though free tier exists)
- Less recommended for simple Streamlit apps

---

## Important Notes

### Before Deploying:
1. **Make sure your data file is in the repository** - The Excel file needs to be committed to GitHub
2. **Check file paths** - The code uses relative paths like `'Data/sandy_stats_since_21 copy.xlsx'` which should work fine
3. **Test locally first** - Make sure everything works with `streamlit run dashboard.py`

### After Deploying:
- Your dashboard will be publicly accessible
- Anyone with the URL can view it
- Updates happen automatically when you push to GitHub
- You can add a custom domain later if needed

### For Your Portfolio:
You can embed the dashboard or link to it. Example HTML:
```html
<a href="https://your-dashboard.streamlit.app" target="_blank">
    View Interactive Dashboard: Sandy Alcantara Performance Analysis
</a>
```

---

## Troubleshooting

**Issue: "Module not found" errors**
- Make sure `requirements.txt` includes all dependencies
- Streamlit Cloud will automatically install packages from requirements.txt

**Issue: "File not found" errors**
- Make sure the Data folder and Excel file are committed to GitHub
- Check that file paths in the code match the repository structure

**Issue: Dashboard loads but shows errors**
- Check the Streamlit Cloud logs (click "Manage app" → "Logs")
- Make sure all Python packages are in requirements.txt

---

## Quick Start Commands

If you're new to Git, here's a quick reference:

```bash
# Check if git is installed
git --version

# Navigate to your project folder
cd "/Users/josephkorman/Desktop/Coding/Vibe Coding for MGMT 504"

# Initialize git repository
git init

# Add all files
git add .

# Create commit
git commit -m "Initial commit"

# Add GitHub remote (replace with your actual repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git push -u origin main
```

---

## Need Help?

- Streamlit Community Cloud Docs: https://docs.streamlit.io/streamlit-community-cloud
- Streamlit Forum: https://discuss.streamlit.io/
- GitHub Help: https://docs.github.com/

Good luck with your deployment! 🚀

