import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy import signal
import pandas as pd

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Filter Analyzer",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── THEME STATE ─────────────────────────────────────────────────────────────

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

THEME = st.session_state.theme

if THEME == "dark":
    C = dict(
        bg_main="#010409",   bg_surface="#0d1117",  bg_deep="#161b22",
        border="#21262d",    border_mid="#30363d",
        text="#e6edf3",      text_muted="#a4b1be",
        accent="#58a6ff",    accent_bg="#1c2d4b",   accent_border="#1f4068",
        warn="#f0883e",
        fig_bg="#0d1117",    plot_bg="#0d1117",
        spine="#30363d",     grid_maj="#21262d",    grid_min="#161b22",
        tick="#8b98a5",
    )
else:
    C = dict(
        bg_main="#ffffff",   bg_surface="#f6f8fa",  bg_deep="#eaeef2",
        border="#d0d7de",    border_mid="#8c959f",
        text="#000000",      text_muted="#3a424a",
        accent="#0969da",    accent_bg="#ddf4ff",   accent_border="#54aeff",
        warn="#9a6700",
        fig_bg="#ffffff",    plot_bg="#f6f8fa",
        spine="#d0d7de",     grid_maj="#eaeef2",    grid_min="#f6f8fa",
        tick="#3a424a",
    )


# ─── CUSTOM CSS ──────────────────────────────────────────────────────────────

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700&family=Outfit:wght@700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 14px;
}}
.stApp {{ background: {C['bg_main']}; color: {C['text']}; }}
[data-testid="stSidebar"] {{
    background: {C['bg_surface']};
    border-right: 1px solid {C['border']};
}}
[data-testid="stSidebar"] * {{ color: {C['text']} !important; }}

.app-title {{
    font-family: 'Outfit', sans-serif;
    font-size: 2.1rem;
    font-weight: 800;
    color: {C['text']};
    letter-spacing: -0.5px;
    margin-bottom: 0;
}}
.app-sub {{
    color: {C['text_muted']};
    font-size: 0.8rem;
    margin-top: 4px;
    margin-bottom: 1.5rem;
}}
.badge {{
    display: inline-block;
    background: {C['accent_bg']};
    color: {C['accent']};
    border: 1px solid {C['accent_border']};
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    margin-left: 10px;
    vertical-align: middle;
}}
.section-header {{
    font-size: 0.7rem;
    font-weight: 700;
    color: {C['accent']};
    letter-spacing: 0.1em;
    text-transform: uppercase;
    border-bottom: 1px solid {C['border']};
    padding-bottom: 6px;
    margin-bottom: 14px;
    margin-top: 10px;
}}
.hs-card {{
    background: {C['bg_surface']};
    border: 1px solid {C['border']};
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 10px;
    transition: box-shadow 0.2s ease, border-color 0.2s ease;
}}
.hs-card:hover {{
    border-color: {C['accent_border']};
    box-shadow: 0 4px 18px rgba(0,0,0,0.12);
}}
.hs-order {{
    font-size: 0.67rem;
    color: {C['text_muted']};
    font-weight: 700;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
    text-transform: uppercase;
}}
.hs-formula {{
    font-size: 0.83rem;
    color: {C['text']};
    word-break: break-all;
    line-height: 1.7;
}}
.hs-mag {{
    font-size: 0.8rem;
    color: {C['accent']};
    margin-top: 8px;
    font-weight: 600;
}}
.metric-label {{ font-size: 0.65rem; color: {C['text_muted']}; letter-spacing: 0.06em; }}
.metric-value {{ font-size: 1rem; color: {C['text']}; font-weight: 700; margin-top: 2px; }}
.stDataFrame {{ font-size: 0.83rem !important; }}

/* ── Font Awesome (Solid) ─────────────────────────────────────────────────── */
@font-face {{
    font-family: "Font Awesome 6 Free";
    font-style: normal;
    font-weight: 900;
    src: url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/webfonts/fa-solid-900.woff2") format("woff2");
}}
/* Apply FA font only to the theme-toggle button */
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] p {{
    font-family: "Font Awesome 6 Free" !important;
    font-weight: 900 !important;
    font-size: 1rem !important;
}}
/* Multiselect chips — green instead of red ─────────────────────────────── */
[data-testid="stMultiSelect"] [data-baseweb="tag"] {{
    background-color: {"#0d2b0d" if THEME == "dark" else "#dcfce7"} !important;
    border: 1px solid {"#3fb950" if THEME == "dark" else "#16a34a"} !important;
}}
[data-testid="stMultiSelect"] [data-baseweb="tag"] span {{
    color: {"#3fb950" if THEME == "dark" else "#16a34a"} !important;
    font-weight: 600 !important;
}}
/* Stronger sidebar label contrast ────────────────────────────────────────── */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] p {{
    color: {C['text']} !important;
    font-weight: 500 !important;
}}

