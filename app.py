from datetime import datetime, timezone
import streamlit as st

st.set_page_config(page_title="Big Picture Market Pulse", layout="wide")


def _asof_ts():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


# =========================
# CSS
# =========================
CSS = """
<style>
.block-container {max-width: 1750px; padding-top: 0.85rem; padding-bottom: 2rem;}
.section-title {font-weight: 950; font-size: 1.05rem; margin: 0.5rem 0 0.4rem 0;}
.small-muted {opacity: 0.75; font-size: 0.9rem;}
.hr {border-top: 1px solid rgba(255,255,255,0.12); margin: 14px 0;}
.hr-big {border-top: 2px solid rgba(255,255,255,0.18); margin: 18px 0 16px 0;}

.card {
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.03);
  border-radius: 12px;
  padding: 10px 12px;          /* tighter */
  margin-bottom: 10px;         /* tighter */
}
.card h3{margin:0 0 8px 0; font-size: 1.0rem; font-weight: 950;}
.card .hint{opacity:0.72; font-size:0.86rem; margin-top:-2px; margin-bottom:8px;}

.badge{
  display:inline-block;
  padding: 2px 8px;
  border-radius: 999px;
  font-weight: 900;
  font-size: 0.78rem;
  letter-spacing: 0.2px;
  border: 1px solid rgba(255,255,255,0.12);
}
.badge-yes{background: rgba(124,252,154,0.15); color:#7CFC9A;}
.badge-no{background: rgba(255,107,107,0.12); color:#FF6B6B;}
.badge-neutral{background: rgba(255,200,60,0.12); color: rgba(255,200,60,0.98);}

.pill{
  display:inline-block;
  padding: 3px 10px;
  border-radius: 999px;
  font-weight: 950;
  font-size: 0.82rem;
  border: 1px solid rgba(255,255,255,0.12);
}
.pill-red{background: rgba(255,80,80,0.16); color:#FF6B6B;}
.pill-amber{background: rgba(255,200,60,0.16); color: rgba(255,200,60,0.98);}
.pill-green{background: rgba(80,255,120,0.16); color:#7CFC9A;}

.metric-grid{
  display:grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px 14px;
}
.metric-row{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap: 10px;
  padding: 6px 10px;
  border-radius: 10px;
  border: 1px solid rgba(255,255,255,0.08);
  background: rgba(255,255,255,0.02);
}
.metric-row .k{opacity:0.85; font-weight:800;}
.metric-row .v{font-weight:950;}

.kv{
  display:flex;
  align-items:baseline;
  justify-content:space-between;
  gap: 10px;
  padding: 6px 10px;           /* tighter */
  border-radius: 10px;
  border: 1px solid rgba(255,255,255,0.08);
  background: rgba(255,255,255,0.02);
  margin-bottom: 7px;          /* tighter */
}
.kv .k{opacity:0.82; font-weight:850;}
.kv .v{font-weight:950;}

.snapshot-label{
  opacity: 0.85;
  font-weight: 900;
  font-size: 0.9rem;
  letter-spacing: 0.2px;
  text-transform: uppercase;
  margin: 4px 0 10px 0;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ============================================================
# LOCKED MANUAL INPUTS (EDIT WEEKLY HERE)
# ============================================================
MANUAL_ASOF_LABEL = "Manual inputs updated: 2026-01-09"

MANUAL_INPUTS = {
    "Stock Market Exposure": {"Exposure": "40-60%"},
    "Market Type": {"Type": "Bull Quiet"},
    "Trend Condition (QQQ)": {
        "Above 5DMA": "Yes",
        "Above 10DMA": "Yes",
        "Above 20DMA": "Yes",
        "Above 50DMA": "Yes",
        "Above 200DMA": "No",
    },
    "Nasdaq Net 52-Week New High/Low": {"Daily": 231, "Weekly": 811, "Monthly": -828},
    "Market Indicators": {
        "VIX": 16.34,
        "PCC": 0.67,
        "Credit (IEI vs HYG)": "Aligned",
        "U.S. Dollar": "Downtrend",
        "DXY Price": 103.25,
        "Distribution Days": 2,
        "Up/Down Volume (Daily)": 2.36,
        "Up/Down Volume (Weekly)": 2.10,
        "Up/Down Volume (Monthly)": 1.80,
        "A/D Ratio (Daily)": 2.20,
        "A/D Ratio (Weekly)": 1.95,
        "A/D Ratio (Monthly)": 1.70,
    },
    "Macro": {"Fed Funds": 4.09, "M2 Money": 22.2, "10yr": 4.02},
    "Breadth & Participation": {
        "% Price Above 10DMA": 56,
        "% Price Above 20DMA": 49,
        "% Price Above 50DMA": 58,
        "% Price Above 200DMA": 68,
    },
    "Composite Model": {
        "Monetary Policy": 1.0,
        "Liquidity Flow": 2.0,
        "Rates & Credit": 2.0,
        "Tape Strength": 2.0,
        "Sentiment": 1.0,
    },
    "Hot Sectors / Industry Groups": {"Notes": ""},
    "Market Correlations": {"Correlated": "Dow, Nasdaq", "Uncorrelated": "Dollar, Bonds"},
}

EXPOSURE_PILL = {
    "0-20%": "pill pill-red",
    "20-40%": "pill pill-amber",
    "40-60%": "pill pill-green",
    "60-80%": "pill pill-green",
    "80-100%": "pill pill-green",
}


def _yesno_badge(v: str) -> str:
    v = str(v).strip().lower()
    if v in ["yes", "y", "true", "1"]:
        return '<span class="badge badge-yes">YES</span>'
    if v in ["no", "n", "false", "0"]:
        return '<span class="badge badge-no">NO</span>'
    return '<span class="badge badge-neutral">—</span>'


def _num_color(v):
    try:
        v = float(v)
    except Exception:
        return "opacity:0.85; font-weight:950;"
    if v > 0:
        return "color:#7CFC9A; font-weight:950;"
    if v < 0:
        return "color:#FF6B6B; font-weight:950;"
    return "opacity:0.85; font-weight:950;"


def _score_to_label(score: float):
    try:
        score = float(score)
    except Exception:
        score = 1.0
    if score <= 0.5:
        return ("Bad", "badge badge-no")
    if score < 1.5:
        return ("Neutral", "badge badge-neutral")
    return ("Good", "badge badge-yes")


def _total_score_pill(total: float) -> str:
    try:
        total = float(total)
    except Exception:
        total = 0.0
    if total >= 7.0:
        return "pill pill-green"
    if total >= 5.0:
        return "pill pill-amber"
    return "pill pill-red"


def _kv(label: str, value_html: str):
    st.markdown(
        f'<div class="kv"><div class="k">{label}</div><div class="v">{value_html}</div></div>',
        unsafe_allow_html=True,
    )


def _pill_for_market_type(mt: str) -> str:
    mt = (mt or "").strip().lower()
    if mt in ["bull quiet", "bull volatile"]:
        return "pill pill-green"
    if mt in ["bear quiet", "bear volatile"]:
        return "pill pill-red"
    if mt in ["sideways quiet", "sideways volatile"]:
        return "pill pill-amber"
    return "pill pill-amber"


def _pill_for_credit(val: str) -> str:
    v = (val or "").strip().lower()
    if v == "aligned":
        return "pill pill-green"
    if v in ["divergent", "divergence"]:
        return "pill pill-red"
    return "pill pill-amber"


def _pill_for_dollar(val: str) -> str:
    v = (val or "").strip().lower()
    if v == "downtrend":
        return "pill pill-green"
    if v == "uptrend":
        return "pill pill-red"
    if v == "sideways":
        return "pill pill-amber"
    return "pill pill-amber"


# -------------------------
# SECTION 1: Market Data
# -------------------------
def render_market_data(mi: dict):
    st.markdown('<div class="snapshot-label">Screenshot 1: Market Data Snapshot</div>', unsafe_allow_html=True)

    # 3-column top area for a clean single screenshot
    c1, c2, c3 = st.columns([1.05, 1.25, 1.15])

    with c1:
        st.markdown('<div class="card"><h3>Stock Market Exposure</h3>', unsafe_allow_html=True)
        ex = str(mi.get("Stock Market Exposure", {}).get("Exposure", "")).strip()
        pill_class = EXPOSURE_PILL.get(ex, "pill pill-amber")
        st.markdown(f'Current: <span class="{pill_class}">{ex or "—"}</span>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card"><h3>Market Type</h3>', unsafe_allow_html=True)
        mt = str(mi.get("Market Type", {}).get("Type", "")).strip()
        _kv("Type", f'<span class="{_pill_for_market_type(mt)}">{mt or "—"}</span>')
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card"><h3>Trend Condition (QQQ)</h3><div class="hint">Simple yes/no filters.</div>', unsafe_allow_html=True)
        tc = mi.get("Trend Condition (QQQ)", {}) or {}
        keys = ["Above 5DMA", "Above 10DMA", "Above 20DMA", "Above 50DMA", "Above 200DMA"]
        for k in keys:
            _kv(k, _yesno_badge(tc.get(k, "—")))
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card"><h3>Nasdaq Net 52-Week New High/Low</h3><div class="hint">Positive = green, negative = red.</div>', unsafe_allow_html=True)
        hl = mi.get("Nasdaq Net 52-Week New High/Low", {}) or {}
        d = hl.get("Daily", "")
        w = hl.get("Weekly", "")
        m = hl.get("Monthly", "")
        st.markdown(
            f"""
            <div class="metric-grid">
              <div class="metric-row"><div class="k">Daily</div><div class="v" style="{_num_color(d)}">{d}</div></div>
              <div class="metric-row"><div class="k">Weekly</div><div class="v" style="{_num_color(w)}">{w}</div></div>
              <div class="metric-row"><div class="k">Monthly</div><div class="v" style="{_num_color(m)}">{m}</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card"><h3>Market Indicators</h3><div class="hint">Tape / sentiment inputs.</div>', unsafe_allow_html=True)
        ind = mi.get("Market Indicators", {}) or {}

        _kv("VIX", f'{ind.get("VIX","—")}')
        _kv("Put/Call (PCC)", f'{ind.get("PCC","—")}')

        credit_val = str(ind.get("Credit (IEI vs HYG)", "—"))
        _kv("Credit (IEI vs HYG)", f'<span class="{_pill_for_credit(credit_val)}">{credit_val}</span>')

        dollar_val = str(ind.get("U.S. Dollar", "—"))
        _kv("U.S. Dollar", f'<span class="{_pill_for_dollar(dollar_val)}">{dollar_val}</span>')

        _kv("DXY Price", f'{ind.get("DXY Price","—")}')
        _kv("Distribution Days", f'{ind.get("Distribution Days","—")}')

        st.markdown('<div class="small-muted" style="margin: 8px 0 6px 0;"><b>Up/Down Volume Ratio</b></div>', unsafe_allow_html=True)
        _kv("Daily", f'{ind.get("Up/Down Volume (Daily)","—")}')
        _kv("Weekly", f'{ind.get("Up/Down Volume (Weekly)","—")}')
        _kv("Monthly", f'{ind.get("Up/Down Volume (Monthly)","—")}')

        st.markdown('<div class="small-muted" style="margin: 10px 0 6px 0;"><b>Advance/Decline Ratio</b></div>', unsafe_allow_html=True)
        _kv("Daily", f'{ind.get("A/D Ratio (Daily)","—")}')
        _kv("Weekly", f'{ind.get("A/D Ratio (Weekly)","—")}')
        _kv("Monthly", f'{ind.get("A/D Ratio (Monthly)","—")}')

        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="card"><h3>Macro</h3><div class="hint">High-level backdrop.</div>', unsafe_allow_html=True)
        mac = mi.get("Macro", {}) or {}
        _kv("Fed Funds", f'{mac.get("Fed Funds","—")}')
        _kv("M2 Money", f'{mac.get("M2 Money","—")}')
        _kv("10yr", f'{mac.get("10yr","—")}')
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card"><h3>Breadth & Participation</h3><div class="hint">Percent above key moving averages.</div>', unsafe_allow_html=True)
        br = mi.get("Breadth & Participation", {}) or {}
        _kv("% Price Above 10DMA", f'{br.get("% Price Above 10DMA","—")}%')
        _kv("% Price Above 20DMA", f'{br.get("% Price Above 20DMA","—")}%')
        _kv("% Price Above 50DMA", f'{br.get("% Price Above 50DMA","—")}%')
        _kv("% Price Above 200DMA", f'{br.get("% Price Above 200DMA","—")}%')
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card"><h3>Hot Sectors / Industry Groups</h3>', unsafe_allow_html=True)
        hs = mi.get("Hot Sectors / Industry Groups", {}) or {}
        notes = str(hs.get("Notes", "") or "").strip()
        st.markdown(notes if notes else "_(none)_")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card"><h3>Market Correlations</h3>', unsafe_allow_html=True)
        mc = mi.get("Market Correlations", {}) or {}
        _kv("Correlated", f'{mc.get("Correlated","—")}')
        _kv("Uncorrelated", f'{mc.get("Uncorrelated","—")}')
        st.markdown("</div>", unsafe_allow_html=True)


