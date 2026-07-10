import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # headless backend — required on Streamlit Cloud, where the
                       # default backend can segfault inside Streamlit's threads
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager

# Georgia exists on macOS/Windows but not on Streamlit Cloud's Linux servers,
# where asking for it floods the log with findfont errors. Fall back to
# DejaVu Serif, which ships with matplotlib and is available everywhere.
_installed_fonts = {f.name for f in font_manager.fontManager.ttflist}
CHART_FONT = "Georgia" if "Georgia" in _installed_fonts else "DejaVu Serif"

# Readable, on-brand defaults for every chart (serif, larger type than the
# old 8–10px). Explicit sizes in each chart still win where set.
plt.rcParams.update({
    "font.family": CHART_FONT,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
})

# ======================
# DESIGN SYSTEM
# ======================

DESIGN = {
    "font": "Georgia, serif",

    "colors": {
        "primary": "#2E3EED",
        "secondary": "#ACA9BE",
        "dark": "#7A749B",
        "sidebar": "#F6CAA8",
        "background": "#F8F9FA",
        "text": "#000000"
    },

    "sizes": {
        "main_title": "42px",
        "section_title": "26px",
        "sub_title": "20px",
        "body": "16px"
    }
}


# ======================
# SEMANTIC COLOR PALETTE
# ======================

COLOR_LOW = "#3C9D6B"      # Low risk / non-smoker — muted green
COLOR_MEDIUM = "#E8B86D"   # Medium risk — muted gold
COLOR_HIGH = "#ED5F5F"     # High risk / smoker — muted red
COLOR_PRIMARY = "#2E3EED"  # Neutral accent — general bars, KPIs, premium
COLOR_NEUTRAL = "#7A749B"  # Neutral gray — cost (pre-markup), non-risk-coded charts

RISK_ORDER = ["Low", "Medium", "High"]
RISK_PALETTE = [COLOR_LOW, COLOR_MEDIUM, COLOR_HIGH]

SMOKER_ORDER = ["no", "yes"]
SMOKER_PALETTE = {"no": COLOR_LOW, "yes": COLOR_HIGH}
# ======================
# FORMATTING FUNCTIONS
# ======================

def chart_header(text):
    st.markdown(
        f"""
        <p style="
        font-family:{DESIGN['font']};
        font-size:15px;
        font-weight:bold;
        margin-bottom:6px;
        white-space:nowrap;
        ">
        {text}
        </p>
        """,
        unsafe_allow_html=True
    )


def chart_caption(text):
    st.markdown(
        f"""
        <p style="
        font-family:{DESIGN['font']};
        font-size:10px;
        color:#666666;
        height:40px;
        line-height:1.3;
        text-align:center;
        margin-top:-8px;
        margin-bottom:0px;
        ">
        {text}
        </p>
        """,
        unsafe_allow_html=True
    )


def metric_card(label, value, color="#2E3EED"):
    """Blue score card with a white label and value."""
    st.markdown(
        f"""
<div style="background-color:{color}; padding:12px; border-radius:10px; text-align:center;">
    <div style="color:white; font-size:13px; font-weight:600;">
        {label}
    </div>
    <div style="color:white; font-size:20px; font-weight:bold; margin-top:4px;">
        {value}
    </div>
</div>
""",
        unsafe_allow_html=True,
    )


# CONFIG
# ======================
st.set_page_config(page_title="Insurance Dashboard", layout="wide")
# ======================
# GLOBAL PAGE STYLE
# ======================

