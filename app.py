"""
SHWASA – Personal Air-Quality Exposure Tracking System
Frontend UI Prototype

Built with Streamlit, Plotly, and Custom CSS.
Follows clean modular architecture: presentation logic separated from data models.
"""

import os
import base64
from pathlib import Path
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go

# Import dummy/static data structures
from data import OVERVIEW_METRICS, ACTIVITY_BLOCKS, get_forecast_data

# ==============================================================================
# Page Configuration & Light Theme Setup
# ==============================================================================
st.set_page_config(
    page_title="SHWASA – Air Quality Exposure Dashboard",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def render_html(raw_html: str):
    """
    Renders pure HTML cleanly without markdown indentation parsing issues.
    Strips leading whitespace from every line so CommonMark never treats it as a code block.
    """
    clean_lines = [line.strip() for line in raw_html.strip().splitlines() if line.strip()]
    cleaned_html = "".join(clean_lines)
    st.html(cleaned_html)

# ==============================================================================
# Custom CSS: Modern Environmental Aesthetic
# Deep Forest Green, Teal, Off-White, Subtle Greys
# ==============================================================================
CUSTOM_CSS = """
<style>
/* Import Clean Modern Typography */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {
    --forest-950: #061910;
    --forest-900: #0a2e1d;
    --forest-800: #10432b;
    --forest-700: #185a3b;
    --forest-600: #1f724b;
    --teal-800: #115e59;
    --teal-700: #0f766e;
    --teal-600: #0d9488;
    --teal-500: #14b8a6;
    --teal-100: #ccfbf1;
    --teal-50: #f0fdfa;
    --sage-100: #e8f5e9;
    --sage-700: #1b5e20;
    --bg-page: #f8fafc;
    --bg-card: #ffffff;
    --border-color: #e2e8f0;
    --border-subtle: #edf2f7;
    --text-primary: #0f172a;
    --text-secondary: #334155;
    --text-muted: #64748b;
}

/* Global resets & typography */
html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    background-color: var(--bg-page) !important;
    color: var(--text-primary) !important;
}

/* Hide default Streamlit decoration header & footer */
header[data-testid="stHeader"] {
    display: none !important;
}
footer {
    display: none !important;
}
#MainMenu {
    visibility: hidden;
}

/* Main content width & padding */
.block-container {
    max-width: 1240px !important;
    padding-top: 1.8rem !important;
    padding-bottom: 3rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* Headings text color override - high contrast */
h1, h2, h3, h4, .section-title {
    color: var(--forest-900) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
}

/* -------------------------------------------------------------------------- */
/* Header Component Styles                                                    */
/* -------------------------------------------------------------------------- */
.shwasa-header-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 24px 32px;
    margin-bottom: 26px;
    box-shadow: 0 4px 16px -2px rgba(10, 46, 29, 0.06);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 20px;
}

.shwasa-brand-container {
    display: flex;
    align-items: center;
    gap: 18px;
}

.shwasa-logo-emblem {
    width: 64px;
    height: 64px;
    background: #ffffff;
    border: 1.5px solid #ccfbf1;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 6px;
    box-shadow: 0 4px 14px rgba(13, 148, 136, 0.12);
    flex-shrink: 0;
}

.shwasa-logo-img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    display: block;
}

.shwasa-title-text {
    font-size: 2.3rem !important;
    font-weight: 800 !important;
    color: #0a2e1d !important;
    letter-spacing: -0.03em;
    margin: 0 !important;
    line-height: 1.1;
}

.shwasa-subtitle-text {
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    color: #0d9488 !important;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    margin: 3px 0 0 0 !important;
}

.shwasa-greeting-panel {
    background: #f0fdfa;
    border: 1.5px solid #ccfbf1;
    border-radius: 14px;
    padding: 12px 22px;
    display: flex;
    align-items: center;
    gap: 14px;
    box-shadow: 0 2px 6px rgba(13, 148, 136, 0.08);
}

.shwasa-live-dot {
    width: 12px;
    height: 12px;
    background-color: #0d9488;
    border-radius: 50%;
    box-shadow: 0 0 0 4px rgba(20, 184, 166, 0.25);
    animation: pulse-ring 2.5s infinite;
}

@keyframes pulse-ring {
    0% { box-shadow: 0 0 0 0 rgba(20, 184, 166, 0.5); }
    70% { box-shadow: 0 0 0 8px rgba(20, 184, 166, 0); }
    100% { box-shadow: 0 0 0 0 rgba(20, 184, 166, 0); }
}

.shwasa-greeting-headline {
    font-size: 1.25rem !important;
    font-weight: 800 !important;
    color: #0d9488 !important;
    margin: 2px 0 0 0 !important;
    line-height: 1.2;
}

.shwasa-status-text {
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    color: #0a2e1d !important;
    margin: 0 !important;
}

.shwasa-greeting-date {
    font-size: 0.80rem !important;
    font-weight: 600 !important;
    color: #0f766e !important;
    margin: 2px 0 0 0 !important;
}

/* -------------------------------------------------------------------------- */
/* Section Titles & Badges                                                    */
/* -------------------------------------------------------------------------- */
.section-heading-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    margin-top: 8px;
}

.section-title {
    font-size: 1.32rem !important;
    font-weight: 750 !important;
    color: #0a2e1d !important;
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 0 !important;
    letter-spacing: -0.01em;
}

.section-badge-pill {
    background: #f0fdfa;
    color: #0f766e;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 9999px;
    border: 1px solid #ccfbf1;
    display: inline-block;
}

/* -------------------------------------------------------------------------- */
/* Overview Metric Cards                                                      */
/* -------------------------------------------------------------------------- */
.overview-card-box {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 24px 28px;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.04);
    position: relative;
    overflow: hidden;
    height: 100%;
}

.overview-card-box:hover {
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.07);
    border-color: #cbd5e1;
}

.overview-accent-stripe-1 {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #0a2e1d, #0d9488);
}

.overview-accent-stripe-2 {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #0d9488, #10b981);
}

.overview-header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.overview-metric-title {
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    color: #334155 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 0 !important;
}

.overview-chip {
    font-size: 0.74rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 6px;
    background: #f1f5f9;
    color: #475569;
}

.overview-val-slot {
    display: flex;
    align-items: baseline;
    gap: 10px;
    min-height: 60px;
    margin-bottom: 14px;
}

.overview-empty-dash {
    font-family: 'JetBrains Mono', monospace;
    font-size: 3.4rem;
    font-weight: 800;
    color: #cbd5e1;
    line-height: 1;
    user-select: none;
}

.overview-unit-label {
    font-size: 1.25rem;
    font-weight: 700;
    color: #0f766e;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.overview-footer-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 14px;
    border-top: 1px solid #f1f5f9;
    font-size: 0.82rem;
    color: #64748b;
    font-weight: 500;
}

.status-dot-indicator {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #94a3b8;
    margin-right: 6px;
}

/* -------------------------------------------------------------------------- */
/* Today's Activity Container & Scroll Panel                                  */
/* Requirement: Dedicated internal vertical scrollbar                         */
/* Top 3 blocks visible initially (~280px); remaining 2 reached via scroll    */
/* -------------------------------------------------------------------------- */
.activity-wrapper-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 20px 22px;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.04);
    height: 100%;
}

.activity-panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #64748b;
    padding-bottom: 8px;
    border-bottom: 1px solid #f1f5f9;
}

.activity-scroll-container {
    max-height: 255px;
    overflow-y: scroll;
    overflow-x: hidden;
    padding-right: 6px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

/* Clean Custom Scrollbar */
.activity-scroll-container::-webkit-scrollbar {
    width: 6px;
}

.activity-scroll-container::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 6px;
}

.activity-scroll-container::-webkit-scrollbar-thumb {
    background: #94a3b8;
    border-radius: 6px;
}

.activity-scroll-container::-webkit-scrollbar-thumb:hover {
    background: #64748b;
}

/* Activity Row Item */
.activity-row {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: all 0.15s ease;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.02);
}

.activity-row:hover {
    border-color: #cbd5e1;
    background: #f8fafc;
}

.activity-row-left {
    display: flex;
    align-items: center;
    gap: 14px;
}

.activity-block-tag {
    background: #0a2e1d;
    color: #ffffff;
    font-size: 0.74rem;
    font-weight: 700;
    padding: 4px 9px;
    border-radius: 6px;
    letter-spacing: 0.03em;
    font-family: 'JetBrains Mono', monospace;
    white-space: nowrap;
}

.activity-title {
    font-size: 0.94rem !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    margin: 0 !important;
}

.activity-metrics-line {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 0.78rem;
    color: #475569;
    margin-top: 3px;
    font-family: 'JetBrains Mono', monospace;
}

.activity-metrics-line b {
    color: #0a2e1d;
}

.badge-indoor {
    background: #e0f2fe;
    color: #0369a1;
    font-size: 0.74rem;
    font-weight: 700;
    padding: 5px 12px;
    border-radius: 9999px;
    border: 1px solid #bae6fd;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    white-space: nowrap;
}

.badge-outdoor {
    background: #e8f5e9;
    color: #1b5e20;
    font-size: 0.74rem;
    font-weight: 700;
    padding: 5px 12px;
    border-radius: 9999px;
    border: 1px solid #c8e6c9;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    white-space: nowrap;
}

/* -------------------------------------------------------------------------- */
/* Forecast Outer Box & Bordered Containers                                   */
/* -------------------------------------------------------------------------- */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 18px !important;
    padding: 8px 12px !important;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.04) !important;
}

/* Align edit timeline button to the right */
div[data-testid="column"]:has(button[key="edit_timeline_btn"]),
div[data-testid="column"] button:has(span:contains("Edit Timeline")) {
    float: right;
}

/* -------------------------------------------------------------------------- */
/* Streamlit Buttons Styling                                                  */
/* -------------------------------------------------------------------------- */
/* Edit Timeline Button */
div[data-testid="stButton"] > button[kind="secondary"] {
    background-color: #ffffff !important;
    color: #0a2e1d !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    padding: 6px 16px !important;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05) !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stButton"] > button[kind="secondary"]:hover {
    border-color: #0d9488 !important;
    color: #0f766e !important;
    background-color: #f0fdfa !important;
}

/* Prominent Bottom Action Button */
.summary-button-wrap {
    margin-top: 36px;
    margin-bottom: 24px;
    display: flex;
    justify-content: center;
}

div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #0a2e1d 0%, #0d9488 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 16px 48px !important;
    font-size: 1.05rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 6px 20px rgba(10, 46, 29, 0.25) !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stButton"] > button[kind="primary"]:hover {
    box-shadow: 0 8px 26px rgba(10, 46, 29, 0.35) !important;
    transform: translateY(-2px) !important;
}

/* Footer note */
.prototype-credits {
    text-align: center;
    font-size: 0.80rem;
    font-weight: 600;
    color: #94a3b8;
    margin-top: 24px;
}
</style>
"""

# ==============================================================================
# Helper: Dynamic Greeting Based on Local Time
# ==============================================================================
def get_dynamic_greeting() -> str:
    """
    Computes a friendly greeting based on the current local hour:
    - 00:00 - 11:59: 'Good Morning'
    - 12:00 - 16:59: 'Good Afternoon'
    - 17:00 - 23:59: 'Good Evening'
    """
    current_hour = datetime.now().hour
    if current_hour < 12:
        return "Good Morning"
    elif current_hour < 17:
        return "Good Afternoon"
    else:
        return "Good Evening"

def get_logo_html() -> str:
    """
    Returns an HTML image tag with the base64-encoded wind & green leaf logo
    matching the user's reference design.
    """
    logo_path = Path(__file__).parent / "assets" / "shwasa_logo.png"
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            b64_str = base64.b64encode(f.read()).decode("utf-8")
        return f'<img src="data:image/png;base64,{b64_str}" class="shwasa-logo-img" alt="SHWASA Air Logo" />'
    
    # SVG fallback matching the wind-flow + green leaf motif
    return """
    <svg width="44" height="44" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M15 32H65C74 32 78 22 70 17C64 13 54 20 54 26" stroke="#00A3FF" stroke-width="7" stroke-linecap="round"/>
        <path d="M8 48H72C83 48 87 62 76 68C67 73 57 63 60 54" stroke="#0D9488" stroke-width="7" stroke-linecap="round"/>
        <path d="M18 64H55C63 64 68 74 61 80C54 84 46 76 48 69" stroke="#14B8A6" stroke-width="7" stroke-linecap="round"/>
        <path d="M74 24C78 12 90 10 93 11C95 21 87 31 77 33C74 33 73 28 74 24Z" fill="#22C55E"/>
    </svg>
    """

# ==============================================================================
# UI Component: Header (Title: SHWASA, and then Good Afternoon)
# ==============================================================================
def render_header():
    """
    Renders the dashboard top header:
    - Prominently displays the Title: SHWASA with the user's wind & leaf logo
    - Displays dynamic greeting: Good Afternoon (or Morning/Evening)
    """
    greeting = get_dynamic_greeting()
    date_str = datetime.now().strftime("%A, %d %B %Y")
    logo_markup = get_logo_html()
    
    header_html = f"""
    <div class="shwasa-header-card">
        <div class="shwasa-brand-container">
            <div class="shwasa-logo-emblem">
                {logo_markup}
            </div>
            <div>
                <h1 class="shwasa-title-text">SHWASA</h1>
                <p class="shwasa-greeting-headline">{greeting}!</p>
                <p class="shwasa-subtitle-text">Personal Air-Quality Exposure Tracking System</p>
            </div>
        </div>
        <div class="shwasa-greeting-panel">
            <div class="shwasa-live-dot"></div>
            <div>
                <p class="shwasa-status-text">System Active • Live Tracking</p>
                <p class="shwasa-greeting-date">{date_str}</p>
            </div>
        </div>
    </div>
    """
    render_html(header_html)

# ==============================================================================
# UI Component: Today's Overview
# ==============================================================================
def render_overview_section():
    """
    Renders the Today's Overview section with two distinct cards:
    - Card 1: Nearby PM2.5 (empty numerical value, unit µg/m³)
    - Card 2: Exposure So Far (empty numerical value, unit µg·h/m³)
    """
    section_header_html = """
    <div class="section-heading-row">
        <h2 class="section-title"><span>🍃</span> Today's Overview</h2>
        <span class="section-badge-pill">Live Telemetry</span>
    </div>
    """
    render_html(section_header_html)
    
    col1, col2 = st.columns(2, gap="medium")
    
    nearby_data = OVERVIEW_METRICS["nearby_pm25"]
    exposure_data = OVERVIEW_METRICS["exposure_so_far"]
    
    with col1:
        card1_html = f"""
        <div class="overview-card-box">
            <div class="overview-accent-stripe-1"></div>
            <div class="overview-header-row">
                <span class="overview-metric-title">{nearby_data['title']}</span>
                <span class="overview-chip">{nearby_data['badge']}</span>
            </div>
            <div class="overview-val-slot">
                <span class="overview-empty-dash">{nearby_data['display_placeholder']}</span>
                <span class="overview-unit-label">{nearby_data['unit']}</span>
            </div>
            <div class="overview-footer-row">
                <div>
                    <span class="status-dot-indicator"></span>
                    <span>{nearby_data['status']}</span>
                </div>
                <span>Sensor Station #1</span>
            </div>
        </div>
        """
        render_html(card1_html)
        
    with col2:
        card2_html = f"""
        <div class="overview-card-box">
            <div class="overview-accent-stripe-2"></div>
            <div class="overview-header-row">
                <span class="overview-metric-title">{exposure_data['title']}</span>
                <span class="overview-chip">{exposure_data['badge']}</span>
            </div>
            <div class="overview-val-slot">
                <span class="overview-empty-dash">{exposure_data['display_placeholder']}</span>
                <span class="overview-unit-label">{exposure_data['unit']}</span>
            </div>
            <div class="overview-footer-row">
                <div>
                    <span class="status-dot-indicator"></span>
                    <span>{exposure_data['status']}</span>
                </div>
                <span>Cumulative Dose</span>
            </div>
        </div>
        """
        render_html(card2_html)

# ==============================================================================
# UI Component: Today's Activity (With Dedicated Vertical Scrollbar)
# ==============================================================================
def render_activity_section():
    """
    Renders Today's Activity section:
    - Edit Timeline button near section heading, aligned right (visible, non-functional)
    - Exactly 5 activity blocks (Block 1 - Block 5)
    - Start time: 00:00, End time: 00:00, Duration: 00:00
    - Indoor / Outdoor classification badges
    - INTERNAL SCROLLBAR: Only top 3 activity blocks visible initially,
      remaining 2 accessible by scrolling inside the container.
    """
    # Header row with title and Edit Timeline button aligned right
    head_left, head_right = st.columns([3, 1], vertical_alignment="center")
    with head_left:
        render_html("""
            <div style="display: flex; align-items: center; gap: 10px;">
                <h2 class="section-title"><span>⏱️</span> Today's Activity</h2>
                <span class="section-badge-pill">5 Blocks</span>
            </div>
        """)
    with head_right:
        # Visible, non-functional secondary button aligned right
        st.button("✏️ Edit Timeline", key="edit_timeline_btn", type="secondary", help="Timeline editing will be available in future releases.")
    
    # Generate cleanly styled HTML for each activity block row
    rows_html_list = []
    for block in ACTIVITY_BLOCKS:
        is_indoor = block["classification"].lower() == "indoor"
        class_badge = (
            '<span class="badge-indoor">🏢 Indoor</span>'
            if is_indoor
            else '<span class="badge-outdoor">🌲 Outdoor</span>'
        )
        
        row_str = f"""
        <div class="activity-row">
            <div class="activity-row-left">
                <span class="activity-block-tag">{block['block_label']}</span>
                <div>
                    <p class="activity-title">{block['name']}</p>
                    <div class="activity-metrics-line">
                        <span>Start: <b>{block['start_time']}</b></span>
                        <span>•</span>
                        <span>End: <b>{block['end_time']}</b></span>
                        <span>•</span>
                        <span>Dur: <b>{block['duration']}</b></span>
                    </div>
                </div>
            </div>
            <div>
                {class_badge}
            </div>
        </div>
        """
        rows_html_list.append(row_str)
        
    all_rows_html = "".join(rows_html_list)
    
    activity_panel_html = f"""
    <div class="activity-wrapper-card">
        <div class="activity-panel-header">
            <span>Activity Timeline</span>
            <span>Scroll inside (Top 3 of 5 visible)</span>
        </div>
        <div class="activity-scroll-container">
            {all_rows_html}
        </div>
    </div>
    """
    render_html(activity_panel_html)

# ==============================================================================
# UI Component: PM2.5 Forecast Graph (Plotly)
# ==============================================================================
def render_forecast_section():
    """
    Renders the PM2.5 Forecast section with a smooth Plotly line graph.
    - X-axis: Time (next hour)
    - Y-axis: PM2.5 concentration (µg/m³)
    - Subtle grid matching the environmental palette
    - Custom clean hover tooltip
    - Clear demo/sample data badge
    """
    render_html("""
        <div class="section-heading-row">
            <h2 class="section-title"><span>📈</span> PM2.5 Forecast</h2>
            <span class="section-badge-pill" style="background: #fef3c7; color: #b45309; border-color: #fde68a;">
                Sample Demo Data
            </span>
        </div>
    """)
    
    # Retrieve forecast demo timeseries
    forecast_data = get_forecast_data()
    timestamps = forecast_data["timestamps"]
    pm25_vals = forecast_data["pm25"]
    
    # Create smooth spline line graph with Plotly
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=pm25_vals,
            mode="lines+markers",
            name="PM2.5 Forecast",
            line=dict(
                shape="spline",
                smoothing=1.1,
                color="#0D9488",
                width=3.2,
            ),
            fill="tozeroy",
            fillcolor="rgba(13, 148, 136, 0.08)",
            marker=dict(
                size=6,
                color="#0F766E",
                line=dict(width=2, color="#FFFFFF"),
            ),
            hovertemplate=(
                "<span style='font-size:12px; font-weight:600; color:#64748B;'>%{x}</span><br>"
                "<span style='font-size:14px; font-weight:700; color:#0F766E;'>%{y:.1f} µg/m³</span>"
                "<extra></extra>"
            ),
        )
    )
    
    fig.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        margin=dict(l=45, r=20, t=10, b=40),
        height=275,
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font_size=12,
            font_family="Plus Jakarta Sans",
            bordercolor="#E2E8F0",
        ),
        xaxis=dict(
            title=dict(
                text="Time (Next 60 Minutes)",
                font=dict(size=12, color="#475569", family="Plus Jakarta Sans"),
            ),
            showgrid=True,
            gridcolor="#F1F5F9",
            gridwidth=1,
            zeroline=False,
            tickfont=dict(size=11, color="#64748B", family="JetBrains Mono"),
            tickmode="auto",
            nticks=7,
        ),
        yaxis=dict(
            title=dict(
                text="PM2.5 (µg/m³)",
                font=dict(size=12, color="#475569", family="Plus Jakarta Sans"),
            ),
            showgrid=True,
            gridcolor="#F1F5F9",
            gridwidth=1,
            zeroline=False,
            tickfont=dict(size=11, color="#64748B", family="JetBrains Mono"),
            range=[min(pm25_vals) - 5, max(pm25_vals) + 5],
        ),
        showlegend=False,
    )
    
    # Forecast Chart Container with Border
    with st.container(border=True):
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "responsive": True,
            },
        )

