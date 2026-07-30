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
