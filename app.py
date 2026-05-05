import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import sqlite3
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="ESG Talk vs Walk · Greenwashing Detector",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

  :root {
    --green-dark:  #1a3a2a;
    --green-mid:   #2d6a4f;
    --green-light: #52b788;
    --green-pale:  #b7e4c7;
    --cream:       #f8f5ee;
    --gold:        #c9a84c;
    --red-flag:    #c0392b;
    --amber-flag:  #d68910;
    --blue-s:      #1a6b8a;
    --brown-g:     #7b5e2a;
    --text-dark:   #1a1a1a;
    --card-bg:     #ffffff;
    --border:      #e0ead4;
  }

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text-dark);
  }
  .stApp { background: var(--cream); }

  [data-testid="stSidebar"] {
    background: var(--green-dark) !important;
    color: #ffffff !important;
  }
  [data-testid="stSidebar"] * { color: #e8f5e9 !important; }
  [data-testid="stSidebar"] .stMarkdown h2,
  [data-testid="stSidebar"] .stMarkdown h3 { color: var(--green-pale) !important; }

  .hero-banner {
    background: linear-gradient(135deg, var(--green-dark) 0%, var(--green-mid) 60%, var(--green-light) 100%);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
  }
  .hero-banner::before {
    content: "📊";
    font-size: 7rem;
    position: absolute;
    right: 2.5rem;
    top: 50%;
    transform: translateY(-50%);
    opacity: 0.10;
  }
  .hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    color: #ffffff;
    margin: 0 0 0.4rem 0;
    line-height: 1.2;
  }
  .hero-sub {
    color: var(--green-pale);
    font-size: 1rem;
    font-weight: 300;
    margin: 0;
  }
  .hero-pill {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.3);
    color: #fff;
    border-radius: 20px;
    padding: 3px 14px;
    font-size: 0.75rem;
    font-weight: 500;
    margin-top: 1rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }

  .section-header {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem;
    color: var(--green-dark);
    border-left: 4px solid var(--green-light);
    padding-left: 0.75rem;
    margin: 2rem 0 1rem 0;
  }

  .metric-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    height: 100%;
  }
  .metric-card .label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--green-mid);
    font-weight: 600;
    margin-bottom: 0.5rem;
  }
  .metric-card .value {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    color: var(--green-dark);
    line-height: 1;
  }
  .metric-card .sublabel {
    font-size: 0.78rem;
    color: #888;
    margin-top: 0.3rem;
  }

  .claim-card {
    background: var(--card-bg);
    border-left: 4px solid var(--green-light);
    border-radius: 0 10px 10px 0;
    padding: 0.8rem 1.1rem;
    margin-bottom: 0.6rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
  }
  .claim-card.cat-S { border-left-color: var(--blue-s); }
  .claim-card.cat-G { border-left-color: var(--brown-g); }

  .badge {
    display: inline-block;
    border-radius: 12px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-right: 6px;
  }
  .badge-E  { background: #eafaf1; color: var(--green-mid); }
  .badge-S  { background: #e8f4f8; color: var(--blue-s); }
  .badge-G  { background: #fdf6ec; color: var(--brown-g); }
  .badge-strong   { background: #e8f8f5; color: #1a7a5e; }
  .badge-moderate { background: #fef9e7; color: #9a7000; }
  .badge-weak     { background: #fdecea; color: #922b21; }

  .source-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.8rem 1.1rem;
    margin-bottom: 0.6rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }

  .flag-high   { background:#fdecea; border:1.5px solid var(--red-flag);
                 color:var(--red-flag); border-radius:8px;
                 padding:0.55rem 1.1rem; font-weight:600; display:inline-block; }
  .flag-medium { background:#fef9e7; border:1.5px solid var(--amber-flag);
                 color:var(--amber-flag); border-radius:8px;
                 padding:0.55rem 1.1rem; font-weight:600; display:inline-block; }
  .flag-low    { background:#eafaf1; border:1.5px solid var(--green-light);
                 color:var(--green-mid); border-radius:8px;
                 padding:0.55rem 1.1rem; font-weight:600; display:inline-block; }

  .disclaimer {
    background: #fff8e6;
    border: 1px solid #f0d080;
    border-radius: 8px;
    padding: 0.85rem 1.2rem;
    font-size: 0.82rem;
    color: #7a5c00;
    margin-top: 1rem;
  }
  .info-box {
    background: #eaf4fb;
    border: 1px solid #aed6f1;
    border-radius: 8px;
    padding: 0.85rem 1.2rem;
    font-size: 0.82rem;
    color: #1a5276;
    margin-top: 0.5rem;
  }

  .footer {
    text-align: center;
    font-size: 0.75rem;
    color: #aaa;
    padding: 2rem 0 1rem 0;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
  }

  hr { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

INTENSITY_WEIGHTS = {"strong": 1.0, "moderate": 0.6, "weak": 0.3}
CATEGORY_WEIGHTS  = {"E": 0.50, "S": 0.30, "G": 0.20}
CATEGORY_COLORS   = {"E": "#2d6a4f", "S": "#1a6b8a", "G": "#7b5e2a"}
CATEGORY_ICONS    = {"E": "🌿", "S": "👥", "G": "🏛️"}

# Reference max: 3 strong claims per category → talk_raw = 3.0
TALK_REF_MAX = 3.0

SECTORS = ["Consumer Goods", "Energy", "Technology", "Retail", "Finance",
           "Healthcare", "Industrials", "Materials", "Other"]


# ══════════════════════════════════════════════════════════════════════════════
# SQLITE
# ══════════════════════════════════════════════════════════════════════════════

DB_PATH = os.path.join(os.path.dirname(__file__), "esg_data.db")


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _init_db():
    with _conn() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS analyses (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT    NOT NULL,
            sector       TEXT,
            analysis_date TEXT   NOT NULL,
            talk_score   REAL,
            walk_score   REAL,
            gap_score    REAL,
            gap_level    TEXT
        );
        CREATE TABLE IF NOT EXISTS claims (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id  INTEGER REFERENCES analyses(id),
            claim_text   TEXT,
            esg_category TEXT,
            subcategory  TEXT,
            intensity    TEXT,
            contribution REAL
        );
        CREATE TABLE IF NOT EXISTS walk_sources (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id    INTEGER REFERENCES analyses(id),
            source_type    TEXT,
            source_name    TEXT,
            headline       TEXT,
            sentiment_score REAL,
            weight         REAL
        );
        """)


_init_db()


def save_analysis(company_name, sector, talk_score, walk_score,
                  gap_score, gap_level, claims, sources):
    today = datetime.today().strftime("%Y-%m-%d")
    with _conn() as c:
        cur = c.execute(
            """INSERT INTO analyses
               (company_name,sector,analysis_date,talk_score,walk_score,gap_score,gap_level)
               VALUES (?,?,?,?,?,?,?)""",
            (company_name, sector, today,
             round(talk_score, 2), round(walk_score, 2),
             round(gap_score, 4), gap_level),
        )
        aid = cur.lastrowid
        for cl in claims:
            c.execute(
                "INSERT INTO claims (analysis_id,claim_text,esg_category,subcategory,intensity,contribution) VALUES (?,?,?,?,?,?)",
                (aid, cl["text"], cl["category"], cl.get("subcategory", ""),
                 cl["intensity"], round(cl.get("contribution", 0), 4)),
            )
        for s in sources:
            c.execute(
                "INSERT INTO walk_sources (analysis_id,source_type,source_name,headline,sentiment_score,weight) VALUES (?,?,?,?,?,?)",
                (aid, s["type"], s["name"], s["headline"],
                 round(s["sentiment"], 4), round(s["weight"], 2)),
            )


def load_history(company_name: str) -> pd.DataFrame:
    with _conn() as c:
        rows = c.execute(
            """SELECT analysis_date,talk_score,walk_score,gap_score,gap_level
               FROM analyses WHERE company_name=? ORDER BY analysis_date""",
            (company_name,),
        ).fetchall()
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame([dict(r) for r in rows])


def load_all_latest() -> pd.DataFrame:
    """Most recent analysis per company."""
    with _conn() as c:
        rows = c.execute("""
            SELECT company_name, sector, talk_score, walk_score,
                   gap_score, gap_level, MAX(analysis_date) as analysis_date
            FROM analyses
            GROUP BY company_name
            ORDER BY gap_score DESC
        """).fetchall()
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame([dict(r) for r in rows])


# ══════════════════════════════════════════════════════════════════════════════
# DEMO DATA
# ══════════════════════════════════════════════════════════════════════════════

DEMO_COMPANIES = {
    "EcoFashion Ltd": {
        "sector": "Consumer Goods",
        "claims": [
            {"text": "100% sustainable cotton sourced across all product lines by 2024",
             "category": "E", "subcategory": "Materials",  "intensity": "strong"},
            {"text": "Zero waste to landfill commitment with verified supplier audits",
             "category": "E", "subcategory": "Waste",      "intensity": "strong"},
            {"text": "Net-zero Scope 3 emissions target by 2030 across value chain",
             "category": "E", "subcategory": "Climate",    "intensity": "moderate"},
            {"text": "Living wage guaranteed to all Tier-1 and Tier-2 suppliers",
             "category": "S", "subcategory": "Labour",     "intensity": "strong"},
            {"text": "Gender parity achieved on board of directors in 2023",
             "category": "G", "subcategory": "Diversity",  "intensity": "strong"},
            {"text": "Annual third-party ESG audit published on company website",
             "category": "G", "subcategory": "Reporting",  "intensity": "moderate"},
        ],
        "sources": [
            {"type": "News",       "name": "The Guardian",
             "headline": "EcoFashion Bangladesh suppliers still paid below legal minimum wage",
             "sentiment": -0.82, "weight": 1.0},
            {"type": "Regulatory", "name": "UK ASA Ruling",
             "headline": "Advertising Standards upholds greenwashing complaint vs EcoFashion",
             "sentiment": -0.91, "weight": 3.0},
            {"type": "News",       "name": "Reuters",
             "headline": "EcoFashion factory audit reveals zero-waste claims unverified",
             "sentiment": -0.73, "weight": 1.0},
            {"type": "Reviews",    "name": "Glassdoor",
             "headline": "Supply chain staff report pressure to pass audits; culture of cover-up flagged",
             "sentiment": -0.28, "weight": 0.6},
            {"type": "News",       "name": "Bloomberg",
             "headline": "Fashion greenwashing report names EcoFashion among most egregious offenders",
             "sentiment": -0.65, "weight": 1.0},
        ],
    },
    "GreenTech Solutions": {
        "sector": "Technology",
        "claims": [
            {"text": "85% of operations powered by renewable energy via onsite solar and PPAs",
             "category": "E", "subcategory": "Energy",    "intensity": "strong"},
            {"text": "ISO 14001:2015 environmental management certification maintained",
             "category": "E", "subcategory": "Management","intensity": "strong"},
            {"text": "15% reduction in GHG emission intensity vs 2019 baseline",
             "category": "E", "subcategory": "Climate",   "intensity": "moderate"},
            {"text": "Employee wellbeing programme including mental health support",
             "category": "S", "subcategory": "Wellbeing", "intensity": "moderate"},
        ],
        "sources": [
            {"type": "News",       "name": "Bloomberg",
             "headline": "GreenTech Solutions wins EU Sustainability Award for third consecutive year",
             "sentiment": 0.78, "weight": 1.0},
            {"type": "Regulatory", "name": "EPA Database",
             "headline": "No enforcement actions recorded — full compliance with all environmental regulations",
             "sentiment": 0.15, "weight": 3.0},
            {"type": "News",       "name": "Financial Times",
             "headline": "GreenTech data centres achieve carbon neutral status ahead of schedule",
             "sentiment": 0.72, "weight": 1.0},
            {"type": "Reviews",    "name": "Glassdoor",
             "headline": "Employees describe genuine sustainability culture; high retention in ESG team",
             "sentiment": 0.65, "weight": 0.6},
        ],
    },
    "CleanEnergy Corp": {
        "sector": "Energy",
        "claims": [
            {"text": "100% renewable energy portfolio — wind and solar across 12 countries",
             "category": "E", "subcategory": "Energy",    "intensity": "strong"},
            {"text": "Net-zero operations achieved in 2023 with independent third-party verification",
             "category": "E", "subcategory": "Climate",   "intensity": "strong"},
            {"text": "Zero harm safety record maintained for four consecutive years",
             "category": "S", "subcategory": "Safety",    "intensity": "strong"},
            {"text": "Community benefit funds established in all operating regions",
             "category": "S", "subcategory": "Community", "intensity": "moderate"},
            {"text": "Transparent ESG reporting aligned to TCFD and GRI Standards",
             "category": "G", "subcategory": "Reporting", "intensity": "strong"},
        ],
        "sources": [
            {"type": "News",       "name": "Reuters",
             "headline": "CleanEnergy wind farm approved after contested planning inquiry raises local concerns",
             "sentiment": -0.12, "weight": 1.0},
            {"type": "Regulatory", "name": "Energy Regulator",
             "headline": "Minor compliance notice issued for grid connection disclosure delays",
             "sentiment": -0.35, "weight": 3.0},
            {"type": "News",       "name": "Bloomberg",
             "headline": "CleanEnergy reports strong renewable output; analysts broadly positive on ESG credentials",
             "sentiment": 0.55, "weight": 1.0},
            {"type": "Reviews",    "name": "Glassdoor",
             "headline": "Positive employee reviews; some concerns about pace of community consultation",
             "sentiment": 0.38, "weight": 0.6},
        ],
    },
    "SustainRetail Group": {
        "sector": "Retail",
        "claims": [
            {"text": "Plastic-free packaging across all own-brand products committed by end-2023",
             "category": "E", "subcategory": "Waste",    "intensity": "strong"},
            {"text": "Fair trade certified supply chain for all coffee and cocoa products",
             "category": "S", "subcategory": "Labour",   "intensity": "strong"},
            {"text": "Carbon reduction roadmap aligned to Science Based Targets initiative",
             "category": "E", "subcategory": "Climate",  "intensity": "moderate"},
            {"text": "Food waste halved versus 2020 baseline through redistribution partnerships",
             "category": "E", "subcategory": "Waste",    "intensity": "moderate"},
            {"text": "Diversity and inclusion targets exceeded for third year running",
             "category": "G", "subcategory": "Diversity","intensity": "moderate"},
        ],
        "sources": [
            {"type": "News",       "name": "Which?",
             "headline": "Sustainability audit finds only 60% of SustainRetail lines meet plastic-free claim",
             "sentiment": -0.52, "weight": 1.0},
            {"type": "Regulatory", "name": "CMA",
             "headline": "Competition authority reviewing green claims — SustainRetail among retailers under scrutiny",
             "sentiment": -0.68, "weight": 3.0},
            {"type": "Reviews",    "name": "Trustpilot",
             "headline": "Customer reviews mixed: 'more marketing than reality' a recurring theme",
             "sentiment": -0.38, "weight": 0.6},
            {"type": "News",       "name": "BBC",
             "headline": "SustainRetail food waste programme praised by charity redistribution partners",
             "sentiment": 0.42, "weight": 1.0},
        ],
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# SCORING ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def compute_talk_score(claims: list) -> tuple[float, list]:
    """
    Normalised Talk score (0–100) and per-claim contributions.
    Reference max = 3 strong claims per E/S/G dimension (talk_raw = 3.0).
    """
    if not claims:
        return 0.0, []

    talk_raw = sum(
        INTENSITY_WEIGHTS[c["intensity"]] * CATEGORY_WEIGHTS[c["category"]]
        for c in claims
    )
    talk_score = min(100.0, (talk_raw / TALK_REF_MAX) * 100.0)

    enriched = []
    for c in claims:
        contrib_raw = INTENSITY_WEIGHTS[c["intensity"]] * CATEGORY_WEIGHTS[c["category"]]
        contrib_pct = (contrib_raw / talk_raw * 100.0) if talk_raw > 0 else 0.0
        enriched.append({**c, "contribution": round(contrib_pct, 1)})

    return round(talk_score, 1), enriched


def compute_walk_score(sources: list) -> float:
    """
    Weighted-average Walk score (0–100).
    Sentiment (-1 to +1) → mapped to (0 to 100).
    Regulatory sources carry 3× weight by default if weight not specified.
    """
    if not sources:
        return 50.0  # neutral when no external data

    total_weight = sum(s["weight"] for s in sources)
    if total_weight == 0:
        return 50.0

    weighted_sum = sum(
        ((s["sentiment"] + 1.0) / 2.0 * 100.0) * s["weight"]
        for s in sources
    )
    return round(weighted_sum / total_weight, 1)


def compute_gap(talk_score: float, walk_score: float) -> dict:
    """
    Gap = max(0, Talk − Walk) / 100  (normalised 0–1).
    Negative gap (walk > talk) means the company under-claims — flagged as Authentic.
    """
    if talk_score == 0:
        return {"raw": 0.0, "pct": 0.0, "level": "LOW",
                "label": "No Claims", "authentic": False}

    raw = (talk_score - walk_score) / 100.0
    pct = max(0.0, raw) * 100.0

    if raw < 0:
        level, label, authentic = "LOW", "Authentic / Under-claims", True
    elif pct < 20:
        level, label, authentic = "LOW",    "Low Risk",    False
    elif pct < 40:
        level, label, authentic = "MEDIUM", "Medium Risk", False
    else:
        level, label, authentic = "HIGH",   "High Risk",   False

    return {"raw": round(raw, 4), "pct": round(pct, 1),
            "level": level, "label": label, "authentic": authentic}


# ══════════════════════════════════════════════════════════════════════════════
# UI COMPONENTS
# ══════════════════════════════════════════════════════════════════════════════

def render_hero():
    st.markdown("""
    <div class="hero-banner">
      <p class="hero-title">ESG Talk vs Walk<br>Greenwashing Detector</p>
      <p class="hero-sub">
        Compare what companies <em>say</em> about sustainability against what external
        sources <em>confirm</em> — and surface the gap.
      </p>
      <span class="hero-pill">📍 Trinity College Dublin · MSc Business Analytics · 2026</span>
    </div>
    """, unsafe_allow_html=True)


def render_score_cards(talk: float, walk: float, gap: dict):
    c1, c2, c3, c4 = st.columns(4)

    talk_col = "#2d6a4f" if talk >= 60 else ("#d68910" if talk >= 35 else "#c0392b")
    walk_col = "#2d6a4f" if walk >= 60 else ("#d68910" if walk >= 35 else "#c0392b")

    with c1:
        st.markdown(f"""<div class="metric-card">
          <div class="label">Talk Score</div>
          <div class="value" style="color:{talk_col}">{talk}</div>
          <div class="sublabel">ESG claims strength</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""<div class="metric-card">
          <div class="label">Walk Score</div>
          <div class="value" style="color:{walk_col}">{walk}</div>
          <div class="sublabel">external sentiment</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        gap_col = {"HIGH": "#c0392b", "MEDIUM": "#d68910", "LOW": "#2d6a4f"}[gap["level"]]
        flag_map = {
            "HIGH":   '<span class="flag-high">🔴 HIGH RISK</span>',
            "MEDIUM": '<span class="flag-medium">🟡 MEDIUM RISK</span>',
            "LOW":    '<span class="flag-low">🟢 LOW RISK</span>',
        }
        pct_display = f"+{gap['pct']:.0f}%" if not gap["authentic"] else "−"
        st.markdown(f"""<div class="metric-card">
          <div class="label">Gap Score</div>
          <div class="value" style="color:{gap_col}">{pct_display}</div>
          <div class="sublabel">{flag_map[gap['level']]}</div>
        </div>""", unsafe_allow_html=True)

    with c4:
        delta_txt = ("Walk > Talk — company under-promises"
                     if gap["authentic"]
                     else f"Talk exceeds Walk by {abs(talk - walk):.0f} pts")
        st.markdown(f"""<div class="metric-card">
          <div class="label">Verdict</div>
          <div style="margin-top:0.5rem; font-size:0.9rem; font-weight:600;
                      color:{'#2d6a4f' if gap['authentic'] else '#c0392b' if gap['level']=='HIGH' else '#d68910' if gap['level']=='MEDIUM' else '#2d6a4f'}">
            {gap['label']}
          </div>
          <div class="sublabel" style="margin-top:0.4rem">{delta_txt}</div>
        </div>""", unsafe_allow_html=True)


def render_gap_gauge(gap: dict):
    level_colors = {"HIGH": "#c0392b", "MEDIUM": "#d68910", "LOW": "#2d6a4f"}
    color = level_colors[gap["level"]]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=gap["pct"],
        number={"suffix": "%", "font": {"size": 42, "family": "DM Serif Display",
                                        "color": color}},
        title={"text": "Talk–Walk Gap Score",
               "font": {"size": 15, "family": "DM Sans", "color": "#555"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1,
                     "tickcolor": "#ccc", "tickfont": {"size": 11}},
            "bar":  {"color": color, "thickness": 0.28},
            "bgcolor": "white",
            "borderwidth": 0,
            "steps": [
                {"range": [0,  20], "color": "#eafaf1"},
                {"range": [20, 40], "color": "#fef9e7"},
                {"range": [40, 100], "color": "#fdecea"},
            ],
            "threshold": {
                "line":      {"color": "#c0392b", "width": 3},
                "thickness": 0.82,
                "value":     40,
            },
        },
    ))
    fig.update_layout(
        height=280,
        margin=dict(t=60, b=20, l=30, r=30),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans"),
    )
    return fig


def render_talk_panel(claims: list, talk_score: float):
    st.markdown('<div class="section-header">Talk Pipeline — ESG Claims Extracted</div>',
                unsafe_allow_html=True)
    st.caption(f"**Talk Score: {talk_score}/100** · {len(claims)} claim(s) extracted from "
               "sustainability reports and official website")

    for cl in claims:
        cat   = cl["category"]
        intns = cl["intensity"]
        cat_class = f"cat-{cat}"
        st.markdown(f"""
        <div class="claim-card {cat_class}">
          <span class="badge badge-{cat}">{CATEGORY_ICONS[cat]} {cat}</span>
          <span class="badge badge-{intns}">{intns}</span>
          <span style="font-size:0.75rem;color:#999;margin-left:4px">{cl.get('subcategory','')}</span>
          <div style="margin-top:0.35rem;font-size:0.9rem;color:#222">{cl['text']}</div>
          <div style="margin-top:0.25rem;font-size:0.72rem;color:#aaa">
            Contribution to Talk score: {cl.get('contribution', 0):.1f}%
          </div>
        </div>
        """, unsafe_allow_html=True)


def render_walk_panel(sources: list, walk_score: float):
    st.markdown('<div class="section-header">Walk Pipeline — External Evidence</div>',
                unsafe_allow_html=True)
    st.caption(f"**Walk Score: {walk_score}/100** · {len(sources)} source(s) · "
               "Regulatory actions carry 3× weight")

    for s in sources:
        senti = s["sentiment"]
        senti_pct  = (senti + 1) / 2 * 100
        senti_col  = ("#2d6a4f" if senti > 0.2 else
                      "#d68910" if senti > -0.2 else "#c0392b")
        senti_lbl  = ("Positive" if senti > 0.2 else
                      "Neutral"  if senti > -0.2 else "Negative")
        weight_tag = "3× weight" if s["weight"] >= 3 else f"{s['weight']}× weight"
        st.markdown(f"""
        <div class="source-card">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span style="font-size:0.8rem;font-weight:600;color:#555">
              {s['type']} · {s['name']}
              <span style="font-size:0.7rem;color:#aaa;margin-left:6px">{weight_tag}</span>
            </span>
            <span style="font-size:0.8rem;font-weight:600;color:{senti_col}">
              {senti_lbl} ({senti:+.2f})
            </span>
          </div>
          <div style="margin-top:0.3rem;font-size:0.88rem;color:#333;font-style:italic">
            "{s['headline']}"
          </div>
        </div>
        """, unsafe_allow_html=True)


def render_contribution_chart(claims: list):
    """SHAP-style bar chart — claim contribution to Talk score."""
    if not claims:
        return None
    labels = [f"{CATEGORY_ICONS[c['category']]} {c['text'][:55]}…"
              if len(c['text']) > 55 else f"{CATEGORY_ICONS[c['category']]} {c['text']}"
              for c in claims]
    contribs = [c.get("contribution", 0) for c in claims]
    colors   = [CATEGORY_COLORS[c["category"]] for c in claims]

    fig = go.Figure(go.Bar(
        x=contribs, y=labels, orientation="h",
        marker=dict(color=colors, cornerradius=4),
        text=[f"{v:.1f}%" for v in contribs],
        textposition="outside",
    ))
    fig.update_layout(
        title=dict(text="Claim Contribution to Talk Score (SHAP-style)",
                   font=dict(size=13, family="DM Sans"), x=0),
        xaxis=dict(range=[0, max(contribs) * 1.35],
                   showgrid=False, zeroline=False,
                   ticksuffix="%", title="Contribution (%)"),
        yaxis=dict(showgrid=False, automargin=True,
                   tickfont=dict(size=11)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans"),
        height=max(220, 46 * len(claims)),
        margin=dict(l=10, r=80, t=40, b=20),
        showlegend=False,
    )
    return fig


def render_sentiment_chart(sources: list):
    """Horizontal bar chart of per-source sentiment scores."""
    if not sources:
        return None
    labels  = [f"{s['type'][:3].upper()} · {s['name']}" for s in sources]
    sentis  = [s["sentiment"] for s in sources]
    weights = [s["weight"] for s in sources]
    colors  = ["#2d6a4f" if v > 0.2 else "#d68910" if v > -0.2 else "#c0392b"
               for v in sentis]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=sentis, y=labels, orientation="h",
        marker=dict(color=colors, cornerradius=4),
        text=[f"{v:+.2f} (wt {w:.1f}×)" for v, w in zip(sentis, weights)],
        textposition="outside",
        name="Sentiment",
    ))
    fig.add_vline(x=0, line_color="#999", line_width=1.5)
    fig.update_layout(
        title=dict(text="Source Sentiment Scores",
                   font=dict(size=13, family="DM Sans"), x=0),
        xaxis=dict(range=[-1.3, 1.3], showgrid=False,
                   zeroline=False, title="Sentiment (−1 = negative, +1 = positive)"),
        yaxis=dict(showgrid=False, automargin=True,
                   tickfont=dict(size=11)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans"),
        height=max(200, 48 * len(sources)),
        margin=dict(l=10, r=100, t=40, b=20),
        showlegend=False,
    )
    return fig


def render_company_comparison(df: pd.DataFrame):
    """Multi-company gap score comparison bar chart."""
    if df.empty:
        return None

    color_map = {"HIGH": "#c0392b", "MEDIUM": "#d68910", "LOW": "#2d6a4f"}
    colors = [color_map.get(lv, "#888") for lv in df["gap_level"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["gap_score_pct"],
        y=df["company_name"],
        orientation="h",
        marker=dict(color=colors, cornerradius=5),
        text=[f"{v:.0f}% · {l}" for v, l in zip(df["gap_score_pct"], df["gap_level"])],
        textposition="outside",
    ))
    fig.add_vline(x=20, line_dash="dot",  line_color="#d68910",
                  annotation_text="Medium threshold",
                  annotation_position="top right",
                  annotation_font_color="#d68910")
    fig.add_vline(x=40, line_dash="dash", line_color="#c0392b",
                  annotation_text="High threshold",
                  annotation_position="top right",
                  annotation_font_color="#c0392b")
    fig.update_layout(
        title=dict(text="Talk–Walk Gap by Company",
                   font=dict(size=14, family="DM Serif Display"), x=0),
        xaxis=dict(range=[0, 90], showgrid=False,
                   zeroline=False, ticksuffix="%"),
        yaxis=dict(showgrid=False, automargin=True),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans"),
        height=max(250, 55 * len(df)),
        margin=dict(l=10, r=120, t=50, b=20),
        showlegend=False,
    )
    return fig


def render_history_chart(history_df: pd.DataFrame, company_name: str):
    """Line chart of gap score over time for a single company."""
    if history_df.empty or len(history_df) < 2:
        return None

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=history_df["analysis_date"],
        y=history_df["talk_score"],
        mode="lines+markers",
        name="Talk Score",
        line=dict(color="#2d6a4f", width=2.5),
        marker=dict(size=7),
    ))
    fig.add_trace(go.Scatter(
        x=history_df["analysis_date"],
        y=history_df["walk_score"],
        mode="lines+markers",
        name="Walk Score",
        line=dict(color="#1a6b8a", width=2.5),
        marker=dict(size=7),
    ))
    fig.add_trace(go.Scatter(
        x=history_df["analysis_date"],
        y=history_df["gap_score"] * 100,
        mode="lines+markers",
        name="Gap % ",
        line=dict(color="#c0392b", width=2, dash="dot"),
        marker=dict(size=6),
        yaxis="y2",
    ))
    fig.update_layout(
        title=dict(text=f"Historical Trend — {company_name}",
                   font=dict(size=13, family="DM Sans"), x=0),
        xaxis=dict(showgrid=False),
        yaxis=dict(title="Score (0–100)", showgrid=True,
                   gridcolor="#eee", range=[0, 110]),
        yaxis2=dict(title="Gap %", overlaying="y", side="right",
                    range=[0, 110], showgrid=False),
        legend=dict(orientation="h", y=-0.2),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans"),
        height=300,
        margin=dict(l=10, r=60, t=40, b=40),
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# ANALYSIS RUNNER
# ══════════════════════════════════════════════════════════════════════════════

def run_analysis(company_name: str, sector: str, claims: list, sources: list,
                 save: bool = True):
    talk_score, enriched_claims = compute_talk_score(claims)
    walk_score = compute_walk_score(sources)
    gap        = compute_gap(talk_score, walk_score)

    if save and company_name.strip():
        save_analysis(company_name, sector, talk_score, walk_score,
                      gap["raw"], gap["level"], enriched_claims, sources)

    # ── Score cards
    render_score_cards(talk_score, walk_score, gap)
    st.markdown("---")

    # ── Gap gauge + SHAP-style chart
    col_gauge, col_shap = st.columns([1, 1.4])
    with col_gauge:
        st.plotly_chart(render_gap_gauge(gap), use_container_width=True)
        flag_map = {
            "HIGH":   '<span class="flag-high">🔴 HIGH greenwashing risk</span>',
            "MEDIUM": '<span class="flag-medium">🟡 MEDIUM greenwashing risk</span>',
            "LOW":    '<span class="flag-low">🟢 LOW greenwashing risk</span>',
        }
        st.markdown(f"<div style='text-align:center;margin-top:-1rem'>"
                    f"{flag_map[gap['level']]}</div>", unsafe_allow_html=True)
        if gap["level"] != "LOW":
            st.markdown("""
            <div class="disclaimer" style="margin-top:1rem">
              ⚠️ <b>Responsible AI:</b> Greenwashing flags are algorithmically generated.
              Verify with an ESG consultant before regulatory or reputational action.
            </div>""", unsafe_allow_html=True)
        if gap["authentic"]:
            st.markdown("""
            <div class="info-box" style="margin-top:1rem">
              ✅ Walk score exceeds Talk score — external evidence is <em>stronger</em>
              than official claims. The company appears to under-promise and over-deliver.
            </div>""", unsafe_allow_html=True)

    with col_shap:
        fig_shap = render_contribution_chart(enriched_claims)
        if fig_shap:
            st.plotly_chart(fig_shap, use_container_width=True)

    st.markdown("---")

    # ── Talk + Walk panels side by side
    col_talk, col_walk = st.columns(2)
    with col_talk:
        render_talk_panel(enriched_claims, talk_score)
    with col_walk:
        render_walk_panel(sources, walk_score)
        fig_sent = render_sentiment_chart(sources)
        if fig_sent:
            st.plotly_chart(fig_sent, use_container_width=True)

    # ── Historical trend
    history = load_history(company_name)
    if not history.empty and len(history) >= 2:
        st.markdown("---")
        st.markdown('<div class="section-header">Historical Trend</div>',
                    unsafe_allow_html=True)
        history["gap_score"] = pd.to_numeric(history["gap_score"], errors="coerce")
        fig_hist = render_history_chart(history, company_name)
        if fig_hist:
            st.plotly_chart(fig_hist, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# JSON UPLOAD PARSING
# ══════════════════════════════════════════════════════════════════════════════

def parse_upload(raw: dict) -> tuple[str, str, list, list]:
    company = raw.get("company_name", "Unknown Company")
    sector  = raw.get("sector", "Other")
    claims  = raw.get("claims", [])
    sources = raw.get("walk_sources", raw.get("sources", []))

    # Normalise field names
    norm_claims = []
    for c in claims:
        norm_claims.append({
            "text":        c.get("text", c.get("claim_text", "")),
            "category":    c.get("category", "E").upper(),
            "subcategory": c.get("subcategory", c.get("esg_subcategory", "")),
            "intensity":   c.get("intensity", "moderate").lower(),
        })

    norm_sources = []
    for s in sources:
        s_type = s.get("type", s.get("source_type", "News"))
        norm_sources.append({
            "type":      s_type,
            "name":      s.get("name", s.get("source_name", "")),
            "headline":  s.get("headline", ""),
            "sentiment": float(s.get("sentiment", s.get("sentiment_score", 0.0))),
            "weight":    float(s.get("weight", 3.0 if s_type == "Regulatory" else 1.0)),
        })

    return company, sector, norm_claims, norm_sources


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🔍 Talk vs Walk")
    st.markdown("**ESG Greenwashing Detector**  \nTrinity College Dublin · MSc BA 2026")
    st.markdown("---")

    mode = st.radio(
        "Mode",
        ["🎭 Demo Companies", "📤 Upload Pipeline JSON", "✏️ Manual Entry",
         "📊 Multi-Company View"],
        index=0,
    )
    st.markdown("---")

    st.markdown("**Scoring method**")
    st.markdown("""
    - **Talk**: LLM-extracted ESG claims weighted by intensity (strong/moderate/weak)
      and ESG category (E 50% · S 30% · G 20%)
    - **Walk**: FinBERT-scored external sources, regulatory actions weighted 3×
    - **Gap**: `max(0, Talk − Walk) / 100`
      — thresholds: Low <20% · Medium 20–39% · High ≥40%
    """)
    st.markdown("---")
    st.markdown("**Pipeline sources**")
    st.markdown("Website · CSR PDFs · NewsAPI/GDELT · SEC/EPA · Glassdoor")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

render_hero()

# ── DEMO MODE ─────────────────────────────────────────────────────────────────
if mode == "🎭 Demo Companies":
    company_name = st.selectbox(
        "Select a company",
        list(DEMO_COMPANIES.keys()),
        help="Pre-loaded demo data illustrating the full pipeline output.",
    )
    data = DEMO_COMPANIES[company_name]
    st.markdown(f'<div class="section-header">Analysis — {company_name} '
                f'<span style="font-size:0.85rem;color:#888;font-family:DM Sans">'
                f'({data["sector"]})</span></div>', unsafe_allow_html=True)

    col_info, _ = st.columns([2, 1])
    with col_info:
        st.markdown("""
        <div class="info-box">
          📌 <b>Demo mode</b> — results are pre-computed to illustrate the pipeline.
          In production, claims are extracted by the LLM layer (Groq/Llama 3) and
          sentiment is scored by FinBERT from live news and regulatory sources.
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("▶ Run Analysis", type="primary", use_container_width=True):
        with st.spinner("Running pipeline…"):
            run_analysis(company_name, data["sector"],
                         data["claims"], data["sources"], save=True)

# ── UPLOAD MODE ───────────────────────────────────────────────────────────────
elif mode == "📤 Upload Pipeline JSON":
    st.markdown('<div class="section-header">Upload Pipeline Output (JSON)</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
      📌 Upload the structured JSON produced by the Talk + Walk pipeline scripts.
      The schema expects: <code>company_name</code>, <code>sector</code>,
      <code>claims</code> (array with <code>text, category, subcategory, intensity</code>),
      and <code>walk_sources</code> (array with
      <code>type, name, headline, sentiment, weight</code>).
    </div>""", unsafe_allow_html=True)

    # Download sample schema
    sample = {
        "company_name": "Acme Corp",
        "sector": "Industrials",
        "claims": [
            {"text": "Net-zero Scope 1 & 2 by 2030",
             "category": "E", "subcategory": "Climate", "intensity": "strong"},
            {"text": "Living wage for all direct employees",
             "category": "S", "subcategory": "Labour", "intensity": "moderate"},
        ],
        "walk_sources": [
            {"type": "Regulatory", "name": "EPA",
             "headline": "No enforcement actions recorded",
             "sentiment": 0.10, "weight": 3.0},
            {"type": "News", "name": "Reuters",
             "headline": "Acme misses 2025 emissions target by 12%",
             "sentiment": -0.55, "weight": 1.0},
        ],
    }
    st.download_button(
        "⬇️ Download sample JSON schema",
        data=json.dumps(sample, indent=2),
        file_name="pipeline_output_sample.json",
        mime="application/json",
    )

    uploaded = st.file_uploader("Upload pipeline output JSON", type=["json"])
    if uploaded:
        try:
            raw = json.load(uploaded)
            company_name, sector, claims, sources = parse_upload(raw)
            st.success(f"✅ Loaded: **{company_name}** · "
                       f"{len(claims)} claim(s) · {len(sources)} source(s)")
            st.markdown("---")
            if st.button("▶ Run Analysis", type="primary", use_container_width=True):
                with st.spinner("Running pipeline…"):
                    run_analysis(company_name, sector, claims, sources, save=True)
        except Exception as e:
            st.error(f"Could not parse JSON: {e}")

# ── MANUAL ENTRY ──────────────────────────────────────────────────────────────
elif mode == "✏️ Manual Entry":
    st.markdown('<div class="section-header">Manual Entry</div>', unsafe_allow_html=True)
    st.caption("Enter scores directly — useful for testing or when pipeline output isn't available.")

    with st.form("manual_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            company_name = st.text_input("Company Name", placeholder="e.g. Acme Corp")
        with col_b:
            sector = st.selectbox("Sector", SECTORS)

        st.markdown("##### Talk — ESG Claims")
        st.caption("Add one claim per row. Separate multiple claims with a blank line.")

        num_claims = st.number_input("Number of claims", 1, 15, 3, step=1)
        claims = []
        for i in range(int(num_claims)):
            c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
            with c1:
                txt = st.text_input(f"Claim {i+1}", key=f"cl_text_{i}",
                                    placeholder="Describe the ESG claim")
            with c2:
                cat = st.selectbox("Category", ["E", "S", "G"], key=f"cl_cat_{i}")
            with c3:
                sub = st.text_input("Sub-cat", key=f"cl_sub_{i}",
                                    placeholder="e.g. Climate")
            with c4:
                intns = st.selectbox("Intensity", ["strong", "moderate", "weak"],
                                     key=f"cl_int_{i}")
            if txt.strip():
                claims.append({"text": txt, "category": cat,
                                "subcategory": sub, "intensity": intns})

        st.markdown("---")
        st.markdown("##### Walk — External Sources")

        num_sources = st.number_input("Number of sources", 1, 10, 2, step=1)
        sources = []
        for i in range(int(num_sources)):
            c1, c2, c3, c4, c5 = st.columns([1, 1, 3, 1, 1])
            with c1:
                stype = st.selectbox("Type", ["News", "Regulatory", "Reviews"],
                                     key=f"src_type_{i}")
            with c2:
                sname = st.text_input("Source", key=f"src_name_{i}",
                                      placeholder="e.g. Reuters")
            with c3:
                headline = st.text_input("Headline / summary", key=f"src_hl_{i}")
            with c4:
                senti = st.slider("Sentiment", -1.0, 1.0, 0.0, 0.05,
                                  key=f"src_sent_{i}",
                                  help="-1 = very negative, +1 = very positive")
            with c5:
                default_w = 3.0 if stype == "Regulatory" else 1.0
                weight = st.number_input("Weight", 0.1, 5.0, default_w,
                                         step=0.1, key=f"src_wt_{i}")
            if headline.strip() or sname.strip():
                sources.append({"type": stype, "name": sname,
                                 "headline": headline, "sentiment": senti,
                                 "weight": weight})

        submitted = st.form_submit_button("▶ Run Analysis", type="primary",
                                          use_container_width=True)

    if submitted:
        if not claims:
            st.warning("Add at least one claim to run the analysis.")
        else:
            with st.spinner("Running pipeline…"):
                run_analysis(company_name or "Company", sector,
                             claims, sources, save=True)

# ── MULTI-COMPANY VIEW ────────────────────────────────────────────────────────
elif mode == "📊 Multi-Company View":
    st.markdown('<div class="section-header">Multi-Company Comparison</div>',
                unsafe_allow_html=True)

    all_df = load_all_latest()

    if all_df.empty:
        st.markdown("""
        <div class="info-box">
          📌 No analyses saved yet. Run at least one company analysis to see
          the comparison view. Switch to <b>Demo Companies</b> mode and click
          <em>Run Analysis</em> for each company to populate this view.
        </div>""", unsafe_allow_html=True)
    else:
        all_df["gap_score_pct"] = (all_df["gap_score"].clip(lower=0) * 100).round(1)

        fig_cmp = render_company_comparison(all_df)
        if fig_cmp:
            st.plotly_chart(fig_cmp, use_container_width=True)

        st.markdown("---")
        st.markdown("##### All Company Records")

        display_df = all_df[["company_name", "sector", "talk_score", "walk_score",
                              "gap_score_pct", "gap_level", "analysis_date"]].copy()
        display_df.columns = ["Company", "Sector", "Talk", "Walk",
                               "Gap %", "Risk Level", "Last Analysed"]

        def _row_color(row):
            colors = {"HIGH": "background-color:#fdecea",
                      "MEDIUM": "background-color:#fef9e7",
                      "LOW": "background-color:#eafaf1"}
            return [colors.get(row["Risk Level"], "")] * len(row)

        st.dataframe(
            display_df.style.apply(_row_color, axis=1),
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "⬇️ Export CSV",
            data=display_df.to_csv(index=False),
            file_name="esg_gap_results.csv",
            mime="text/csv",
        )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  ESG Talk vs Walk · Greenwashing Detection Tool · Sundus Afreen · MSc Business Analytics · TCD 2026<br>
  Pipeline: BeautifulSoup · PyPDF2 · Groq / Llama 3 · FinBERT · SHAP · Streamlit
  · Gap Formula: <code>max(0, Talk − Walk) / 100</code>
</div>
""", unsafe_allow_html=True)