/* ── Gradient app title ────────────────────────────────────────────────── */
.app-title {{
    background: linear-gradient(130deg, {C['accent']} 0%, {'#bc8cff' if THEME == 'dark' else '#6e40c9'} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}
/* ── Sidebar top accent line ─────────────────────────────────────────── */
[data-testid="stSidebar"] > div:first-child {{
    border-top: 3px solid {C['accent']};
}}
/* ── Badge glow ──────────────────────────────────────────────────────── */
.badge {{
    box-shadow: 0 0 14px {C['accent']}55;
}}
/* ── Section header ── left accent bar ────────────────────────────────── */
.section-header {{
    border-left: 3px solid {C['accent']};
    border-bottom: 1px solid {C['border']};
    padding-left: 12px;
}}
/* ── hs-card gradient ───────────────────────────────────────────────── */
.hs-card {{
    background: linear-gradient(145deg, {C['bg_surface']} 0%, {C['bg_deep']} 100%);
}}
/* ── Metric cards ──────────────────────────────────────────────────── */
[data-testid="stMetric"] {{
    background: {C['bg_surface']};
    border: 1px solid {C['border']};
    border-radius: 12px;
    padding: 14px 18px !important;
    transition: box-shadow 0.2s ease, border-color 0.2s ease;
}}
[data-testid="stMetric"]:hover {{
    border-color: {C['accent_border']};
    box-shadow: 0 4px 18px {'rgba(88,166,255,0.15)' if THEME == 'dark' else 'rgba(9,105,218,0.10)'};
}}
[data-testid="stMetricLabel"] > div {{
    font-size: 0.66rem !important;
    color: {C['text_muted']} !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}}
[data-testid="stMetricValue"] > div {{
    font-size: 1.35rem !important;
    color: {C['accent']} !important;
    font-weight: 700 !important;
}}
/* ── Fade-in animation ──────────────────────────────────────────────── */
@keyframes fadeSlideUp {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
.hs-card {{ animation: fadeSlideUp 0.35s ease forwards; }}
/* ── Custom scrollbar ─────────────────────────────────────────────── */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: {C['bg_deep']}; }}
::-webkit-scrollbar-thumb {{ background: {C['border_mid']}; border-radius: 4px; }}
::-webkit-scrollbar-thumb:hover {{ background: {C['accent']}; }}
/* ── Tab styling ────────────────────────────────────────────────────── */
[data-testid="stTabs"] [role="tab"] {{
    border-radius: 8px 8px 0 0 !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    transition: background 0.2s ease !important;
}}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
    background: {C['accent_bg']} !important;
    color: {C['accent']} !important;
}}
/* ── Number inputs ───────────────────────────────────────────────── */
[data-testid="stNumberInput"] input {{
    border-radius: 8px !important;
}}
[data-testid="stNumberInput"] input:focus {{
    border-color: {C['accent']} !important;
    box-shadow: 0 0 0 3px {C['accent']}22 !important;
}}
/* ── Download button ─────────────────────────────────────────────── */
[data-testid="stDownloadButton"] button {{
    width: 100%;
    border-radius: 8px !important;
    font-weight: 600 !important;
    color: {C['accent']} !important;
    border-color: {C['accent_border']} !important;
    background: {C['accent_bg']} !important;
    transition: all 0.2s ease !important;
}}
[data-testid="stDownloadButton"] button:hover {{
    background: {C['accent']} !important;
    color: {'#ffffff' if THEME == 'light' else '#010409'} !important;
}}
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ────────────────────────────────────────────────────────────────

ORDER_COLORS = [
    "#58a6ff", "#3fb950", "#f0883e", "#bc8cff",
    "#f85149", "#ffa657", "#79c0ff", "#56d364",
    "#ff7b72", "#d2a8ff", "#ffa198", "#7ee787"
]

FILTER_LABELS = {"LPF": "Low-Pass", "HPF": "High-Pass", "BPF": "Band-Pass", "BSF": "Band-Stop"}

# ─── TRANSFER FUNCTION HELPERS ────────────────────────────────────────────────