st.markdown(
    """
    <style>

    /* ======================
       GLOBAL FONT
       ====================== */
    html, body, [class*="css"],
    .stApp,
    .stMarkdown,
    .stText,
    p,
    label,
    input,
    textarea {
        font-family: Georgia, serif !important;
    }


    /* ======================
       SIDEBAR
       ====================== */

    /* Sidebar background */
section[data-testid="stSidebar"] {
    background-color: #F6CAA8 !important;
}


    /* Sidebar font */
    section[data-testid="stSidebar"] * {
        font-family: Georgia, serif !important;
    }


    /* About this project title */
    section[data-testid="stSidebar"] h1 {
        color: black !important;
        font-size: 26px !important;
        font-weight: bold !important;
    }


    /* Objectives / Tools / Data */
    section[data-testid="stSidebar"] h3 {
        color: black !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }


    /* Sidebar body text */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] label {
        color: black !important;
        font-size: 16px !important;
    }


    /* ======================
       FILTER COLORS
       ====================== */

    /* Selected values in multiselect */
    div[data-baseweb="tag"] {
        background-color: #2E3EED !important;
        color: white !important;
    }


    /* Slider handle */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #2E3EED !important;
        border-color: #2E3EED !important;
    }


    /* Slider active range */
    .stSlider [data-baseweb="slider"] div[role="presentation"] {
        background-color: #2E3EED !important;
    }


    /* ======================
       TITLE SIZE
       ====================== */

    h1 {
        font-size: 42px !important;
        font-weight: bold !important;
    }


    h2 {
        font-size: 26px !important;
        font-weight: bold !important;
    }


    h3 {
        font-size: 20px !important;
        font-weight: bold !important;
    }

    /* Headings inherit Georgia from the global font rule above */
    h1, h2, h3, h4, h5, h6 {
        font-family: Georgia, serif !important;
    }

/* ======================
   PAGE SIDE MARGINS
   ====================== */

.block-container {
    padding-left: 10.5rem !important;
    padding-right: 10.5rem !important;
}


/* ======================
   STICKY TOP FILTER BAR
   ====================== */

/* The filters live in st.container(key="filter_bar"). A sticky element only
   sticks WITHIN its parent's box, so pinning the inner keyed div fails (its
   wrapper is only as tall as the bar). Instead we make sticky the wrapper
   that is a DIRECT child of the tall page column — that gives it the full
   page height to travel over, so it truly freezes at the top on scroll. */
[data-testid="stMainBlockContainer"] div[data-testid="stVerticalBlock"] > div:has(.st-key-filter_bar),
.block-container div[data-testid="stVerticalBlock"] > div:has(.st-key-filter_bar) {
    position: sticky;
    top: 3.5rem;                 /* just below Streamlit's top header */
    z-index: 1000;
    background-color: #FFFFFF;
}

/* Fallback: also pin the keyed element itself, in case the key class lands
   directly on the flex-child wrapper in this Streamlit version. */
.st-key-filter_bar {
    position: sticky;
    top: 3.5rem;
    z-index: 1000;
    background-color: #FFFFFF;
    padding: 14px 20px 4px 20px;
    border-radius: 10px;
    margin-bottom: 18px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

/* Tighten the spacing of the widgets inside the sticky bar */
.st-key-filter_bar [data-testid="stVerticalBlock"] {
    gap: 0.4rem;
}

/* Selected filter chips (yes / no, region names): blue background + white
   text, matching the three KPI score cards. */
.st-key-filter_bar div[data-baseweb="tag"] {
    background-color: #2E3EED !important;
}
.st-key-filter_bar div[data-baseweb="tag"] span,
.st-key-filter_bar div[data-baseweb="tag"] svg {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}

/* Streamlit renders a thin header strip at the very top; make it opaque
   white so scrolling content never shows through above the pinned bar. */
[data-testid="stHeader"] {
    background-color: #FFFFFF !important;
}



    </style>
    """,
    unsafe_allow_html=True
)


# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    return pd.read_csv("insurance.csv")


df = load_data()


# ======================
# FILTERS (STICKY TOP BAR)
# ======================
# Placed at the top of the main page (not the sidebar) so every visitor
# sees them, and pinned via CSS (.st-key-filter_bar) so they stay usable
# while scrolling.
with st.container(key="filter_bar"):
    st.markdown(
        f"""
        <p style="font-family:{DESIGN['font']}; font-weight:bold;
        font-size:15px; color:#000000; margin:0 0 2px 0;">
        🔎 Filters — adjust the portfolio view
        </p>
        """,
        unsafe_allow_html=True
    )

    fcol1, fcol2, fcol3 = st.columns(3)

    with fcol1:
        selected_region = st.multiselect(
            "Region",
            df["region"].unique(),
            default=list(df["region"].unique())
        )

    with fcol2:
        selected_smoker = st.multiselect(
            "Smoker",
            df["smoker"].unique(),
            default=list(df["smoker"].unique())
        )

    with fcol3:
        age_range = st.slider(
            "Age Range",
            int(df["age"].min()),
            int(df["age"].max()),
            (18, 64)
        )


# ======================
# TITLE (CENTERED)
# ======================

st.markdown(
    f"""
<div style="background-color:{DESIGN['colors']['sidebar']}; padding:25px; border-radius:12px; text-align:center; margin-bottom:20px;">
<h1 style="color:{COLOR_PRIMARY}; font-size:42px; font-weight:bold; margin-bottom:5px;">
Health Insurance Portfolio Analytics
</h1>

<p style="color:#555555; font-size:18px; margin-top:0;">
Executive Overview • Risk Drivers • Portfolio Structure
</p>

</div>
""",
    unsafe_allow_html=True
)