# -------------------------
# SECTION 2: Composite Model
# -------------------------
def render_composite_section(mi: dict):
    st.markdown('<div class="snapshot-label">Screenshot 2: Composite Model Snapshot</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><h3>Composite Model</h3><div class="hint">0.0–2.0 each • Total out of 10.</div>', unsafe_allow_html=True)

    cm = mi.get("Composite Model", {}) or {}
    components = ["Monetary Policy", "Liquidity Flow", "Rates & Credit", "Tape Strength", "Sentiment"]

    total = 0.0
    for comp in components:
        v = float(cm.get(comp, 0.0) or 0.0)
        total += v
        lbl, cls = _score_to_label(v)

        if v <= 0.5:
            score_pill = "pill pill-red"
        elif v < 1.5:
            score_pill = "pill pill-amber"
        else:
            score_pill = "pill pill-green"

        _kv(comp, f'<span class="{cls}">{lbl.upper()}</span> <span class="{score_pill}">{v:.1f}</span>')

    total_pill = _total_score_pill(total)
    st.markdown(
        f'<div style="margin-top:10px;"><b>Total Score:</b> <span class="{total_pill}">{total:.1f}</span> <span class="small-muted">/ 10.0</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# UI
# =========================
st.title("Big Picture Market Pulse")
st.caption(f"As of: {_asof_ts()}")
st.caption(MANUAL_ASOF_LABEL)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# Screenshot block 1
render_market_data(MANUAL_INPUTS)

# Big divider between screenshot zones
st.markdown('<div class="hr-big"></div>', unsafe_allow_html=True)

# Screenshot block 2
render_composite_section(MANUAL_INPUTS)