@st.cache_data
def get_filter_system(method, cheby_type, ftype, order, wc1, wc2, ripple_db=1.0, rs_db=60.0):
    """Returns scipy lti system for the given parameters."""
    btype_map = {"LPF": "low", "HPF": "high", "BPF": "bandpass", "BSF": "bandstop"}
    btype = btype_map[ftype]

    Wn = wc1 if ftype in ("LPF", "HPF") else [wc1, wc2]

    try:
        if method == "Butterworth":
            z, p, k = signal.butter(order, Wn, btype=btype, analog=True, output="zpk")
        elif method == "Chebyshev" and cheby_type == "Type I":
            z, p, k = signal.cheby1(order, ripple_db, Wn, btype=btype, analog=True, output="zpk")
        else:  # Chebyshev Type II
            z, p, k = signal.cheby2(order, rs_db, Wn, btype=btype, analog=True, output="zpk")
        return z, p, k
    except Exception:
        return None, None, None


def poly_to_str(coeffs, var="s"):
    """Convert polynomial coefficients to readable string."""
    coeffs = np.real(coeffs)
    n = len(coeffs) - 1
    terms = []
    for i, c in enumerate(coeffs):
        power = n - i
        if abs(c) < 1e-10:
            continue
        c_str = f"{abs(c):.4g}"
        if power == 0:
            term = c_str
        elif power == 1:
            term = f"{c_str}{var}"
        else:
            term = f"{c_str}{var}^{power}"
        sign = "+" if c >= 0 else "-"
        terms.append((sign, term))
    if not terms:
        return "0"
    result = ""
    for i, (sign, term) in enumerate(terms):
        if i == 0:
            result += f"-{term}" if sign == "-" else term
        else:
            result += f" {sign} {term}"
    return result


def get_hjw_magnitude_expr(ftype, order, wc1, mag_at_wc, db_at_wc, wc2=None):
    """Return a human-readable |H(jω)| expression using actual computed values."""
    base = f"|H(jωc)| = {mag_at_wc:.5f}  ({db_at_wc:.2f} dB)  @ ωc={wc1:.4g}"
    if ftype in ("BPF", "BSF") and wc2 is not None:
        base += f"  …  {wc2:.4g}"
    return base


def poly_magnitude_sq_coeffs(coeffs):
    """
    Given H(s) polynomial coefficients [c0, ..., cn] (c0*s^n + ... + cn),
    return coefficients of |P(jω)|² as a numpy array in ω (highest power first).
    """
    coeffs = np.real(coeffs)
    n = len(coeffs) - 1
    re, im = {}, {}
    for i, c in enumerate(coeffs):
        pw = n - i
        j_pw = pw % 4
        if   j_pw == 0: re[pw] = re.get(pw, 0.0) + c
        elif j_pw == 1: im[pw] = im.get(pw, 0.0) + c
        elif j_pw == 2: re[pw] = re.get(pw, 0.0) - c
        elif j_pw == 3: im[pw] = im.get(pw, 0.0) - c

    def dict_to_poly(d):
        if not d:
            return np.poly1d([0.0])
        max_p = max(d) + 1
        arr = np.zeros(max_p)
        for p, c in d.items():
            arr[max_p - 1 - p] = c
        return np.poly1d(arr)

    re_p = dict_to_poly(re)
    im_p = dict_to_poly(im)
    return (re_p * re_p + im_p * im_p).coeffs


def poly_w_str(coeffs, var="w"):
    """Format poly-in-ω coefficient array as a human-readable string."""
    coeffs = np.real(coeffs)
    first = next((i for i, c in enumerate(coeffs) if abs(c) > 1e-8), len(coeffs))
    coeffs = coeffs[first:]
    if len(coeffs) == 0:
        return "0"
    n = len(coeffs) - 1
    terms = []
    for i, c in enumerate(coeffs):
        pw = n - i
        if abs(c) < 1e-8:
            continue
        c_abs = f"{abs(c):.4g}"
        if pw == 0:
            term = c_abs
        elif pw == 1:
            term = var if abs(abs(c) - 1) < 1e-8 else f"{c_abs}*{var}"
        else:
            term = f"{var}^{pw}" if abs(abs(c) - 1) < 1e-8 else f"{c_abs}*{var}^{pw}"
        terms.append(("+" if c >= 0 else "-", term))
    if not terms:
        return "0"
    result = ("-" if terms[0][0] == "-" else "") + terms[0][1]
    for sign, term in terms[1:]:
        result += f" {sign} {term}"
    return result