# ======================
# ABOUT (MAIN PAGE, COLLAPSIBLE)
# ======================
# Kept on the main page rather than the sidebar so first-time visitors can
# actually find it. Expanded by default so the context is seen at least once.
with st.expander("ℹ️  About this dashboard — what it shows & how to use it", expanded=True):
    st.markdown("""
This dashboard helps you understand what drives medical costs in our portfolio,
identify which member segments carry the most risk, and see how pricing
decisions affect our margin.

**What you can do here**
- Use the filter bar at the top to slice the portfolio by region, smoking status, and age
- Adjust the per-tier **Premium Markup** sliders (in the Pricing section) to see how pricing affects profit
- See which factors (smoking, age, risk tier) drive cost the most
- Compare current costs against proposed premiums by risk segment

**About the data** — Synthetic health insurance dataset (1,338 members) tracking
age, BMI, smoking status, region, and annual medical charges.
""")


# Apply filters
df = df[
   (df["region"].isin(selected_region)) &
   (df["smoker"].isin(selected_smoker)) &
   (df["age"].between(age_range[0], age_range[1]))
]

# Stop early if the current filters leave no members — otherwise every
# downstream chart and metric would error on an empty dataset.
if df.empty:
    st.warning(
        "No members match the current filters. "
        "Please select at least one region and smoker status, "
        "and widen the age range."
    )
    st.stop()
# ======================
# CREATE RISK SCORE
# ======================


df["risk_score"] = (
   (df["age"] >= 50).astype(int) +
   (df["bmi"] >= 30).astype(int) +
   (df["smoker"] == "yes").astype(int)
)
# ======================
# CREATE RISK TIERS
# ======================


def get_tier(score):
   if score <= 1:
       return "Low"
   elif score == 2:
       return "Medium"
   else:
       return "High"


df["risk_tier"] = df["risk_score"].apply(get_tier)


# ======================
# PORTFOLIO SNAPSHOT (SCORE CARDS)
# ======================

st.markdown("## Portfolio Snapshot")

# Six headline metrics for the filtered portfolio, shown as blue score cards.
snapshot_metrics = [
    ("Total Members", f"{len(df):,}"),
    # One decimal: whole-year rounding shows "39" for every region/smoker
    # slice (segment averages differ by <1 year), which reads as a frozen card.
    ("Avg Age", f"{df['age'].mean():.1f}"),
    ("Avg BMI", f"{df['bmi'].mean():.1f}"),
    ("Median Cost", f"${df['charges'].median():,.0f}"),
    ("Average Cost", f"${df['charges'].mean():,.0f}"),
    ("Highest Cost", f"${df['charges'].max():,.0f}"),
]

for col, (label, value) in zip(st.columns(6), snapshot_metrics):
    with col:
        metric_card(label, value)


# ======================
# KEY TAKEAWAYS (data-driven, shown up top so the story lands before scrolling)
# ======================
takeaways = []

smk = df.groupby("smoker")["charges"].mean()
if {"yes", "no"} <= set(smk.index) and smk["no"] > 0:
    takeaways.append(
        f"🚬 <b>Smokers cost {smk['yes'] / smk['no']:.1f}× more</b> than non-smokers "
        f"(${smk['yes']:,.0f} vs ${smk['no']:,.0f} on average)."
    )

tier_means = df.groupby("risk_tier")["charges"].mean()
if {"Low", "High"} <= set(tier_means.index) and tier_means["Low"] > 0:
    takeaways.append(
        f"📈 Average cost climbs <b>{tier_means['High'] / tier_means['Low']:.1f}×</b> from "
        f"Low (${tier_means['Low']:,.0f}) to High (${tier_means['High']:,.0f}) risk."
    )

high_share = (df["risk_tier"] == "High").mean()
takeaways.append(
    f"⚠️ <b>{high_share:.0%} of members are High-risk</b> — a small group that is the "
    f"most expensive per head and a concentrated cost center."
)

