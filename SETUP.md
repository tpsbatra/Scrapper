# CTRI Search App — Setup Guide

Two steps: deploy the Worker, then put the frontend on GitHub Pages.

---

## STEP 1 — Deploy the Cloudflare Worker

1. Go to https://dash.cloudflare.com and log in
2. Click **Workers & Pages** in the left menu
3. Click **Create** → **Create Worker**
4. Give it a name e.g. `ctri-worker`
5. Click **Deploy** (ignore the default code)
6. Click **Edit code** (top right)
7. **Delete ALL the existing code** in the editor
8. Open `worker.js` from this package and **paste the entire contents**
9. Click **Deploy** (top right)
10. Copy your Worker URL — it looks like:
    `https://ctri-worker.yourname.workers.dev`

---

## STEP 2 — Set up the Frontend on GitHub Pages

### 2a — Update the Worker URL in index.html

1. Open `index.html` in any text editor (Notepad is fine)
2. Find this line near the bottom:
   ```
   const WORKER_URL = "YOUR_WORKER_URL_HERE";
   ```
3. Replace `YOUR_WORKER_URL_HERE` with your Worker URL from Step 1
   Example:
   ```
   const WORKER_URL = "https://ctri-worker.yourname.workers.dev";
   ```
4. Save the file

### 2b — Upload to GitHub

1. Go to your **Scrapper** repository on GitHub
2. Click **Add file → Upload files**
3. Upload the updated `index.html`
4. Click **Commit changes**

### 2c — Enable GitHub Pages

1. In your repository, click **Settings**
2. Scroll down to **Pages** (left menu)
3. Under **Source**, select **Deploy from a branch**
4. Branch: **main** / Folder: **/ (root)**
5. Click **Save**
6. Wait 1-2 minutes, then your app will be live at:
   `https://tpsbatra.github.io/Scrapper`

---

## Done! 🎉

Share the link `https://tpsbatra.github.io/Scrapper` with your team.
They enter the password **Ethics** and can search for any condition.

---

## Quick Reference

| What | Where |
|---|---|
| Frontend URL | https://tpsbatra.github.io/Scrapper |
| Password | Ethics |
| Worker URL | https://ctri-worker.yourname.workers.dev |
| To change password | Edit `index.html` → find `const PASSWORD = "Ethics"` |