# ==============================================================================
# UI Component: Generate Today's Summary Action
# ==============================================================================
def render_summary_action():
    """
    Renders the prominent 'Generate Today's Summary' button at the bottom.
    Visible but non-functional for this prototype phase.
    """
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        st.button(
            "📊 Generate Today's Summary",
            key="generate_summary_btn",
            type="primary",
            use_container_width=True,
            help="Summary generation will connect to the exposure calculation module.",
        )
    
    render_html("""
        <div class="prototype-credits">
            SHWASA v0.1 Prototype • Environmental Monitoring System • Frontend UI Stage
        </div>
    """)

# ==============================================================================
# Main Application Controller
# ==============================================================================
def main():
    # Inject Custom CSS Styles
    st.html(CUSTOM_CSS)
    
    # 1. Header (Brand: SHWASA, Dynamic Greeting: Good Afternoon)
    render_header()
    
    # 2. Today's Overview (Nearby PM2.5, Exposure So Far)
    render_overview_section()
    
    render_html("<div style='height: 18px;'></div>")
    
    # 3. Two-Column Dashboard Core: Today's Activity & PM2.5 Forecast
    col_activity, col_forecast = st.columns([1, 1], gap="medium")
    
    with col_activity:
        render_activity_section()
        
    with col_forecast:
        render_forecast_section()
        
    # 4. Action: Generate Today's Summary
    render_summary_action()

if __name__ == "__main__":
    main()