st.markdown(
    f"""
    <div style="background-color:#F1F3FF; border-left:5px solid {COLOR_PRIMARY};
        border-radius:8px; padding:14px 18px; margin-top:14px; font-family:{DESIGN['font']};">
        <div style="font-weight:bold; font-size:16px; color:{COLOR_PRIMARY}; margin-bottom:6px;">
            Key Takeaways
        </div>
        <ul style="margin:0; padding-left:20px; font-size:15px; color:#000000;">
            {''.join(f'<li style="margin-bottom:4px;">{t}</li>' for t in takeaways)}
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")


# ======================
# RISK VISUALS
# ======================

st.markdown("## Risk Driver Analysis")

# ======================
# COST DRIVER IMPORTANCE (standardized OLS)
# ======================
# Substantiates the "smoking is the strongest driver" claim with numbers:
# fit cost on standardized smoking / age / BMI, then compare the absolute
# standardized coefficients (larger = bigger effect per standard deviation).
driver_df = df.copy()
driver_df["smoker_bin"] = (driver_df["smoker"] == "yes").astype(int)
driver_labels = {"smoker_bin": "Smoking", "age": "Age", "bmi": "BMI"}

# Drop predictors with no variation (e.g. smoker filtered to one value → std 0).
usable = [p for p in ["smoker_bin", "age", "bmi"] if driver_df[p].std() > 0]

if usable and df["charges"].std() > 0:
    X = driver_df[usable].apply(lambda c: (c - c.mean()) / c.std()).to_numpy()
    y = ((driver_df["charges"] - driver_df["charges"].mean()) / df["charges"].std()).to_numpy()
    design = np.column_stack([np.ones(len(y)), X])
    coefs, *_ = np.linalg.lstsq(design, y, rcond=None)

    importance = (
        pd.DataFrame({"driver": [driver_labels[p] for p in usable], "weight": np.abs(coefs[1:])})
        .sort_values("weight")
    )

    # Headline chart on the left, plain-language reading on the right, so the
    # single wide bar doesn't float alone in the middle of the page.
    dcol1, dcol2 = st.columns([3, 2], vertical_alignment="center")
    with dcol1:
        chart_header("What drives cost the most? (standardized effect size)")
        figd, axd = plt.subplots(figsize=(6, 2.6))
        axd.barh(importance["driver"], importance["weight"], color=COLOR_PRIMARY, edgecolor="white")
        axd.set_xlabel("Relative importance  ( |standardized coefficient| )", fontsize=11, fontname=CHART_FONT)
        axd.tick_params(labelsize=10)
        for lab in axd.get_xticklabels() + axd.get_yticklabels():
            lab.set_fontname(CHART_FONT)
        st.pyplot(figd, use_container_width=True)
        plt.close(figd)
    with dcol2:
        st.markdown(
            f"""
            <div style="font-family:{DESIGN['font']}; font-size:15px; color:#000000;">
            <b style="color:{COLOR_PRIMARY};">How to read this</b><br>
            Each bar is a factor's effect on cost per standard deviation, holding the
            others fixed. <b>Smoking's effect is several times larger than age or BMI</b> —
            so pricing should lean hardest on smoking status, treating age and BMI as
            secondary adjustments.
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("#### Cost drivers in detail")
col1, col2, col3, col4 = st.columns(4)

# ======================
# 1. COST DISTRIBUTION
# ======================
with col1:
    chart_header("Cost Distribution")

    fig1, ax1 = plt.subplots(figsize=(4, 3))

    # Overlay by smoker — the cost distribution is bimodal, and the second
    # (higher) hump is almost entirely smokers. A single-color histogram hides
    # that; splitting it tells the real story.
    bins = 15
    for grp, color, lbl in [("no", COLOR_LOW, "Non-Smoker"), ("yes", COLOR_HIGH, "Smoker")]:
        vals = df.loc[df["smoker"] == grp, "charges"]
        if not vals.empty:
            ax1.hist(vals, bins=bins, color=color, edgecolor="white", alpha=0.75, label=lbl)

    ax1.set_title("Medical Cost Distribution", fontsize=13, fontname=CHART_FONT)
    ax1.set_xlabel("Annual Medical Cost ($)", fontsize=11, fontname=CHART_FONT)
    ax1.set_ylabel("Number of Members", fontsize=11, fontname=CHART_FONT)
    # Compact $k labels — full amounts ($10,000, $20,000, …) are wider than
    # the tick spacing in this small chart and collide into one another.
    ax1.xaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: "$0" if x == 0 else f"${x / 1000:,.0f}k")
    )
    ax1.tick_params(labelsize=10)
    ax1.legend(fontsize=9, title_fontsize=10)

    for label in ax1.get_xticklabels():
        label.set_fontname(CHART_FONT)
    for label in ax1.get_yticklabels():
        label.set_fontname(CHART_FONT)

    st.pyplot(fig1, use_container_width=False)
    plt.close(fig1)
    chart_caption("Costs are bimodal: a low-cost cluster and a higher second hump made up almost entirely of smokers.")


