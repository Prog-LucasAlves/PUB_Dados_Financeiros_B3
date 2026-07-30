import streamlit as st


def inject_custom_css():
    st.markdown(
        """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@300;400;500;700&display=swap');

    /* ═══════════════════════════════════════════ */
    /*  KEYFRAME ANIMATIONS                       */
    /* ═══════════════════════════════════════════ */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 4px rgba(16, 185, 129, 0.3); }
        50% { box-shadow: 0 0 12px rgba(16, 185, 129, 0.6); }
    }
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    @keyframes borderGlow {
        0%, 100% { border-color: rgba(16, 185, 129, 0.08); }
        50% { border-color: rgba(16, 185, 129, 0.2); }
    }

    /* ═══════════════════════════════════════════ */
    /*  GLOBAL FOUNDATION                         */
    /* ═══════════════════════════════════════════ */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0A0D11 !important;
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #E2E8F0 !important;
    }
    [data-testid="stHeader"] {
        background: linear-gradient(180deg, #0A0D11 0%, transparent 100%) !important;
        backdrop-filter: blur(8px) !important;
    }
    [data-testid="stMainBlockContainer"] {
        padding-top: 0 !important;
    }

    /* ═══════════════════════════════════════════ */
    /*  SIDEBAR — BRANDED                         */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D1117 0%, #0A0D11 100%) !important;
        border-right: 1px solid rgba(16, 185, 129, 0.06) !important;
    }
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h3 {
        color: #10B981 !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #111519 !important;
        border: 1px solid rgba(16, 185, 129, 0.12) !important;
        border-radius: 8px !important;
        transition: border-color 0.2s ease !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] > div:hover {
        border-color: rgba(16, 185, 129, 0.3) !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] > div:focus-within {
        border-color: #10B981 !important;
        box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.1) !important;
    }
    [data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[role="slider"] {
        background-color: #10B981 !important;
    }
    [data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"] {
        color: #10B981 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 600 !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        color: #F1F5F9 !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em !important;
    }

    .status-card {
        background: rgba(17, 21, 25, 0.8);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        font-family: 'Outfit', sans-serif;
        color: #F1F5F9;
        margin-top: 10px;
        animation: fadeInUp 0.35s ease-out;
    }
    .status-title {
        font-size: 14px;
        font-weight: 600;
        color: #F8FAFC;
        margin-bottom: 8px;
    }
    .status-body {
        font-size: 13px;
        color: #94A3B8;
        font-family: 'JetBrains Mono', monospace;
    }

    :root {
        --bg: #0A0D11;
        --panel: rgba(17, 21, 25, 0.84);
        --panel-strong: rgba(15, 19, 23, 0.95);
        --border: rgba(255, 255, 255, 0.06);
        --text: #E2E8F0;
        --muted: #94A3B8;
        --accent: #10B981;
        --accent-2: #22C55E;
        --danger: #EF4444;
    }

    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 3rem !important;
    }

    .hero-header {
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 24px 24px 20px;
        margin: 0 0 18px 0;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.16), rgba(15, 23, 42, 0.92));
        box-shadow: 0 16px 50px rgba(0, 0, 0, 0.25);
        animation: fadeInUp 0.45s ease-out;
    }
    .hero-header--analytical {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.18), rgba(2, 6, 23, 0.95));
    }
    .hero-header--comparative {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.16), rgba(17, 24, 39, 0.95));
    }
    .hero-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 16px;
    }
    .hero-logo {
        font-size: 1.05rem;
        font-weight: 800;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: #F8FAFC;
    }
    .hero-logo-accent {
        color: #34D399;
        margin-right: 6px;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,0.08);
        color: #E2E8F0;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    .hero-badge-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: var(--accent);
        box-shadow: 0 0 12px rgba(16,185,129,0.7);
    }
    .hero-title {
        font-size: clamp(1.6rem, 2.5vw, 2.5rem);
        font-weight: 800;
        line-height: 1.05;
        margin-bottom: 8px;
        color: #F8FAFC;
    }
    .hero-subtitle {
        font-size: 1rem;
        line-height: 1.6;
        max-width: 860px;
        color: #CBD5E1;
        margin-bottom: 14px;
    }
    .hero-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 12px;
    }
    .hero-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 10px 14px;
        border-radius: 999px;
        text-decoration: none;
        font-weight: 700;
        transition: transform 160ms ease, box-shadow 160ms ease;
    }
    .hero-btn:hover {
        transform: translateY(-1px);
    }
    .hero-btn-primary {
        background: linear-gradient(90deg, var(--accent), var(--accent-2));
        color: #04110E;
        box-shadow: 0 10px 22px rgba(16, 185, 129, 0.2);
    }
    .hero-btn-secondary {
        background: rgba(255,255,255,0.08);
        color: #F8FAFC;
        border: 1px solid rgba(255,255,255,0.12);
    }

    .sample-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
        margin: 14px 0 22px;
    }
    .sample-card {
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 14px;
        background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
    }
    .sample-card.active {
        border-color: rgba(16,185,129,0.35);
        box-shadow: 0 0 0 1px rgba(16,185,129,0.16), 0 12px 24px rgba(0,0,0,0.18);
    }
    .sample-kicker {
        display: inline-block;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        color: #34D399;
        margin-bottom: 6px;
        font-weight: 700;
    }
    .sample-title {
        font-size: 1rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 6px;
    }
    .sample-copy {
        font-size: 0.9rem;
        color: #94A3B8;
        line-height: 1.45;
    }

    .metric-card {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.96), rgba(11, 18, 30, 0.9));
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 18px;
        padding: 18px 18px 16px;
        margin-bottom: 12px;
        box-shadow: 0 14px 34px rgba(0,0,0,0.22);
        transition: transform 160ms ease, border-color 160ms ease, box-shadow 160ms ease;
    }
    .metric-card:hover {
        transform: translateY(-1px);
        border-color: rgba(16,185,129,0.2);
    }
    .metric-label {
        font-size: 0.86rem;
        font-weight: 700;
        color: #94A3B8;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 8px;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 1.55rem;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.15;
        word-break: break-word;
    }
    .metric-delta {
        margin-top: 9px;
        font-size: 0.88rem;
        font-weight: 700;
    }
    .delta-positive {
        color: #34D399;
    }
    .delta-negative {
        color: #F87171;
    }
    .tooltip-container {
        position: relative;
        color: #34D399;
        cursor: help;
        font-size: 0.78rem;
    }
    .tooltip-text {
        visibility: hidden;
        opacity: 0;
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        top: calc(100% + 8px);
        width: 240px;
        background: rgba(3, 7, 18, 0.96);
        color: #E2E8F0;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 8px 10px;
        font-size: 0.8rem;
        line-height: 1.4;
        z-index: 20;
        transition: opacity 160ms ease;
        pointer-events: none;
    }
    .tooltip-container:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
    }

    .custom-hr {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(16,185,129,0.3), transparent);
        margin: 1.4rem 0;
    }

    .dashboard-panel {
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.07);
        padding: 18px;
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.94), rgba(10, 14, 22, 0.93));
        box-shadow: 0 16px 40px rgba(0,0,0,0.22);
        margin-bottom: 14px;
    }
    .panel-title {
        font-size: 0.95rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 10px;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .panel-subtitle {
        color: #94A3B8;
        font-size: 0.9rem;
        line-height: 1.5;
        margin-bottom: 12px;
    }
    .kpi-strip {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 10px;
        margin-bottom: 12px;
    }
    .kpi-box {
        border-radius: 14px;
        padding: 12px 14px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        min-height: 92px;
    }
    .kpi-label {
        font-size: 0.73rem;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.14rem;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.2;
    }
    .kpi-trend {
        margin-top: 6px;
        font-size: 0.8rem;
        font-weight: 700;
    }

    .graham-card {
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.06);
        padding: 16px;
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.96), rgba(10, 14, 22, 0.94));
        box-shadow: 0 12px 30px rgba(0,0,0,0.16);
    }
    .graham-positive {
        border-color: rgba(16,185,129,0.24);
    }
    .graham-negative {
        border-color: rgba(248,113,113,0.24);
    }
    .graham-title {
        font-size: 1.02rem;
        color: #F8FAFC;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .graham-text {
        color: #94A3B8;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    .graham-highlight {
        color: #F8FAFC;
        font-weight: 700;
    }
    .graham-values-row {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 10px;
    }
    .graham-value-box {
        background: rgba(255,255,255,0.04);
        border-radius: 12px;
        padding: 10px;
    }
    .graham-value-box-label {
        font-size: 0.78rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }
    .graham-value-box-number {
        font-size: 1rem;
        font-weight: 800;
    }

    /* ═══════════════════════════════════════════ */
    /*  STREAMLIT COMPONENT CONTRAST OVERRIDES    */
    /* ═══════════════════════════════════════════ */
    /* Expanders */
    [data-testid="stExpander"] {
        background-color: #111519 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
        overflow: hidden !important;
    }
    [data-testid="stExpander"] details {
        background-color: #111519 !important;
        border: none !important;
    }
    [data-testid="stExpander"] summary {
        color: #F8FAFC !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 12px 16px !important;
    }
    [data-testid="stExpander"] summary:hover {
        color: #00E676 !important;
    }
    [data-testid="stExpander"] summary svg {
        fill: #00E676 !important;
        color: #00E676 !important;
    }
    [data-testid="stExpander"] [data-testid="stVerticalBlock"] {
        padding: 8px 16px 16px 16px !important;
    }

    /* Tabs */
    [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        gap: 8px !important;
        padding-bottom: 4px !important;
    }
    [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #94A3B8 !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 8px 16px !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    [data-baseweb="tab"]:hover {
        color: #F8FAFC !important;
        background-color: rgba(255, 255, 255, 0.03) !important;
    }
    [data-baseweb="tab"][aria-selected="true"] {
        color: #00E676 !important;
        background-color: rgba(0, 230, 118, 0.08) !important;
        border-bottom: 2px solid #00E676 !important;
    }

    /* Selectbox Dropdown Menu Popover */
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    div[role="listbox"] {
        background-color: #161A1F !important;
        border: 1px solid rgba(0, 230, 118, 0.25) !important;
        border-radius: 10px !important;
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.6) !important;
    }
    [role="option"],
    [data-baseweb="menu"] li {
        color: #F8FAFC !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.92rem !important;
        padding: 10px 14px !important;
        background-color: transparent !important;
    }
    [role="option"]:hover,
    [role="option"][aria-selected="true"],
    [data-baseweb="menu"] li:hover {
        background-color: rgba(0, 230, 118, 0.15) !important;
        color: #00E676 !important;
        font-weight: 600 !important;
    }

    /* Selectbox Main Button Text */
    [data-baseweb="select"] span {
        color: #F8FAFC !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 500 !important;
    }

    /* Dataframes & Tables */
    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        background-color: #161A1F !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 12px !important;
        padding: 6px !important;
        color: #F8FAFC !important;
    }
    [data-testid="stDataFrame"] table,
    [data-testid="stTable"] table {
        color: #F8FAFC !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    [data-testid="stDataFrame"] th,
    [data-testid="stTable"] th {
        background-color: #111418 !important;
        color: #94A3B8 !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    /* Captions & Text */
    [data-testid="stCaptionContainer"],
    .stCaption {
        color: #94A3B8 !important;
        font-size: 0.88rem !important;
        font-family: 'Outfit', sans-serif !important;
    }
    .stMarkdown p {
        color: #CBD5E1;
        font-family: 'Outfit', sans-serif;
    }
    .stMarkdown strong {
        color: #F8FAFC;
    }

    .footer-container {
        padding: 24px 0 12px;
        margin-top: 24px;
        border-top: 1px solid rgba(255,255,255,0.08);
        text-align: center;
    }
    .footer-brand {
        color: #F8FAFC;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 6px;
    }
    .footer-brand span {
        color: #00E676;
    }
    .footer-copy {
        color: #64748B;
        font-size: 0.82rem;
    }
    </style>

    """,
        unsafe_allow_html=True,
    )


def render_status_card(title, text, type="neutral"):
    border_class = "status-neutral"
    dot_color = "#64748B"
    if type == "success":
        border_class = "status-success"
        dot_color = "#10B981"
    elif type == "alert":
        border_class = "status-alert"
        dot_color = "#EF4444"

    card_html = f"""
    <div class="status-card {border_class}">
        <div class="status-title" style="display: flex; align-items: center; gap: 8px; font-weight: 600;">
            <span class="hero-badge-dot" style="background: {dot_color}; width: 6px; height: 6px; border-radius: 50%; display: inline-block;"></span>
            {title}
        </div>
        <div class="status-body" style="margin-top: 8px; font-size: 13px; line-height: 1.5;">{text}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
