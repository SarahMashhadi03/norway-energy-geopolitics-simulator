# ============================================================================
# NORWAY ENERGY GEOPOLITICS SIMULATOR
# Policy Testing & Strategic Intelligence Platform
# Based on DNV Energy Transition Outlook Norway 2025
# Designed by: Sarah Mashhadi (sarahmashhadi03@gmail.com) | System Dynamics Modeler & Energy Geopolitics
# ============================================================================

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import time
import io
import base64
import textwrap
from pyvis.network import Network
import streamlit.components.v1 as components

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Norway Energy Geopolitics Simulator",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    /* ------------------------------------------------------------
       GLOBAL VERTICAL COMPACTION
       Move the whole dashboard upward and reduce unused whitespace
       without changing the internal structure of individual tabs.
       ------------------------------------------------------------ */
    div[data-testid="stMainBlockContainer"],
    section.main > div.block-container,
    .main .block-container {
        /* The native Streamlit header is hidden below, so no fixed overlay
           can cover the dashboard title after a tab-triggered rerun. */
        padding-top: 1.35rem !important;
        padding-bottom: 1rem !important;
    }

    /* Remove Streamlit's fixed white header layer.
       Tab 5 triggers reruns; with the native header visible, that fixed layer
       could remain above the page and cover the upper half of the main title. */
    header[data-testid="stHeader"] {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
    }

    /* Remove the toolbar/menu chrome together with the hidden header. */
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    #MainMenu {
        display: none !important;
    }

    /* Compact, but with enough separation to prevent text collisions. */
    div[data-testid="stVerticalBlock"] {
        gap: 0.62rem;
    }

    .main-title {
        font-size: 2.05rem;
        color: #0A1628;
        text-align: center;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, #0A1628 0%, #1B3A5C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 0;
        line-height: 1.22;
        margin: 0 0 15px 0;
    }
    .main-subtitle {
        text-align: center;
        color: #4A6A8A;
        font-size: 0.92rem;
        line-height: 1.35;
        margin: 0 0 12px 0;
        font-weight: 300;
        letter-spacing: 1px;
    }
    .designer-credit {
        text-align: center;
        color: #8A9AAA;
        font-size: 0.75rem;
        line-height: 1.35;
        margin: 0 0 8px 0;
    }
    .story-card {
        background: linear-gradient(145deg, #f8fafc, #eef2f6);
        border-radius: 16px;
        padding: 30px;
        border: 1px solid #dde4ec;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        min-height: 350px;
    }
    .story-title {
        font-size: 1.8rem;
        color: #0A1628;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .story-subtitle {
        font-size: 0.94rem;
        color: #4A6A8A;
        margin-bottom: 20px;
        font-weight: 400;
    }
    .story-content {
        font-size: 1rem;
        line-height: 1.8;
        color: #2d3748;
    }
    .story-image {
        font-size: 3.5rem;
        text-align: center;
        margin-bottom: 15px;
    }
    .story-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    .story-title-container {
        flex: 1;
    }
    .story-map {
        width: 180px;
        height: auto;
        margin-left: 20px;
        flex-shrink: 0;
    }
    .story-map img {
        width: 100%;
        height: auto;
        border-radius: 8px;
        border: 2px solid #dde4ec;
    }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 15px 12px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        transition: all 0.2s;
    }
    .metric-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0A1628;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #6A8AAA;
        margin-top: 3px;
    }
    .scenario-box {
        background: linear-gradient(135deg, #f0f7ff, #e8f0fa);
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 5px solid #2E86AB;
        margin: 10px 0;
    }
    .scenario-detail-box {
        background: linear-gradient(135deg, #f8fafc, #f1f4f9);
        border-radius: 12px;
        padding: 20px 24px;
        border: 1px solid #e2e8f0;
        margin: 10px 0;
    }
    .causal-box {
        background: linear-gradient(135deg, #f0f7ff, #e8f0fa);
        border-radius: 12px;
        padding: 20px 24px;
        border-left: 5px solid #2E86AB;
        margin: 10px 0;
    }
    .causal-loop-box {
        background: linear-gradient(135deg, #fef9e7, #fdf2d0);
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 5px solid #f39c12;
        margin: 10px 0;
    }
    .insight-box {
        background: linear-gradient(135deg, #fef9e7, #fdf2d0);
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 5px solid #f39c12;
        margin: 10px 0;
    }
    .insight-critical {
        background: linear-gradient(135deg, #fef2f2, #fde8e8);
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 5px solid #E74C3C;
        margin: 10px 0;
    }
    .insight-success {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 5px solid #22C55E;
        margin: 10px 0;
    }
    .insight-info {
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 5px solid #3B82F6;
        margin: 10px 0;
    }
    .reset-box {
        background: linear-gradient(135deg, #fef2f2, #fde8e8);
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 5px solid #E74C3C;
        margin: 10px 0;
    }
    .footer {
        text-align: center;
        color: #8a9aaa;
        font-size: 0.75rem;
        padding-top: 20px;
        border-top: 1px solid #e2e8f0;
        margin-top: 30px;
    }
    .stTabs [data-baseweb="tab-list"] {
        display: grid !important;
        grid-template-columns: 0.66fr 0.66fr 1.02fr 0.88fr 1.18fr 1.00fr !important;
        width: 100% !important;
        max-width: 100% !important;
        gap: 2px !important;
        background-color: transparent;
        padding: 3px 0 2px 0;
        margin: 9px 0 6px 0;
        overflow: hidden !important;
        box-sizing: border-box !important;
    }
    .stTabs [data-baseweb="tab"] {
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        justify-content: center !important;
        padding: 5px 4px !important;
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.72rem !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        box-sizing: border-box !important;
    }

    .stTabs [data-baseweb="tab"] p {
        width: 100% !important;
        min-width: 0 !important;
        margin: 0 !important;
        font-size: inherit !important;
        line-height: 1.15 !important;
        text-align: center !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0A1628;
    }
    div[data-testid="stMetricDelta"] {
        font-size: 0.85rem;
    }
    hr {
        margin: 20px 0;
        border-color: #e2e8f0;
    }
    .stButton button {
        font-weight: 500;
        transition: all 0.2s;
    }
    .stButton button:hover {
        transform: scale(1.02);
    }
    .slider-section {
        background: #f8fafc;
        border-radius: 12px;
        padding: 15px 20px;
        border: 1px solid #e2e8f0;
        margin-bottom: 15px;
    }
    .slider-section h4 {
        color: #1a3a5c;
        margin-bottom: 10px;
        font-weight: 600;
    }
    .scenario-subtab {
        padding: 10px 0;
    }
    .causal-card {
        background: white;
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 15px;
        transition: all 0.2s;
    }
    .causal-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }
    .causal-card h4 {
        color: #0A1628;
        margin-top: 0;
        margin-bottom: 8px;
    }
    .causal-card .effect {
        color: #2E86AB;
        font-weight: 600;
    }
    .causal-card .direction {
        font-size: 1.2rem;
        font-weight: 700;
    }
    .causal-card .positive {
        color: #22C55E;
    }
    .causal-card .negative {
        color: #E74C3C;
    }
    .loop-card {
        background: linear-gradient(135deg, #f8fafc, #f1f4f9);
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid #dde4ec;
        margin-bottom: 15px;
    }
    .loop-card h4 {
        color: #1a3a5c;
        margin-top: 0;
    }
    .causal-diagram {
        text-align: center;
        padding: 20px;
        background: #f8fafc;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin: 10px 0;
    }
    .causal-diagram .arrow {
        font-size: 1.8rem;
        color: #2E86AB;
        padding: 0 10px;
    }
    .causal-diagram .node {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 600;
        margin: 5px 0;
    }
    .causal-diagram .node-blue {
        background: #dbeafe;
        color: #1a3a5c;
    }
    .causal-diagram .node-green {
        background: #dcfce7;
        color: #166534;
    }
    .causal-diagram .node-red {
        background: #fde8e8;
        color: #991b1b;
    }
    .causal-diagram .node-yellow {
        background: #fef9e7;
        color: #92400e;
    }
    .story-line-item {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 10px;
        font-size: 1rem;
        line-height: 1.6;
    }
    .story-line-item .icon {
        font-size: 1.5rem;
        flex-shrink: 0;
        width: 32px;
        text-align: center;
    }
    
    @keyframes pulse-glow {
        0% { opacity: 0.85; transform: scale(1); text-shadow: 0 0 2px rgba(231, 76, 60, 0.2); }
        50% { opacity: 1; transform: scale(1.02); text-shadow: 0 0 12px rgba(231, 76, 60, 0.6); }
        100% { opacity: 0.85; transform: scale(1); text-shadow: 0 0 2px rgba(231, 76, 60, 0.2); }
    }
    .animated-dilemma {
        display: inline-block;
        animation: pulse-glow 2.5s infinite ease-in-out;
        color: #E74C3C;
        font-weight: 800;
        font-size: 1.15rem;
        letter-spacing: 0.3px;
    }
    
    /* کاهش فاصله بین ردیف‌های اسلایدرها */
    .policy-slider-section {
        margin-bottom: 5px;
        padding: 8px 12px;
        background: #f8fafc;
        border-radius: 8px;
        border: 1px solid #eef2f6;
    }
    .policy-slider-section .stSlider {
        padding-top: 2px;
        padding-bottom: 2px;
    }
    .policy-section-title {
        font-size: 0.94rem;
        font-weight: 600;
        color: #0A1628;
        margin-bottom: 6px;
        text-align: center;
    }
    /* لژند کوچکتر برای نمودارها */
    .chart-legend {
        font-size: 0.7rem !important;
    }
    .chart-legend .legendtext {
        font-size: 0.7rem !important;
    }


    /* ------------------------------------------------------------
       DASHBOARD TYPOGRAPHY SYSTEM
       One consistent hierarchy for titles, subtitles, cards,
       controls and supporting text across all five main tabs.
       ------------------------------------------------------------ */
    :root {
        --fs-page-title: 2.00rem;
        --fs-page-subtitle: 0.92rem;
        --fs-tab-title: 1.08rem;
        --fs-tab-subtitle: 0.86rem;
        --fs-section-title: 0.86rem;
        --fs-card-title: 0.71rem;
        --fs-body: 0.80rem;
        --fs-small: 0.70rem;
        --fs-control: 0.78rem;
        --lh-tight: 1.18;
        --lh-normal: 1.42;
        --tab-header-bottom: 10px;
    }

    html, body, [class*="css"] {
        font-family: Inter, Arial, sans-serif;
    }

    .main-title {
        font-size: var(--fs-page-title) !important;
        line-height: 1.20 !important;
        margin: 0 0 12px 0 !important;
    }

    .main-subtitle {
        font-size: var(--fs-page-subtitle) !important;
        line-height: 1.34 !important;
        margin: 0 0 10px 0 !important;
    }

    .designer-credit {
        font-size: 0.77rem !important;
        line-height: 1.36 !important;
        margin: 0 0 6px 0 !important;
    }

    .designer-credit + .designer-credit {
        margin-top: 1px !important;
        margin-bottom: 10px !important;
    }

    /* Identical title/subtitle position in every main tab. */
    .dashboard-tab-header {
        margin: 0 0 var(--tab-header-bottom) 0 !important;
        padding: 0 !important;
    }

    .dashboard-tab-header h4 {
        margin: 0 0 2px 0 !important;
        padding: 0 !important;
        color: #0A1628 !important;
        font-size: var(--fs-tab-title) !important;
        line-height: var(--lh-tight) !important;
        font-weight: 700 !important;
    }

    .dashboard-tab-header p {
        margin: 0 !important;
        padding: 0 !important;
        color: #4A6A8A !important;
        font-size: var(--fs-tab-subtitle) !important;
        line-height: 1.35 !important;
        font-weight: 400 !important;
    }

    /* Final shared alignment for all five main-tab headers. */
    .stTabs [data-baseweb="tab-panel"] .dashboard-tab-header {
        position: relative !important;
        top: auto !important;
        transform: none !important;
        margin-top: 0 !important;
        margin-bottom: var(--tab-header-bottom) !important;
        padding: 0 !important;
    }

    /* Standard text hierarchy inside tab content. */
    .stTabs [data-baseweb="tab-panel"] h1,
    .stTabs [data-baseweb="tab-panel"] h2,
    .stTabs [data-baseweb="tab-panel"] h3 {
        color: #0A1628;
    }

    .stTabs [data-baseweb="tab-panel"] h4 {
        font-size: 0.98rem !important;
        line-height: 1.20 !important;
        margin: 0 0 3px 0 !important;
    }

    .stTabs [data-baseweb="tab-panel"] h5 {
        font-size: 0.84rem !important;
        line-height: 1.22 !important;
        margin: 0 0 3px 0 !important;
    }

    .stTabs [data-baseweb="tab-panel"] p,
    .stTabs [data-baseweb="tab-panel"] li {
        line-height: var(--lh-normal);
    }

    /* Streamlit controls: one consistent size. */
    div[data-testid="stSelectbox"] label,
    div[data-testid="stSlider"] label,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stTextInput"] label,
    div[data-testid="stRadio"] label,
    div[data-testid="stCheckbox"] label {
        font-size: var(--fs-control) !important;
        line-height: 1.25 !important;
    }

    div[data-testid="stSelectbox"] [data-baseweb="select"],
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stButton"] button {
        font-size: var(--fs-control) !important;
    }

    div[data-testid="stButton"] button {
        line-height: 1.20 !important;
        font-weight: 600 !important;
    }

    /* Metrics and compact executive cards. */
    div[data-testid="stMetricValue"] {
        font-size: 1.35rem !important;
        line-height: 1.12 !important;
    }

    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricDelta"] {
        font-size: 0.72rem !important;
        line-height: 1.25 !important;
    }

    .scenario-section-label,
    .policy-section-title {
        font-size: var(--fs-section-title) !important;
        line-height: 1.20 !important;
        font-weight: 700 !important;
    }

    /* Normalize the many compact inline labels already used in cards. */
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size: 0.59rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size:0.59rem"],
    .stTabs [data-baseweb="tab-panel"] span[style*="font-size: 0.59rem"],
    .stTabs [data-baseweb="tab-panel"] span[style*="font-size:0.59rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size: 0.60rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size:0.60rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size: 0.61rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size:0.61rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size: 0.62rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size:0.62rem"] {
        font-size: var(--fs-card-title) !important;
        line-height: 1.22 !important;
    }

    .stTabs [data-baseweb="tab-panel"] div[style*="font-size: 0.67rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size:0.67rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size: 0.68rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size:0.68rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size: 0.69rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size:0.69rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size: 0.70rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size:0.70rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size: 0.71rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size:0.71rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size: 0.72rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size:0.72rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size: 0.73rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size:0.73rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size: 0.74rem"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size:0.74rem"],
    .stTabs [data-baseweb="tab-panel"] p[style*="font-size: 0.75rem"],
    .stTabs [data-baseweb="tab-panel"] p[style*="font-size:0.75rem"] {
        font-size: var(--fs-body) !important;
        line-height: var(--lh-normal) !important;
    }

    /* Keep nested-tab navigation readable but clearly secondary. */
    .stTabs .stTabs [data-baseweb="tab"] {
        font-size: 0.72rem !important;
        padding: 4px 6px !important;
        font-weight: 500 !important;
    }

    /* ------------------------------------------------------------
       CONSISTENT CONTENT SPACING
       Keep headings, status badges and supporting text visually close
       without making the dashboard feel cramped.
       ------------------------------------------------------------ */
    .stTabs [data-baseweb="tab-panel"] h4 {
        margin-top: 0 !important;
        margin-bottom: 2px !important;
        line-height: 1.18 !important;
    }

    .stTabs [data-baseweb="tab-panel"] h4 + p {
        margin-top: 0 !important;
        margin-bottom: 5px !important;
        line-height: 1.24 !important;
    }

    .stTabs [data-baseweb="tab-panel"]
    div[style*="justify-content: space-between"][style*="align-items: baseline"] {
        align-items: center !important;
        margin-bottom: 1px !important;
    }

    .stTabs [data-baseweb="tab-panel"]
    div[style*="justify-content: space-between"] h4 {
        padding: 0 !important;
    }

    .stTabs [data-baseweb="tab-panel"]
    div[style*="justify-content: space-between"] + p {
        margin-top: 0 !important;
        margin-bottom: 5px !important;
        line-height: 1.24 !important;
    }

    /* Slightly tighten spacing between consecutive content blocks in tabs. */
    .stTabs [data-baseweb="tab-panel"] > div[data-testid="stVerticalBlock"] {
        gap: 0.50rem !important;
    }

    /* ------------------------------------------------------------
       FINAL VISUAL HIERARCHY & FONT CONSISTENCY
       ------------------------------------------------------------ */

    /* Use one text font throughout the dashboard without overriding
       Streamlit's icon font. */
    html, body, .stApp,
    button, input, textarea, select,
    [data-baseweb="tab"],
    [data-testid="stMarkdownContainer"],
    [data-testid="stMetric"],
    [data-testid="stDataFrame"],
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary p {
        font-family: Inter, Arial, sans-serif !important;
    }

    /* Streamlit renders expander arrows and several interface icons through
       Material Symbols. Preserve that font so icon names are not displayed
       as visible words such as "keyboard_arrow_right". */
    span[data-testid="stIconMaterial"],
    [data-testid="stIconMaterial"],
    .material-symbols-rounded,
    .material-symbols-outlined {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined" !important;
        font-weight: normal !important;
        font-style: normal !important;
        font-size: 1.15rem !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-feature-settings: "liga" !important;
        -webkit-font-smoothing: antialiased !important;
        font-feature-settings: "liga" !important;
    }

    /* Keep Story accordion headings compact and properly aligned. */
    [data-testid="stExpander"] summary {
        min-height: 42px !important;
        padding: 7px 12px !important;
        align-items: center !important;
    }

    [data-testid="stExpander"] summary p {
        margin: 0 !important;
        font-size: 0.88rem !important;
        line-height: 1.25 !important;
        font-weight: 500 !important;
        color: #17344D !important;
    }

    /* Main tab titles must remain clearly above all internal content. */
    .dashboard-tab-header h4 {
        font-size: var(--fs-tab-title) !important;
        font-weight: 720 !important;
        line-height: 1.20 !important;
    }

    .dashboard-tab-header p {
        font-size: var(--fs-tab-subtitle) !important;
        line-height: 1.34 !important;
        font-weight: 400 !important;
    }

    /* Consistent, readable content hierarchy across every tab. */
    .stTabs [data-baseweb="tab-panel"] {
        font-size: var(--fs-body) !important;
        color: #2F4A59;
    }

    .stTabs [data-baseweb="tab-panel"] p,
    .stTabs [data-baseweb="tab-panel"] li,
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size"] {
        font-family: Inter, Arial, sans-serif !important;
    }

    .stTabs [data-baseweb="tab-panel"] h4:not(.dashboard-tab-header h4) {
        font-size: 0.96rem !important;
        line-height: 1.22 !important;
    }

    .stTabs [data-baseweb="tab-panel"] h5 {
        font-size: 0.86rem !important;
    }

    /* Small executive labels remain secondary, but not footnote-sized. */
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size: 0.5"],
    .stTabs [data-baseweb="tab-panel"] span[style*="font-size: 0.5"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size:0.5"],
    .stTabs [data-baseweb="tab-panel"] span[style*="font-size:0.5"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size: 0.6"],
    .stTabs [data-baseweb="tab-panel"] span[style*="font-size: 0.6"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size:0.6"],
    .stTabs [data-baseweb="tab-panel"] span[style*="font-size:0.6"] {
        font-size: var(--fs-small) !important;
        line-height: 1.30 !important;
    }

    .stTabs [data-baseweb="tab-panel"] div[style*="font-size: 0.7"],
    .stTabs [data-baseweb="tab-panel"] span[style*="font-size: 0.7"],
    .stTabs [data-baseweb="tab-panel"] p[style*="font-size: 0.7"],
    .stTabs [data-baseweb="tab-panel"] div[style*="font-size:0.7"],
    .stTabs [data-baseweb="tab-panel"] span[style*="font-size:0.7"],
    .stTabs [data-baseweb="tab-panel"] p[style*="font-size:0.7"] {
        font-size: var(--fs-body) !important;
        line-height: 1.38 !important;
    }

    /* Keep all nested tab bars on one line.
       This fixes the six Reference Dynamics subtabs without enlarging
       the page or forcing a second row. */
    .stTabs .stTabs [data-baseweb="tab-list"] {
        display: flex !important;
        grid-template-columns: none !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
        gap: 2px !important;
        overflow: hidden !important;
        padding: 2px 0 !important;
    }

    .stTabs .stTabs [data-baseweb="tab"] {
        flex: 1 1 0 !important;
        width: auto !important;
        min-width: 0 !important;
        max-width: none !important;
        padding: 4px 3px !important;
        font-size: 0.66rem !important;
        line-height: 1.12 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
    }

    .stTabs .stTabs [data-baseweb="tab"] p {
        font-size: inherit !important;
        line-height: 1.12 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    
    /* ---------------- Policy controls: visual balance ---------------- */
    .policy-control-title {
        margin: 0 0 4px 0 !important;
        padding: 0 !important;
        font-size: 0.86rem !important;
        font-weight: 650 !important;
        line-height: 1.22 !important;
        color: #29495B !important;
    }

    .policy-control-subtitle {
        margin: 0 0 10px 0 !important;
        padding: 0 !important;
        font-size: 0.72rem !important;
        line-height: 1.30 !important;
        color: #4A6A8A !important;
    }

    /* Prevent title and subtitle markdown blocks from visually colliding. */
    [data-testid="stMarkdownContainer"]:has(.policy-control-title),
    [data-testid="stMarkdownContainer"]:has(.policy-control-subtitle) {
        margin: 0 !important;
        padding: 0 !important;
    }

    [data-testid="stMarkdownContainer"]:has(.policy-control-title) p,
    [data-testid="stMarkdownContainer"]:has(.policy-control-subtitle) p {
        margin: 0 !important;
        padding: 0 !important;
        line-height: inherit !important;
    }

    /* Slider labels in Tab 4. */
    div[data-testid="stSlider"] label {
        font-size: 0.74rem !important;
        font-weight: 500 !important;
        line-height: 1.26 !important;
    }

    /* Numeric values above sliders. */
    .stSlider p {
        font-size: 0.72rem !important;
        line-height: 1.22 !important;
    }


/* Make controls and policy content readable without increasing
       card padding or chart height. */
    div[data-testid="stSelectbox"] label,
    div[data-testid="stSlider"] label,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stTextInput"] label,
    div[data-testid="stRadio"] label,
    div[data-testid="stCheckbox"] label,
    div[data-testid="stButton"] button {
        font-size: var(--fs-control) !important;
    }

    .policy-lab-subtitle,
    .policy-evidence-kicker,
    .scenario-side-insight-row,
    .scenario-intro-subtitle {
        font-size: var(--fs-body) !important;
        line-height: 1.38 !important;
    }

    /* ============================================================
       EXECUTIVE COVER TAB — full-width light hero
       Scoped to .executive-cover so existing tabs remain unchanged.
       ============================================================ */
    .executive-cover {
        position: relative;
        width: 100%;
        min-height: 470px;
        overflow: hidden;
        border: none;
        border-radius: 0;
        background: linear-gradient(135deg, #ffffff 0%, #f3f9fc 52%, #e8f4f9 100%);
        box-shadow: none;
    }

    .executive-cover-grid {
        display: grid;
        grid-template-columns: minmax(0, 1.06fr) minmax(390px, 0.94fr);
        min-height: 470px;
        width: 100%;
    }

    .executive-cover-copy {
        position: relative;
        z-index: 2;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        padding: 14px 42px 32px 44px;
        background:
            radial-gradient(circle at 10% 6%, rgba(78, 145, 174, 0.08), transparent 31%),
            linear-gradient(135deg, #ffffff 0%, #f6fbfd 56%, #eaf5f9 100%);
    }

    .executive-cover-title {
        margin: 0;
        color: #12344A;
        font-size: clamp(1.55rem, 1.9vw, 2rem);
        font-weight: 720;
        line-height: 1.06;
        letter-spacing: -0.03em;
    }

    .executive-cover-subtitle {
        margin: 10px 0 0 0;
        color: #2F708A;
        font-size: clamp(1rem, 1.28vw, 1.20rem);
        font-weight: 520;
        line-height: 1.30;
    }

    .executive-cover-text {
        max-width: 690px;
        margin-top: 18px;
        color: #405D6D;
        font-size: 0.88rem;
        line-height: 1.55;
    }

    .executive-cover-question {
        max-width: 690px;
        margin-top: 19px;
        padding: 12px 14px;
        border-left: 3px solid #D6A93C;
        border-radius: 0 9px 9px 0;
        background: rgba(255, 255, 255, 0.88);
        color: #29495B;
        font-size: 0.77rem;
        line-height: 1.45;
        box-shadow: 0 2px 8px rgba(31, 72, 94, 0.05);
    }

    .executive-cover-question-label {
        display: block;
        margin-bottom: 3px;
        color: #B48420;
        font-size: 0.62rem;
        font-weight: 750;
        letter-spacing: 0.045em;
        text-transform: uppercase;
    }

    .executive-cover-credit {
        margin-top: 13px;
        color: #5B7482;
        font-size: 0.72rem;
        line-height: 1.35;
    }

    .executive-cover-credit strong {
        color: #29495B;
        font-weight: 700;
    }

    .executive-cover-image {
        position: relative;
        min-height: 470px;
        background-position: center;
        background-size: cover;
        filter: saturate(0.78) brightness(1.16) contrast(0.92);
    }

    .executive-cover-image::before {
        content: "";
        position: absolute;
        inset: 0;
        background:
            linear-gradient(90deg, rgba(238,247,250,0.46) 0%, rgba(238,247,250,0.06) 35%),
            linear-gradient(0deg, rgba(22,62,80,0.05), transparent 44%);
    }

    @media (max-width: 980px) {
        .executive-cover-grid {
            grid-template-columns: 1fr;
        }

        .executive-cover-copy {
            padding: 30px 27px 28px 27px;
        }

        .executive-cover-image {
            min-height: 260px;
        }
    }

        .executive-cover-copy {
            padding: 32px 27px 29px 27px;
        }

        .executive-cover-image {
            min-height: 270px;
        }
    }

</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    if 'scenario_history' not in st.session_state:
        st.session_state.scenario_history = []
    if 'scenario_counter' not in st.session_state:
        st.session_state.scenario_counter = 0
    if 'scenario_names' not in st.session_state:
        st.session_state.scenario_names = {}

init_session_state()

# ============================================================================
# QUERY PARAMS FOR RESET
# ============================================================================

query_params = st.query_params
if 'reset' in query_params and query_params['reset'] == 'true':
    st.session_state.scenario_history = []
    st.session_state.scenario_counter = 0
    st.session_state.scenario_names = {}
    st.query_params.clear()
    st.rerun()

# ============================================================================
# DNV-ANCHORED REFERENCE DATA
# Exact report values are used where stated explicitly; intermediate points
# are smooth visualization anchors chosen to remain consistent with the
# published DNV trajectory. The exploratory policy engine below is not DNV's
# proprietary model.
# ============================================================================

DNV_DATA = {
    'year': [2024, 2030, 2035, 2040, 2045, 2050, 2055, 2060],
    'supply': [156, 163, 173, 186, 201, 215, 227, 238],
    'demand': [140, 159, 176, 183, 191, 200, 208, 217],
    'demand_data_centres': [0.5, 2.0, 5.0, 9.0, 14.0, 19.0, 24.0, 29.0],
    'emissions': [44.6, 36.0, 28.5, 22.5, 17.5, 13.0, 10.5, 8.6],
    # Export reference series used in the dashboard.
    # DNV 2024 production reference: crude oil = 106 MSm³oe/yr (~1.83 Mbpd);
    # natural gas (including NGL) = 135 Bcm/yr. Export volumes are lower.
    'gas': [125, 112, 98, 80, 63, 48, 35, 25],
    'oil': [95, 82, 66, 45, 34, 27, 22, 18],
    # Internal key retained for compatibility; this represents WIND share of electricity generation.
    'renewable': [10, 12, 15, 19, 23, 27, 29, 30],
    'hydro': [138, 140, 143, 145, 147, 149, 149, 149],
    'onshore_wind': [16, 20, 25, 30, 34, 36, 38, 36],
    'offshore_wind': [0, 0, 1, 12, 20, 26, 31, 36],
    'carbon_price': [75, 125, 150, 180, 210, 230, 230, 230]
}

# Approximate midpoint of Norway's stated target ranges, shown only as a visual guide.
TARGETS = {2030: 23.4, 2035: 14.3, 2050: 3.9}

def create_interpolators():
    dnv = {}
    for key in DNV_DATA.keys():
        if key != 'year':
            dnv[key] = interp1d(DNV_DATA['year'], DNV_DATA[key], 
                                kind='cubic', fill_value='extrapolate')
    return dnv

DNV = create_interpolators()

# ============================================================================
# DNV-INFORMED EXPLORATORY PATHWAYS (NOT OFFICIAL DNV SCENARIOS)
# ============================================================================

DNV_SCENARIOS_DETAILED = {
    "📘 DNV Reference (Best Estimate)": {
        "wind_mult": 1.0,
        "carbon_mult": 1.0,
        "sanctions_val": 0.78,
        "eu_policy_val": "moderate",
        "oil_p": 75,
        "grid_inv": "medium",
        "datacentre_growth": 1.0,
        "description": "DNV's published single best-estimate forecast, used here as the reference trajectory.",
        "assumptions": """
        **Key Assumptions:**
        - Moderate EU policy alignment
        - Gradual wind development (baseline pace)
        - Carbon price follows current trajectory
        - Moderate geopolitical tensions
        - Stable oil & gas prices around $75/bbl
        - Grid investment at current levels
        - Data centre growth follows baseline projections
        """,
        "key_results": """
        **Reference findings:**
        - Temporary power deficit in the early 2030s; annual surplus returns from 2037
        - Emissions reduction: ~75% by 2050 (below the 90–95% target)
        - Gas exports fall to roughly 25 billion m³/yr by 2060
        - Wind supplies about 30% of electricity generation by 2060
        - ETS carbon price reaches about $230/tCO2
        - Norway again has annual electricity surplus in the 2040s
        """
    },
    "🚀 Green Transition (Accelerated)": {
        "wind_mult": 1.5,
        "carbon_mult": 1.4,
        "sanctions_val": 0.70,
        "eu_policy_val": "fast",
        "oil_p": 65,
        "grid_inv": "high",
        "datacentre_growth": 1.2,
        "description": "Faster renewable deployment, stronger carbon pricing, and rapid EU policy alignment.",
        "assumptions": """
        **Key Assumptions:**
        - Fast EU policy alignment
        - Aggressive wind development (1.5x baseline)
        - Strong carbon price (1.4x baseline)
        - Low geopolitical tensions
        - Lower oil & gas prices ($65/bbl)
        - High grid investment capacity
        - Slightly higher data centre growth
        """,
        "key_results": """
        **Illustrative direction (calculated dynamically in the dashboard):**
        - Faster wind and grid build-out improves the electricity balance
        - Stronger carbon pricing reduces emissions faster than the reference
        - Fossil exports decline faster than the reference trajectory
        - Wind's share of generation rises above the reference trajectory
        """
    },
    "⛽ Delayed Transition (Fossil Stubborn)": {
        "wind_mult": 0.6,
        "carbon_mult": 0.6,
        "sanctions_val": 0.90,
        "eu_policy_val": "slow",
        "oil_p": 110,
        "grid_inv": "low",
        "datacentre_growth": 0.8,
        "description": "Slower wind development, weaker carbon prices, and geopolitical disruption delaying the transition.",
        "assumptions": """
        **Key Assumptions:**
        - Slow EU policy alignment
        - Weak wind development (0.6x baseline)
        - Weak carbon price (0.6x baseline)
        - High geopolitical tensions
        - High oil & gas prices ($110/bbl)
        - Low grid investment capacity
        - Lower data centre growth (economic slowdown)
        """,
        "key_results": """
        **Illustrative direction (calculated dynamically in the dashboard):**
        - Weaker wind, grid and carbon-policy settings increase power-system stress
        - Emissions remain above the reference trajectory
        - Fossil exports remain stronger for longer
        - Wind's share of generation stays below the reference trajectory
        """
    },
    "⚡ Power Crisis (Grid Constrained)": {
        "wind_mult": 0.8,
        "carbon_mult": 0.9,
        "sanctions_val": 0.85,
        "eu_policy_val": "slow",
        "oil_p": 95,
        "grid_inv": "low",
        "datacentre_growth": 1.5,
        "description": "Grid bottlenecks prevent renewable integration, leading to power shortages and slower transition.",
        "assumptions": """
        **Key Assumptions:**
        - Slow EU policy alignment
        - Moderate wind development (0.8x baseline)
        - Moderate carbon price (0.9x baseline)
        - High geopolitical tensions
        - Elevated oil & gas prices ($95/bbl)
        - Low grid investment capacity
        - High data centre growth (rapid digitalization)
        """,
        "key_results": """
        **Illustrative direction (calculated dynamically in the dashboard):**
        - Rapid demand growth combined with weak grid expansion increases system stress
        - Grid bottlenecks limit wind integration
        - Emissions fall more slowly than in a stronger-policy pathway
        - Fossil exports remain comparatively resilient
        """
    },
    "🌊 Offshore Wind Boom": {
        "wind_mult": 1.8,
        "carbon_mult": 1.2,
        "sanctions_val": 0.75,
        "eu_policy_val": "moderate",
        "oil_p": 70,
        "grid_inv": "high",
        "datacentre_growth": 1.0,
        "description": "Massive offshore wind deployment enabled by grid investment and supportive policy.",
        "assumptions": """
        **Key Assumptions:**
        - Moderate EU policy alignment
        - Aggressive wind development (1.8x baseline)
        - Strong carbon price (1.2x baseline)
        - Low geopolitical tensions
        - Moderate oil & gas prices ($70/bbl)
        - High grid investment capacity
        - Baseline data centre growth
        """,
        "key_results": """
        **Illustrative direction (calculated dynamically in the dashboard):**
        - Strong wind expansion and grid investment improve supply adequacy
        - Emissions fall faster than in the reference trajectory
        - Gas exports decline faster as the domestic power system expands
        - Wind's share of generation rises substantially
        """
    }
}

# ============================================================================
# DYNAMIC SIMULATION ENGINE
# ============================================================================

def get_dynamic_scenario_data(wind_mult, carbon_mult, sanctions_val, eu_policy_val, oil_p, grid_inv, datacentre_growth=1.0):
    years = np.arange(2024, 2061)
    
    base_supply = DNV['supply'](years)
    base_demand = DNV['demand'](years)
    base_dc_demand = DNV['demand_data_centres'](years)
    base_emissions = DNV['emissions'](years)
    base_gas = DNV['gas'](years)
    base_oil = DNV['oil'](years)
    base_renewable = DNV['renewable'](years)
    base_carbon = DNV['carbon_price'](years)
    
    grid_factor_map = {"low": 0.88, "medium": 1.0, "high": 1.10}
    grid_factor = grid_factor_map.get(grid_inv, 1.0)
    
    oil_price_ratio = oil_p / 75
    
    oil_production_factor = oil_price_ratio ** 0.4
    oil = base_oil * oil_production_factor
    oil_export_profitability = 1 + (oil_price_ratio - 1) * 0.15
    oil = oil * oil_export_profitability
    wind_oil_reduction = 1 - (wind_mult - 1) * 0.10
    oil = oil * wind_oil_reduction
    carbon_oil_reduction = 1 - (carbon_mult - 1) * 0.08
    oil = oil * carbon_oil_reduction
    sanctions_oil_factor = 1 - (sanctions_val - 0.78) * 0.8
    oil = oil * sanctions_oil_factor
    eu_oil_factor = {"slow": 1.04, "moderate": 1.0, "fast": 0.95}.get(eu_policy_val, 1.0)
    oil = oil * eu_oil_factor
    
    gas_production_factor = oil_price_ratio ** 0.3
    gas = base_gas * gas_production_factor
    gas_export_profitability = 1 + (oil_price_ratio - 1) * 0.2
    gas = gas * gas_export_profitability
    wind_gas_reduction = 1 - (wind_mult - 1) * 0.15
    gas = gas * wind_gas_reduction
    carbon_gas_reduction = 1 - (carbon_mult - 1) * 0.10
    gas = gas * carbon_gas_reduction
    sanctions_gas_factor = 1 - (sanctions_val - 0.78) * 0.8
    gas = gas * sanctions_gas_factor
    eu_gas_factor = {"slow": 1.06, "moderate": 1.0, "fast": 0.93}.get(eu_policy_val, 1.0)
    gas = gas * eu_gas_factor
    
    wind_supply_factor = 1 + (wind_mult - 1) * 0.45 * grid_factor
    carbon_wind_factor = 1 + (carbon_mult - 1) * 0.15
    renewable_attractiveness = 1 + (oil_price_ratio - 1) * 0.2
    eu_wind_pressure = {"slow": 0.92, "moderate": 1.0, "fast": 1.08}.get(eu_policy_val, 1.0)
    sanctions_supply_factor = 1 - (sanctions_val - 0.78) * 0.3
    
    supply = (base_supply 
              * wind_supply_factor 
              * carbon_wind_factor 
              * eu_wind_pressure 
              * renewable_attractiveness
              * sanctions_supply_factor
              * grid_factor)
    
    demand_price_factor = 1 - (oil_price_ratio - 1) * 0.3
    dc_demand = base_dc_demand * (1 + (datacentre_growth - 1.0) * 0.8)
    sanctions_demand_factor = 1 + (sanctions_val - 0.78) * 0.2
    grid_demand_factor = 1 / grid_factor
    
    demand = (base_demand + (dc_demand - base_dc_demand)) * demand_price_factor * eu_gas_factor * sanctions_demand_factor * grid_demand_factor
    
    wind_emissions_factor = 1 - (wind_mult - 1) * 0.25
    carbon_emissions_factor = 1.0 / (carbon_mult * 0.5 + 0.5)
    sanctions_emissions_factor = 1 + (sanctions_val - 0.78) * 0.5
    emissions_price_factor = 1 - (oil_price_ratio - 1) * 0.15
    eu_emissions_factor = {"slow": 1.05, "moderate": 1.0, "fast": 0.92}.get(eu_policy_val, 1.0)
    grid_emissions_factor = 1 - (grid_factor - 0.88) * 0.2
    
    emissions = (base_emissions 
                 * wind_emissions_factor 
                 * carbon_emissions_factor 
                 * sanctions_emissions_factor 
                 * emissions_price_factor
                 * eu_emissions_factor
                 * grid_emissions_factor)
    
    renewable = np.clip(base_renewable * wind_mult * grid_factor * carbon_wind_factor * renewable_attractiveness, 0, 100)
    power_balance = supply - demand
    
    deficit_year = None
    for i, val in enumerate(power_balance):
        if val < 0 and deficit_year is None:
            deficit_year = int(years[i])
            break
    
    uncertainty = 0.10
    supply_upper = supply * (1 + uncertainty)
    supply_lower = supply * (1 - uncertainty)
    emissions_upper = emissions * (1 + uncertainty)
    emissions_lower = emissions * (1 - uncertainty)
    
    return {
        'year': years,
        'electricity_supply': supply,
        'electricity_supply_upper': supply_upper,
        'electricity_supply_lower': supply_lower,
        'electricity_demand': demand,
        'data_centre_demand': dc_demand,
        'emissions': emissions,
        'emissions_upper': emissions_upper,
        'emissions_lower': emissions_lower,
        # Internal key names retained for compatibility; these series represent exports.
        'gas_production': gas,
        'oil_production': oil,
        'renewable_share': renewable / 100,
        'carbon_price': base_carbon * carbon_mult,
        'power_balance': power_balance,
        'deficit_year': deficit_year
    }


def get_dnv_informed_scenario(scenario_key):
    scenario = DNV_SCENARIOS_DETAILED.get(scenario_key, DNV_SCENARIOS_DETAILED["📘 DNV Reference (Best Estimate)"])
    return get_dynamic_scenario_data(
        wind_mult=scenario["wind_mult"],
        carbon_mult=scenario["carbon_mult"],
        sanctions_val=scenario["sanctions_val"],
        eu_policy_val=scenario["eu_policy_val"],
        oil_p=scenario["oil_p"],
        grid_inv=scenario["grid_inv"],
        datacentre_growth=scenario["datacentre_growth"]
    ), scenario["description"]

# ============================================================================
# PLOTTING FUNCTIONS
# ============================================================================

def plot_supply_demand(data, show_uncertainty=True, show_baseline=True, reference_only=False):
    base_data = get_dynamic_scenario_data(1.0, 1.0, 0.78, "moderate", 75, "medium", 1.0)
    
    fig = go.Figure()
    
    if not reference_only:
        fig.add_trace(go.Scatter(
            x=data['year'], y=data['electricity_supply'],
            name='Simulated Supply',
            line=dict(color='#2E86AB', width=3),
            fill='tozeroy', fillcolor='rgba(46, 134, 171, 0.12)'
        ))
    
    if show_uncertainty and not reference_only:
        fig.add_trace(go.Scatter(
            x=np.concatenate([data['year'], data['year'][::-1]]),
            y=np.concatenate([data['electricity_supply_upper'], data['electricity_supply_lower'][::-1]]),
            fill='toself',
            fillcolor='rgba(46, 134, 171, 0.10)',
            line=dict(color='rgba(46, 134, 171, 0.2)', width=1, dash='dot'),
            name='Uncertainty Range (±10%)',
            showlegend=True
        ))
    
    if not reference_only:
        fig.add_trace(go.Scatter(
            x=data['year'], y=data['electricity_demand'],
            name='Simulated Demand (incl. Data Centres)',
            line=dict(color='#E74C3C', width=3),
            fill='tozeroy', fillcolor='rgba(231, 76, 60, 0.08)'
        ))
    
    fig.add_trace(go.Scatter(
        x=data['year'], y=data['data_centre_demand'],
        name='Data-centre electricity demand',
        line=dict(color='#9B59B6', width=2, dash='dot'),
        opacity=0.8
    ))
    
    if show_baseline:
        fig.add_trace(go.Scatter(
            x=base_data['year'], y=base_data['electricity_supply'],
            name='DNV Reference Supply',
            line=dict(color='#2E86AB', width=3 if reference_only else 2, dash='solid' if reference_only else 'dash'),
            opacity=0.7 if not reference_only else 1.0,
            showlegend=True
        ))
        fig.add_trace(go.Scatter(
            x=base_data['year'], y=base_data['electricity_demand'],
            name='DNV Reference Demand',
            line=dict(color='#E74C3C', width=3 if reference_only else 2, dash='solid' if reference_only else 'dash'),
            opacity=0.7 if not reference_only else 1.0,
            showlegend=True
        ))
    
    fig.update_layout(
        title=dict(
            text='⚡ Electricity Supply & Demand',
            y=0.95,
            yanchor='bottom',
            x=0.15,
            xanchor='center',
            font=dict(size=14)
        ),
        xaxis_title='Year',
        yaxis_title='TWh/yr',
        height=400,
        hovermode='x unified',
        legend=dict(
            orientation='v', 
            yanchor='top', 
            y=1, 
            xanchor='left', 
            x=1.02,
            font=dict(size=10)
        ),
        template='plotly_white',
        font=dict(family='Inter, sans-serif', size=11),
        margin=dict(b=40)
    )
    return fig


def plot_emissions(data, show_uncertainty=True, show_baseline=True, reference_only=False):
    base_data = get_dynamic_scenario_data(1.0, 1.0, 0.78, "moderate", 75, "medium", 1.0)
    
    fig = go.Figure()
    
    if not reference_only:
        fig.add_trace(go.Scatter(
            x=data['year'], y=data['emissions'],
            name='Simulated Emissions',
            line=dict(color='#27AE60', width=3),
            fill='tozeroy', fillcolor='rgba(39, 174, 96, 0.12)'
        ))
    
    if show_uncertainty and not reference_only:
        fig.add_trace(go.Scatter(
            x=np.concatenate([data['year'], data['year'][::-1]]),
            y=np.concatenate([data['emissions_upper'], data['emissions_lower'][::-1]]),
            fill='toself',
            fillcolor='rgba(39, 174, 96, 0.10)',
            line=dict(color='rgba(39, 174, 96, 0.2)', width=1, dash='dot'),
            name='Uncertainty Range (±10%)',
            showlegend=True
        ))
    
    if show_baseline:
        fig.add_trace(go.Scatter(
            x=base_data['year'], y=base_data['emissions'],
            name='DNV Reference GHG Emissions',
            line=dict(color='#27AE60', width=3 if reference_only else 2, dash='solid' if reference_only else 'dash'),
            opacity=0.7 if not reference_only else 1.0,
            showlegend=True
        ))
    
    fig.add_trace(go.Scatter(
        x=list(TARGETS.keys()), y=list(TARGETS.values()),
        name='Stated climate targets (mid-range)',
        line=dict(color='#E74C3C', width=3, dash='dash'),
        showlegend=True
    ))
    
    fig.update_layout(
        title=dict(
            text='🌍 GHG Emissions vs. Targets',
            y=0.95,
            yanchor='bottom',
            x=0.15,
            xanchor='center',
            font=dict(size=13)
        ),
        xaxis_title='Year',
        yaxis_title='MtCO2e/yr',
        height=400,
        hovermode='x unified',
        legend=dict(
            orientation='v', 
            yanchor='top', 
            y=1, 
            xanchor='left', 
            x=1.02,
            font=dict(size=10)
        ),
        template='plotly_white',
        font=dict(family='Inter, sans-serif', size=11),
        margin=dict(b=45)
    )
    return fig


def plot_power_balance(data):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['year'], y=data['power_balance'],
        name='Power Balance',
        line=dict(color='#8E44AD', width=3),
        fill='tozeroy', fillcolor='rgba(142, 68, 173, 0.15)'
    ))
    
    fig.add_hline(y=0, line_dash='dash', line_color='gray', line_width=1.5)
    
    if data['deficit_year']:
        fig.add_vline(
            x=data['deficit_year'],
            line_dash='dot',
            line_color='#E74C3C',
            line_width=2,
            annotation_text=f'⚠️ Deficit Year: {data["deficit_year"]}',
            annotation_position='top'
        )
    
    fig.update_layout(
        title=dict(
            text='📊 Power Balance / Deficit Assessment',
            y=0.95,
            yanchor='bottom',
            x=0.17,
            xanchor='center',
            font=dict(size=13)
        ),
        xaxis_title='Year',
        yaxis_title='TWh/yr',
        height=400,
        hovermode='x unified',
        legend=dict(
            orientation='v', 
            yanchor='top', 
            y=1, 
            xanchor='left', 
            x=1.02,
            font=dict(size=10)
        ),
        template='plotly_white',
        font=dict(family='Inter, sans-serif', size=11),
        margin=dict(b=45)
    )
    return fig


def plot_energy_mix():
    years = [2024, 2060]
    fig = go.Figure()
    
    for year in years:
        idx = DNV_DATA['year'].index(year)
        hydro = DNV_DATA['hydro'][idx]
        onshore = DNV_DATA['onshore_wind'][idx]
        offshore = DNV_DATA['offshore_wind'][idx]
        other = max(0, DNV_DATA['supply'][idx] - hydro - onshore - offshore - 2)
        thermal = 2
        
        fig.add_trace(go.Bar(
            name=str(year),
            x=['Hydropower', 'Onshore Wind', 'Offshore Wind', 'Solar & Other', 'Thermal'],
            y=[hydro, onshore, offshore, other, thermal],
            text=[f'{v:.0f} TWh' for v in [hydro, onshore, offshore, other, thermal]],
            textposition='inside',
            textfont=dict(color='white', size=11),
            marker_color=['#3498DB', '#2ECC71', '#1ABC9C', '#F1C40F', '#E67E22']
        ))
    
    fig.update_layout(
        title='Norway\'s Electricity Mix: 2024 vs 2060',
        xaxis_title='Energy Source',
        yaxis_title='TWh/yr',
        height=400,
        barmode='group',
        legend=dict(
            orientation='v', 
            yanchor='top', 
            y=0.95, 
            xanchor='left', 
            x=1.02,
            font=dict(size=10)
        ),
        template='plotly_white',
        font=dict(family='Inter, sans-serif', size=11)
    )
    return fig


def plot_export_composition(data):
    base_data = get_dynamic_scenario_data(1.0, 1.0, 0.78, "moderate", 75, "medium", 1.0)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['year'], y=data['gas_production'],
        name='Natural Gas Exports',
        line=dict(color='#E67E22', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=data['year'], y=data['oil_production'],
        name='Oil Exports',
        line=dict(color='#2C3E50', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=base_data['year'], y=base_data['gas_production'],
        name='DNV Baseline Gas (Reference)',
        line=dict(color='#E67E22', width=2, dash='dash'),
        opacity=0.6,
        showlegend=True
    ))
    
    fig.add_trace(go.Scatter(
        x=base_data['year'], y=base_data['oil_production'],
        name='DNV Baseline Oil (Reference)',
        line=dict(color='#2C3E50', width=2, dash='dash'),
        opacity=0.6,
        showlegend=True
    ))
    
    fig.update_layout(
        title='🛢️ Oil & Gas Export Trends',
        xaxis_title='Year',
        yaxis_title='MSm³oe/yr',
        height=400,
        hovermode='x unified',
        template='plotly_white',
        font=dict(family='Inter, sans-serif', size=11),
        legend=dict(
            orientation='v', 
            yanchor='top', 
            y=1, 
            xanchor='left', 
            x=1.02,
            font=dict(size=10)
        )
    )
    return fig


def plot_renewable_share(data, show_baseline=True, reference_only=False):
    base_data = get_dynamic_scenario_data(1.0, 1.0, 0.78, "moderate", 75, "medium", 1.0)
    
    fig = go.Figure()

    if not reference_only:  
        fig.add_trace(go.Scatter(
            x=data['year'],
            y=data['renewable_share'] * 100,
            name='Simulated Wind Share',
            line=dict(color='#2ECC71', width=3),
            fill='tozeroy',
            fillcolor='rgba(46, 204, 113, 0.15)'
        ))
    
    if show_baseline:
        fig.add_trace(go.Scatter(
            x=base_data['year'],
            y=base_data['renewable_share'] * 100,
            name='DNV Baseline Wind Share (Reference)',
            line=dict(color='#2ECC71', width=3 if reference_only else 2, dash='solid' if reference_only else 'dash'),
            opacity=1.0 if reference_only else 0.7,
            showlegend=True
        ))
    
    fig.add_hline(
        y=50,
        line_dash='dot',
        line_color='gray',
        line_width=1,
        annotation_text='50% Wind Share',
        annotation_position='bottom right'
    )
    
    fig.update_layout(
        title=dict(
            text='💨 Wind Share of Electricity Generation',
            y=0.95,
            yanchor='top',
            x=0.2,
            xanchor='center',
            font=dict(size=13)
        ),
        xaxis_title='Year',
        yaxis_title='Wind Share (%)',
        height=400,
        hovermode='x unified',
        legend=dict(
            orientation='v', 
            yanchor='top', 
            y=1, 
            xanchor='left', 
            x=1.02,
            font=dict(size=10)
        ),
        template='plotly_white',
        font=dict(family='Inter, sans-serif', size=11),
        margin=dict(t=50, b=45)
    )
    return fig

# ============================================================================
# SCENARIO STORAGE FUNCTIONS
# ============================================================================

def save_scenario(scenario_params, simulated_data, scenario_name):
    row_2060 = pd.DataFrame(simulated_data).iloc[-1]
    
    scenario_record = {
        'Scenario ID': len(st.session_state.scenario_history) + 1,
        'Scenario Name': scenario_name if scenario_name else f"Scenario {len(st.session_state.scenario_history) + 1}",
        'Wind Multiplier': scenario_params['wind_mult'],
        'Carbon Price Impact': scenario_params['carbon_mult'],
        'Geopolitical Tension': scenario_params['sanctions_val'],
        'EU Policy Speed': scenario_params['eu_policy_val'],
        'Oil Price ($/bbl)': scenario_params['oil_p'],
        'Grid Investment': scenario_params['grid_inv'],
        'Data Centre Growth': scenario_params['datacentre_growth'],
        'Supply (2060) TWh': round(row_2060['electricity_supply'], 1),
        'Demand (2060) TWh': round(row_2060['electricity_demand'], 1),
        'Emissions (2060) MtCO2e': round(row_2060['emissions'], 1),
        'Wind Share (%)': round(row_2060['renewable_share'] * 100, 1),
        'Gas exports (MSm³oe/yr)': round(row_2060['gas_production'], 1),
        'Oil exports (MSm³oe/yr)': round(row_2060['oil_production'], 1),
        'Carbon Price ($/tCO2)': round(row_2060['carbon_price'], 0),
        'Deficit Year': simulated_data['deficit_year'] if simulated_data['deficit_year'] else 'None'
    }
    
    st.session_state.scenario_history.append(scenario_record)
    st.session_state.scenario_counter += 1


def get_scenario_csv():
    if not st.session_state.scenario_history:
        return None
    df = pd.DataFrame(st.session_state.scenario_history)
    return df.to_csv(index=False).encode('utf-8')


def get_insight_text(scenario_params):
    data = get_dynamic_scenario_data(**scenario_params)
    
    deficit = data['deficit_year']
    final_emissions = data['emissions'][-1]
    final_renewable = data['renewable_share'][-1] * 100
    final_gas = data['gas_production'][-1]
    final_oil = data['oil_production'][-1]
    baseline_gas = 25
    baseline_wind_share = 30
    baseline_deficit = get_dynamic_scenario_data(1.0, 1.0, 0.78, 'moderate', 75, 'medium', 1.0)['deficit_year']
    dc_demand_2060 = data['data_centre_demand'][-1]
    oil_p = scenario_params['oil_p']
    wind_mult = scenario_params['wind_mult']
    carbon_mult = scenario_params['carbon_mult']
    sanctions_val = scenario_params['sanctions_val']
    eu_policy_val = scenario_params['eu_policy_val']
    grid_inv = scenario_params['grid_inv']
    
    insights = []
    
    if oil_p > 110:
        insights.append(("info", f"🛢️ **High oil & gas price (${oil_p}/bbl):** Incentivizes fossil investment but may slow economic growth."))
    elif oil_p < 60:
        insights.append(("info", f"🛢️ **Low oil & gas price (${oil_p}/bbl):** Reduces fossil investment but may slow renewable transition."))
    else:
        insights.append(("info", f"🛢️ **Oil & gas price at ${oil_p}/bbl:** Moderate price level, aligned with DNV baseline."))
    
    if wind_mult > 1.5:
        insights.append(("success", f"🌬️ **High wind development ({wind_mult:.1f}x baseline):** Strong renewable growth reducing emissions and fossil fuel demand."))
    elif wind_mult < 0.7:
        insights.append(("critical", f"🌬️ **Low wind development ({wind_mult:.1f}x baseline):** Renewable transition lagging, increasing fossil reliance."))
    
    if carbon_mult > 1.3:
        insights.append(("success", f"💨 **Strong carbon price ({carbon_mult:.1f}x baseline):** Effectively reducing emissions."))
    elif carbon_mult < 0.7:
        insights.append(("critical", f"💨 **Weak carbon price ({carbon_mult:.1f}x baseline):** Emissions reduction slower than needed."))
    
    if sanctions_val > 0.9:
        insights.append(("critical", f"🛑 **High geopolitical tension ({sanctions_val:.2f}):** Disrupting supply and raising emissions."))
    elif sanctions_val < 0.6:
        insights.append(("success", f"🛑 **Low geopolitical tension ({sanctions_val:.2f}):** Stable supply conditions."))
    
    if eu_policy_val == "fast":
        insights.append(("success", "🇪🇺 **Fast EU policy alignment:** Reducing fossil exports and accelerating renewables."))
    elif eu_policy_val == "slow":
        insights.append(("warning", "🇪🇺 **Slow EU policy alignment:** May delay energy transition."))
    
    if grid_inv == "high":
        insights.append(("success", "🔌 **High grid investment:** Enables renewable integration and reduces losses."))
    elif grid_inv == "low":
        insights.append(("critical", "🔌 **Low grid investment:** Grid bottlenecks limit renewable integration."))
    
    if deficit is None:
        insights.append(("success", "✅ **No annual power deficit detected in this exploratory pathway.**"))
    elif baseline_deficit is not None and deficit < baseline_deficit:
        insights.append(("critical", f"⚠️ **Power deficit appears by {deficit}** – earlier than the DNV-informed reference."))
    elif baseline_deficit is not None and deficit > baseline_deficit:
        insights.append(("success", f"✅ **Power deficit is delayed until {deficit}** relative to the reference."))
    else:
        insights.append(("warning", f"📊 **Power deficit appears by {deficit}** – close to the DNV-informed reference timing."))
    
    if final_emissions > 5.2:
        insights.append(("critical", f"🌍 **2060 emissions remain at {final_emissions:.1f} MtCO2e** – still above Norway's 2050 target range."))
    else:
        insights.append(("success", f"🌱 **2060 emissions fall to {final_emissions:.1f} MtCO2e** – within the approximate 2050 target range."))
    
    if final_gas > baseline_gas * 1.2:
        insights.append(("warning", f"🛢️ **Gas exports remain strong ({final_gas:.1f} MSm³oe/yr)** – European demand resilient."))
    elif final_gas < baseline_gas * 0.8:
        insights.append(("success", f"🌱 **Gas exports declining ({final_gas:.1f} MSm³oe/yr)** – transitioning away from fossil exports."))
    else:
        insights.append(("warning", f"🛢️ **Gas exports at {final_gas:.1f} MSm³oe/yr** – aligned with DNV baseline."))
    
    if final_oil > 20:
        insights.append(("warning", f"🛢️ **Oil exports remain strong ({final_oil:.1f} MSm³oe/yr)** – significant production."))
    elif final_oil < 10:
        insights.append(("success", f"🌱 **Oil exports declining ({final_oil:.1f} MSm³oe/yr)** – reducing oil dependency."))
    else:
        insights.append(("warning", f"🛢️ **Oil exports at {final_oil:.1f} MSm³oe/yr** – moderate production level."))
    
    if final_renewable > baseline_wind_share + 3:
        insights.append(("success", f"💨 **Wind generation share reaches {final_renewable:.0f}%** – above the ~30% DNV reference for 2060."))
    elif final_renewable < baseline_wind_share - 3:
        insights.append(("critical", f"⚡ **Wind generation share reaches {final_renewable:.0f}%** – below the ~30% DNV reference for 2060."))
    else:
        insights.append(("info", f"💨 **Wind generation share reaches {final_renewable:.0f}%** – close to the DNV reference."))
    
    if dc_demand_2060 > 20:
        insights.append(("critical", f"📊 **Data centre demand reaches {dc_demand_2060:.1f} TWh** – major driver of electricity-demand growth."))
    elif dc_demand_2060 > 10:
        insights.append(("warning", f"📊 **Data centre demand reaches {dc_demand_2060:.1f} TWh** – significant contributor."))
    
    return insights

# ============================================================================
# STORY SCENES
# ============================================================================

STORY_SCENES = {
    1: {
        "title": "Norway: A Nation of Energy Abundance",
        "subtitle": "For decades, Norway has been defined by energy abundance and independence. In 2024:",
        "image": "",
        "content": """
        <div class="story-header">
            <div class="story-title-container">
                <div class="story-title"> Norway: A Nation of Energy Abundance</div>
                <div class="story-subtitle">For decades, Norway has been defined by energy abundance and independence . In 2024:</div>
            </div>
            <div class="story-map">
                <svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;border-radius:8px;border:2px solid #dde4ec;background:#f0f4f8;">
                    <rect width="900" height="600" fill="#c6e2ff"/>
                    <rect x="250" y="150" width="400" height="300" fill="#ba0c2f"/>
                    <rect x="380" y="150" width="60" height="300" fill="#ffffff"/>
                    <rect x="250" y="270" width="400" height="60" fill="#ffffff"/>
                    <rect x="400" y="150" width="30" height="300" fill="#00205b"/>
                    <rect x="250" y="285" width="400" height="30" fill="#00205b"/>
                </svg>
            </div>
        </div>
        
        <div style="font-size: 1rem; line-height: 1.8; color: #2d3748; margin-top: 0;">
            <div class="story-line-item">
                <span class="icon">💧</span>
                <span><b>Hydropower</b> provided <b>88%</b> of electricity – renewable, flexible, and deeply integrated.</span>
            </div>
            <div class="story-line-item">
                <span class="icon">🛢️</span>
                <span>Oil & Gas exports made Norway a key supplier to Europe <b>(30% of Europe's gas).</b></span>
            </div>
            <div class="story-line-item">
                <span class="icon">⚡</span>
                <span><b>10-20 TWh/yr net electricity export (average in recent years).</b></span>
            </div>
            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #e2e8f0;"></div>
            <div class="story-line-item">
                <span class="icon">🔒</span>
                <span>Energy Independence has been a cornerstone of Norwegian prosperity.</span>
            </div>
            <div class="story-line-item">
                <span class="icon">🌍</span>
                <span><b>But the world is changing. Norway now faces a <span class="animated-dilemma">three-way dilemma</span> that will define its future.</b></span>
            </div>
        </div>
        """,
        "key_data": {}
    },
    2: {
        "title": "⚖️ The Norwegian Trilemma",
        "subtitle": "",
        "image": "",
        "content": """
        Norway must balance three competing objectives:
        
        1. **🛢️ Sustaining Energy Exports** – Norway supplies ~30% of Europe's gas – a vital lifeline after Russian supply losses. But this locks capital and talent into the fossil sector, slowing the green transition.
        
        2. **🌱 Enabling Green Industrial Growth** – New green industries (batteries, hydrogen, data centres) need clean, affordable power. But rising demand strains the grid – without new capacity, Norway risks losing its competitive edge.
        
        3. **🌍 Delivering Rapid Emissions Cuts** – Norway has committed to <b>90-95% reduction by 2050</b>, yet current forecasts show only 75% reduction, leaving a significant gap that requires extensive carbon credits.
        
        **⚠️ The Risk:** Norway currently risks falling short on all three ambitions – exports decline, green industries stall, and emissions remain too high.
        """,
        "key_data": {}
    },
    3: {
        "title": "⚡ The Temporary Power Deficit",
        "subtitle": "Demand is outpacing supply – Norway faces a power deficit from the early 2030s",
        "image": "",
        "content": """        
        Electricity demand is growing much faster than new supply:
        
        - **Data Centres & AI**: Electricity demand reaches 29 TWh by 2060, including 21 TWh for AI-supporting services
        - **Electric Vehicles**: EVs accounted for 93% of new passenger-car sales in the first three quarters of 2025
        - **Industry Electrification**: Oil & gas platforms switching to shore power
        
        **The Result:** Norway will face a power deficit from the early 2030s, requiring net imports.
        """,
        "key_data": {"Deficit Starts": "2033", "Surplus Returns": "2037", "Data Centre Demand (2060)": "29 TWh", "EV Share (2025)": "93%"}
    },
    4: {
        "title": "🌬️ Wind: The Only Scalable Solution",
        "subtitle": "Wind power is the only technology that can scale fast enough",
        "image": "",
        "content": """
        **💨 Why Wind Matters**
        
        Wind power is the ONLY commercially mature, scalable solution:
        
        - **Onshore Wind**: Capacity to triple from 5 GW to 13 GW by 2060
        - **Offshore Wind**: Growing from about 0.1 GW today to about 8 GW by 2060
        - **Cost Competitiveness**: Onshore wind is now cheaper than fossil fuels
        
        **The Challenge:** Local opposition and slow permitting have stalled new projects since 2019.
        """,
        "key_data": {"Wind Capacity (2024)": "5 GW", "Wind Capacity (2060)": "~21 GW", "Offshore Wind (2060)": "~8 GW", "Onshore Wind (2060)": "13 GW"}
    },
    5: {
        "title": "🌍 Emissions Gap: Norway is Not on Track",
        "subtitle": "Without extensive carbon credits, Norway will miss its climate targets",
        "image": "",
        "content": """
        **📊 The Emissions Gap**
        
        Norway's targets vs. DNV forecast:
        
        | Year | Target | Forecast | Gap |
        |------|--------|----------|-----|
        | 2030 | 55% ↓ | 30% ↓ | 25% |
        | 2035 | 70-75% ↓ | 45% ↓ | 25-30% |
        | 2050 | 90-95% ↓ | 75% ↓ | 15-20% |
        
        **The Solution:** Norway will need to purchase international carbon credits worth approximately NOK 15bn annually.
        """,
        "key_data": {"2030 Gap": "25%", "2035 Gap": "25-30%", "2050 Gap": "15-20%", "Annual Credits Cost": "NOK 15bn"}
    },
    6: {
        "title": "🔮 What's Next?",
        "subtitle": "The choices Norway makes today will shape its future for decades",
        "image": "",
        "content": """
        **🎯 Key Strategic Choices**
        
        Norway's future depends on decisions in three areas:
        
        1. **📜 Policy Clarity**: Clear, stable policies to attract investment
        2. **⚡ Grid Investment**: Statnett plan: NOK 150-200bn for grid upgrades
        3. **🌬️ Wind Deployment**: Faster permitting and local acceptance
        
        **The Opportunity:** Norway's choices on policy, grid development and wind deployment will strongly shape the speed and credibility of the transition.
        """,
        "key_data": {"Grid Investment": "Statnett: NOK 150-200bn / decade", "EU Policy Alignment": "559 EEA-relevant acts unimplemented", "CCS Capacity (2060)": "6.9 MtCO2/yr"}
    }
}

# ============================================================================
# MAIN APP
# ============================================================================

st.markdown(
    '<div class="main-title">Norway Energy Geopolitics Simulator</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="main-subtitle">Interactive Policy Testing & Strategic Intelligence Platform</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="designer-credit">Independent exploratory analysis informed by published data in the DNV Energy Transition Outlook Norway 2025 and author-defined assumptions </div>',
    unsafe_allow_html=True,
)


# ============================================================================
# TABS - ترتیب جدید: Story, Reference, System Dynamics, Policy Explorer, DNV Scenarios
# ============================================================================

tab_cover, tab_story, tab_data, tab_causal, tab_policy, tab_scenarios = st.tabs([
    "🎯 Briefing",
    "📖 Story",
    "📊 Reference Dynamics",
    "🔄 Causal Loops",
    "⚙️ Decision Support",
    "🎯 DNV-Informed Pathways"
])


# ============================================================================
# COVER: EXECUTIVE STRATEGIC FRAMING
# Self-contained. Existing five tab bodies remain unchanged.
# ============================================================================

with tab_cover:
    cover_html = textwrap.dedent("""
    <section class="executive-cover">
        <div class="executive-cover-grid">

            <div class="executive-cover-copy">
<div class="executive-cover-title">
                    Norway’s Strategic Energy Position
                </div>

                <div class="executive-cover-subtitle">
                    Security, dependencies and transition in a changing Europe
                </div>

                <div class="executive-cover-text">
                    Norway’s energy geopolitics is increasingly shaped by the
                    interaction between European energy security, petroleum
                    dependence, electricity infrastructure and emerging
                    low-carbon industries. Decisions that strengthen security
                    or competitiveness today may create new dependencies and
                    constraints over time. This dashboard applies a system
                    dynamics perspective to examine those strategic interactions
                    and their implications for Norway’s long-term position.
                </div>
<div class="executive-cover-question">
                    <span class="executive-cover-question-label">Strategic question</span>
                    How can Norway sequence energy-security commitments,
                    infrastructure investment and industrial transition without
                    reinforcing old dependencies or creating new ones?
                </div>

                <div class="executive-cover-credit">
                    Prepared by <strong>Sarah Mashhadi</strong> · (sarahmashhadi03@gmail.com) • System Dynamics Modeler & Energy Transition Researcher.
                </div>
            </div>

            <div
                class="executive-cover-image"
                style="background-image:
                url('data:image/jpeg;base64,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VhGmxrTLWmxrZMzLUQw1uxtawy1puawxMtxCGsNrWGxjDa1hzmXSIa0p7FpT2NyUzYlMxOTUQ/N2ew7PY/X2Y7Mm5dr8a09iFp7H7VpkLTLGSU/C6manMP3OYaXsNxkzMPxOYa3N2P1uYanMOkS5zD8rmmtWn6XNNbmm4lmYfnVCVQ3K0hWmoYpqjYlUNyoSqGkalQxGxaoYKNaoTBtglULCNSoQqG5UJchYSWhUJg2qhMGoZaoEFqmogqMImwjYpEEATGwjYuBBREbCNi4EARGwjYuBAERsI2LgQBEbCNi4EARGwjYuBAERsI2LgQBEbAuABUCC42EbEEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQYVC4MQBEGUTUqNjKJr0IqYLRDKJr0LRCLAiFIhlEKRDLTEFRsZgqCCYMohSIUiEVKIUiGUQpE2IsMIhaNMomxbWmZahlrTa1phiG1rTEy1DLWm9jDDGm9jTnlLpEMsYbmMMsYfoYw4zLrEIaw2Iw2Iw2Iw5zLcQ08g5D9HIOQza0/KrCHMP1qwhWbGolJh+FzDS5h+57DQ9h0iWJh+F7DQ5p+17TQ9p1xlymH43NNTmn6nNNLkOsSxL86tNaofochrVDcMS0qhKobVTYwqGmZalQlUNqoSqFhGuNiVQ2wSqFRqVCVQ2qmpKoUaVQhU1NyoQqbGoZalTUxBsVNjEbFhEohmDMGYKiYEFxsI2AiBBcbCNgIgQXGwjYCIEFxsI2AiBBcbCNgIgQXGwjYCIEFxsI2AiAXGw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EFwIAiBBcCAIgQXAgCIEFwIAiBBcCAIgQXAgCIEFwIAiBBcCAIgQXAgCIEFwIAiBBcCAIgQXAgCIEFwIAiBBcCAIgQXAgCIEFwIAiBBcCAIgQXAgCIEFwIAiBBcCAIgQXAgCIEFwIAiBBcCAIgQXAgCIEFwIAiBBcCAIgQXAgCIEFwIAiBBcCAIgQXAgCIEFwIAiBBcCAIgQXAgCIEFwIAiBBcCAIgQXAgCIEFwIAiBBcCAIgQXAgCIEFwIAiBBcCAIgQXAgCICopcBU0CtUGUQqBAGILRBBSIZaZRC0QwiFohFETYzBlEKggxBlEMohmCKwUiBE1MohFEQtEMQWhmVhTTY01tNjTMtQ2tNzVNDTY1YOcw3Ev0tU2tcfnapsapzmHSJfqa4tHH5kcWjjnOLcS/RzDmNPMOYm1bbFcQ5xKuNauLGKTLLnSaXKU5TU5TpEMTKXKaXKW5ZNTjpEMTKHGtxbiFOkMS1qhCobFIg1DMoVCTYqEqhplCmILgwqFREKSqbGyCVQo1qhKobFQhUKjUqEqhsVCYKjWqGILVBBplKIpmCkQzAEQILgQERAguBAEQILgQBECC4EARAguBAEQILgQBECC4EARALgAVAguNhGwVECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECC42EbARAguNhGwEQILjYRsBECELjYRsBrgRsWqCAJRCkQQZRDLSkQpEMIhSIRVIhSGEQpCBBmEMxsZT5CKxBlEMwZRCKwhSCNjKEWFIhaEoUmhmYaWhaKa0LRTMwsS2tWDYjjSilIpiYaiW9HFo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MiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqRJMiQUqQTIBSZEkyJFrSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqRJMiRZSpEkyJFlKkSTIkWUqQTIFlJkSAZUkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkSAAkAAf/9k=');">
            </div>

        </div>
    </section>
    """)

    # Render the cover in an isolated HTML component. This prevents
    # Streamlit Markdown from treating the large base64 image as code.
    cover_document = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            html, body {
                margin: 0;
                padding: 0;
                overflow: hidden;
                background: transparent;
                font-family: Inter, Arial, sans-serif;
            }
/* ============================================================
       EXECUTIVE COVER TAB — full-width light hero
       Scoped to .executive-cover so existing tabs remain unchanged.
       ============================================================ */
    .executive-cover {
        position: relative;
        width: 100%;
        min-height: 470px;
        overflow: hidden;
        border: none;
        border-radius: 0;
        background: linear-gradient(135deg, #ffffff 0%, #f3f9fc 52%, #e8f4f9 100%);
        box-shadow: none;
    }

    .executive-cover-grid {
        display: grid;
        grid-template-columns: minmax(0, 1.06fr) minmax(390px, 0.94fr);
        min-height: 470px;
        width: 100%;
    }

    .executive-cover-copy {
        position: relative;
        z-index: 2;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        padding: 14px 42px 32px 44px;
        background:
            radial-gradient(circle at 10% 6%, rgba(78, 145, 174, 0.08), transparent 31%),
            linear-gradient(135deg, #ffffff 0%, #f6fbfd 56%, #eaf5f9 100%);
    }

    .executive-cover-title {
        margin: 0;
        color: #12344A;
        font-size: clamp(1.55rem, 1.9vw, 2rem);
        font-weight: 720;
        line-height: 1.06;
        letter-spacing: -0.03em;
    }

    .executive-cover-subtitle {
        margin: 10px 0 0 0;
        color: #2F708A;
        font-size: clamp(1rem, 1.28vw, 1.20rem);
        font-weight: 520;
        line-height: 1.30;
    }

    .executive-cover-text {
        max-width: 690px;
        margin-top: 18px;
        color: #405D6D;
        font-size: 0.88rem;
        line-height: 1.55;
    }

    .executive-cover-question {
        max-width: 690px;
        margin-top: 19px;
        padding: 12px 14px;
        border-left: 3px solid #D6A93C;
        border-radius: 0 9px 9px 0;
        background: rgba(255, 255, 255, 0.88);
        color: #29495B;
        font-size: 0.77rem;
        line-height: 1.45;
        box-shadow: 0 2px 8px rgba(31, 72, 94, 0.05);
    }

    .executive-cover-question-label {
        display: block;
        margin-bottom: 3px;
        color: #B48420;
        font-size: 0.62rem;
        font-weight: 750;
        letter-spacing: 0.045em;
        text-transform: uppercase;
    }

    .executive-cover-credit {
        margin-top: 13px;
        color: #5B7482;
        font-size: 0.72rem;
        line-height: 1.35;
    }

    .executive-cover-credit strong {
        color: #29495B;
        font-weight: 700;
    }

    .executive-cover-image {
        position: relative;
        min-height: 470px;
        background-position: center;
        background-size: cover;
        filter: saturate(0.78) brightness(1.16) contrast(0.92);
    }

    .executive-cover-image::before {
        content: "";
        position: absolute;
        inset: 0;
        background:
            linear-gradient(90deg, rgba(238,247,250,0.46) 0%, rgba(238,247,250,0.06) 35%),
            linear-gradient(0deg, rgba(22,62,80,0.05), transparent 44%);
    }

    @media (max-width: 980px) {
        .executive-cover-grid {
            grid-template-columns: 1fr;
        }

        .executive-cover-copy {
            padding: 30px 27px 28px 27px;
        }

        .executive-cover-image {
            min-height: 260px;
        }
    }

        .executive-cover-copy {
            padding: 32px 27px 29px 27px;
        }

        .executive-cover-image {
            min-height: 270px;
        }
    }
        </style>
    </head>
    <body>
    """ + cover_html + """
    </body>
    </html>
    """

    components.html(
        cover_document,
        height=470,
        scrolling=False,
    )


# ============================================================================
# TAB 1: STORY - VERSION 2 (آکاردئونی - Expandable Sections)
# ============================================================================

with tab_story:
    st.markdown("""
    <div class="dashboard-tab-header">
        <h4>Norway's Energy Geopolitics Story</h4>
        <p>Norway, a nation at a crossroads – balancing energy abundance, green transition, and geopolitical pressures.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================================
    # بخش ۱: Key Metrics (به‌صورت پیش‌فرض باز)
    # ============================================================
    with st.expander("📊 Key Metrics (2024) – Norway's Energy Snapshot", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f0f7ff, #e0ecf9); border-radius: 12px; padding: 18px 12px; text-align: center; border: 1px solid #dde4ec;">
                <div style="font-size: 2rem; font-weight: 700; color: #0A1628;">88%</div>
                <div style="font-size: 0.85rem; color: #4A6A8A;">💧 Hydropower Share</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #fef9e7, #fdf2d0); border-radius: 12px; padding: 18px 12px; text-align: center; border: 1px solid #dde4ec;">
                <div style="font-size: 2rem; font-weight: 700; color: #0A1628;">30%</div>
                <div style="font-size: 0.85rem; color: #4A6A8A;">🛢️ Europe's Gas Supply</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f0fdf4, #dcfce7); border-radius: 12px; padding: 18px 12px; text-align: center; border: 1px solid #dde4ec;">
                <div style="font-size: 1.5rem; font-weight: 700; color: #0A1628;">10-20 TWh/yr</div>
                <div style="font-size: 0.85rem; color: #4A6A8A;">⚡ Net Electricity Export</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #fef2f2, #fde8e8); border-radius: 12px; padding: 18px 12px; text-align: center; border: 1px solid #dde4ec;">
                <div style="font-size: 1.5rem; font-weight: 700; color: #E74C3C;">⚠️ 2030s</div>
                <div style="font-size: 0.85rem; color: #4A6A8A;">Power Deficit Starts</div>
            </div>
            """, unsafe_allow_html=True)
    
    # ============================================================
    # بخش ۲: The Trilemma
    # ============================================================
    with st.expander("⚖️ The Norwegian Trilemma – Three Competing Objectives", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div style="background: #f8fafc; border-radius: 12px; padding: 16px 18px; border-left: 4px solid #E67E22; height: 140px; display: flex; flex-direction: column; justify-content: center;">
                <div style="font-size: 1.5rem; margin-bottom: 3px;">🛢️</div>
                <div style="font-weight: 600; font-size: 1rem; color: #0A1628;">Sustaining Energy Exports</div>
                <div style="font-size: 0.85rem; color: #4A6A8A; margin-top: 4px; line-height: 1.5;">
                    Norway supplies <b>~30% of Europe's gas</b>. But this <b>locks capital and talent</b> into the fossil sector.
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="background: #f8fafc; border-radius: 12px; padding: 16px 18px; border-left: 4px solid #22C55E; height: 140px; display: flex; flex-direction: column; justify-content: center;">
                <div style="font-size: 1.5rem; margin-bottom: 3px;">🌱</div>
                <div style="font-weight: 600; font-size: 1rem; color: #0A1628;">Green Industrial Growth</div>
                <div style="font-size: 0.85rem; color: #4A6A8A; margin-top: 4px; line-height: 1.5;">
                    New industries need <b>clean, affordable power</b>. Rising demand strains the grid.
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div style="background: #f8fafc; border-radius: 12px; padding: 16px 18px; border-left: 4px solid #E74C3C; height: 140px; display: flex; flex-direction: column; justify-content: center;">
                <div style="font-size: 1.5rem; margin-bottom: 3px;">🌍</div>
                <div style="font-weight: 600; font-size: 1rem; color: #0A1628;">Rapid Emissions Cuts</div>
                <div style="font-size: 0.85rem; color: #4A6A8A; margin-top: 4px; line-height: 1.5;">
                    2050 target: <b>90-95%</b> | Forecast: <b>75%</b> | Planned credits: <b>~NOK 15bn/year</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
        # هشدار جمع‌بندی
        st.markdown("""
        <div style="background: #fef2f2; border-radius: 10px; padding: 10px 16px; border: 1px solid #fde8e8; text-align: center; margin-top: 8px;">
            <span style="color: #E74C3C; font-weight: 600;">⚠️ The Risk:</span>
            <span style="color: #4A6A8A;"> Norway currently risks falling short on all three ambitions.</span>
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================================
    # بخش ۳: Key Challenges
    # ============================================================
    with st.expander("⚡ Key Challenges – Power Deficit, Wind, Emissions & Grid", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="background: #f8fafc; border-radius: 12px; padding: 14px 16px; border: 1px solid #e2e8f0; margin-bottom: 10px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
                    <span style="font-size: 1.5rem;">⚡</span>
                    <span style="font-weight: 600; color: #0A1628;">Temporary Power Deficit</span>
                </div>
                <div style="font-size: 0.85rem; color: #4A6A8A; line-height: 1.5;">
                    Data-centre electricity demand reaches <b>29 TWh</b> by 2060, including <b>21 TWh</b> for AI-supporting services. Temporary deficit from the <b>early 2030s</b>.
                </div>
            </div>
            <div style="background: #f8fafc; border-radius: 12px; padding: 14px 16px; border: 1px solid #e2e8f0;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
                    <span style="font-size: 1.5rem;">🌬️</span>
                    <span style="font-weight: 600; color: #0A1628;">Wind: The Scalable Solution</span>
                </div>
                <div style="font-size: 0.85rem; color: #4A6A8A; line-height: 1.5;">
                    Onshore: <b>5 GW → 13 GW</b> | Offshore: <b>~0.1 GW → ~8 GW</b> (by 2060)<br>
                    <span style="color: #E74C3C; font-size: 0.8rem;">⚠️ Local opposition & slow permitting since 2019</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="background: #f8fafc; border-radius: 12px; padding: 14px 16px; border: 1px solid #e2e8f0; margin-bottom: 10px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
                    <span style="font-size: 1.5rem;">🌍</span>
                    <span style="font-weight: 600; color: #0A1628;">Emissions Gap</span>
                </div>
                <div style="font-size: 0.85rem; color: #4A6A8A; line-height: 1.5;">
                    <b>2030:</b> Target 55% ↓ | Forecast 30% ↓ (Gap: 25%)<br>
                    <b>2035:</b> Target 70-75% ↓ | Forecast 45% ↓ (Gap: 25-30%)<br>
                    <b>2050:</b> Target 90-95% ↓ | Forecast 75% ↓ (Gap: 15-20%)
                </div>
            </div>
            <div style="background: #f8fafc; border-radius: 12px; padding: 14px 16px; border: 1px solid #e2e8f0;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
                    <span style="font-size: 1.5rem;">🔌</span>
                    <span style="font-weight: 600; color: #0A1628;">Grid Investment Needed</span>
                </div>
                <div style="font-size: 0.85rem; color: #4A6A8A; line-height: 1.5;">
                    Statnett's plan outlines <b>NOK 150-200bn</b> of grid investment over the next decade.<br>
                    <span style="font-size: 0.8rem; color: #6A8AAA;">559 EEA-relevant acts unimplemented (Jan 2025)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # ============================================================
    # بخش ۴: What's Next (با توضیحات بیشتر)
    # ============================================================
    with st.expander("🔮 What's Next? – Norway's Strategic Choices", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 16px; border: 1px solid #e2e8f0; text-align: center; height: 140px; display: flex; flex-direction: column; justify-content: center;">
                <div style="font-size: 2rem;">📜</div>
                <div style="font-weight: 600; font-size: 1rem; color: #0A1628;">Policy Clarity</div>
                <div style="font-size: 0.85rem; color: #4A6A8A; margin-top: 4px;">Clear, stable policies to attract investment</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 16px; border: 1px solid #e2e8f0; text-align: center; height: 140px; display: flex; flex-direction: column; justify-content: center;">
                <div style="font-size: 2rem;">⚡</div>
                <div style="font-weight: 600; font-size: 1rem; color: #0A1628;">Grid Investment</div>
                <div style="font-size: 0.85rem; color: #4A6A8A; margin-top: 4px;">Statnett plan: NOK 150-200bn over the next decade</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 16px; border: 1px solid #e2e8f0; text-align: center; height: 140px; display: flex; flex-direction: column; justify-content: center;">
                <div style="font-size: 2rem;">🌬️</div>
                <div style="font-weight: 600; font-size: 1rem; color: #0A1628;">Wind Deployment</div>
                <div style="font-size: 0.85rem; color: #4A6A8A; margin-top: 4px;">Faster permitting & local acceptance</div>
            </div>
            """, unsafe_allow_html=True)
        
        # بخش فرصت
        st.markdown("""
        <div style="background: linear-gradient(135deg, #dcfce7, #f0fdf4); border-radius: 10px; padding: 12px 16px; text-align: center; border: 1px solid #bbf7d0; margin-top: 10px;">
            <span style="font-weight: 600; color: #166534;">🚀 The Opportunity:</span>
            <span style="color: #2d3748;"> Norway's choices on policy, grid development and wind deployment will strongly shape the speed and credibility of the transition.</span>
        </div>
        """, unsafe_allow_html=True)
    

# ============================================================================
# TAB 2: REFERENCE MODE OF BEHAVIOR AND DYNAMICS PROBLEM
# ============================================================================

with tab_data:
    
    st.markdown("""
    <div class="dashboard-tab-header">
        <h4>Reference Mode of Behavior and Dynamics Problem</h4>
        <p>See how power demand, emissions, exports and the energy mix evolve in DNV’s 2025 reference forecast.</p>
    </div>
    """, unsafe_allow_html=True)
    
    base_data = get_dynamic_scenario_data(1.0, 1.0, 0.78, "moderate", 75, "medium", 1.0)
    
    # ایجاد زیرتب‌ها
    subtab1, subtab2, subtab3, subtab4, subtab5, subtab6 = st.tabs([
        "📈 Supply & Demand",
        "🌍 GHG Emissions",
        "📊 Power Balance",
        "🛢️ Oil & Gas Exports",
        "💨 Wind Share",
        "🏭 Energy Mix"
    ])
    
    # ========== SUBTAB 1: Supply & Demand ==========
    with subtab1:
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1px;">
            <h4 style="margin: 0; color: #0A1628; font-size: 1.05rem; line-height: 1.18;">⚡ Norway moves from power surplus to deficit in the early 2030s: </h4>
        </div>
        <p style="margin: 0 0 5px 0; color: #4A6A8A; font-size: 0.75rem; line-height: 1.24;">Demand growth turns electricity availability into a strategic constraint.</p>
        """, unsafe_allow_html=True)
        
        chart_col, insight_col = st.columns([1.45, 1.05], gap="medium")
        
        with chart_col:
            fig1 = plot_supply_demand(base_data, show_uncertainty=False, show_baseline=True, reference_only=True)
            fig1.update_layout(
                title=dict(text=""),
                height=302,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.14,
                    xanchor="left",
                    x=0,
                    font=dict(size=9),
                    bgcolor="rgba(255,255,255,0.82)"
                ),
                margin=dict(l=35, r=10, t=48, b=35),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(title="", showgrid=True, gridcolor="#f0f0f0"),
                yaxis=dict(title="Electricity (TWh)", showgrid=True, gridcolor="#f0f0f0")
            )
            # اضافه کردن Annotation برای نقطه شروع کسری
            fig1.add_vline(x=2033, line_dash="dash", line_color="#E74C3C", line_width=1.5, opacity=0.7)
            fig1.add_annotation(x=2033, y=180, text="Deficit begins", showarrow=True, arrowhead=2, ax=30, ay=-30, font=dict(size=9, color="#E74C3C"), arrowcolor="#E74C3C")
            st.plotly_chart(fig1, width='stretch', key="ref_supply_chart", config={"displayModeBar": False, "responsive": True})
        
        with insight_col:
            st.markdown("""
            <div style="display: flex; gap: 6px; margin-bottom: 6px; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 60px; background: #f8fafc; border-radius: 6px; padding: 6px 8px; text-align: center; border: 1px solid #eef2f6;">
                    <div style="font-size: 0.55rem; color: #6A8AAA;">Deficit begins</div>
                    <div style="font-size: 0.9rem; font-weight: 700; color: #0A1628; line-height: 1.2;">2033</div>
                </div>
                <div style="flex: 1; min-width: 60px; background: #f8fafc; border-radius: 6px; padding: 6px 8px; text-align: center; border: 1px solid #eef2f6;">
                    <div style="font-size: 0.55rem; color: #6A8AAA;">Peak import</div>
                    <div style="font-size: 0.9rem; font-weight: 700; color: #0A1628; line-height: 1.2;">5 TWh</div>
                </div>
                <div style="flex: 1; min-width: 60px; background: #f8fafc; border-radius: 6px; padding: 6px 8px; text-align: center; border: 1px solid #eef2f6;">
                    <div style="font-size: 0.55rem; color: #6A8AAA;">Demand growth</div>
                    <div style="font-size: 0.9rem; font-weight: 700; color: #0A1628; line-height: 1.2;">29 TWh</div>
                    <div style="font-size: 0.55rem; color: #4A6A8A;">Data centres</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: #fef9e7; border-radius: 6px; padding: 8px 10px; border-left: 3px solid #E67E22; margin-top: 4px;">
                <div style="font-size: 0.6rem; color: #6A8AAA; font-weight: 600;">🚗 DRIVER</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #0A1628;">Electrification & Data Centres</div>
                <div style="font-size: 0.7rem; color: #4A6A8A;">Rapid demand growth from EVs, industry, and AI</div>
            </div>
            <div style="background: #fef2f2; border-radius: 6px; padding: 8px 10px; border-left: 3px solid #E74C3C; margin-top: 3px;">
                <div style="font-size: 0.6rem; color: #6A8AAA; font-weight: 600;">🔒 CONSTRAINT</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #0A1628;">Slow Wind & Grid Expansion</div>
                <div style="font-size: 0.7rem; color: #4A6A8A;">Supply growth lagging behind demand</div>
            </div>
            <div style="background: #eff6ff; border-radius: 6px; padding: 8px 10px; border-left: 3px solid #2E86AB; margin-top: 3px;">
                <div style="font-size: 0.6rem; color: #6A8AAA; font-weight: 600;">⚡ STRATEGIC IMPLICATION</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #0A1628;">Higher Import Dependence</div>
                <div style="font-size: 0.7rem; color: #4A6A8A;">Norway becomes a net importer</div>
            </div>
            """, unsafe_allow_html=True)
        
    
    # ========== SUBTAB 2: GHG Emissions ==========
    with subtab2:
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1px;">
            <h4 style="margin: 0; color: #0A1628; font-size: 1.05rem; line-height: 1.18;">🌍 Norway's climate ambition is moving faster than domestic delivery</h4>
        </div>
        <p style="margin: 0 0 5px 0; color: #4A6A8A; font-size: 0.75rem; line-height: 1.24;">The emissions gap increasingly becomes a credibility and policy-coordination problem.</p>
        """, unsafe_allow_html=True)
        
        chart_col, insight_col = st.columns([1.45, 1.05], gap="medium")
        
        with chart_col:
            fig2 = plot_emissions(base_data, show_uncertainty=False, show_baseline=True, reference_only=True)
            fig2.update_layout(
                title=dict(text=""),
                height=315,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.14,
                    xanchor="left",
                    x=0,
                    font=dict(size=9),
                    bgcolor="rgba(255,255,255,0.82)"
                ),
                margin=dict(l=35, r=10, t=48, b=35),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(title="", showgrid=True, gridcolor="#f0f0f0"),
                yaxis=dict(title="Emissions (MtCO₂)", showgrid=True, gridcolor="#f0f0f0")
            )
            # اضافه کردن Annotation برای شکاف هدف
            fig2.add_vline(x=2030, line_dash="dash", line_color="#E74C3C", line_width=1.5, opacity=0.5)
            fig2.add_annotation(x=2030, y=20, text="2030 target gap: 25%", showarrow=True, arrowhead=2, ax=40, ay=-30, font=dict(size=8, color="#E74C3C"), arrowcolor="#E74C3C")
            st.plotly_chart(fig2, width='stretch', key="ref_emissions_chart", config={"displayModeBar": False, "responsive": True})
        
        with insight_col:
            st.markdown("""
            <div style="display: flex; gap: 6px; margin-bottom: 6px; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 60px; background: #f8fafc; border-radius: 6px; padding: 6px 8px; text-align: center; border: 1px solid #eef2f6;">
                    <div style="font-size: 0.55rem; color: #6A8AAA;">2030 Target</div>
                    <div style="font-size: 0.9rem; font-weight: 700; color: #0A1628; line-height: 1.2;">55% ↓</div>
                    <div style="font-size: 0.55rem; color: #4A6A8A;">from 1990</div>
                </div>
                <div style="flex: 1; min-width: 60px; background: #f8fafc; border-radius: 6px; padding: 6px 8px; text-align: center; border: 1px solid #eef2f6;">
                    <div style="font-size: 0.55rem; color: #6A8AAA;">2030 Forecast</div>
                    <div style="font-size: 0.9rem; font-weight: 700; color: #E74C3C; line-height: 1.2;">30% ↓</div>
                    <div style="font-size: 0.55rem; color: #4A6A8A;">25% gap</div>
                </div>
                <div style="flex: 1; min-width: 60px; background: #f8fafc; border-radius: 6px; padding: 6px 8px; text-align: center; border: 1px solid #eef2f6;">
                    <div style="font-size: 0.55rem; color: #6A8AAA;">2050 Forecast</div>
                    <div style="font-size: 0.9rem; font-weight: 700; color: #E74C3C; line-height: 1.2;">75% ↓</div>
                    <div style="font-size: 0.55rem; color: #4A6A8A;">15-20% gap</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: #fef9e7; border-radius: 6px; padding: 8px 10px; border-left: 3px solid #E67E22; margin-top: 4px;">
                <div style="font-size: 0.6rem; color: #6A8AAA; font-weight: 600;">🚗 DRIVER</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #0A1628;">Slow Structural Transformation</div>
                <div style="font-size: 0.7rem; color: #4A6A8A;">Persistent investment in oil and gas</div>
            </div>
            <div style="background: #fef2f2; border-radius: 6px; padding: 8px 10px; border-left: 3px solid #E74C3C; margin-top: 3px;">
                <div style="font-size: 0.6rem; color: #6A8AAA; font-weight: 600;">🔒 CONSTRAINT</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #0A1628;">Fossil Lock-in & Insufficient Policy</div>
                <div style="font-size: 0.7rem; color: #4A6A8A;">High earnings reduce urgency for change</div>
            </div>
            <div style="background: #eff6ff; border-radius: 6px; padding: 8px 10px; border-left: 3px solid #2E86AB; margin-top: 3px;">
                <div style="font-size: 0.6rem; color: #6A8AAA; font-weight: 600;">⚡ STRATEGIC IMPLICATION</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #0A1628;">Dependence on International Credits</div>
                <div style="font-size: 0.7rem; color: #4A6A8A;">~NOK 15bn/year for carbon credits</div>
            </div>
            """, unsafe_allow_html=True)
        
    
    # ========== SUBTAB 3: Power Balance (European Interdependence) ==========
    with subtab3:
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1px;">
            <h4 style="margin: 0; color: #0A1628; font-size: 1.05rem; line-height: 1.18;">🔌 Norway shifts from electricity independence toward deeper European interdependence</h4>
        </div>
        <p style="margin: 0 0 5px 0; color: #4A6A8A; font-size: 0.75rem; line-height: 1.24;">The geopolitical implication of the power deficit.</p>
        """, unsafe_allow_html=True)
        
        chart_col, insight_col = st.columns([1.45, 1.05], gap="medium")
        
        with chart_col:
            fig3 = plot_power_balance(base_data)
            fig3.update_layout(
                title=dict(text=""),
                height=315,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.14,
                    xanchor="left",
                    x=0,
                    font=dict(size=9),
                    bgcolor="rgba(255,255,255,0.82)"
                ),
                margin=dict(l=35, r=10, t=48, b=35),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(title="", showgrid=True, gridcolor="#f0f0f0"),
                yaxis=dict(title="Balance (TWh)", showgrid=True, gridcolor="#f0f0f0")
            )
            # اضافه کردن ناحیه سایه برای دوره کسری
            fig3.add_vrect(x0=2033, x1=2037, fillcolor="#E74C3C", opacity=0.08, line_width=0)
            fig3.add_annotation(x=2035, y=-2, text="Deficit period", showarrow=False, font=dict(size=8, color="#E74C3C", weight="bold"))
            st.plotly_chart(fig3, width='stretch', key="ref_balance_chart", config={"displayModeBar": False, "responsive": True})
        
        with insight_col:
            st.markdown("""
            <div style="display: flex; gap: 6px; margin-bottom: 6px; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 60px; background: #f8fafc; border-radius: 6px; padding: 6px 8px; text-align: center; border: 1px solid #eef2f6;">
                    <div style="font-size: 0.55rem; color: #6A8AAA;">Current Status</div>
                    <div style="font-size: 0.8rem; font-weight: 700; color: #0A1628; line-height: 1.2;">Net Exporter</div>
                    <div style="font-size: 0.55rem; color: #4A6A8A;">10-20 TWh/yr</div>
                </div>
                <div style="flex: 1; min-width: 60px; background: #f8fafc; border-radius: 6px; padding: 6px 8px; text-align: center; border: 1px solid #eef2f6;">
                    <div style="font-size: 0.55rem; color: #6A8AAA;">Future Status</div>
                    <div style="font-size: 0.8rem; font-weight: 700; color: #E74C3C; line-height: 1.2;">Net Importer</div>
                    <div style="font-size: 0.55rem; color: #4A6A8A;">from 2033</div>
                </div>
                <div style="flex: 1; min-width: 60px; background: #f8fafc; border-radius: 6px; padding: 6px 8px; text-align: center; border: 1px solid #eef2f6;">
                    <div style="font-size: 0.55rem; color: #6A8AAA;">Key Exposure</div>
                    <div style="font-size: 0.8rem; font-weight: 700; color: #0A1628; line-height: 1.2;">European Prices</div>
                    <div style="font-size: 0.55rem; color: #4A6A8A;">Interconnectors</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: #fef9e7; border-radius: 6px; padding: 8px 10px; border-left: 3px solid #E67E22; margin-top: 4px;">
                <div style="font-size: 0.6rem; color: #6A8AAA; font-weight: 600;">🔀 DRIVER</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #0A1628;">Rising Domestic Demand</div>
                <div style="font-size: 0.7rem; color: #4A6A8A;">Electrification and data centres</div>
            </div>
            <div style="background: #fef2f2; border-radius: 6px; padding: 8px 10px; border-left: 3px solid #E74C3C; margin-top: 3px;">
                <div style="font-size: 0.6rem; color: #6A8AAA; font-weight: 600;">🔀 CONSTRAINT</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #0A1628;">Intermittent Renewables & Grid</div>
                <div style="font-size: 0.7rem; color: #4A6A8A;">Variable wind and solar integration</div>
            </div>
            <div style="background: #eff6ff; border-radius: 6px; padding: 8px 10px; border-left: 3px solid #2E86AB; margin-top: 3px;">
                <div style="font-size: 0.6rem; color: #6A8AAA; font-weight: 600;">⚡ STRATEGIC IMPLICATION</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #0A1628;">European Price Exposure</div>
                <div style="font-size: 0.7rem; color: #4A6A8A;">Interconnectors increase market exposure while providing flexibility</div>
            </div>
            """, unsafe_allow_html=True)
        
    
    # ========== SUBTAB 4: Oil & Gas Exports ==========
    with subtab4:
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1px;">
            <h4 style="margin: 0; color: #0A1628; font-size: 1.05rem; line-height: 1.18;">🛢️ Norway's strategic relevance rises before its export model contracts</h4>
        </div>
        <p style="margin: 0 0 5px 0; color: #4A6A8A; font-size: 0.75rem; line-height: 1.24;">Export trajectories are shown below. DNV 2024 production: oil 106 MSm³oe/yr (~1.83 Mbpd); gas 135 Bcm/yr.</p>
        """, unsafe_allow_html=True)
        
        chart_col, insight_col = st.columns([1.45, 1.05], gap="medium")
        
        with chart_col:
            fig4 = plot_export_composition(base_data)
            fig4.update_layout(
                title=dict(text=""),
                height=315,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.14,
                    xanchor="left",
                    x=0,
                    font=dict(size=9),
                    bgcolor="rgba(255,255,255,0.82)"
                ),
                margin=dict(l=35, r=10, t=48, b=35),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(title="", showgrid=True, gridcolor="#f0f0f0"),
                yaxis=dict(title="Exports (MSm³oe/yr)", showgrid=True, gridcolor="#f0f0f0")
            )
            # اضافه کردن Annotation برای نقطه کاهش
            fig4.add_vline(x=2040, line_dash="dash", line_color="#E67E22", line_width=1.5, opacity=0.5)
            fig4.add_annotation(x=2040, y=60, text="Oil & gas production ~halves by 2040", showarrow=True, arrowhead=2, ax=40, ay=-30, font=dict(size=8, color="#E67E22"), arrowcolor="#E67E22")
            st.plotly_chart(fig4, width='stretch', key="ref_exports_chart", config={"displayModeBar": False, "responsive": True})
        
        with insight_col:
            st.markdown("""
            <div style="display: flex; gap: 6px; margin-bottom: 6px; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 60px; background: #f8fafc; border-radius: 6px; padding: 6px 8px; text-align: center; border: 1px solid #eef2f6;">
                    <div style="font-size: 0.55rem; color: #6A8AAA;">Europe's Gas</div>
                    <div style="font-size: 0.9rem; font-weight: 700; color: #0A1628; line-height: 1.2;">30%</div>
                    <div style="font-size: 0.55rem; color: #4A6A8A;">of supply today</div>
                </div>
                <div style="flex: 1; min-width: 60px; background: #f8fafc; border-radius: 6px; padding: 6px 8px; text-align: center; border: 1px solid #eef2f6;">
                    <div style="font-size: 0.55rem; color: #6A8AAA;">by 2040</div>
                    <div style="font-size: 0.9rem; font-weight: 700; color: #E67E22; line-height: 1.2;">50% ↓</div>
                    <div style="font-size: 0.55rem; color: #4A6A8A;">production</div>
                </div>
                <div style="flex: 1; min-width: 60px; background: #f8fafc; border-radius: 6px; padding: 6px 8px; text-align: center; border: 1px solid #eef2f6;">
                    <div style="font-size: 0.55rem; color: #6A8AAA;">by 2060</div>
                    <div style="font-size: 0.9rem; font-weight: 700; color: #E74C3C; line-height: 1.2;">80% ↓</div>
                    <div style="font-size: 0.55rem; color: #4A6A8A;">exports</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: #fef9e7; border-radius: 6px; padding: 8px 10px; border-left: 3px solid #E67E22; margin-top: 4px;">
                <div style="font-size: 0.6rem; color: #6A8AAA; font-weight: 600;">🚗 DRIVER</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #0A1628;">European Security Demand</div>
                <div style="font-size: 0.7rem; color: #4A6A8A;">Reliable supply after Russian losses</div>
            </div>
            <div style="background: #fef2f2; border-radius: 6px; padding: 8px 10px; border-left: 3px solid #E74C3C; margin-top: 3px;">
                <div style="font-size: 0.6rem; color: #6A8AAA; font-weight: 600;">🔒 CONSTRAINT</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #0A1628;">Declining Fossil Demand</div>
                <div style="font-size: 0.7rem; color: #4A6A8A;">Europe's decarbonization pathway</div>
            </div>
            <div style="background: #eff6ff; border-radius: 6px; padding: 8px 10px; border-left: 3px solid #2E86AB; margin-top: 3px;">
                <div style="font-size: 0.6rem; color: #6A8AAA; font-weight: 600;">⚡ STRATEGIC IMPLICATION</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #0A1628;">Post-Petroleum Export Model Needed</div>
                <div style="font-size: 0.7rem; color: #4A6A8A;">Hydrogen? Electricity? Industrial goods?</div>
            </div>
            """, unsafe_allow_html=True)
        
    
    # ========== SUBTAB 5: Wind Share (Wind Scale-up) ==========
    with subtab5:
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1px;">
            <h4 style="margin: 0; color: #0A1628; font-size: 1.05rem; line-height: 1.18;">💨 Wind must scale rapidly, but deployment remains politically and economically constrained</h4>
        </div>
        <p style="margin: 0 0 5px 0; color: #4A6A8A; font-size: 0.75rem; line-height: 1.24;">The only scalable solution to the power deficit.</p>
        """, unsafe_allow_html=True)
        
        chart_col, insight_col = st.columns([1.45, 1.05], gap="medium")
        
        with chart_col:
            fig5 = plot_renewable_share(base_data, show_baseline=True)
            fig5.update_layout(
                title=dict(text=""),
                height=315,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.14,
                    xanchor="left",
                    x=0,
                    font=dict(size=9),
                    bgcolor="rgba(255,255,255,0.82)"
                ),
                margin=dict(l=35, r=10, t=48, b=35),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(title="", showgrid=True, gridcolor="#f0f0f0"),
                yaxis=dict(title="Wind Share (%)", showgrid=True, gridcolor="#f0f0f0")
            )
            # اضافه کردن Annotation برای نقطه 50%
            fig5.add_hline(y=50, line_dash="dash", line_color="#22C55E", line_width=1.5, opacity=0.5)
            fig5.add_annotation(x=2050, y=52, text="50% wind-generation share", showarrow=False, font=dict(size=8, color="#22C55E"))
            st.plotly_chart(fig5, width='stretch', key="ref_renewable_chart", config={"displayModeBar": False, "responsive": True})
        
        with insight_col:
            st.markdown("""
            <div style="display: flex; gap: 6px; margin-bottom: 6px; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 60px; background: #f8fafc; border-radius: 6px; padding: 6px 8px; text-align: center; border: 1px solid #eef2f6;">
                    <div style="font-size: 0.55rem; color: #6A8AAA;">Onshore (2060)</div>
                    <div style="font-size: 0.9rem; font-weight: 700; color: #0A1628; line-height: 1.2;">13 GW</div>
                    <div style="font-size: 0.55rem; color: #4A6A8A;">from 5 GW today</div>
                </div>
                <div style="flex: 1; min-width: 60px; background: #f8fafc; border-radius: 6px; padding: 6px 8px; text-align: center; border: 1px solid #eef2f6;">
                    <div style="font-size: 0.55rem; color: #6A8AAA;">Offshore (2040)</div>
                    <div style="font-size: 0.9rem; font-weight: 700; color: #0A1628; line-height: 1.2;">~6.5 GW</div>
                    <div style="font-size: 0.55rem; color: #4A6A8A;">to ~8 GW by 2060</div>
                </div>
                <div style="flex: 1; min-width: 60px; background: #f8fafc; border-radius: 6px; padding: 6px 8px; text-align: center; border: 1px solid #eef2f6;">
                    <div style="font-size: 0.55rem; color: #6A8AAA;">Total Wind</div>
                    <div style="font-size: 0.9rem; font-weight: 700; color: #0A1628; line-height: 1.2;">~21 GW</div>
                    <div style="font-size: 0.55rem; color: #4A6A8A;">~4x growth</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: #fef9e7; border-radius: 6px; padding: 8px 10px; border-left: 3px solid #E67E22; margin-top: 4px;">
                <div style="font-size: 0.6rem; color: #6A8AAA; font-weight: 600;">🚗 DRIVER</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #0A1628;">Rising Electricity Demand</div>
                <div style="font-size: 0.7rem; color: #4A6A8A;">Need for clean, scalable power</div>
            </div>
            <div style="background: #fef2f2; border-radius: 6px; padding: 8px 10px; border-left: 3px solid #E74C3C; margin-top: 3px;">
                <div style="font-size: 0.6rem; color: #6A8AAA; font-weight: 600;">🔒 CONSTRAINT</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #0A1628;">Cost, Permitting & Acceptance</div>
                <div style="font-size: 0.7rem; color: #4A6A8A;">Local opposition since 2019</div>
            </div>
            <div style="background: #eff6ff; border-radius: 6px; padding: 8px 10px; border-left: 3px solid #2E86AB; margin-top: 3px;">
                <div style="font-size: 0.6rem; color: #6A8AAA; font-weight: 600;">⚡ STRATEGIC IMPLICATION</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #0A1628;">Delayed Return to Power Surplus</div>
                <div style="font-size: 0.7rem; color: #4A6A8A;">Grid investment critical</div>
            </div>
            """, unsafe_allow_html=True)
        
    
    # ========== SUBTAB 6: Energy Mix ==========
    with subtab6:
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1px;">
            <h4 style="margin: 0; color: #0A1628; font-size: 1.05rem; line-height: 1.18;">🏭 Can the future power mix expand fast enough to replace declining fossil-energy advantages?</h4>
        </div>
        <p style="margin: 0 0 5px 0; color: #4A6A8A; font-size: 0.75rem; line-height: 1.24;">The challenge is not only changing the mix; it is expanding the entire electricity system fast enough.</p>
        """, unsafe_allow_html=True)
        
        chart_col, insight_col = st.columns([1.45, 1.05], gap="medium")
        
        with chart_col:
            fig6 = plot_energy_mix()
            fig6.update_layout(
                title=dict(text=""),
                height=315,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.14,
                    xanchor="left",
                    x=0,
                    font=dict(size=9),
                    bgcolor="rgba(255,255,255,0.82)"
                ),
                margin=dict(l=35, r=10, t=48, b=35),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(title="", showgrid=False),
                yaxis=dict(title="TWh", showgrid=True, gridcolor="#f0f0f0")
            )
            st.plotly_chart(fig6, width='stretch', key="ref_mix_chart", config={"displayModeBar": False, "responsive": True})
        
        with insight_col:
            st.markdown("""
            <div style="display: flex; gap: 6px; margin-bottom: 6px; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 60px; background: #f8fafc; border-radius: 6px; padding: 6px 8px; text-align: center; border: 1px solid #eef2f6;">
                    <div style="font-size: 0.55rem; color: #6A8AAA;">Hydropower</div>
                    <div style="font-size: 0.9rem; font-weight: 700; color: #0A1628; line-height: 1.2;">149 TWh</div>
                    <div style="font-size: 0.55rem; color: #4A6A8A;">63% in 2060</div>
                </div>
                <div style="flex: 1; min-width: 60px; background: #f8fafc; border-radius: 6px; padding: 6px 8px; text-align: center; border: 1px solid #eef2f6;">
                    <div style="font-size: 0.55rem; color: #6A8AAA;">Wind</div>
                    <div style="font-size: 0.9rem; font-weight: 700; color: #0A1628; line-height: 1.2;">~72 TWh</div>
                    <div style="font-size: 0.55rem; color: #4A6A8A;">~30% in 2060</div>
                </div>
                <div style="flex: 1; min-width: 60px; background: #f8fafc; border-radius: 6px; padding: 6px 8px; text-align: center; border: 1px solid #eef2f6;">
                    <div style="font-size: 0.55rem; color: #6A8AAA;">Total Supply</div>
                    <div style="font-size: 0.9rem; font-weight: 700; color: #0A1628; line-height: 1.2;">238 TWh</div>
                    <div style="font-size: 0.55rem; color: #4A6A8A;">+82 TWh growth</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: #fef9e7; border-radius: 6px; padding: 8px 10px; border-left: 3px solid #E67E22; margin-top: 4px;">
                <div style="font-size: 0.6rem; color: #6A8AAA; font-weight: 600;">🏗️ FOUNDATION</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #0A1628;">Flexible Hydropower</div>
                <div style="font-size: 0.7rem; color: #4A6A8A;">Backbone of the system</div>
            </div>
            <div style="background: #eff6ff; border-radius: 6px; padding: 8px 10px; border-left: 3px solid #2E86AB; margin-top: 3px;">
                <div style="font-size: 0.6rem; color: #6A8AAA; font-weight: 600;">🚀 GROWTH ENGINE</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #0A1628;">Wind Power</div>
                <div style="font-size: 0.7rem; color: #4A6A8A;">Onshore + Offshore</div>
            </div>
            <div style="background: #fef2f2; border-radius: 6px; padding: 8px 10px; border-left: 3px solid #E74C3C; margin-top: 3px;">
                <div style="font-size: 0.6rem; color: #6A8AAA; font-weight: 600;">⚡ SYSTEM REQUIREMENT</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #0A1628;">Grid & Balancing Capacity</div>
                <div style="font-size: 0.7rem; color: #4A6A8A;">Statnett plan: NOK 150-200bn</div>
            </div>
            """, unsafe_allow_html=True)
        

# ============================================================================
# TAB 3: CAUSAL LOOPS (GRAPHICAL VERSION WITH PYVIS)
# ============================================================================

with tab_causal:
    # معرفی کوتاه - فقط ۳ خط
    st.markdown("""
    <div class="dashboard-tab-header">
        <h4>Four qualitative feedback structures illustrate how Norway's energy transition may accelerate, stall or reinforce fossil dependence.</h4>
        <p>Select a loop to explore its mechanism, dominant constraint and geopolitical consequence.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ایجاد زیرتب‌ها - بدون expander اضافی
    subtab_loop1, subtab_loop2, subtab_loop3, subtab_loop4, subtab_summary = st.tabs([
        "🟢 R1 — Green Industrial Expansion",
        "⚖️ B1 — Policy Implementation Friction",
        "🌍 R2 — Energy-Security Lock-in",
        "🧠 R3 — Fossil-Sector Resource Lock-in",
        "📋 Strategic Interpretation"
    ])
    
    def create_causal_loop_diagram(nodes_data, edges_data, height=310):
        """
        Create a fixed, presentation-ready causal-loop diagram as inline SVG.

        Nodes are locked to a circular layout and links follow curved outer arcs,
        so each graphic reads as a feedback loop rather than a generic network.
        """
        import math
        import html

        width = 760
        svg_height = 330
        center_x = width / 2
        center_y = 160

        node_count = len(nodes_data)
        radius_x = 245 if node_count >= 5 else 225
        radius_y = 112
        node_width = 142 if node_count >= 5 else 154
        node_height = 48

        node_lookup = {}
        positioned_nodes = []

        for index, node in enumerate(nodes_data):
            angle = -math.pi / 2 + (2 * math.pi * index / node_count)
            x = center_x + radius_x * math.cos(angle)
            y = center_y + radius_y * math.sin(angle)

            positioned = {
                **node,
                "x": x,
                "y": y,
                "angle": angle,
            }
            positioned_nodes.append(positioned)
            node_lookup[node["id"]] = positioned

        negative_links = sum(
            1 for edge in edges_data
            if str(edge.get("label", "")).strip() == "-"
        )
        is_balancing = negative_links % 2 == 1
        loop_code = "B" if is_balancing else "R"
        loop_label = "BALANCING" if is_balancing else "REINFORCING"
        loop_color = "#B7791F" if is_balancing else "#1F7A5A"
        loop_fill = "#FFF8E8" if is_balancing else "#ECFDF5"

        marker_defs = []
        path_elements = []
        edge_label_elements = []

        for edge_index, edge in enumerate(edges_data):
            source = node_lookup[edge["source"]]
            target = node_lookup[edge["target"]]

            if node_count >= 5:
                # Use dedicated connection ports for the five-node R1 loop.
                # The former chord-based geometry made several arrows look
                # disconnected. These ports create five smooth, continuous arcs
                # that meet each node cleanly and consistently.
                connection_key = (edge["source"], edge["target"])

                custom_connections = {
                    ("Wind", "Supply"): {
                        "start": (source["x"] + node_width / 2 + 4, source["y"] + 2),
                        "control": (target["x"] - 18, source["y"] - 24),
                        "end": (target["x"] - node_width / 2 - 11, target["y"] - 13),
                        "label": (target["x"] - 92, source["y"] - 26),
                    },
                    ("Supply", "Price"): {
                        "start": (source["x"] + 30, source["y"] + node_height / 2 + 4),
                        "control": (source["x"] + 80, (source["y"] + target["y"]) / 2),
                        "end": (target["x"] + node_width / 2 + 11, target["y"] - 12),
                        "label": (source["x"] + 72, (source["y"] + target["y"]) / 2),
                    },
                    ("Price", "GreenIndustry"): {
                        "start": (source["x"] - node_width / 2 - 4, source["y"] + 7),
                        "control": (center_x, target["y"] + 78),
                        "end": (target["x"] + node_width / 2 + 11, target["y"] + 5),
                        "label": (center_x, target["y"] + 64),
                    },
                    ("GreenIndustry", "Demand"): {
                        "start": (source["x"] - 35, source["y"] - node_height / 2 - 4),
                        "control": (source["x"] - 105, (source["y"] + target["y"]) / 2),
                        "end": (target["x"] - 30, target["y"] + node_height / 2 + 11),
                        "label": (source["x"] - 92, (source["y"] + target["y"]) / 2 + 5),
                    },
                    ("Demand", "Wind"): {
                        "start": (source["x"] + node_width / 2 + 4, source["y"] - 12),
                        "control": (source["x"] + 70, source["y"] - 88),
                        "end": (target["x"] - node_width / 2 - 11, target["y"] + 4),
                        "label": (source["x"] + 88, source["y"] - 70),
                    },
                }

                geometry = custom_connections[connection_key]
                x1, y1 = geometry["start"]
                control_x, control_y = geometry["control"]
                x2, y2 = geometry["end"]
                label_x, label_y = geometry["label"]

                # Used only by the generic label offset code below.
                outward_x = 0
                outward_y = 0

            else:
                dx = target["x"] - source["x"]
                dy = target["y"] - source["y"]
                distance = max(math.hypot(dx, dy), 1)
                ux = dx / distance
                uy = dy / distance

                half_width = node_width / 2
                half_height = node_height / 2

                source_scale = min(
                    half_width / max(abs(ux), 1e-6),
                    half_height / max(abs(uy), 1e-6),
                )
                target_scale = min(
                    half_width / max(abs(ux), 1e-6),
                    half_height / max(abs(uy), 1e-6),
                )

                line_clearance = 7
                arrowhead_clearance = 15

                x1 = source["x"] + ux * (source_scale + line_clearance)
                y1 = source["y"] + uy * (source_scale + line_clearance)
                x2 = target["x"] - ux * (target_scale + arrowhead_clearance)
                y2 = target["y"] - uy * (target_scale + arrowhead_clearance)

                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                radial_x = mid_x - center_x
                radial_y = mid_y - center_y
                radial_length = max(math.hypot(radial_x, radial_y), 1)
                outward_x = radial_x / radial_length
                outward_y = radial_y / radial_length

                curve_strength = 60
                control_x = mid_x + outward_x * curve_strength
                control_y = mid_y + outward_y * curve_strength

            edge_color = edge.get("color", "#55707F")
            marker_id = f"arrow_{edge_index}"

            marker_defs.append(
                f'''
                <marker id="{marker_id}" markerWidth="8" markerHeight="8"
                        refX="7.2" refY="4" orient="auto"
                        markerUnits="strokeWidth">
                    <path d="M 0 0 L 8 4 L 0 8 z"
                          fill="{edge_color}"></path>
                </marker>
                '''
            )

            path_elements.append(
                f'''
                <path d="M {x1:.1f},{y1:.1f}
                         Q {control_x:.1f},{control_y:.1f}
                           {x2:.1f},{y2:.1f}"
                      fill="none"
                      stroke="{edge_color}"
                      stroke-width="2.8"
                      stroke-linecap="round"
                      marker-end="url(#{marker_id})">
                    <title>{html.escape(edge.get("title", ""))}</title>
                </path>
                '''
            )

            if node_count < 5:
                label_x = (
                    0.25 * x1 + 0.5 * control_x + 0.25 * x2
                    + outward_x * 5
                )
                label_y = (
                    0.25 * y1 + 0.5 * control_y + 0.25 * y2
                    + outward_y * 5
                )
            sign = html.escape(str(edge.get("label", "")))

            edge_label_elements.append(
                f'''
                <g transform="translate({label_x:.1f},{label_y:.1f})">
                    <circle r="12" fill="#FFFFFF"
                            stroke="{edge_color}"
                            stroke-width="1.8"></circle>
                    <text text-anchor="middle"
                          dominant-baseline="central"
                          font-family="Inter, Arial, sans-serif"
                          font-size="15"
                          font-weight="700"
                          fill="{edge_color}">{sign}</text>
                </g>
                '''
            )

        node_elements = []

        for node in positioned_nodes:
            raw_label = str(node.get("label", ""))
            title = html.escape(node.get("title", ""))
            color = node.get("color", "#2E86AB")

            words = raw_label.split()
            if len(words) >= 3:
                split_at = max(1, len(words) // 2)
                line_1 = html.escape(" ".join(words[:split_at]))
                line_2 = html.escape(" ".join(words[split_at:]))

                label_svg = f'''
                    <text x="{node["x"]:.1f}"
                          y="{node["y"] - 4:.1f}"
                          text-anchor="middle"
                          font-family="Inter, Arial, sans-serif"
                          font-size="12.5"
                          font-weight="650"
                          fill="#17384C">
                        <tspan x="{node["x"]:.1f}" dy="0">{line_1}</tspan>
                        <tspan x="{node["x"]:.1f}" dy="15">{line_2}</tspan>
                    </text>
                '''
            else:
                label = html.escape(raw_label)
                label_svg = f'''
                    <text x="{node["x"]:.1f}"
                          y="{node["y"] + 1:.1f}"
                          text-anchor="middle"
                          dominant-baseline="central"
                          font-family="Inter, Arial, sans-serif"
                          font-size="12.8"
                          font-weight="650"
                          fill="#17384C">{label}</text>
                '''

            node_elements.append(
                f'''
                <g>
                    <rect x="{node["x"] - node_width / 2:.1f}"
                          y="{node["y"] - node_height / 2:.1f}"
                          width="{node_width}"
                          height="{node_height}"
                          rx="15"
                          fill="#FFFFFF"
                          stroke="{color}"
                          stroke-width="2.2"></rect>                    {label_svg}
                    <title>{title}</title>
                </g>
                '''
            )

        svg = f'''
        <div class="cld-frame">
            <svg viewBox="0 0 {width} {svg_height}"
                 role="img"
                 aria-label="Fixed causal feedback loop diagram"
                 preserveAspectRatio="xMidYMid meet">
                <defs>
                    {''.join(marker_defs)}
                </defs>

                <ellipse cx="{center_x}"
                         cy="{center_y}"
                         rx="{radius_x - 54}"
                         ry="{radius_y - 32}"
                         fill="none"
                         stroke="#DDE7EC"
                         stroke-width="1.2"
                         stroke-dasharray="4 7"></ellipse>

                {''.join(path_elements)}
                {''.join(edge_label_elements)}

                <g>
                    <circle cx="{center_x}"
                            cy="{center_y}"
                            r="38"
                            fill="{loop_fill}"
                            stroke="{loop_color}"
                            stroke-width="2"></circle>
                    <text x="{center_x}"
                          y="{center_y - 4}"
                          text-anchor="middle"
                          font-family="Inter, Arial, sans-serif"
                          font-size="22"
                          font-weight="750"
                          fill="{loop_color}">{loop_code}</text>
                    <text x="{center_x}"
                          y="{center_y + 15}"
                          text-anchor="middle"
                          font-family="Inter, Arial, sans-serif"
                          font-size="8.5"
                          font-weight="700"
                          letter-spacing="1"
                          fill="{loop_color}">{loop_label}</text>
                </g>

                {''.join(node_elements)}
            </svg>
        </div>

        <style>
            html, body {{
                margin: 0;
                padding: 0;
                background: transparent;
                overflow: hidden;
                font-family: Inter, Arial, sans-serif;
            }}

            .cld-frame {{
                width: 100%;
                height: {height}px;
                box-sizing: border-box;
                border: 1px solid #E4ECEF;
                border-radius: 12px;
                background:
                    radial-gradient(
                        circle at center,
                        rgba(238,245,247,0.72) 0%,
                        rgba(255,255,255,0) 58%
                    ),
                    #FBFDFE;
                padding: 2px 6px;
            }}

            .cld-frame svg {{
                width: 100%;
                height: 100%;
                display: block;
            }}
        </style>
        '''

        return svg


    def create_r1_reference_diagram(height=310):
        """
        Fixed R1 layout matching the approved reference:
        Demand → Wind → Supply → Price → Green Industry → Demand.
        """
        return f"""
        <div class="r1-frame">
            <svg viewBox="0 0 900 430"
                 role="img"
                 aria-label="R1 Green Industrial Expansion reinforcing loop"
                 preserveAspectRatio="xMidYMid meet">
                <defs>
                    <marker id="r1-green-arrow" markerWidth="9" markerHeight="9"
                            refX="8" refY="4.5" orient="auto"
                            markerUnits="strokeWidth">
                        <path d="M 0 0 L 9 4.5 L 0 9 z" fill="#16A34A"></path>
                    </marker>
                    <marker id="r1-red-arrow" markerWidth="9" markerHeight="9"
                            refX="8" refY="4.5" orient="auto"
                            markerUnits="strokeWidth">
                        <path d="M 0 0 L 9 4.5 L 0 9 z" fill="#E53935"></path>
                    </marker>
                    <filter id="r1-soft-shadow" x="-20%" y="-20%" width="140%" height="140%">
                        <feDropShadow dx="0" dy="3" stdDeviation="3"
                                      flood-color="#17384C" flood-opacity="0.10"/>
                    </filter>
                </defs>

                <!-- Curved loop connections -->
                <path d="M 235 145
                         C 285 70, 345 58, 390 62"
                      fill="none" stroke="#16A34A" stroke-width="3.2"
                      stroke-linecap="round"
                      marker-end="url(#r1-green-arrow)"></path>

                <path d="M 510 62
                         C 595 60, 650 78, 700 145"
                      fill="none" stroke="#16A34A" stroke-width="3.2"
                      stroke-linecap="round"
                      marker-end="url(#r1-green-arrow)"></path>

                <path d="M 755 196
                         C 780 245, 770 282, 730 320"
                      fill="none" stroke="#E53935" stroke-width="3.2"
                      stroke-linecap="round"
                      marker-end="url(#r1-red-arrow)"></path>

                <path d="M 635 348
                         C 555 382, 430 382, 350 348"
                      fill="none" stroke="#E53935" stroke-width="3.2"
                      stroke-linecap="round"
                      marker-end="url(#r1-red-arrow)"></path>

                <path d="M 250 320
                         C 188 286, 164 238, 182 195"
                      fill="none" stroke="#16A34A" stroke-width="3.2"
                      stroke-linecap="round"
                      marker-end="url(#r1-green-arrow)"></path>

                <!-- Polarity markers -->
                <g transform="translate(300,86)">
                    <circle r="15" fill="#FFFFFF" stroke="#16A34A" stroke-width="2"></circle>
                    <text text-anchor="middle" dominant-baseline="central"
                          font-family="Inter, Arial, sans-serif"
                          font-size="18" font-weight="750" fill="#16A34A">+</text>
                </g>

                <g transform="translate(625,86)">
                    <circle r="15" fill="#FFFFFF" stroke="#16A34A" stroke-width="2"></circle>
                    <text text-anchor="middle" dominant-baseline="central"
                          font-family="Inter, Arial, sans-serif"
                          font-size="18" font-weight="750" fill="#16A34A">+</text>
                </g>

                <g transform="translate(770,258)">
                    <circle r="15" fill="#FFFFFF" stroke="#E53935" stroke-width="2"></circle>
                    <text text-anchor="middle" dominant-baseline="central"
                          font-family="Inter, Arial, sans-serif"
                          font-size="18" font-weight="750" fill="#E53935">−</text>
                </g>

                <g transform="translate(490,380)">
                    <circle r="15" fill="#FFFFFF" stroke="#E53935" stroke-width="2"></circle>
                    <text text-anchor="middle" dominant-baseline="central"
                          font-family="Inter, Arial, sans-serif"
                          font-size="18" font-weight="750" fill="#E53935">−</text>
                </g>

                <g transform="translate(168,258)">
                    <circle r="15" fill="#FFFFFF" stroke="#16A34A" stroke-width="2"></circle>
                    <text text-anchor="middle" dominant-baseline="central"
                          font-family="Inter, Arial, sans-serif"
                          font-size="18" font-weight="750" fill="#16A34A">+</text>
                </g>

                <!-- Centre badge -->
                <g filter="url(#r1-soft-shadow)">
                    <circle cx="450" cy="220" r="54"
                            fill="#ECFDF5" stroke="#1F7A5A" stroke-width="2.4"></circle>
                    <text x="450" y="212" text-anchor="middle"
                          font-family="Inter, Arial, sans-serif"
                          font-size="30" font-weight="750" fill="#1F7A5A">R</text>
                    <text x="450" y="238" text-anchor="middle"
                          font-family="Inter, Arial, sans-serif"
                          font-size="10" font-weight="750"
                          letter-spacing="1.2" fill="#1F7A5A">REINFORCING</text>
                </g>

                <!-- Nodes -->
                <g filter="url(#r1-soft-shadow)">
                    <rect x="70" y="130" width="170" height="64" rx="18"
                          fill="#FFFFFF" stroke="#E12D2D" stroke-width="2.8"></rect>
                    <text x="155" y="168" text-anchor="middle"
                          font-family="Inter, Arial, sans-serif"
                          font-size="16" font-weight="700" fill="#17384C">📈 Demand</text>
                </g>

                <g filter="url(#r1-soft-shadow)">
                    <rect x="390" y="32" width="160" height="64" rx="18"
                          fill="#FFFFFF" stroke="#2CA02C" stroke-width="2.8"></rect>
                    <text x="470" y="70" text-anchor="middle"
                          font-family="Inter, Arial, sans-serif"
                          font-size="16" font-weight="700" fill="#17384C">🌬️ Wind</text>
                </g>

                <g filter="url(#r1-soft-shadow)">
                    <rect x="700" y="130" width="170" height="64" rx="18"
                          fill="#FFFFFF" stroke="#2478B8" stroke-width="2.8"></rect>
                    <text x="785" y="168" text-anchor="middle"
                          font-family="Inter, Arial, sans-serif"
                          font-size="16" font-weight="700" fill="#17384C">⚡ Supply</text>
                </g>

                <g filter="url(#r1-soft-shadow)">
                    <rect x="635" y="320" width="170" height="64" rx="18"
                          fill="#FFFFFF" stroke="#FF7F0E" stroke-width="2.8"></rect>
                    <text x="720" y="358" text-anchor="middle"
                          font-family="Inter, Arial, sans-serif"
                          font-size="16" font-weight="700" fill="#17384C">💲 Price</text>
                </g>

                <g filter="url(#r1-soft-shadow)">
                    <rect x="180" y="320" width="190" height="64" rx="18"
                          fill="#FFFFFF" stroke="#2CA02C" stroke-width="2.8"></rect>
                    <text x="275" y="348" text-anchor="middle"
                          font-family="Inter, Arial, sans-serif"
                          font-size="15" font-weight="700" fill="#17384C">🏭 Green Industry</text>
                </g>

                <!-- Compact legend -->
                <g transform="translate(330,412)">
                    <circle cx="0" cy="0" r="10" fill="#FFFFFF"
                            stroke="#16A34A" stroke-width="1.8"></circle>
                    <text x="0" y="1" text-anchor="middle" dominant-baseline="central"
                          font-family="Inter, Arial, sans-serif"
                          font-size="12" font-weight="750" fill="#16A34A">+</text>
                    <text x="17" y="4"
                          font-family="Inter, Arial, sans-serif"
                          font-size="11.5" fill="#526B7A">Positive relationship</text>

                    <circle cx="210" cy="0" r="10" fill="#FFFFFF"
                            stroke="#E53935" stroke-width="1.8"></circle>
                    <text x="210" y="1" text-anchor="middle" dominant-baseline="central"
                          font-family="Inter, Arial, sans-serif"
                          font-size="12" font-weight="750" fill="#E53935">−</text>
                    <text x="227" y="4"
                          font-family="Inter, Arial, sans-serif"
                          font-size="11.5" fill="#526B7A">Negative relationship</text>
                </g>
            </svg>
        </div>

        <style>
            html, body {{
                margin: 0;
                padding: 0;
                overflow: hidden;
                background: transparent;
                font-family: Inter, Arial, sans-serif;
            }}

            .r1-frame {{
                width: 100%;
                height: {height}px;
                box-sizing: border-box;
                border: 1px solid #E2E8F0;
                border-radius: 14px;
                background: #FBFDFE;
                padding: 2px 6px;
            }}

            .r1-frame svg {{
                width: 100%;
                height: 100%;
                display: block;
            }}
        </style>
        """

    # ===== LOOP 1: R1 — Green Industrial Expansion =====
    with subtab_loop1:
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1px;">
            <h4 style="margin: 0; color: #0A1628; font-size: 1rem;">R1 — Green Industrial Expansion</h4>
            <span style="background: #dcfce7; padding: 2px 10px; border-radius: 12px; font-size: 0.6rem; color: #166534; font-weight: 600; border: 1px solid #bbf7d0;">🔄 REINFORCING · OPPORTUNITY</span>
        </div>
        <p style="margin: 0 0 5px 0; color: #4A6A8A; font-size: 0.75rem; line-height: 1.24;">Wind deployment can expand power availability and support conditions for green industrial growth.</p>
        """, unsafe_allow_html=True)
        
        diagram_col, insight_col = st.columns([1.65, 1], gap="medium")
        
        with diagram_col:
            nodes_data = [
                {'id': 'Wind', 'label': '🌬️ Wind', 'color': '#2ca02c', 'size': 30, 'title': 'Wind Development Multiplier'},
                {'id': 'Supply', 'label': '⚡ Supply', 'color': '#1f77b4', 'size': 26, 'title': 'Electricity Supply'},
                {'id': 'Price', 'label': '💲 Price', 'color': '#ff7f0e', 'size': 26, 'title': 'Electricity Price'},
                {'id': 'GreenIndustry', 'label': '🏭 Green Industry', 'color': '#2ca02c', 'size': 30, 'title': 'Green Industrial Growth'},
                {'id': 'Demand', 'label': '📈 Demand', 'color': '#d62728', 'size': 26, 'title': 'Electricity Demand'}
            ]
            edges_data = [
                {'source': 'Wind', 'target': 'Supply', 'label': '+', 'color': '#22C55E', 'title': 'More wind → More supply'},
                {'source': 'Supply', 'target': 'Price', 'label': '-', 'color': '#E74C3C', 'title': 'More supply → Lower prices'},
                {'source': 'Price', 'target': 'GreenIndustry', 'label': '-', 'color': '#E74C3C', 'title': 'Higher prices → Less green industry'},
                {'source': 'GreenIndustry', 'target': 'Demand', 'label': '+', 'color': '#22C55E', 'title': 'More green industry → More demand'},
                {'source': 'Demand', 'target': 'Wind', 'label': '+', 'color': '#22C55E', 'title': 'More demand → More wind investment'}
            ]
            html_content = create_r1_reference_diagram(height=310)
            components.html(html_content, height=320)
            st.markdown("""
            <div style="margin-top: 4px;">
                <span style="font-size: 0.6rem; color: #6A8AAA; background: #f0f4f8; padding: 2px 8px; border-radius: 10px;">DNV signal · Wind is the only scalable near-term option</span>
            </div>
            """, unsafe_allow_html=True)
        
        with insight_col:
            st.markdown("""
            <div style="background: #f8fafc; border-radius: 8px; padding: 10px 12px; border: 1px solid #e6edf1; margin-bottom: 7px;">
                <div style="font-size: 0.59rem; color: #6A8AAA; font-weight: 700; letter-spacing: 0.35px;">LOOP LOGIC</div>
                <div style="font-size: 0.73rem; line-height: 1.48; color: #0A1628; margin-top: 2px;">
                    Wind ↑ → Supply availability ↑ → Power-market pressure ↓ → Conditions for green industry improve → Demand ↑ → Incentive for new supply ↑
                </div>
            </div>

            <div style="background: #F0FDF4; border-radius: 8px; padding: 9px 12px; border-left: 3px solid #16A34A; margin-bottom: 7px;">
                <div style="font-size: 0.59rem; color: #16A34A; font-weight: 700; letter-spacing: 0.35px;">KEY INSIGHT</div>
                <div style="font-size: 0.73rem; line-height: 1.42; color: #0A1628; margin-top: 2px;">
                    A reinforcing dynamic is possible when new supply, grid capacity and credible industrial demand develop together.
                </div>
            </div>

            <div style="background: #EEF5F8; border-radius: 8px; padding: 9px 12px; border-left: 3px solid #2E86AB;">
                <div style="font-size: 0.59rem; color: #2E6F95; font-weight: 700; letter-spacing: 0.35px;">STRATEGIC QUESTION</div>
                <div style="font-size: 0.73rem; line-height: 1.42; color: #0A1628; margin-top: 2px;">
                    How can Norway coordinate permitting, grid development and industrial demand so that temporary power scarcity does not delay investment?
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # ===== LOOP 2: B1 — Policy Implementation Friction =====
    with subtab_loop2:
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1px;">
            <h4 style="margin: 0; color: #0A1628; font-size: 1rem;">B1 — Policy Implementation Friction</h4>
            <span style="background: #fef9e7; padding: 2px 10px; border-radius: 12px; font-size: 0.6rem; color: #92400e; font-weight: 600; border: 1px solid #fdf2d0;">⚖️ BALANCING · POLICY FRICTION</span>
        </div>
        <p style="margin: 0 0 5px 0; color: #4A6A8A; font-size: 0.75rem; line-height: 1.24;">Climate-policy implementation can slow when perceived competitiveness, affordability or distributional costs intensify political resistance.</p>
        """, unsafe_allow_html=True)
        
        diagram_col, insight_col = st.columns([1.65, 1], gap="medium")
        
        with diagram_col:
            nodes_data = [
                {'id': 'PolicyStringency', 'label': '📜 Policy Stringency', 'color': '#ff7f0e', 'size': 30, 'title': 'Effective Climate-Policy Stringency'},
                {'id': 'AdjustmentPressure', 'label': '🏭 Adjustment Pressure', 'color': '#d62728', 'size': 26, 'title': 'Perceived Competitiveness, Affordability & Adjustment Pressure'},
                {'id': 'PoliticalResistance', 'label': '📢 Political Resistance', 'color': '#9467bd', 'size': 26, 'title': 'Political Resistance & Competitiveness Concerns'},
                {'id': 'ImplementationDelay', 'label': '⏳ Implementation Delay', 'color': '#8c564b', 'size': 26, 'title': 'Delay, Flexibility or Moderation in Policy Implementation'}
            ]
            edges_data = [
                {'source': 'PolicyStringency', 'target': 'AdjustmentPressure', 'label': '+', 'color': '#22C55E', 'title': 'Stronger policy → More near-term adjustment pressure, all else equal'},
                {'source': 'AdjustmentPressure', 'target': 'PoliticalResistance', 'label': '+', 'color': '#22C55E', 'title': 'More perceived adjustment pressure → More political resistance'},
                {'source': 'PoliticalResistance', 'target': 'ImplementationDelay', 'label': '+', 'color': '#22C55E', 'title': 'More resistance → More delay, flexibility or moderation'},
                {'source': 'ImplementationDelay', 'target': 'PolicyStringency', 'label': '-', 'color': '#E74C3C', 'title': 'More implementation delay → Lower effective policy stringency'}
            ]
            html_content = create_causal_loop_diagram(nodes_data, edges_data, height=310)
            components.html(html_content, height=320)
            st.markdown("""
            <div style="margin-top: 4px;">
                <span style="font-size: 0.6rem; color: #6A8AAA; background: #f0f4f8; padding: 2px 8px; border-radius: 10px;">DNV signal · Policy ambition only affects outcomes when backed by concrete measures and implementation</span>
            </div>
            """, unsafe_allow_html=True)
        
        with insight_col:
            st.markdown("""
            <div style="background: #f8fafc; border-radius: 8px; padding: 10px 12px; border: 1px solid #e6edf1; margin-bottom: 7px;">
                <div style="font-size: 0.59rem; color: #6A8AAA; font-weight: 700; letter-spacing: 0.35px;">LOOP LOGIC</div>
                <div style="font-size: 0.73rem; line-height: 1.48; color: #0A1628; margin-top: 2px;">
                    Policy stringency ↑ → Adjustment pressure ↑ → Political resistance ↑ → Implementation delay/flexibility ↑ → Effective policy stringency ↓
                </div>
            </div>

            <div style="background: #FFFBEB; border-radius: 8px; padding: 9px 12px; border-left: 3px solid #B7791F; margin-bottom: 7px;">
                <div style="font-size: 0.59rem; color: #B7791F; font-weight: 700; letter-spacing: 0.35px;">KEY INSIGHT</div>
                <div style="font-size: 0.73rem; line-height: 1.42; color: #0A1628; margin-top: 2px;">
                    Competitiveness and affordability concerns can slow or soften implementation, reducing the effective strength of policy signals.
                </div>
            </div>

            <div style="background: #EEF5F8; border-radius: 8px; padding: 9px 12px; border-left: 3px solid #2E86AB;">
                <div style="font-size: 0.59rem; color: #2E6F95; font-weight: 700; letter-spacing: 0.35px;">STRATEGIC QUESTION</div>
                <div style="font-size: 0.73rem; line-height: 1.42; color: #0A1628; margin-top: 2px;">
                    How can Norway maintain credible climate-policy implementation while managing competitiveness, affordability and carbon-leakage concerns?
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # ===== LOOP 3: R2 — Energy-Security Lock-in =====
    with subtab_loop3:
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1px;">
            <h4 style="margin: 0; color: #0A1628; font-size: 1rem;">R2 — Energy-Security Lock-in</h4>
            <span style="background: #fef2f2; padding: 2px 10px; border-radius: 12px; font-size: 0.6rem; color: #991b1b; font-weight: 600; border: 1px solid #fde8e8;">🔄 REINFORCING · LOCK-IN RISK</span>
        </div>
        <p style="margin: 0 0 5px 0; color: #4A6A8A; font-size: 0.75rem; line-height: 1.24;">Geopolitical shocks can strengthen the perceived security value of Norwegian gas and reinforce attention to the fossil export sector.</p>
        """, unsafe_allow_html=True)
        
        diagram_col, insight_col = st.columns([1.65, 1], gap="medium")
        
        with diagram_col:
            nodes_data = [
                {'id': 'SecurityDemand', 'label': '🛡️ Security Demand', 'color': '#d62728', 'size': 30, 'title': 'European Security-Driven Demand for Norwegian Gas'},
                {'id': 'GasRevenues', 'label': '💰 Gas Revenues', 'color': '#ff7f0e', 'size': 26, 'title': 'Norwegian Gas Revenues'},
                {'id': 'FossilAttention', 'label': '🏗️ Fossil Attention', 'color': '#8c564b', 'size': 26, 'title': 'Capital, Talent & Political Attention to the Gas Sector'},
                {'id': 'SupplyCommitment', 'label': '🔗 Supply Commitment', 'color': '#d62728', 'size': 30, 'title': 'Commitment to Maintain Norwegian Gas Supply Capacity'}
            ]
            edges_data = [
                {'source': 'SecurityDemand', 'target': 'GasRevenues', 'label': '+', 'color': '#22C55E', 'title': 'More security-driven demand → Higher gas revenues'},
                {'source': 'GasRevenues', 'target': 'FossilAttention', 'label': '+', 'color': '#22C55E', 'title': 'Higher revenues → More capital, talent and political attention'},
                {'source': 'FossilAttention', 'target': 'SupplyCommitment', 'label': '+', 'color': '#22C55E', 'title': 'More sector attention → Stronger commitment to maintain gas supply capacity'},
                {'source': 'SupplyCommitment', 'target': 'SecurityDemand', 'label': '+', 'color': '#22C55E', 'title': 'Greater reliable supply commitment → Stronger perceived security value and continued demand'}
            ]
            html_content = create_causal_loop_diagram(nodes_data, edges_data, height=310)
            components.html(html_content, height=320)
            st.markdown("""
            <div style="margin-top: 4px;">
                <span style="font-size: 0.6rem; color: #6A8AAA; background: #f0f4f8; padding: 2px 8px; border-radius: 10px;">DNV signal · Europe's security concerns lock in capital and talent</span>
            </div>
            """, unsafe_allow_html=True)
        
        with insight_col:
            st.markdown("""
            <div style="background: #f8fafc; border-radius: 8px; padding: 10px 12px; border: 1px solid #e6edf1; margin-bottom: 7px;">
                <div style="font-size: 0.59rem; color: #6A8AAA; font-weight: 700; letter-spacing: 0.35px;">LOOP LOGIC</div>
                <div style="font-size: 0.73rem; line-height: 1.48; color: #0A1628; margin-top: 2px;">
                    Security-driven gas demand ↑ → Gas revenues ↑ → Fossil-sector attention ↑ → Supply commitment ↑ → Perceived security value and demand ↑
                </div>
            </div>

            <div style="background: #FEF2F2; border-radius: 8px; padding: 9px 12px; border-left: 3px solid #DC2626; margin-bottom: 7px;">
                <div style="font-size: 0.59rem; color: #DC2626; font-weight: 700; letter-spacing: 0.35px;">KEY INSIGHT</div>
                <div style="font-size: 0.73rem; line-height: 1.42; color: #0A1628; margin-top: 2px;">
                    Energy-security shocks can reinforce capital, talent and political attention around the gas sector, creating a risk of longer-lived lock-in.
                </div>
            </div>

            <div style="background: #EEF5F8; border-radius: 8px; padding: 9px 12px; border-left: 3px solid #2E86AB;">
                <div style="font-size: 0.59rem; color: #2E6F95; font-weight: 700; letter-spacing: 0.35px;">STRATEGIC QUESTION</div>
                <div style="font-size: 0.73rem; line-height: 1.42; color: #0A1628; margin-top: 2px;">
                    How can Norway preserve security leverage without extending fossil dependence?
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # ===== LOOP 4: R3 — Fossil-Sector Resource Lock-in =====
    with subtab_loop4:
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1px;">
            <h4 style="margin: 0; color: #0A1628; font-size: 1rem;">R3 — Fossil-Sector Resource Lock-in</h4>
            <span style="background: #fef2f2; padding: 2px 10px; border-radius: 12px; font-size: 0.6rem; color: #991b1b; font-weight: 600; border: 1px solid #fde8e8;">🔄 REINFORCING · RESOURCE TRAP</span>
        </div>
        <p style="margin: 0 0 5px 0; color: #4A6A8A; font-size: 0.75rem; line-height: 1.24;">High fossil-sector returns can attract scarce capital and skills, slowing the build-out of competing transition activities.</p>
        """, unsafe_allow_html=True)
        
        diagram_col, insight_col = st.columns([1.65, 1], gap="medium")
        
        with diagram_col:
            nodes_data = [
                {'id': 'OilGasProfitability', 'label': '💰 Fossil Returns', 'color': '#ff7f0e', 'size': 30, 'title': 'Relative Returns in Oil & Gas'},
                {'id': 'TalentAttraction', 'label': '🧑‍🔬 Talent Attraction', 'color': '#2ca02c', 'size': 26, 'title': 'Talent & Capital Attraction to Petroleum'},
                {'id': 'GreenResourceScarcity', 'label': '📉 Green Scarcity', 'color': '#d62728', 'size': 26, 'title': 'Green-Sector Resource Scarcity'},
                {'id': 'FossilDominance', 'label': '🧲 Fossil Dominance', 'color': '#9467bd', 'size': 26, 'title': 'Persistence of Fossil-Sector Investment and Capability Dominance'}
            ]
            edges_data = [
                {'source': 'OilGasProfitability', 'target': 'TalentAttraction', 'label': '+', 'color': '#22C55E', 'title': 'Higher profitability → More talent attraction to petroleum'},
                {'source': 'TalentAttraction', 'target': 'GreenResourceScarcity', 'label': '+', 'color': '#22C55E', 'title': 'More attraction → Less resources for green transition'},
                {'source': 'GreenResourceScarcity', 'target': 'FossilDominance', 'label': '+', 'color': '#22C55E', 'title': 'Greater green-sector scarcity → Slower competing transition build-out and more persistent fossil-sector dominance'},
                {'source': 'FossilDominance', 'target': 'OilGasProfitability', 'label': '+', 'color': '#22C55E', 'title': 'More persistent fossil-sector dominance → Greater relative attractiveness of continued fossil investment'}
            ]
            html_content = create_causal_loop_diagram(nodes_data, edges_data, height=310)
            components.html(html_content, height=320)
            st.markdown("""
            <div style="margin-top: 4px;">
                <span style="font-size: 0.6rem; color: #6A8AAA; background: #f0f4f8; padding: 2px 8px; border-radius: 10px;">DNV signal · Oil and gas absorb capital and skilled labour that could support renewable energy, electrification and grids</span>
            </div>
            """, unsafe_allow_html=True)
        
        with insight_col:
            st.markdown("""
            <div style="background: #f8fafc; border-radius: 8px; padding: 10px 12px; border: 1px solid #e6edf1; margin-bottom: 7px;">
                <div style="font-size: 0.59rem; color: #6A8AAA; font-weight: 700; letter-spacing: 0.35px;">LOOP LOGIC</div>
                <div style="font-size: 0.73rem; line-height: 1.48; color: #0A1628; margin-top: 2px;">
                    Fossil returns ↑ → Talent/capital attraction ↑ → Green-sector scarcity ↑ → Fossil-sector dominance persists ↑ → Relative attractiveness of fossil investment ↑
                </div>
            </div>

            <div style="background: #F5F3FF; border-radius: 8px; padding: 9px 12px; border-left: 3px solid #7C3AED; margin-bottom: 7px;">
                <div style="font-size: 0.59rem; color: #7C3AED; font-weight: 700; letter-spacing: 0.35px;">KEY INSIGHT</div>
                <div style="font-size: 0.73rem; line-height: 1.42; color: #0A1628; margin-top: 2px;">
                    High fossil-sector returns can crowd out scarce skills and capital, reinforcing the sector's relative investment advantage.
                </div>
            </div>

            <div style="background: #EEF5F8; border-radius: 8px; padding: 9px 12px; border-left: 3px solid #2E86AB;">
                <div style="font-size: 0.59rem; color: #2E6F95; font-weight: 700; letter-spacing: 0.35px;">STRATEGIC QUESTION</div>
                <div style="font-size: 0.73rem; line-height: 1.42; color: #0A1628; margin-top: 2px;">
                    How can scarce capabilities be redirected without weakening current energy security?
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # ===== SUMMARY TAB — STRATEGIC INTERPRETATION =====
    with subtab_summary:
        st.markdown(
            '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">'
            '<div>'
            '<h4 style="margin:0; color:#0A1628; font-size:1.02rem;">📋 Strategic Interpretation</h4>'
            '<p style="margin:2px 0 0 0; color:#4A6A8A; font-size:0.72rem;">'
            'The pathways describe possible futures; these qualitative feedback hypotheses help explore mechanisms that may contribute to them.'
            '</p>'
            '</div>'
            '<span style="background:#EEF5F8; padding:3px 10px; border-radius:12px; '
            'font-size:0.57rem; color:#2E6F95; font-weight:700; border:1px solid #DCE9EF;">'
            'QUALITATIVE SYSTEMS VIEW'
            '</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div style="display:grid; grid-template-columns:repeat(3, minmax(0,1fr)); gap:9px;">'

            '<div style="background:#FFFFFF; border:1px solid #E3EBEF; border-radius:10px; '
            'padding:11px 12px; min-height:126px;">'
            '<div style="display:flex; align-items:center; gap:6px;">'
            '<span style="font-size:1rem;">🔗</span>'
            '<span style="font-size:0.60rem; color:#2E6F95; font-weight:750; letter-spacing:0.35px;">'
            'SYSTEM PERSPECTIVE'
            '</span>'
            '</div>'
            '<div style="font-size:0.75rem; line-height:1.40; color:#0A1628; margin-top:6px; font-weight:600;">'
            'Energy security, competitiveness and decarbonization are connected—not separate policy domains.'
            '</div>'
            '<div style="margin-top:8px; padding-top:7px; border-top:1px solid #EDF2F5; '
            'font-size:0.66rem; line-height:1.35; color:#526B7A;">'
            '<b>Decision lens:</b> How do today\'s actions reshape tomorrow\'s feedbacks?'
            '</div>'
            '</div>'

            '<div style="background:#FFFFFF; border:1px solid #E3EBEF; border-radius:10px; '
            'padding:11px 12px; min-height:126px;">'
            '<div style="display:flex; align-items:center; gap:6px;">'
            '<span style="font-size:1rem;">⏱️</span>'
            '<span style="font-size:0.60rem; color:#B45309; font-weight:750; letter-spacing:0.35px;">'
            'TRANSITION DYNAMICS'
            '</span>'
            '</div>'
            '<div style="font-size:0.75rem; line-height:1.40; color:#0A1628; margin-top:6px; font-weight:600;">'
            'Feedbacks can operate at different speeds; infrastructure, permitting and skills can introduce important delays.'
            '</div>'
            '<div style="margin-top:8px; padding-top:7px; border-top:1px solid #EDF2F5; '
            'font-size:0.66rem; line-height:1.35; color:#526B7A;">'
            '<b>Decision lens:</b> Which delays deserve the earliest attention?'
            '</div>'
            '</div>'

            '<div style="background:#FFFFFF; border:1px solid #E3EBEF; border-radius:10px; '
            'padding:11px 12px; min-height:126px;">'
            '<div style="display:flex; align-items:center; gap:6px;">'
            '<span style="font-size:1rem;">🧩</span>'
            '<span style="font-size:0.60rem; color:#15803D; font-weight:750; letter-spacing:0.35px;">'
            'POLICY COORDINATION'
            '</span>'
            '</div>'
            '<div style="font-size:0.75rem; line-height:1.40; color:#0A1628; margin-top:6px; font-weight:600;">'
            'Single measures can shift pressure elsewhere; coordinated packages can reduce unintended consequences.'
            '</div>'
            '<div style="margin-top:8px; padding-top:7px; border-top:1px solid #EDF2F5; '
            'font-size:0.66rem; line-height:1.35; color:#526B7A;">'
            '<b>Decision lens:</b> How can policies reinforce rather than offset one another?'
            '</div>'
            '</div>'

            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div style="margin-top:9px; background:#ECFDF5; border:1px solid #CDEEDF; '
            'border-radius:10px; padding:10px 13px; display:flex; align-items:flex-start; gap:9px;">'
            '<span style="font-size:1.05rem;">💡</span>'
            '<div>'
            '<div style="font-size:0.59rem; color:#157A55; font-weight:750; letter-spacing:0.35px;">'
            'SYSTEMS-THINKING TAKEAWAY'
            '</div>'
            '<div style="font-size:0.74rem; line-height:1.42; color:#123D32; margin-top:3px;">'
            'The loop perspective does not identify a single best pathway; it highlights interactions, delays '
            'and unintended consequences that merit closer attention.'
            '</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div style="margin-top:7px; padding:7px 12px; background:#F5F8FA; border-radius:8px; '
            'border:1px solid #E4EBEF; text-align:center;">'
            '<span style="font-size:0.67rem; color:#526B7A;">'
            '<b>From scenarios to systems:</b> this dashboard complements the DNV outlook with a qualitative '
            'author-developed interpretation of feedbacks linking energy security, industrial competitiveness and decarbonization.'
            '</span>'
            '</div>',
            unsafe_allow_html=True,
        )
# ============================================================================
# TAB 4: Interactive Decision Support
# ============================================================================

# External conditions are assumptions Norway must prepare for.
POLICY_EXTERNAL_SCENARIOS = {
    "Reference conditions": {
        "sanctions_slider": 0.78,
        "eu_slider": "moderate",
        "oil_slider": 75,
        "datacentre_slider": 1.0,
    },
    "High geopolitical stress": {
        "sanctions_slider": 1.15,
        "eu_slider": "slow",
        "oil_slider": 140,
        "datacentre_slider": 1.10,
    },
    "Rapid EU transition": {
        "sanctions_slider": 0.78,
        "eu_slider": "fast",
        "oil_slider": 60,
        "datacentre_slider": 1.0,
    },
    "High oil-price environment": {
        "sanctions_slider": 0.85,
        "eu_slider": "moderate",
        "oil_slider": 120,
        "datacentre_slider": 0.95,
    },
}

# Policy packages contain levers Norway can influence directly.
POLICY_RESPONSE_PACKAGES = {
    "Reference policy": {
        "wind_slider": 1.0,
        "carbon_slider": 1.0,
        "grid_slider": "medium",
    },
    "Green acceleration": {
        "wind_slider": 1.8,
        "carbon_slider": 1.5,
        "grid_slider": "high",
    },
    "Grid-first transition": {
        "wind_slider": 1.30,
        "carbon_slider": 1.10,
        "grid_slider": "high",
    },
    "Power-security response": {
        "wind_slider": 1.25,
        "carbon_slider": 0.95,
        "grid_slider": "high",
    },
}


def initialise_policy_lab_state():
    """Initialise Policy Lab controls before widgets are rendered."""
    defaults = {
        "policy_selected_external": "Reference conditions",
        "policy_selected_package": "Reference policy",
        "sanctions_slider": 0.78,
        "eu_slider": "moderate",
        "oil_slider": 75,
        "datacentre_slider": 1.0,
        "wind_slider": 1.0,
        "carbon_slider": 1.0,
        "grid_slider": "medium",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def apply_policy_external_scenario():
    """Apply only external assumptions; policy settings remain unchanged."""
    selected = st.session_state["policy_selected_external"]
    for key, value in POLICY_EXTERNAL_SCENARIOS[selected].items():
        st.session_state[key] = value


def apply_policy_response_package():
    """Apply only policy-response settings; external assumptions remain unchanged."""
    selected = st.session_state["policy_selected_package"]
    for key, value in POLICY_RESPONSE_PACKAGES[selected].items():
        st.session_state[key] = value


def reset_policy_decision_lab():
    """Reset both selectors and all controls to the reference pathway."""
    st.session_state["policy_selected_external"] = "Reference conditions"
    st.session_state["policy_selected_package"] = "Reference policy"

    for key, value in POLICY_EXTERNAL_SCENARIOS["Reference conditions"].items():
        st.session_state[key] = value

    for key, value in POLICY_RESPONSE_PACKAGES["Reference policy"].items():
        st.session_state[key] = value


def policy_values_match(current_values, preset_values, tolerance=1e-9):
    """Return True when current widget values still match a selected preset."""
    for key, expected in preset_values.items():
        current = current_values.get(key)
        if isinstance(expected, float):
            if current is None or abs(float(current) - expected) > tolerance:
                return False
        elif current != expected:
            return False
    return True


with tab_policy:
    initialise_policy_lab_state()

    # Compact layout for the left control rail
    st.markdown("""
    <div class="dashboard-tab-header">
        <h4>Interactive Decision Support</h4>
        <p>Combine an external environment with a Norwegian policy response, then compare the resulting pathway with the DNV reference case. Use the presets as starting points and fine-tune the assumptions in the control panel.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
        .policy-lab-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 18px;
            margin: 0 0 10px 0;
            padding: 13px 16px;
            border: 1px solid #e1e8ed;
            border-radius: 12px;
            background: linear-gradient(135deg, #f8fafc 0%, #f2f7fa 100%);
        }
        .policy-lab-title {
            margin: 0;
            color: #0A1628;
            font-size: 1.35rem;
            font-weight: 750;
            line-height: 1.2;
        }
        .policy-lab-subtitle {
            margin-top: 4px;
            color: #58758a;
            font-size: 0.79rem;
            line-height: 1.45;
        }
        .policy-lab-badge {
            flex: 0 0 auto;
            padding: 5px 9px;
            border: 1px solid #d8e5eb;
            border-radius: 999px;
            background: #ffffff;
            color: #4A6A8A;
            font-size: 0.58rem;
            font-weight: 700;
            white-space: nowrap;
        }
        .policy-selection-strip {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin: 4px 0 10px 0;
            padding: 8px 11px;
            border: 1px solid #e2e9ed;
            border-radius: 9px;
            background: #f8fafb;
        }
        .policy-selection-label {
            color: #7b8d98;
            font-size: 0.58rem;
            font-weight: 750;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }
        .policy-selection-value {
            margin-top: 2px;
            color: #28495b;
            font-size: 0.72rem;
            font-weight: 700;
        }
        .policy-section-kicker {
            margin: 6px 0 5px 0;
            color: #6A8AAA;
            font-size: 0.64rem;
            font-weight: 750;
            letter-spacing: 0.07em;
            text-transform: uppercase;
        }
        .policy-outlook-title {
            color: #17384d;
            font-size: 0.76rem;
            font-weight: 750;
            margin-bottom: 0;
            line-height: 1.15;
        }
        /* Compact only the Current policy outlook container. */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.policy-outlook-anchor) {
            padding-top: 0.25rem !important;
            padding-bottom: 0.20rem !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.policy-outlook-anchor)
        div[data-testid="stMetricLabel"] {
            font-size: 0.66rem !important;
            line-height: 1.15 !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.policy-outlook-anchor)
        div[data-testid="stMetricValue"] {
            font-size: 1.18rem !important;
            line-height: 1.08 !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.policy-outlook-anchor)
        div[data-testid="stMetricDelta"] {
            font-size: 0.64rem !important;
            line-height: 1.15 !important;
        }
        .policy-evidence-kicker {
            margin: -12px 0 0 0;
            color: #6A8AAA;
            font-size: 0.62rem;
            font-weight: 750;
            letter-spacing: 0.07em;
            text-transform: uppercase;
        }
        .policy-outlook-note {
            color: #748894;
            font-size: 0.67rem;
            line-height: 1.35;
        }
        .decision-summary {
            min-height: 248px;
            padding: 11px 13px;
            border: 1px solid #dfe8ec;
            border-radius: 11px;
            background: #f8fafb;
        }
        .decision-summary h4 {
            margin: 0 0 6px 0;
            color: #17384d;
            font-size: 0.90rem;
        }
        .decision-block {
            padding: 6px 0;
            border-bottom: 1px solid #e4eaee;
        }
        .decision-block:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }
        .decision-label {
            margin-bottom: 4px;
            color: #6A8AAA;
            font-size: 0.64rem;
            font-weight: 800;
            letter-spacing: 0.055em;
            text-transform: uppercase;
        }
        .decision-item {
            margin: 3px 0;
            color: #405d6e;
            font-size: 0.77rem;
            line-height: 1.40;
        }
        .policy-caption {
            margin-top: 7px;
            color: #8998a1;
            font-size: 0.59rem;
            line-height: 1.35;
            text-align: center;
        }

        /* Compact Scenario setup controls: External scenario, Policy package,
           and Reset to reference should read as controls, not headings. */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.policy-control-anchor)
        div[data-testid="stSelectbox"] label {
            font-size: 0.66rem !important;
            line-height: 1.20 !important;
            font-weight: 600 !important;
            margin-bottom: 2px !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.policy-control-anchor)
        div[data-testid="stSelectbox"] [data-baseweb="select"] {
            min-height: 34px !important;
            height: 34px !important;
            font-size: 0.69rem !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.policy-control-anchor)
        div[data-testid="stSelectbox"] [data-baseweb="select"] div {
            font-size: 0.69rem !important;
            line-height: 1.18 !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.policy-control-anchor)
        div[data-testid="stButton"] button {
            min-height: 32px !important;
            height: 32px !important;
            padding: 3px 9px !important;
            font-size: 0.66rem !important;
            line-height: 1.15 !important;
            font-weight: 600 !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.policy-control-anchor)
        span[data-testid="stIconMaterial"] {
            font-size: 0.95rem !important;
        }
        /* Keep headings clear of the first row of controls. */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.policy-control-title)
        > div > div[data-testid="stVerticalBlock"] {
            gap: 0.44rem !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.policy-control-subtitle)
        div[data-testid="stHorizontalBlock"] {
            margin-top: 2px !important;
        }

        @media (max-width: 800px) {
            .policy-lab-header,
            .policy-selection-strip {
                display: block;
            }
            .policy-lab-badge {
                display: inline-block;
                margin-top: 8px;
            }
            .policy-selection-strip > div + div {
                margin-top: 7px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Main two-column workspace:
    # left = compact controls, right = results and interpretation
    control_col, results_col = st.columns(
        [0.92, 2.08],
        gap="large",
        vertical_alignment="top"
    )

    # ------------------------------------------------------------------------
    # LEFT CONTROL RAIL
    # ------------------------------------------------------------------------
    with control_col:
        with st.container(border=True):
            st.markdown('<div class="policy-control-anchor"></div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="policy-control-title">Scenario setup</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                '<div class="policy-control-subtitle">Choose a preset, then adjust individual assumptions.</div>',
                unsafe_allow_html=True
            )

            st.selectbox(
                "External scenario",
                options=list(POLICY_EXTERNAL_SCENARIOS.keys()),
                key="policy_selected_external",
                on_change=apply_policy_external_scenario,
                help=(
                    "Conditions Norway must prepare for, such as geopolitical tension, "
                    "EU transition speed, oil prices and demand growth."
                )
            )

            st.selectbox(
                "Policy package",
                options=list(POLICY_RESPONSE_PACKAGES.keys()),
                key="policy_selected_package",
                on_change=apply_policy_response_package,
                help=(
                    "Responses Norway can influence directly, including wind deployment, "
                    "carbon policy and grid investment."
                )
            )

            st.button(
                "Reset to reference",
                width="stretch",
                key="policy_lab_reset_top",
                on_click=reset_policy_decision_lab
            )

        with st.container(border=True):
            st.markdown(
                '<div class="policy-control-title">External conditions</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                '<div class="policy-control-subtitle">What Norway must prepare for</div>',
                unsafe_allow_html=True
            )

            ext_left, ext_right = st.columns(2, gap="small")

            with ext_left:
                sanctions_val = st.slider(
                    "Geopolitical tension",
                    min_value=0.50,
                    max_value=1.20,
                    step=0.05,
                    key="sanctions_slider",
                    help="Higher tension increases export, price and system risk."
                )

                oil_p = st.slider(
                    "Oil and gas price",
                    min_value=50,
                    max_value=150,
                    step=5,
                    key="oil_slider",
                    help="Higher prices support revenues but may reinforce fossil lock-in."
                )

            with ext_right:
                eu_policy_val = st.select_slider(
                    "EU transition speed",
                    options=["slow", "moderate", "fast"],
                    key="eu_slider",
                    help="Faster EU transition reduces long-term demand for Norwegian gas."
                )

                datacentre_growth = st.slider(
                    "Data-centre growth",
                    min_value=0.50,
                    max_value=2.00,
                    step=0.05,
                    key="datacentre_slider",
                    help="Higher growth increases electricity demand and grid pressure."
                )

        with st.container(border=True):
            st.markdown(
                '<div class="policy-control-title">Policy responses</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                '<div class="policy-control-subtitle">What Norway can influence directly</div>',
                unsafe_allow_html=True
            )

            policy_left, policy_right = st.columns(2, gap="small")

            with policy_left:
                wind_mult = st.slider(
                    "Wind scale-up",
                    min_value=0.50,
                    max_value=2.00,
                    step=0.05,
                    key="wind_slider",
                    help="Faster wind deployment increases electricity supply."
                )

                grid_inv = st.select_slider(
                    "Grid capacity",
                    options=["low", "medium", "high"],
                    key="grid_slider",
                    help="Higher grid capacity supports renewable and demand integration."
                )

            with policy_right:
                carbon_mult = st.slider(
                    "Carbon-policy strength",
                    min_value=0.50,
                    max_value=2.00,
                    step=0.05,
                    key="carbon_slider",
                    help="A stronger carbon signal accelerates emissions reduction."
                )

                st.markdown(
                    """
                    <div style="
                        margin-top:12px;
                        padding:9px 10px;
                        border-radius:8px;
                        background:#eef5f8;
                        color:#58758a;
                        font-size:0.63rem;
                        line-height:1.4;">
                        Changes update the pathway and decision summary immediately.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # Values are available after the widgets are rendered.
    current_external_values = {
        "sanctions_slider": sanctions_val,
        "eu_slider": eu_policy_val,
        "oil_slider": oil_p,
        "datacentre_slider": datacentre_growth,
    }
    current_policy_values = {
        "wind_slider": wind_mult,
        "carbon_slider": carbon_mult,
        "grid_slider": grid_inv,
    }

    selected_external = st.session_state["policy_selected_external"]
    selected_package = st.session_state["policy_selected_package"]

    external_adjusted = not policy_values_match(
        current_external_values,
        POLICY_EXTERNAL_SCENARIOS[selected_external]
    )
    package_adjusted = not policy_values_match(
        current_policy_values,
        POLICY_RESPONSE_PACKAGES[selected_package]
    )

    external_display = selected_external + (" · adjusted" if external_adjusted else "")
    package_display = selected_package + (" · adjusted" if package_adjusted else "")

    # ------------------------------------------------------------------------
    # Simulation and reference case
    # ------------------------------------------------------------------------
    scenario_params = {
        "wind_mult": wind_mult,
        "carbon_mult": carbon_mult,
        "sanctions_val": sanctions_val,
        "eu_policy_val": eu_policy_val,
        "oil_p": oil_p,
        "grid_inv": grid_inv,
        "datacentre_growth": datacentre_growth,
    }

    simulated_data = get_dynamic_scenario_data(**scenario_params)
    base_data = get_dynamic_scenario_data(
        1.0, 1.0, 0.78, "moderate", 75, "medium", 1.0
    )

    years = list(simulated_data["year"])
    base_years = list(base_data["year"])

    idx_2040 = years.index(2040)
    idx_2050 = years.index(2050)
    idx_2060 = years.index(2060)

    base_idx_2040 = base_years.index(2040)
    base_idx_2050 = base_years.index(2050)
    base_idx_2060 = base_years.index(2060)

    deficit_year = simulated_data["deficit_year"]
    deficit_year_ref = base_data["deficit_year"]

    emissions_2050 = float(simulated_data["emissions"][idx_2050])
    emissions_2050_ref = float(base_data["emissions"][base_idx_2050])

    gas_2040 = float(simulated_data["gas_production"][idx_2040])
    gas_2040_ref = float(base_data["gas_production"][base_idx_2040])

    renewable_2060 = float(simulated_data["renewable_share"][idx_2060] * 100)
    renewable_2060_ref = float(base_data["renewable_share"][base_idx_2060] * 100)

    if deficit_year is None and deficit_year_ref is None:
        deficit_delta = "No change vs reference"
    elif deficit_year is None:
        deficit_delta = "Deficit avoided vs reference"
    elif deficit_year_ref is None:
        deficit_delta = "New deficit in this case"
    else:
        year_shift = deficit_year - deficit_year_ref
        if year_shift > 0:
            deficit_delta = f"{year_shift:+d} years vs reference"
        elif year_shift < 0:
            deficit_delta = f"{year_shift:d} years vs reference"
        else:
            deficit_delta = "Same as reference"

    emissions_delta = emissions_2050 - emissions_2050_ref
    gas_delta = gas_2040 - gas_2040_ref
    renewable_delta = renewable_2060 - renewable_2060_ref

    # ------------------------------------------------------------------------
    # Decision logic
    # ------------------------------------------------------------------------
    improvements = []
    tradeoffs = []
    actions = []

    if deficit_year is None or (
        deficit_year_ref is not None and deficit_year > deficit_year_ref
    ):
        improvements.append("Power-system stress is reduced or delayed.")
    elif deficit_year_ref is not None and deficit_year < deficit_year_ref:
        tradeoffs.append("The electricity deficit arrives earlier than in the reference case.")

    if emissions_delta < -0.2:
        improvements.append(f"2050 emissions fall by {abs(emissions_delta):.1f} MtCO₂e.")
    elif emissions_delta > 0.2:
        tradeoffs.append(f"2050 emissions rise by {emissions_delta:.1f} MtCO₂e.")

    if renewable_delta > 1.0:
        improvements.append(f"Wind generation share increases by {renewable_delta:.1f} percentage points.")
    elif renewable_delta < -1.0:
        tradeoffs.append(f"Wind generation share declines by {abs(renewable_delta):.1f} percentage points.")

    if gas_delta < -1.0:
        tradeoffs.append(f"2040 gas exports decline by {abs(gas_delta):.1f} MSm³oe/yr.")
    elif gas_delta > 1.0:
        tradeoffs.append("Higher gas exports may reinforce fossil-sector lock-in.")

    if wind_mult >= 1.30 and grid_inv != "high":
        actions.append("Align grid delivery with the faster wind build-out.")

    if datacentre_growth >= 1.25 and (
        deficit_year is not None and deficit_year <= (deficit_year_ref or 2033)
    ):
        actions.append("Sequence data-centre connections against available power capacity.")

    if emissions_delta >= -0.2:
        actions.append("Strengthen sector-specific decarbonization measures.")

    if oil_p >= 110 and wind_mult < 1.20:
        actions.append("Protect green-sector talent and capital from petroleum crowding-out.")

    if grid_inv == "low":
        actions.append("Raise grid investment capacity before adding new demand.")

    if not improvements:
        improvements.append("No material improvement over the reference pathway is visible.")
    if not tradeoffs:
        tradeoffs.append("No major modelled trade-off dominates this package.")
    if not actions:
        actions.append("Maintain implementation discipline and monitor emerging bottlenecks.")

    def _summary_items(items, limit=2):
        return "".join(
            f'<div class="decision-item">• {item}</div>'
            for item in items[:limit]
        )

    def style_evidence_chart(fig, yaxis_title):
        """Apply one compact, consistent visual style to evidence charts."""
        fig.update_layout(
            title=dict(text=""),
            height=228,
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.01,
                xanchor="left",
                x=0.0,
                font=dict(size=9, color="#29495b"),
                itemwidth=58,
                tracegroupgap=4
            ),
            margin=dict(l=46, r=12, t=29, b=34),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                title="",
                showgrid=False,
                fixedrange=True,
                tickfont=dict(size=9),
                linecolor="rgba(120,140,155,0.25)"
            ),
            yaxis=dict(
                title=yaxis_title,
                showgrid=True,
                gridcolor="rgba(120,140,155,0.14)",
                fixedrange=True,
                tickfont=dict(size=9),
                title_font=dict(size=10)
            ),
            font=dict(family="Inter, sans-serif", size=10)
        )
        return fig

    # ------------------------------------------------------------------------
    # RIGHT RESULTS WORKSPACE
    # ------------------------------------------------------------------------
    with results_col:
        with st.container(border=True):
            st.markdown('<div class="policy-outlook-anchor"></div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="policy-outlook-title">Current policy outlook</div>',
                unsafe_allow_html=True
            )

            kpi1, kpi2, kpi3, kpi4 = st.columns(4, gap="small")

            with kpi1:
                st.metric(
                    "Deficit year",
                    deficit_year if deficit_year else "No deficit",
                    delta=deficit_delta,
                    delta_color="normal"
                )

            with kpi2:
                st.metric(
                    "2050 emissions",
                    f"{emissions_2050:.1f} MtCO₂e",
                    delta=f"{emissions_delta:+.1f} Mt vs reference",
                    delta_color="inverse"
                )

            with kpi3:
                st.metric(
                    "2040 gas exports",
                    f"{gas_2040:.1f} MSm³oe/yr",
                    delta=f"{gas_delta:+.1f} MSm³oe/yr vs reference",
                    delta_color="off"
                )

            with kpi4:
                st.metric(
                    "2060 wind-generation share",
                    f"{renewable_2060:.0f}%",
                    delta=f"{renewable_delta:+.1f} pp vs reference",
                    delta_color="normal"
                )

        st.markdown(
            '<div class="policy-section-kicker">Power-system outlook</div>',
            unsafe_allow_html=True
        )

        chart_col, summary_col = st.columns([1.72, 1], gap="medium")

        with chart_col:
            fig_main = plot_supply_demand(
                simulated_data,
                show_uncertainty=False,
                show_baseline=True
            )

            # Short labels keep the horizontal legend on one compact row.
            policy_main_legend_names = {
                "Simulated Supply": "Policy supply",
                "Simulated Demand (incl. Data Centres)": "Policy demand",
                "Data Centre Demand": "Data centres",
                "DNV Reference Supply": "Reference supply",
                "DNV Reference Demand": "Reference demand",
            }
            for trace in fig_main.data:
                trace.name = policy_main_legend_names.get(trace.name, trace.name)

            fig_main.update_layout(
                title=dict(text=""),
                height=315,
                hovermode="x unified",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.01,
                    xanchor="left",
                    x=0.0,
                    font=dict(size=9),
                    itemwidth=55,
                    tracegroupgap=4
                ),
                margin=dict(l=46, r=12, t=27, b=31),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(
                    title="",
                    showgrid=False,
                    fixedrange=True,
                    tickfont=dict(size=9),
                    linecolor="rgba(120,140,155,0.25)"
                ),
                yaxis=dict(
                    title="TWh/yr",
                    showgrid=True,
                    gridcolor="rgba(120,140,155,0.14)",
                    fixedrange=True,
                    tickfont=dict(size=9),
                    title_font=dict(size=10)
                ),
                font=dict(family="Inter, sans-serif", size=10)
            )

            if deficit_year:
                fig_main.add_vline(
                    x=deficit_year,
                    line_dash="dash",
                    line_width=1.2,
                    line_color="#C6534C"
                )
                fig_main.add_annotation(
                    x=deficit_year,
                    y=1,
                    yref="paper",
                    text=f"Deficit begins {deficit_year}",
                    showarrow=False,
                    yshift=10,
                    font=dict(size=8, color="#A34540")
                )

            st.plotly_chart(
                fig_main,
                width="stretch",
                key="policy_main_chart",
                config={
                    "displayModeBar": False,
                    "responsive": True,
                    "scrollZoom": False
                }
            )

        with summary_col:
            st.markdown(
                f"""
                <div class="decision-summary">
                    <h4>Decision summary</h4>
                    <div class="decision-block">
                        <div class="decision-label">What improves</div>
                        {_summary_items(improvements)}
                    </div>
                    <div class="decision-block">
                        <div class="decision-label">Main trade-offs</div>
                        {_summary_items(tradeoffs)}
                    </div>
                    <div class="decision-block">
                        <div class="decision-label">Priority actions</div>
                        {_summary_items(actions)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Supporting evidence is aligned to the width of the main chart above.
        st.markdown(
            '<div class="policy-evidence-kicker">Supporting evidence</div>',
            unsafe_allow_html=True
        )

        evidence_chart_col, evidence_spacer_col = st.columns(
            [1.72, 1],
            gap="medium",
            vertical_alignment="top"
        )

        with evidence_chart_col:
            evid_tab1, evid_tab2, evid_tab3 = st.tabs([
                "Emissions",
                "Exports",
                "Wind share"
            ])

            with evid_tab1:
                fig_emis = plot_emissions(
                    simulated_data,
                    show_uncertainty=False,
                    show_baseline=True
                )
                evidence_emissions_names = {
                    "Simulated Emissions": "Policy emissions",
                    "DNV Reference GHG Emissions": "Reference",
                    "Stated climate targets (mid-range)": "Targets",
                }
                for trace in fig_emis.data:
                    trace.name = evidence_emissions_names.get(trace.name, trace.name)
                fig_emis = style_evidence_chart(fig_emis, "MtCO₂e")
                st.plotly_chart(
                    fig_emis,
                    width="stretch",
                    key="policy_emis_evid",
                    config={
                        "displayModeBar": False,
                        "responsive": True,
                        "scrollZoom": False
                    }
                )

            with evid_tab2:
                fig_export = plot_export_composition(simulated_data)
                evidence_export_names = {
                    "Natural Gas Exports": "Policy gas",
                    "Oil Exports": "Policy oil",
                    "DNV Baseline Gas (Reference)": "Reference gas",
                    "DNV Baseline Oil (Reference)": "Reference oil",
                }
                for trace in fig_export.data:
                    trace.name = evidence_export_names.get(trace.name, trace.name)
                fig_export = style_evidence_chart(fig_export, "MSm³oe/yr")
                st.plotly_chart(
                    fig_export,
                    width="stretch",
                    key="policy_export_evid",
                    config={
                        "displayModeBar": False,
                        "responsive": True,
                        "scrollZoom": False
                    }
                )

            with evid_tab3:
                fig_ren = plot_renewable_share(
                    simulated_data,
                    show_baseline=True
                )
                evidence_renewable_names = {
                    "Simulated Wind Share": "Policy share",
                    "DNV Baseline Wind Share (Reference)": "Reference",
                }
                for trace in fig_ren.data:
                    trace.name = evidence_renewable_names.get(trace.name, trace.name)
                fig_ren = style_evidence_chart(
                    fig_ren,
                    "Wind share of generation (%)"
                )
                st.plotly_chart(
                    fig_ren,
                    width="stretch",
                    key="policy_ren_evid",
                    config={
                        "displayModeBar": False,
                        "responsive": True,
                        "scrollZoom": False
                    }
                )

            with st.expander("Save and compare scenarios", expanded=False):
                save_name_col, save_button_col, reset_button_col = st.columns(
                    [2, 1, 1],
                    gap="medium",
                    vertical_alignment="bottom"
                )

                with save_name_col:
                    custom_scenario_name = st.text_input(
                        "Scenario name",
                        placeholder="e.g. High stress + green acceleration",
                        key="custom_scenario_input"
                    )

                with save_button_col:
                    if st.button(
                        "Save scenario",
                        width="stretch",
                        key="policy_save_scenario"
                    ):
                        default_name = f"{external_display} | {package_display}"
                        save_scenario(
                            scenario_params,
                            simulated_data,
                            custom_scenario_name.strip() or default_name
                        )
                        st.success("Scenario saved.")
                        st.rerun()

                with reset_button_col:
                    st.button(
                        "Reset reference",
                        width="stretch",
                        key="policy_reset_reference_bottom",
                        on_click=reset_policy_decision_lab
                    )

                if st.session_state.scenario_history:
                    history_df = pd.DataFrame(st.session_state.scenario_history)

                    summary_cols = [
                        "Scenario Name",
                        "Supply (2060) TWh",
                        "Demand (2060) TWh",
                        "Emissions (2060) MtCO2e",
                        "Wind Share (%)",
                        "Deficit Year"
                    ]

                    display_cols = [
                        column for column in summary_cols
                        if column in history_df.columns
                    ]

                    st.dataframe(
                        history_df[display_cols],
                        width="stretch",
                        hide_index=True
                    )

                    download_col, clear_col, _ = st.columns([1.1, 1, 3])

                    with download_col:
                        csv_data = get_scenario_csv()
                        if csv_data:
                            st.download_button(
                                label="Download CSV",
                                data=csv_data,
                                file_name="norway_energy_scenarios.csv",
                                mime="text/csv",
                                width="stretch"
                            )

                    with clear_col:
                        if st.button(
                            "Clear all",
                            width="stretch",
                            key="policy_clear_history"
                        ):
                            st.session_state.scenario_history = []
                            st.session_state.scenario_counter = 0
                            st.rerun()

            st.markdown(
                '<div class="policy-caption">Exploratory scenario model based on simplified, DNV-informed assumptions; not an official DNV forecast and not the proprietary DNV model.</div>',
                unsafe_allow_html=True
            )



# ============================================================================
# TAB 5: DNV-INFORMED PATHWAYS — COMPACT EXECUTIVE VIEW
# ============================================================================

with tab_scenarios:

    # ------------------------------------------------------------------------
    # Local helper functions
    # ------------------------------------------------------------------------

    def scenario_value_at_year(data, variable, year):
        """Return the nearest available value for a selected year."""
        years = np.asarray(data["year"])
        values = np.asarray(data[variable])

        if year <= years.min():
            return float(values[0])
        if year >= years.max():
            return float(values[-1])

        index = int(np.argmin(np.abs(years - year)))
        return float(values[index])


    def format_deficit_year(value):
        return "No deficit" if value is None else str(int(value))


    def scenario_short_name(full_name):
        replacements = {
            "📘 DNV Reference (Best Estimate)": "Reference",
            "🚀 Green Transition (Accelerated)": "Green transition",
            "⛽ Delayed Transition (Fossil Stubborn)": "Delayed transition",
            "⚡ Power Crisis (Grid Constrained)": "Grid constrained",
            "🌊 Offshore Wind Boom": "Offshore wind",
        }
        return replacements.get(full_name, full_name)


    def scenario_icon(full_name):
        icons = {
            "📘 DNV Reference (Best Estimate)": "📘",
            "🚀 Green Transition (Accelerated)": "🌱",
            "⛽ Delayed Transition (Fossil Stubborn)": "🛢️",
            "⚡ Power Crisis (Grid Constrained)": "⚡",
            "🌊 Offshore Wind Boom": "🌊",
        }
        return icons.get(full_name, "◉")


    def compact_scenario_chart(fig, height=305):
        """Apply a compact but high-contrast visual style to pathway charts."""

        # Keep all data lines clearly visible without making the charts visually heavy.
        for trace in fig.data:
            if getattr(trace, "mode", None) and "lines" in trace.mode:
                current_width = getattr(trace.line, "width", None) or 1.0
                trace.line.width = max(float(current_width), 2.6)

                current_opacity = getattr(trace, "opacity", None)
                if current_opacity is None or current_opacity < 0.86:
                    trace.opacity = 0.90

        fig.update_layout(
            title=dict(text=""),
            height=height,
            hovermode="x unified",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=46, r=16, t=30, b=38),
            font=dict(family="Inter, sans-serif", size=10, color="#29495b"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.015,
                xanchor="left",
                x=0,
                font=dict(size=9.2, color="#29495b"),
                bgcolor="rgba(255,255,255,0.72)",
            ),
            xaxis=dict(
                title=dict(text=""),
                showgrid=False,
                tickfont=dict(size=9, color="#526b79"),
                linecolor="rgba(82,107,121,0.35)",
                fixedrange=True,
            ),
            yaxis=dict(
                title_font=dict(size=9, color="#405d6c"),
                tickfont=dict(size=9, color="#526b79"),
                gridcolor="rgba(82,107,121,0.14)",
                zerolinecolor="rgba(82,107,121,0.32)",
                fixedrange=True,
            ),
        )
        return fig


    def build_scenario_summary(selected_name, selected_data, reference_data):
        """Return one main outcome and one principal trade-off."""
        selected_deficit = selected_data["deficit_year"]
        reference_deficit = reference_data["deficit_year"]

        selected_emissions = scenario_value_at_year(selected_data, "emissions", 2050)
        reference_emissions = scenario_value_at_year(reference_data, "emissions", 2050)

        selected_gas = scenario_value_at_year(selected_data, "gas_production", 2040)
        reference_gas = scenario_value_at_year(reference_data, "gas_production", 2040)

        selected_renewables = scenario_value_at_year(selected_data, "renewable_share", 2060) * 100
        reference_renewables = scenario_value_at_year(reference_data, "renewable_share", 2060) * 100

        if selected_deficit is None:
            outcome = "Avoids a modelled power deficit."
        elif reference_deficit is not None and selected_deficit > reference_deficit:
            outcome = f"Delays the power deficit by {selected_deficit - reference_deficit} years."
        elif selected_emissions < reference_emissions - 0.5:
            outcome = f"Cuts 2050 emissions by {reference_emissions - selected_emissions:.1f} MtCO₂e vs reference."
        elif selected_renewables > reference_renewables + 2:
            outcome = f"Raises the 2060 wind-generation share by {selected_renewables - reference_renewables:.1f} percentage points."
        else:
            outcome = "Tracks close to the reference pathway."

        if selected_emissions > reference_emissions + 0.5:
            tradeoff = f"2050 emissions are {selected_emissions - reference_emissions:.1f} MtCO₂e higher than reference."
        elif selected_gas < reference_gas * 0.95:
            gas_change = (selected_gas - reference_gas) / abs(reference_gas) * 100 if reference_gas else 0
            tradeoff = f"2040 gas exports fall {abs(gas_change):.0f}% below reference."
        elif selected_renewables < reference_renewables - 2:
            tradeoff = f"The 2060 wind-generation share is {reference_renewables - selected_renewables:.1f} points lower."
        elif "Grid Constrained" in selected_name:
            tradeoff = "Grid bottlenecks limit renewable integration despite rising demand."
        else:
            tradeoff = "Requires coordinated delivery of policy, grid and generation capacity."

        return {
            "outcome": outcome,
            "tradeoff": tradeoff,
            "emissions_2050": selected_emissions,
            "gas_2040": selected_gas,
            "renewables_2060": selected_renewables,
            "deficit_year": selected_deficit,
        }


    pathway_focus = {
        "📘 DNV Reference (Best Estimate)": {
            "description": "DNV-aligned reference conditions with moderate policy progress, wind deployment, grid expansion and carbon-price growth.",
            "eu": "Moderate",
            "wind": "1.0×",
            "grid": "Medium",
            "oil": "$75/bbl",
        },
        "🚀 Green Transition (Accelerated)": {
            "description": "Faster EU alignment, stronger carbon policy and high grid investment accelerate wind deployment and decarbonization.",
            "eu": "Fast",
            "wind": "1.5×",
            "grid": "High",
            "oil": "$65/bbl",
        },
        "⛽ Delayed Transition (Fossil Stubborn)": {
            "description": "High oil and gas prices, weaker carbon policy and low grid investment slow renewable deployment and prolong fossil dependence.",
            "eu": "Slow",
            "wind": "0.6×",
            "grid": "Low",
            "oil": "$110/bbl",
        },
        "⚡ Power Crisis (Grid Constrained)": {
            "description": "Rapid electricity-demand growth meets slow grid expansion and limited renewable integration, increasing power-system pressure.",
            "eu": "Slow",
            "wind": "0.8×",
            "grid": "Low",
            "oil": "$95/bbl",
        },
        "🌊 Offshore Wind Boom": {
            "description": "Supportive policy, large-scale offshore wind and high grid investment expand domestic supply and reduce power constraints.",
            "eu": "Moderate",
            "wind": "1.8×",
            "grid": "High",
            "oil": "$70/bbl",
        },
    }

    # ------------------------------------------------------------------------
    # Compact page styling
    # ------------------------------------------------------------------------



    # ------------------------------------------------------------------------
    # Calculate all pathways once
    # ------------------------------------------------------------------------

    scenario_results = {}
    for scenario_name in DNV_SCENARIOS_DETAILED.keys():
        scenario_data, _ = get_dnv_informed_scenario(scenario_name)
        scenario_results[scenario_name] = scenario_data

    scenario_names = list(DNV_SCENARIOS_DETAILED.keys())
    reference_name = scenario_names[0]
    reference_data = scenario_results[reference_name]

    if "selected_dnv_pathway" not in st.session_state:
        st.session_state.selected_dnv_pathway = reference_name

    # ------------------------------------------------------------------------
    # Compact two-column workspace
    # ------------------------------------------------------------------------

    # Remove ALL extra space above this section
    st.markdown(
        """
        <div class="dashboard-tab-header">
            <h4>DNV-Informed Pathways</h4>
            <p>Select one of the DNV-informed pathways on the left; review its assumptions and outcomes on the right.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("""
    <style>
        .scenario-intro-title {
            margin: -12px 0 1px 0;
            color: #17384c;
            font-size: 1.00rem;
            font-weight: 780;
        }
        .scenario-intro-subtitle {
            margin: 0 0 7px 0;
            color: #718591;
            font-size: 0.69rem;
            line-height: 1.35;
        }
        .scenario-section-label {
            margin: 5px 0 4px 0;
            color: #607987;
            font-size: 0.66rem;
            font-weight: 700;
            letter-spacing: 0;
            line-height: 1.18;
            text-transform: none;
            white-space: nowrap;
        }
        .selected-pathway-strip {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 14px;
            padding: 8px 11px;
            margin: 6px 0 7px 0;
            border: 1px solid #dfe8ed;
            border-radius: 9px;
            background: #f8fafb;
        }
        .selected-pathway-name {
            color: #17384c;
            font-size: 0.86rem;
            font-weight: 780;
        }
        .selected-pathway-description {
            margin-top: 1px;
            color: #6f8490;
            font-size: 0.63rem;
            line-height: 1.3;
        }
        .selected-pathway-assumptions {
            flex-shrink: 0;
            color: #365969;
            font-size: 0.59rem;
            white-space: nowrap;
        }
        .scenario-result-strip {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            padding: 7px 10px;
            margin: 3px 0 7px 0;
            border: 1px solid #dce8ec;
            border-radius: 8px;
            background: #eef5f7;
            color: #365969;
            font-size: 0.62rem;
            line-height: 1.35;
        }
        .scenario-result-strip b {
            color: #17384c;
        }
        .scenario-method-note {
            margin-top: 6px;
            color: #788b94;
            font-size: 0.64rem;
            line-height: 1.34;
        }
        /* Compact pathway buttons: secondary navigation, not page headings. */
        div[data-testid="stButton"] button {
            min-height: 32px;
            padding: 3px 7px;
            font-size: 0.66rem;
            line-height: 1.16;
            border-radius: 7px;
            font-weight: 550;
        }
        .pathway-side-card {
            margin-top: 7px;
            padding: 9px 9px 8px 9px;
            border: 1px solid #dfe8ed;
            border-radius: 10px;
            background: #f8fafb;
        }
        .pathway-side-title {
            color: #17384c;
            font-size: 0.82rem;
            line-height: 1.20;
            font-weight: 700;
        }
        .pathway-side-description {
            margin-top: 4px;
            color: #58717f;
            font-size: 0.72rem;
            line-height: 1.36;
        }
        .pathway-side-assumptions {
            margin-top: 8px;
            border-top: 1px solid #e1e9ed;
            padding-top: 5px;
        }
        .pathway-side-assumptions > div {
            display: flex;
            justify-content: space-between;
            gap: 8px;
            padding: 3px 0;
            color: #667d89;
            font-size: 0.68rem;
            line-height: 1.24;
        }
        .pathway-side-assumptions b {
            color: #294f61;
        }
        .side-note {
            margin-top: 8px;
        }
        /* Compact selector above the lower pathway comparison chart. */
        div[data-testid="stSelectbox"]:has(
            [data-baseweb="select"]
        ) {
            margin-bottom: 0 !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
            min-height: 34px !important;
            height: 34px !important;
            font-size: 0.74rem !important;
        }

        .scenario-side-insight {
            border: 1px solid #dfe8ec;
            border-radius: 9px;
            background: #f7fafb;
            overflow: hidden;
        }
        .scenario-side-insight-row {
            padding: 10px 12px;
            color: #385665;
            font-size: 0.76rem;
            line-height: 1.38;
        }
        .scenario-side-insight-row + .scenario-side-insight-row {
            border-top: 1px solid #dfe8ec;
        }
        .scenario-side-insight-row span {
            display: block;
            margin-bottom: 4px;
            color: #267d9c;
            font-size: 0.67rem;
            font-weight: 750;
            letter-spacing: 0.045em;
            line-height: 1.18;
            text-transform: uppercase;
        }
        .pathway-table-wrap {
            height: 278px;
            overflow: hidden;
            border: 1px solid #dfe8ec;
            border-radius: 9px;
            background: #ffffff;
        }
        .pathway-table {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
            font-size: 0.70rem;
            color: #365969;
        }
        .pathway-table th {
            padding: 7px 5px;
            background: #f3f7f9;
            color: #4d6876;
            font-size: 0.64rem;
            font-weight: 750;
            line-height: 1.18;
            text-align: center;
            border-bottom: 1px solid #dfe8ec;
        }
        .pathway-table td {
            height: 43px;
            padding: 6px 5px;
            text-align: center;
            border-bottom: 1px solid #edf2f4;
            line-height: 1.2;
            vertical-align: middle;
        }
        .pathway-table td:first-child,
        .pathway-table th:first-child {
            width: 37%;
            text-align: left;
            padding-left: 8px;
        }
        .pathway-table tr.selected-row td {
            background: #edf6f9;
            color: #17384c;
            font-weight: 750;
        }
        .pathway-table tr:last-child td {
            border-bottom: none;
        }
        @media (max-width: 900px) {
            .selected-pathway-strip {
                display: block;
            }
            .selected-pathway-assumptions {
                margin-top: 5px;
                white-space: normal;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    selector_col, content_col = st.columns(
        [0.58, 2.42],
        gap="medium",
        vertical_alignment="top",
    )
    # ------------------------------------------------------------------------
    # LEFT: vertical pathway selector and compact pathway logic
    # ------------------------------------------------------------------------

    with selector_col:
        st.markdown('<div class="scenario-section-label">Pathway</div>', unsafe_allow_html=True)

        for scenario_name in scenario_names:
            is_selected = st.session_state.selected_dnv_pathway == scenario_name
            if st.button(
                f"{scenario_icon(scenario_name)} {scenario_short_name(scenario_name)}",
                key=f"select_pathway_{scenario_short_name(scenario_name).replace(' ', '_')}",
                type="primary" if is_selected else "secondary",
                width="stretch",
            ):
                st.session_state.selected_dnv_pathway = scenario_name
                st.rerun()

        selected_scenario = st.session_state.selected_dnv_pathway
        selected_details = DNV_SCENARIOS_DETAILED[selected_scenario]
        selected_data = scenario_results[selected_scenario]
        selected_summary = build_scenario_summary(selected_scenario, selected_data, reference_data)
        focus = pathway_focus[selected_scenario]

        st.markdown(
            f"""
            <div class="pathway-side-card">
                <div class="pathway-side-title">
                    {scenario_icon(selected_scenario)} {scenario_short_name(selected_scenario)}
                </div>
                <div class="pathway-side-description">{focus["description"]}</div>
                <div class="pathway-side-assumptions">
                    <div><span>EU transition</span><b>{focus["eu"]}</b></div>
                    <div><span>Wind scale-up</span><b>{focus["wind"]}</b></div>
                    <div><span>Grid investment</span><b>{focus["grid"]}</b></div>
                    <div><span>Oil price</span><b>{focus["oil"]}</b></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="scenario-method-note side-note">
                Dashboard-generated pathways informed by DNV’s single best-estimate forecast; not official DNV scenarios.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ------------------------------------------------------------------------
    # RIGHT: two charts, comparison table, interpretation and optional details
    # ------------------------------------------------------------------------

    with content_col:
        # Main chart
        selected_main_chart = plot_supply_demand(
            selected_data,
            show_uncertainty=False,
            show_baseline=(selected_scenario != reference_name),
        )
        selected_main_chart = compact_scenario_chart(selected_main_chart, height=278)

        if selected_data["deficit_year"] is not None:
            selected_main_chart.add_vline(
                x=selected_data["deficit_year"],
                line_width=1.25,
                line_dash="dash",
                line_color="#b6453e",
            )
            selected_main_chart.add_annotation(
                x=selected_data["deficit_year"],
                y=1,
                yref="paper",
                text=f"Deficit {selected_data['deficit_year']}",
                showarrow=False,
                yshift=8,
                font=dict(size=8, color="#9f3933"),
            )

        # Build compact comparison table once
        comparison_rows = []
        for scenario_name, scenario_data in scenario_results.items():
            comparison_rows.append({
                "Pathway": scenario_short_name(scenario_name),
                "Deficit": format_deficit_year(scenario_data["deficit_year"]),
                "2050 emissions": scenario_value_at_year(scenario_data, "emissions", 2050),
                "2060 wind share": scenario_value_at_year(scenario_data, "renewable_share", 2060) * 100,
            })

        comparison_df = pd.DataFrame(comparison_rows)

        # Top row: selected-pathway chart + pathway comparison table
        main_chart_col, table_col = st.columns(
            [1.58, 1.18],
            gap="medium",
            vertical_alignment="top",
        )

        with main_chart_col:
            st.markdown(
                '<div class="scenario-section-label">Selected pathway: supply vs demand</div>',
                unsafe_allow_html=True,
            )
            st.plotly_chart(
                selected_main_chart,
                width="stretch",
                key="selected_dnv_pathway_supply",
                config={"displayModeBar": False, "responsive": True, "scrollZoom": False},
            )

        with table_col:
            st.markdown(
                '<div class="scenario-section-label">Pathways at a glance</div>',
                unsafe_allow_html=True,
            )

            table_rows_html = ""
            for row in comparison_rows:
                full_name = next(
                    name for name in scenario_names
                    if scenario_short_name(name) == row["Pathway"]
                )
                selected_class = "selected-row" if full_name == selected_scenario else ""
                table_rows_html += f"""
                <tr class="{selected_class}">
                    <td>{scenario_icon(full_name)} {row['Pathway']}</td>
                    <td>{row['Deficit']}</td>
                    <td>{row['2050 emissions']:.1f}</td>
                    <td>{row['2060 wind share']:.0f}%</td>
                </tr>
                """

            st.markdown(
                f"""
                <div class="pathway-table-wrap">
                    <table class="pathway-table">
                        <thead>
                            <tr>
                                <th>Pathway</th>
                                <th>Deficit</th>
                                <th>2050<br>Mt</th>
                                <th>2060<br>RES</th>
                            </tr>
                        </thead>
                        <tbody>{table_rows_html}</tbody>
                    </table>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Bottom row: comparison chart with interpretation beside it
        st.markdown(
            '<div style="height:0; margin-top:-10px;"></div>',
            unsafe_allow_html=True,
        )
        comparison_chart_col, insight_col = st.columns(
            [1.58, 1.18],
            gap="medium",
            vertical_alignment="top",
        )

        with comparison_chart_col:
            comparison_control_col, comparison_empty_col = st.columns(
                [0.82, 1.18],
                gap="small",
                vertical_alignment="top",
            )

            with comparison_control_col:
                comparison_metric = st.selectbox(
                    "Comparison metric",
                    options=["Power balance", "GHG emissions", "Gas exports", "Wind share"],
                    key="dnv_pathway_comparison_metric",
                    label_visibility="collapsed",
                )
                st.markdown(
                    '<div class="scenario-section-label" style="text-align:left; margin:-5px 0 0 0; white-space:nowrap;">Cross-pathway comparison</div>',
                    unsafe_allow_html=True,
                )

            # Cross-pathway chart
            metric_configuration = {
                "Power balance": {"variable": "power_balance", "axis_title": "TWh/yr", "multiplier": 1.0},
                "GHG emissions": {"variable": "emissions", "axis_title": "MtCO₂e/yr", "multiplier": 1.0},
                "Gas exports": {"variable": "gas_production", "axis_title": "MSm³oe/yr", "multiplier": 1.0},
                "Wind share": {"variable": "renewable_share", "axis_title": "%", "multiplier": 100.0},
            }

            selected_metric_config = metric_configuration[comparison_metric]
            comparison_fig = go.Figure()

            pathway_line_styles = {
                "📘 DNV Reference (Best Estimate)": {"color": "#245A73", "dash": "solid"},
                "🚀 Green Transition (Accelerated)": {"color": "#1F8A70", "dash": "solid"},
                "⛽ Delayed Transition (Fossil Stubborn)": {"color": "#C4682D", "dash": "dash"},
                "⚡ Power Crisis (Grid Constrained)": {"color": "#C53D4D", "dash": "dashdot"},
                "🌊 Offshore Wind Boom": {"color": "#5B5FB2", "dash": "dot"},
            }

            for scenario_name, scenario_data in scenario_results.items():
                is_selected = scenario_name == selected_scenario
                style = pathway_line_styles[scenario_name]
                comparison_fig.add_trace(
                    go.Scatter(
                        x=scenario_data["year"],
                        y=np.asarray(scenario_data[selected_metric_config["variable"]]) * selected_metric_config["multiplier"],
                        name=scenario_short_name(scenario_name),
                        mode="lines",
                        line=dict(
                            color=style["color"],
                            width=3.6 if is_selected else 2.35,
                            dash="solid" if is_selected else style["dash"],
                        ),
                        opacity=1.0 if is_selected else 0.90,
                        hovertemplate="%{x}: %{y:.1f}<extra>%{fullData.name}</extra>",
                    )
                )

            if comparison_metric == "Power balance":
                comparison_fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="#677d89")

            comparison_fig.update_layout(
                title=dict(text=""),
                height=264,
                hovermode="x unified",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=46, r=12, t=17, b=34),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.002,
                    xanchor="left",
                    x=0,
                    font=dict(size=8.6, color="#29495b"),
                ),
                xaxis=dict(
                    title=dict(text=""),
                    showgrid=False,
                    fixedrange=True,
                    tickfont=dict(size=8.5, color="#526b79"),
                    linecolor="rgba(82,107,121,0.35)",
                ),
                yaxis=dict(
                    title=selected_metric_config["axis_title"],
                    gridcolor="rgba(82,107,121,0.14)",
                    zerolinecolor="rgba(82,107,121,0.32)",
                    fixedrange=True,
                    tickfont=dict(size=8.5, color="#526b79"),
                    title_font=dict(size=8.5, color="#405d6c"),
                ),
                font=dict(family="Inter, sans-serif", size=9.5, color="#29495b"),
            )


            st.plotly_chart(
                comparison_fig,
                width="stretch",
                key="dnv_pathway_cross_comparison",
                config={"displayModeBar": False, "responsive": True},
            )

        with insight_col:
            st.markdown(
                '<div class="scenario-section-label">Interpretation</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <div class="scenario-side-insight">
                    <div class="scenario-side-insight-row">
                        <span>Outcome</span>
                        {selected_summary["outcome"]}
                    </div>
                    <div class="scenario-side-insight-row">
                        <span>Trade-off</span>
                        {selected_summary["tradeoff"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with st.expander("More details", expanded=False):
            assumption_cols = st.columns(7, gap="small")
            assumptions = [
                ("Wind", f"{selected_details['wind_mult']:.1f}×"),
                ("Carbon", f"{selected_details['carbon_mult']:.1f}×"),
                ("Geopolitics", f"{selected_details['sanctions_val']:.2f}"),
                ("EU", selected_details["eu_policy_val"].capitalize()),
                ("Oil price", f"${selected_details['oil_p']}/bbl"),
                ("Grid", selected_details["grid_inv"].capitalize()),
                ("Data centres", f"{selected_details['datacentre_growth']:.1f}×"),
            ]

            for col, (label, value) in zip(assumption_cols, assumptions):
                with col:
                    st.metric(label, value)

            detail_metric = st.selectbox(
                "Additional chart",
                options=["GHG emissions", "Oil & gas exports", "Wind share"],
                key="dnv_pathway_detail_chart",
            )

            if detail_metric == "GHG emissions":
                detail_fig = plot_emissions(
                    selected_data,
                    show_uncertainty=False,
                    show_baseline=(selected_scenario != reference_name),
                )
            elif detail_metric == "Oil & gas exports":
                detail_fig = plot_export_composition(selected_data)
            else:
                detail_fig = plot_renewable_share(
                    selected_data,
                    show_baseline=(selected_scenario != reference_name),
                )

            detail_fig = compact_scenario_chart(detail_fig, height=270)
            st.plotly_chart(
                detail_fig,
                width="stretch",
                key="dnv_selected_pathway_detail",
                config={"displayModeBar": False, "responsive": True},
            )