def build_magnitude_formula(b, a, var="w"):
    """
    Build a copyable |H(jω)| expression from filter b/a coefficients.
    Example: order-1 Butterworth LPF wc=4 → '|H(jw)| = 4 / (w^2 + 16)^(1/2)'
    """
    sq_num = poly_magnitude_sq_coeffs(b)
    sq_den = poly_magnitude_sq_coeffs(a)

    num_trimmed = np.trim_zeros(np.real(sq_num), "f")
    if len(num_trimmed) <= 1:
        const = num_trimmed[0] if len(num_trimmed) == 1 else 0.0
        num_str = f"{np.sqrt(abs(const)):.4g}"
    else:
        num_str = f"({poly_w_str(sq_num, var)})^(1/2)"

    den_str = f"({poly_w_str(sq_den, var)})^(1/2)"
    return f"|H(j{var})| = {num_str} / {den_str}"


# ─── FREQUENCY RESPONSE ───────────────────────────────────────────────────────

@st.cache_data
def compute_response(z, p, k, w_range):
    """Uses ZPK form for numerical stability at high orders."""
    w, H = signal.freqs_zpk(z, p, k, worN=w_range)
    mag = np.abs(H)
    gain_db = 20 * np.log10(np.maximum(mag, 1e-12))
    return w, mag, gain_db


# ─── MATPLOTLIB FIGURE ────────────────────────────────────────────────────────

def plot_magnitude(results, ftype, method, cheby_type, wc1, wc2, ripple_db, rs_db, log_scale, C):
    """Engineering-style interactive Plotly magnitude plot."""
    fig = go.Figure()

    for res in results:
        fig.add_trace(go.Scatter(
            x=res["w"], y=res["mag_db"], mode='lines', 
            line=dict(color=res["color"], width=2.5), 
            name=f"Order {res['order']}"
        ))

    # Error Band Visuals
    if method == "Chebyshev":
        if cheby_type == "Type I":
            fig.add_hline(y=-ripple_db, line_dash="dash", line_color=C["warn"], opacity=0.8, annotation_text=f"-{ripple_db}dB Ripple", annotation_position="bottom right")
        elif cheby_type == "Type II":
            fig.add_hline(y=-rs_db, line_dash="dash", line_color=C["warn"], opacity=0.8, annotation_text=f"-{rs_db}dB Stopband", annotation_position="top right")

    fig.add_hline(y=-3, line_dash="dot", line_color=C["text_muted"], opacity=0.7, annotation_text="-3 dB", annotation_position="bottom left")

    if wc1:
        fig.add_vline(x=wc1, line_dash="dot", line_color=C["warn"], opacity=0.7, annotation_text=f"ωc={wc1}")
    if wc2:
        fig.add_vline(x=wc2, line_dash="dot", line_color=C["warn"], opacity=0.7, annotation_text=f"ωc={wc2}")

    fig.update_layout(
        title=f"{FILTER_LABELS[ftype]} Filter — Magnitude Response",
        xaxis_title="ω  (rad/s)",
        yaxis_title="Magnitude  |H(jω)|  (dB)",
        paper_bgcolor=C["fig_bg"],
        plot_bgcolor=C["plot_bg"],
        font=dict(color=C["text"], family="Plus Jakarta Sans"),
        xaxis=dict(
            type="log" if log_scale else "linear",
            gridcolor=C["grid_maj"], minor=dict(gridcolor=C["grid_min"], showgrid=True), 
            showgrid=True, gridwidth=1, zeroline=False
        ),
        yaxis=dict(
            gridcolor=C["grid_maj"], minor=dict(gridcolor=C["grid_min"], showgrid=True), 
            showgrid=True, gridwidth=1, zeroline=False
        ),
        margin=dict(l=60, r=40, t=80, b=60),
        legend=dict(
            bgcolor=C["fig_bg"], bordercolor=C["border"], borderwidth=1,
            x=0.99, y=0.99, xanchor="right", yanchor="top"
        ),
        hovermode="x unified",
        height=650
    )
    return fig





# ─── SIDEBAR ─────────────────────────────────────────────────────────────────

