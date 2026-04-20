# 📡 Filter Analyzer

A professional, interactive web application built with **Streamlit**, **SciPy**, and **Matplotlib** for visualizing and analyzing continuous-time analog filters in the frequency domain.

## ✨ Features

- **Approximation Methods**: Supports **Butterworth**, **Chebyshev Type I**, and **Chebyshev Type II** filter designs.
- **Filter Responses**: Low-Pass (LPF), High-Pass (HPF), Band-Pass (BPF), and Band-Stop (BSF).
- **Multi-Order Overlay**: Compare multiple filter orders simultaneously (1st through 12th) directly on a unified magnitude plot.
- **Transfer Functions**: Generates and displays the exact magnitude transfer function formula $|H(j\omega)|$ per order, cleanly styled to match the filter's characteristic trace color.
- **Data Export & Tabulation**: High-precision data tables evaluating radial frequency ($\omega$), $|H(j\omega)|$, and Gain (dB) at $0.2 \text{ rad/s}$ intervals. Easily export any order's plot data to CSV.
- **Modern UI Edge**: Built-in Theme-Aware Dark/Light Mode toggle, square-cell engineering magnitude grids, and a beautiful UI utilizing *Outfit* and *Plus Jakarta Sans* typography.

---

## 🚀 Quickstart: Run Locally

1. **Navigate into the directory**
   ```bash
   cd Filter-Analyzer
   ```

2. **Install the dependencies**
   ```bash
   pip install -r Requirements.txt
   ```

3. **Launch the application**
   ```bash
   streamlit run app.py
   ```
   *The Streamlit application will automatically open in your browser at `http://localhost:8501`.*

---

## ☁️ Deployment

**Deploy to Streamlit Community Cloud for free:**

1. Push this repository to GitHub.
2. Visit [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New app**.
4. Select your repository, configure the branch, and set the **Main file path** to `app.py`.
5. Click **Deploy**. Your application will go live with a secure public URL instantly.

---

## 📁 Repository Structure

```text
Filter-Analyzer/
├── app.py               # Main Streamlit web application & logic
├── Requirements.txt     # Python package dependencies
└── README.md            # Project documentation (this file)
```