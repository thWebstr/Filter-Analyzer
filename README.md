# Filter Analyzer — Setup & Deployment Guide

## Run Locally

```bash
# 1. Clone or copy this folder
cd filter_analyzer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```
App opens at → http://localhost:8501

---

## Deploy to Streamlit Cloud (Free, Public URL)

1. Push this folder to a GitHub repo
2. Go to → https://share.streamlit.io
3. Click **New app**
4. Select your repo, branch, and set **Main file path** to `app.py`
5. Click **Deploy** — done. You get a public URL instantly.

---

## Folder Structure

```
filter_analyzer/
├── app.py            ← Main application
├── requirements.txt  ← Dependencies
└── README.md         ← This file
```

---

## Features

- **Approximation methods:** Butterworth, Chebyshev Type I, Chebyshev Type II
- **Filter types:** LPF, HPF, BPF, BSF
- **Orders:** 1st through 12th (multi-select, all overlaid on one graph)
- **Graphs:** Magnitude response (dB) + Phase response — engineering style with major/minor grid
- **Tables:** ω, |H(jω)|, Gain (dB), Phase (°) — one tab per order, CSV export
- **Transfer functions:** H(s) numerator/denominator displayed per order