with st.sidebar:
    _hcol, _tcol = st.columns([4, 1])
    _hcol.markdown("### ⚙️ Configuration")
    _tip = "Switch to Light Mode" if THEME == "dark" else "Switch to Dark Mode"
    _icon = "\uf185" if THEME == "dark" else "\uf186"  # FA: sun / moon
    if _tcol.button(_icon, key="theme_toggle", help=_tip, use_container_width=True):
        st.session_state.theme = "light" if THEME == "dark" else "dark"
        st.rerun()
    st.markdown("---")

    method = st.selectbox("Approximation Method", ["Butterworth", "Chebyshev"])

    cheby_type = None
    ripple_db = 1.0
    rs_db = 60.0
    if method == "Chebyshev":
        cheby_type = st.selectbox("Chebyshev Type", ["Type I", "Type II"])
        if cheby_type == "Type I":
            ripple_db = st.slider("Passband Ripple (dB)", 0.1, 5.0, 1.0, 0.1)
        else:
            rs_db = st.slider("Stopband Attenuation (dB)", 20.0, 100.0, 60.0, 1.0)

    st.markdown("---")

    ftype = st.selectbox("Filter Type", ["LPF", "HPF", "BPF", "BSF"],
                         format_func=lambda x: f"{x} — {FILTER_LABELS[x]}")

    st.markdown("---")

    all_orders = list(range(1, 13))
    selected_orders = st.multiselect(
        "Filter Orders (select multiple)",
        options=all_orders,
        default=[1, 2, 4],
        format_func=lambda x: f"{x}{'st' if x==1 else 'nd' if x==2 else 'rd' if x==3 else 'th'} Order"
    )

    st.markdown("---")

    needs_two = ftype in ("BPF", "BSF")

    if needs_two:
        wc1 = st.number_input("Lower Cutoff ωc1 (rad/s)", min_value=0.01, value=100.0, step=0.2, format="%.1f")
        wc2 = st.number_input("Upper Cutoff ωc2 (rad/s)", min_value=0.01, value=1000.0, step=0.2, format="%.1f")
        if wc2 <= wc1:
            st.error("ωc2 must be greater than ωc1")
    else:
        wc1 = st.number_input("Cutoff Frequency ωc (rad/s)", min_value=0.01, value=1000.0, step=0.2, format="%.1f")
        wc2 = None

    st.markdown("---")

    w_min = st.number_input("ω sweep min (rad/s)", min_value=0.001, value=1.0)
    w_max = st.number_input("ω sweep max (rad/s)", min_value=1.0, value=100000.0)
    n_points = st.slider("Sweep resolution (points)", 200, 2000, 800, 100)
    log_x = st.checkbox("Logarithmic ω axis", value=True)

# ─── MAIN ─────────────────────────────────────────────────────────────────────

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, {C['accent_bg']} 0%, {C['bg_deep']} 55%, {C['bg_surface']} 100%);
    border: 1px solid {C['accent_border']};
    border-radius: 18px;
    padding: 28px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
">
    <div style="
        position:absolute; top:-60px; right:-40px;
        width:220px; height:220px;
        background: radial-gradient(circle, {C['accent']}1a 0%, transparent 70%);
        border-radius:50%; pointer-events:none;
    "></div>
    <div style="
        position:absolute; bottom:-40px; left:35%;
        width:140px; height:140px;
        background: radial-gradient(circle, {'#bc8cff' if THEME == 'dark' else '#6e40c9'}14 0%, transparent 70%);
        border-radius:50%; pointer-events:none;
    "></div>
    <p class="app-title">Filter Analyzer <span class="badge">H(ω) &middot; ω-DOMAIN</span></p>
    <p class="app-sub">Butterworth &middot; Chebyshev I &amp; II &middot; Orders 1&ndash;12 &middot; LPF / HPF / BPF / BSF</p>