# ======================
# 2. COST SPREAD (BOX PLOT)
# ======================
with col2:
    chart_header("Cost Spread: Smoker vs Non-Smoker")

    fig2b, ax2b = plt.subplots(figsize=(4, 3))

    sns.boxplot(
        data=df,
        x="smoker",
        y="charges",
        order=SMOKER_ORDER,
        hue="smoker",
        hue_order=SMOKER_ORDER,
        palette=SMOKER_PALETTE,
        legend=False,
        ax=ax2b
    )

    ax2b.set_title("Cost Spread by Smoking Status", fontsize=13, fontname=CHART_FONT)
    ax2b.set_xlabel("Smoking Status", fontsize=11, fontname=CHART_FONT)
    ax2b.set_ylabel("Annual Medical Cost ($)", fontsize=11, fontname=CHART_FONT)
    ax2b.set_xticklabels(["Non-Smoker", "Smoker"], fontname=CHART_FONT)
    ax2b.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"${y:,.0f}"))
    ax2b.tick_params(labelsize=10)

    st.pyplot(fig2b, use_container_width=False)
    plt.close(fig2b)
    chart_caption("Smokers show both higher and more variable costs.")

# ======================
# 3. SMOKING IMPACT (BAR OF AVERAGES)
# ======================
with col3:
    chart_header("Smoking Impact")

    smoker_cost = df.groupby("smoker")["charges"].mean().reindex(["no", "yes"]).reset_index()

    fig2, ax2 = plt.subplots(figsize=(4, 3))

    sns.barplot(
        data=smoker_cost,
        x="smoker",
        y="charges",
        order=SMOKER_ORDER,
        hue="smoker",
        hue_order=SMOKER_ORDER,
        palette=SMOKER_PALETTE,
        legend=False,
        ax=ax2
    )

    ax2.set_title("Average Cost: Smoker vs Non-Smoker", fontsize=13, fontname=CHART_FONT)
    ax2.set_xlabel("Smoking Status", fontsize=11, fontname=CHART_FONT)
    ax2.set_ylabel("Average Medical Cost ($)", fontsize=11, fontname=CHART_FONT)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"${y:,.0f}"))
    ax2.set_xticklabels(["Non-Smoker", "Smoker"], fontname=CHART_FONT)
    ax2.tick_params(labelsize=10)

    for label in ax2.get_yticklabels():
        label.set_fontname(CHART_FONT)

    st.pyplot(fig2, use_container_width=False)
    plt.close(fig2)
    chart_caption("The smoker/non-smoker gap dwarfs every other factor — it's the portfolio's main cost lever.")


# ======================
# 4. AGE VS COST
# ======================
with col4:
    chart_header("Age vs Cost")

    fig3, ax3 = plt.subplots(figsize=(4, 3))

    sns.scatterplot(
        data=df,
        x="age",
        y="charges",
        hue="smoker",
        hue_order=SMOKER_ORDER,
        palette=SMOKER_PALETTE,
        alpha=0.5,
        ax=ax3
    )

    ax3.set_title("Age vs Annual Medical Cost", fontsize=13, fontname=CHART_FONT)
    ax3.set_xlabel("Age", fontsize=11, fontname=CHART_FONT)
    ax3.set_ylabel("Annual Medical Cost ($)", fontsize=11, fontname=CHART_FONT)
    ax3.legend(title="Smoker", fontsize=10, title_fontsize=11)
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"${y:,.0f}"))
    ax3.tick_params(labelsize=10)

    for label in ax3.get_xticklabels():
        label.set_fontname(CHART_FONT)
    for label in ax3.get_yticklabels():
        label.set_fontname(CHART_FONT)

    st.pyplot(fig3, use_container_width=False)
    plt.close(fig3)
    chart_caption("Cost rises gently with age, but splits into three bands — smokers (red) form the two costly upper bands.")

st.markdown("---")
st.markdown("## Risk Scoring & Segmentation")

st.caption(
    "Each member scores 1 point per risk factor — **age ≥ 50**, **BMI ≥ 30**, and "
    "**smoker** — for a 0–3 score. Tiers: **Low** = 0–1, **Medium** = 2, **High** = 3. "
    "Thresholds are simple rules of thumb, not clinical cut-offs."
)

# ======================
# RISK SCORING & SEGMENTATION (3 COLUMNS)
# ======================

col1, col2, col3 = st.columns(3)


# ======================
# RISK SCORE DISTRIBUTION
# ======================
with col1:

    chart_header("Risk Score Distribution")

    fig4, ax4 = plt.subplots(figsize=(4, 3))


    sns.countplot(
        data=df,
        x="risk_score",
        color=COLOR_NEUTRAL,
        ax=ax4
    )


    ax4.set_title(
        "Member Distribution by Risk Score",
        fontsize=13,
        fontname=CHART_FONT
    )


    ax4.set_xlabel(
        "Risk Score",
        fontsize=11,
        fontname=CHART_FONT
    )


    ax4.set_ylabel(
        "Number of Members",
        fontsize=11,
        fontname=CHART_FONT
    )


    ax4.tick_params(labelsize=10)


    for label in ax4.get_xticklabels():
        label.set_fontname(CHART_FONT)

    for label in ax4.get_yticklabels():
        label.set_fontname(CHART_FONT)


    st.pyplot(fig4, use_container_width=False)
    plt.close(fig4)
    chart_caption("Most members combine zero or one risk factor.")



