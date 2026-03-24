# 🏥 CTRI Clinical Trials Scraper

Automatically searches the **WHO ICTRP portal** for Clinical Trials registered in India (CTRI) and saves results as a CSV file.

> No installation on your computer needed — everything runs on GitHub for free.

---

## 📋 What you'll get

A CSV file saved in the `results/` folder of your GitHub repository containing trials matching your search keyword, with fields like trial title, condition, intervention, sponsor, phase, status, and more.

---

## 🚀 Setup (one-time, takes ~5 minutes)

### Step 1 — Create a free GitHub account
Go to [github.com](https://github.com) and sign up if you don't have an account.

### Step 2 — Create a new repository
1. Click the **+** icon (top right) → **New repository**
2. Name it something like `ctri-scraper`
3. Set it to **Public** or **Private** (either works)
4. Tick **"Add a README file"**
5. Click **Create repository**

### Step 3 — Upload these files
You need to upload **3 files** and **1 folder** to your repository:

| File/Folder | What it does |
|---|---|
| `scraper.py` | The actual scraping code |
| `requirements.txt` | Lists the tools the scraper needs |
| `.github/workflows/scrape.yml` | Tells GitHub when and how to run the scraper |

**How to upload:**
1. In your repository, click **Add file → Upload files**
2. Drag and drop `scraper.py` and `requirements.txt`
3. Click **Commit changes**

For the workflow file:
1. Click **Add file → Create new file**
2. In the filename box type exactly: `.github/workflows/scrape.yml`
   *(GitHub will auto-create the folders)*
3. Paste the contents of `scrape.yml` into the editor
4. Click **Commit changes**

---

## ▶️ Running the scraper

### Option A — Run manually with any keyword (recommended to start)

1. Go to your repository on GitHub
2. Click the **Actions** tab (top menu)
3. On the left, click **CTRI Trial Scraper**
4. Click the **Run workflow** button (right side)
5. Type your keyword (e.g. `hypertension`, `cancer`, `diabetes`)
6. Click the green **Run workflow** button

⏱ It takes about 1–2 minutes to run.

### Option B — Run automatically every week

The scraper is already set up to run every **Sunday at 8am UTC** automatically.
To change the keyword it uses, set a **Repository Secret**:

1. Go to your repo → **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Name: `DEFAULT_KEYWORD`
4. Value: your keyword (e.g. `tuberculosis`)
5. Click **Add secret**

---

## 📥 Downloading your results

After the scraper runs:

1. Click the **Actions** tab
2. Click the most recent run
3. Scroll down to **Artifacts**
4. Click **ctri-results-[keyword]** to download the ZIP

Or find the CSV file committed directly to the `results/` folder in your repository.

---

## 🔄 Running for multiple keywords

Just repeat **Option A** with different keywords — each run creates a separate CSV file named with the keyword and date, e.g.:
```
results/ctri_diabetes_20260324_0800.csv
results/ctri_hypertension_20260324_0805.csv
```

---

## ❓ Troubleshooting

| Problem | Fix |
|---|---|
| Actions tab not visible | Go to Settings → Actions → Allow all actions |
| Scraper runs but 0 results | Try a broader keyword. Check `debug_output.html` in artifacts |
| Workflow file not found | Make sure the path is exactly `.github/workflows/scrape.yml` |

---

## 📌 Notes

- Data comes from [WHO ICTRP](https://trialsearch.who.int), which imports CTRI data **weekly**
- Results are for **research purposes only** per WHO terms of use
- Do not use for marketing or commercial purposes