</div>
""", unsafe_allow_html=True)

if not selected_orders:
    st.warning("Select at least one filter order from the sidebar.")
    st.stop()

if needs_two and wc2 and wc2 <= wc1:
    st.error("Upper cutoff ωc2 must be greater than lower cutoff ωc1.")
    st.stop()

# ─── COMPUTE ALL ORDERS ───────────────────────────────────────────────────────

w_range = np.logspace(np.log10(w_min), np.log10(w_max), n_points) if log_x \
    else np.linspace(w_min, w_max, n_points)

results = []
failed_orders = []

for order in sorted(selected_orders):
    z, p, k = get_filter_system(method, cheby_type, ftype, order, wc1, wc2, ripple_db, rs_db)
    if z is None:
        failed_orders.append(order)
        continue
    w, mag, gain_db = compute_response(z, p, k, w_range)
    b, a = signal.zpk2tf(z, p, k)  # only used for H(s) display
    results.append({
        "order": order,
        "b": b, "a": a,
        "w": w, "mag": mag, "mag_db": gain_db,
        "color": ORDER_COLORS[len(results) % len(ORDER_COLORS)],
    })

if failed_orders:
    st.warning(f"Could not compute orders: {failed_orders}. Check your cutoff frequencies.")

if not results:
    st.error("No valid filter configurations. Adjust parameters.")
    st.stop()

# ─── SECTION 1: TRANSFER FUNCTIONS ───────────────────────────────────────────

st.markdown('<div class="section-header">① Frequency Response H(ω)</div>', unsafe_allow_html=True)

cols = st.columns(min(len(results), 3))
for idx, res in enumerate(results):
    col = cols[idx % len(cols)]
    with col:
        mag_at_wc = np.interp(wc1, res["w"], res["mag"])
        db_at_wc = 20 * np.log10(max(mag_at_wc, 1e-12))
        hw_expr = build_magnitude_formula(res["b"], res["a"])

        st.markdown(f"""
        <div class="hs-card" style="border-left: 3px solid {res['color']}">
            <div class="hs-order">ORDER {res['order']} · {method}{' ' + cheby_type if cheby_type else ''}</div>
            <div style="
                font-family: 'Courier New', monospace;
                font-size: 0.88rem;
                background: {C['bg_deep']};
                color: {res['color']};
                border: 1px solid {C['border']};
                border-radius: 8px;
                padding: 10px 14px;
                margin: 10px 0 4px 0;
                user-select: all;
                cursor: text;
                letter-spacing: 0.02em;
            ">{hw_expr}</div>
            <div style="font-size:0.63rem;color:{C['text_muted']};margin-bottom:8px;
                        letter-spacing:0.04em;">
                ↑ Click to select all &nbsp;·&nbsp; substitute <em>w</em> with your ω
            </div>
            <div class="hs-mag">At ωc = {wc1:.1f} rad/s &nbsp;·&nbsp;
                |H(jωc)| = {mag_at_wc:.5f} &nbsp;|&nbsp; {db_at_wc:.2f} dB
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─── SECTION 2: MAGNITUDE PLOT ────────────────────────────────────────────────

st.markdown('<div class="section-header">② Magnitude Response — All Orders Overlaid</div>', unsafe_allow_html=True)

fig_mag = plot_magnitude(results, ftype, method, cheby_type, wc1, wc2, ripple_db, rs_db, log_x, C)
st.plotly_chart(fig_mag, use_container_width=True, config={"displayModeBar": True})

# ─── SECTION 3: DATA TABLES ───────────────────────────────────────────────────

st.markdown('<div class="section-header">③ Data Tables — ω, |H(ω)|, Gain (dB)</div>', unsafe_allow_html=True)

tab_labels = [f"Order {r['order']}" for r in results]
tabs = st.tabs(tab_labels)

for tab, res in zip(tabs, results):
    with tab:
        # Build table at exact 0.2 rad/s steps, max 500 rows
        step_size = 0.2
        t_start = np.ceil(w_min / step_size) * step_size
        tbl_w = np.round(np.arange(t_start, w_max + 1e-9, step_size), 1)[:500]
        # Keep only values within the computed response range
        tbl_w = tbl_w[(tbl_w >= res["w"].min()) & (tbl_w <= res["w"].max())]
        tbl_mag = np.round(np.interp(tbl_w, res["w"], res["mag"]), 6)
        tbl_db  = np.round(np.interp(tbl_w, res["w"], res["mag_db"]), 4)
        df = pd.DataFrame({
            "ω (rad/s)": tbl_w,
            "|H(jω)|": tbl_mag,
            "Gain (dB)": tbl_db,
        })

        col1, col2 = st.columns(2)
        mag_at_wc = np.interp(wc1, res["w"], res["mag"])
        db_at_wc = 20 * np.log10(max(mag_at_wc, 1e-12))

        col1.metric("|H(jωc)|", f"{mag_at_wc:.5f}")
        col2.metric("Gain at ωc", f"{db_at_wc:.2f} dB")

        st.dataframe(df, use_container_width=True, height=320)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"⬇ Export Order {res['order']} as CSV",
            data=csv,
            file_name=f"filter_order{res['order']}_{ftype}_{method}.csv",
            mime="text/csv",
        )

# ─── FOOTER ───────────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown(
    f'<p style="color:{C["text_muted"]};font-size:0.72rem;text-align:center;">'
    'Filter Analyzer · Butterworth &amp; Chebyshev I/II · Built with Streamlit + SciPy + Plotly'
    '</p>', unsafe_allow_html=True
)