# ======================
# RISK TIER BREAKDOWN
# ======================
with col2:

    chart_header("Risk Tier Breakdown")


    tier_summary = (
        df["risk_tier"]
        .value_counts()
        .reindex(RISK_ORDER, fill_value=0)   # order Low → Medium → High
        .reset_index()
    )
    tier_summary.columns = ["risk_tier", "members"]


    fig5, ax5 = plt.subplots(figsize=(4, 3))



    sns.barplot(
        data=tier_summary,
        x="risk_tier",
        y="members",
        order=RISK_ORDER,
        hue="risk_tier",
        hue_order=RISK_ORDER,
        palette=RISK_PALETTE,
        legend=False,
        ax=ax5
    )


    ax5.set_title(
        "Members by Risk Tier",
        fontsize=13,
        fontname=CHART_FONT
    )


    ax5.set_xlabel(
        "Risk Tier",
        fontsize=11,
        fontname=CHART_FONT
    )


    ax5.set_ylabel(
        "Number of Members",
        fontsize=11,
        fontname=CHART_FONT
    )


    ax5.tick_params(labelsize=10)


    for label in ax5.get_xticklabels():
        label.set_fontname(CHART_FONT)

    for label in ax5.get_yticklabels():
        label.set_fontname(CHART_FONT)


    st.pyplot(fig5, use_container_width=False)
    plt.close(fig5)
    chart_caption("Most members sit in the Low tier; High-risk is a small but disproportionately costly minority.")




# ======================
# COST BY RISK TIER
# ======================
with col3:
    chart_header("Cost Spread by Risk Tier")

    fig6, ax6 = plt.subplots(figsize=(4, 3))

    sns.boxplot(
        data=df,
        x="risk_tier",
        y="charges",
        order=RISK_ORDER,
        hue="risk_tier",
        hue_order=RISK_ORDER,
        palette=RISK_PALETTE,
        legend=False,
        ax=ax6
    )

    ax6.set_title("Cost Spread by Risk Tier", fontsize=13, fontname=CHART_FONT)
    ax6.set_xlabel("Risk Tier", fontsize=11, fontname=CHART_FONT)
    ax6.set_ylabel("Annual Medical Cost ($)", fontsize=11, fontname=CHART_FONT)
    ax6.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"${y:,.0f}"))
    ax6.tick_params(labelsize=10)

    for label in ax6.get_xticklabels():
        label.set_fontname(CHART_FONT)

    for label in ax6.get_yticklabels():
        label.set_fontname(CHART_FONT)

    st.pyplot(fig6, use_container_width=False)
    plt.close(fig6)
    chart_caption("Typical cost climbs sharply by tier; the Low tier is the most spread out, while the small High tier is uniformly expensive.")

st.markdown("---")
st.markdown("## Risk-Based Pricing")

# ======================
# PRICING ASSUMPTIONS (per-tier markup)
# ======================
# Higher tiers carry far more cost *variance* (tail risk), so charging them a
# larger margin than low-risk members reflects real risk loading — unlike a
# single flat markup applied to every tier.
with st.expander("⚙️  Pricing assumptions — set the premium markup for each risk tier", expanded=True):
    mcol1, mcol2, mcol3 = st.columns(3)
    with mcol1:
        markup_low = st.slider("Low-risk markup (%)", 0, 100, 10, step=5)
    with mcol2:
        markup_med = st.slider("Medium-risk markup (%)", 0, 100, 20, step=5)
    with mcol3:
        markup_high = st.slider("High-risk markup (%)", 0, 100, 35, step=5)

tier_markup = {"Low": markup_low, "Medium": markup_med, "High": markup_high}


# ======================
# PREMIUM MODEL (per-tier markup)
# ======================
pricing = df.groupby("risk_tier").agg(
   avg_cost=("charges", "mean"),
   members=("charges", "count")
).reset_index()

# Order tiers Low → Medium → High (groupby returns them alphabetically),
# keeping only tiers present after filtering.
pricing["risk_tier"] = pd.Categorical(
    pricing["risk_tier"], categories=RISK_ORDER, ordered=True
)
pricing = pricing.sort_values("risk_tier").reset_index(drop=True)

