# Health Insurance Portfolio Analytics Dashboard

Insurance portfolio managers must decide how much to mark up each risk tier to maintain healthy margins without making premiums uncompetitive.
Price the tiers too low and high-risk members become unprofitable; price them too high and lower-risk customers are more likely to choose a competitor.
This dashboard shows that smokers incur 3.8× higher medical costs than non-smokers and allows them to test tier-based pricing scenarios before changing premiums.

**[🔗 View Live Dashboard](https://monicaqiao-health-insurance-dashboard.streamlit.app/)**


## Risk Tiers
Members score one point each for age ≥50, BMI ≥30, and smoking.
0–1 = Low, 2 = Medium, 3 = High.

## Key Insights

* **Medical costs increase substantially across the risk tiers.** Average annual medical charges rise from **$8,638** for Low-risk members to **$22,919** for Medium-risk members and **$46,973** for High-risk members—a **5.4×** difference between the lowest and highest risk groups.

* **The High-risk tier is a small but high-cost segment.** Only **41 of 1,338 members (3.1%)** are classified as High-risk, yet they account for **11% of total medical charges**, making accurate pricing for this group disproportionately important to portfolio performance.

* **Smoking status is the strongest predictor of medical costs.** Smokers incur **3.8×** higher average medical charges than non-smokers, with age and BMI providing additional risk differentiation.


## Business Recommendation

Adopt a tier-based pricing strategy of **10%, 20%, and 35% markups for Low-, Medium-, and High-risk members** to better align premiums with underlying risk profiles. Compared with a uniform 20% markup, this approach reduces modelled portfolio profit by **$551,546 (16%)**, but improves pricing alignment by lowering premiums for the low-risk majority and increasing the High-risk tier markup.

The trade-off is a deliberate margin investment: the strategy reduces the average premium for Low-risk members by approximately **$864 per member** while increasing the High-risk tier markup to better reflect their higher expected medical costs. Whether this margin reduction creates long-term value depends on factors not included in this model, particularly customer retention and price sensitivity data. These additional data sources would determine whether the improved competitiveness and risk alignment justify the short-term reduction in modelled profit.

## Dataset

- **Size**: 1,338 insurance policy records
- **Features**: Age, BMI, region (4 regions), smoking status, medical charges
- **Type**: Kaggle Medical Cost Personal Datasets. Source: https://www.kaggle.com/datasets/mirichoi0218/insurance/data


## How to View

1. **Clone and run locally** — see [SETUP.md](SETUP.md) for instructions
2. **Explore the analysis** in [insurance_project.ipynb](insurance_project.ipynb) for detailed exploratory data analysis


## Limitations

- **Cross-sectional data only**
  The dataset represents a single snapshot in time. It does not include longitudinal or time-series information, so we cannot analyze how risk evolves over time.

- **No claim-level detail**
  The dataset provides annual medical costs but does not include individual claim frequency or medical event breakdowns, limiting actuarial depth.

- **No premium information**
  Insurance premiums are not provided, so profitability and underwriting margins are simulated rather than observed.

- **Simplified risk model**
  The risk scoring model is rule-based and constructed from observed trends rather than statistically optimized or machine-learned.

- **Correlation ≠ causation**
  The analysis identifies associations between variables and medical costs but does not establish causal relationships.