pricing["markup_%"] = pricing["risk_tier"].map(tier_markup).astype(float)
pricing["premium"] = pricing["avg_cost"] * (1 + pricing["markup_%"] / 100)
pricing["profit_per_member"] = pricing["premium"] - pricing["avg_cost"]
pricing["total_profit"] = pricing["profit_per_member"] * pricing["members"]
pricing["margin_%"] = (pricing["profit_per_member"] / pricing["avg_cost"]) * 100


# ======================
# DISPLAY TABLE
# ======================
pricing_display = pricing.rename(
    columns=lambda x: x.replace("_", " ").title()
)

st.dataframe(
    pricing_display.style.format(
        {
            "Avg Cost": "${:,.0f}",
            "Markup %": "{:.0f}%",
            "Premium": "${:,.0f}",
            "Profit Per Member": "${:,.0f}",
            "Total Profit": "${:,.0f}",
            "Margin %": "{:.1f}%",
            "Members": "{:,}",
        }
    ).set_table_styles(
        [
            {
                "selector": "th",
                "props": [
                    ("font-weight", "bold"),
                    ("background-color", "#F8F9FA"),
                    ("border-bottom", "1px solid #D1D5DB")
                ]
            },
            {
                "selector": "td",
                "props": [
                    ("background-color", "#F8F9FA"),
                    ("border-bottom", "1px solid #E5E7EB")
                ]
            }
        ]
    ),
    hide_index=True
)


# ======================
# PRICING VISUALS (2 COLUMNS)
# ======================

col1, col2 = st.columns(2)


# ======================
# VISUAL 1 — PREMIUM VS COST
# ======================

with col1:

    chart_header("Cost vs Premium by Risk Tier")


    fig7, ax7 = plt.subplots(figsize=(5, 3))


    pricing_melted = pricing.melt(
        id_vars="risk_tier",
        value_vars=[
            "avg_cost",
            "premium"
        ]
    )

    pricing_melted["variable"] = pricing_melted["variable"].replace({
        "avg_cost": "Average Cost",
        "premium": "Premium"
    })


    sns.barplot(
        data=pricing_melted,
        x="risk_tier",
        y="value",
        hue="variable",
        order=RISK_ORDER,
        palette=[COLOR_NEUTRAL, COLOR_PRIMARY],
        ax=ax7
    )


    ax7.set_title(
        "Cost vs Premium by Risk Tier",
        fontsize=13,
        fontname=CHART_FONT
    )


    ax7.set_xlabel(
        "Risk Tier",
        fontsize=11,
        fontname=CHART_FONT
    )


    ax7.set_ylabel(
        "Medical Cost ($)",
        fontsize=11,
        fontname=CHART_FONT
    )


    ax7.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda y, _: f"${y:,.0f}")
    )


    ax7.tick_params(labelsize=10)


    for label in ax7.get_xticklabels():
        label.set_fontname(CHART_FONT)


    for label in ax7.get_yticklabels():
        label.set_fontname(CHART_FONT)


    ax7.legend(
        title="",
        prop={"family": CHART_FONT, "size": 10}
    )


    st.pyplot(fig7, use_container_width=False)
    plt.close(fig7)
    chart_caption("Premium = average cost plus a per-tier markup (higher tiers carry a larger margin).")


# ======================
# VISUAL 2 — TOTAL PROFIT
# ======================

with col2:
    chart_header("Total Profit by Risk Tier")

    fig8, ax8 = plt.subplots(figsize=(5, 3))

    bars = sns.barplot(
        data=pricing,
        x="risk_tier",
        y="total_profit",
        order=RISK_ORDER,
        hue="risk_tier",
        hue_order=RISK_ORDER,
        palette=RISK_PALETTE,
        legend=False,
        ax=ax8
    )

    ax8.set_title("Total Profit by Risk Tier", fontsize=13, fontname=CHART_FONT)
    ax8.set_xlabel("Risk Tier", fontsize=11, fontname=CHART_FONT)
    ax8.set_ylabel("Total Profit ($)", fontsize=11, fontname=CHART_FONT)
    ax8.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"${y:,.0f}"))
    ax8.tick_params(labelsize=10)

    for label in ax8.get_xticklabels():
        label.set_fontname(CHART_FONT)

    for label in ax8.get_yticklabels():
        label.set_fontname(CHART_FONT)

    # Headroom above the tallest bar so its n= label isn't clipped by the
    # top of the chart.
    ax8.set_ylim(0, pricing["total_profit"].max() * 1.15)

    # add member count labels above each bar
    # keep only tiers that actually exist after filtering, in canonical order
    tier_order = [t for t in RISK_ORDER if t in set(pricing["risk_tier"])]
    pricing_ordered = pricing.set_index("risk_tier").loc[tier_order].reset_index()

    for i, row in pricing_ordered.iterrows():
        ax8.text(
            i,
            row["total_profit"] + (pricing["total_profit"].max() * 0.02),
            f'n={int(row["members"])}',
            ha="center",
            fontsize=10,
            fontname=CHART_FONT
        )

    st.pyplot(fig8, use_container_width=False)
    plt.close(fig8)
    chart_caption("Total profit reflects both margin per member and tier size.")

# Tail-risk caveat: profit above is an *expected* value. The interesting (and
# counter-intuitive) point in this data is that variability is NOT highest in
# the High tier — its members are uniformly expensive — but in the lower tiers,
# where a mostly-cheap population hides the occasional very large claim.
cv_by_tier = (
    df.groupby("risk_tier")["charges"]
    .apply(lambda s: s.std() / s.mean() if len(s) > 1 and s.mean() else 0)
)
if not cv_by_tier.empty:
    worst = cv_by_tier.idxmax()
    st.caption(
        f"⚠️ **Tail-risk note:** profit shown is an *expected* value. Cost variability is "
        f"actually highest in the **{worst}** tier (coefficient of variation ≈ {cv_by_tier.max():.0%}), "
        f"not the High tier — High-risk members are few but uniformly expensive, so the biggest "
        f"per-member *surprise-claim* risk sits in the lower tiers."
    )

st.markdown("---")
st.markdown("## Executive Summary & Business Insights")


# ======================
# INSIGHT 1 — SMOKING IMPACT
# ======================
smoker_effect = df.groupby("smoker")["charges"].mean()

st.markdown("### Smoking is the strongest cost driver")

# Both smoker and non-smoker must be present to compute the ratio.
if "yes" in smoker_effect.index and "no" in smoker_effect.index and smoker_effect["no"] > 0:
    smoker_ratio = smoker_effect["yes"] / smoker_effect["no"]
    st.write(
        f"Smokers cost on average **{smoker_ratio:.1f}× more** than non-smokers "
        f"(**${smoker_effect['yes']:,.0f}** vs **${smoker_effect['no']:,.0f}** per year)."
    )
else:
    st.write(
        "Select both smokers and non-smokers in the filter bar to compare their average cost."
    )


# ======================
# INSIGHT 2 — RISK TIER IMPACT
# ======================
tier_effect = df.groupby("risk_tier")["charges"].mean()

st.markdown("### Risk segmentation is strongly predictive")

# Show the actual tier averages and the Low → High spread instead of a vague claim.
present_tiers = [t for t in RISK_ORDER if t in tier_effect.index]
if len(present_tiers) >= 2:
    parts = " → ".join(f"{t} **${tier_effect[t]:,.0f}**" for t in present_tiers)
    spread = tier_effect[present_tiers[-1]] / tier_effect[present_tiers[0]]
    st.write(
        f"Average annual cost by tier: {parts} — a **{spread:.1f}× spread** "
        f"from {present_tiers[0]} to {present_tiers[-1]} risk."
    )
else:
    st.write("Widen the filters to compare cost across all three risk tiers.")


# ======================
# INSIGHT 3 — HIGH RISK CONCENTRATION
# ======================
high_risk_share = len(df[df["risk_tier"] == "High"]) / len(df)
high_risk_count = int((df["risk_tier"] == "High").sum())


st.markdown("### High-risk concentration")
st.write(
   f"High-risk members represent **{high_risk_share:.1%}** of the portfolio "
   f"(**{high_risk_count:,}** of {len(df):,} members)."
)


# # ======================
# BUSINESS RECOMMENDATIONS
# ======================
st.markdown("### Business Recommendations")

# Data-driven lead line tied to the current filters + markup assumptions.
total_profit = pricing["total_profit"].sum()
lead = f"At the current markup assumptions, the portfolio yields **${total_profit:,.0f}** in modelled profit"
if "High" in set(pricing["risk_tier"]):
    high_row = pricing.loc[pricing["risk_tier"] == "High"].iloc[0]
    high_share_profit = high_row["total_profit"] / total_profit if total_profit else 0
    lead += (
        f", with the **High tier contributing {high_share_profit:.0%}** of it from just "
        f"**{int(high_row['members']):,}** members — a concentrated but predictable cost center."
    )
else:
    lead += "."
st.write(lead)


st.markdown("""
<div style="
    font-family: Georgia, serif;
    font-size: 16px;
    color: black;
">

<ul>
<li>Pricing should strongly differentiate smokers vs non-smokers</li>
<li>Risk-based segmentation improves pricing accuracy vs flat pricing</li>
<li>High-risk group should be monitored for profitability exposure</li>
<li>BMI and age should be used as supporting (not primary) pricing factors</li>
</ul>

</div>
""", unsafe_allow_html=True)
