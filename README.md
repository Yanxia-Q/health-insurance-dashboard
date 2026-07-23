# Health Insurance Portfolio Analytics Dashboard

An interactive Streamlit dashboard that analyzes health insurance data to uncover cost drivers, segment risk, and explore dynamic pricing strategies.

**[🔗 View Live Dashboard](https://monicaqiao-health-insurance-dashboard.streamlit.app/)**

## Overview

This project takes a dataset of 1,338 insurance records and transforms it into an interactive analytics platform.
It demonstrates how data-driven segmentation and risk scoring can inform pricing decisions in the insurance industry.

## Key Insights

- **Smoking is the strongest cost driver** (~3-4x higher medical costs)
- **Age and BMI show clear risk gradients** — systematic cost increases with these factors
- **Risk-based segmentation improves pricing accuracy** — automated classification into Low, Medium, High tiers
- **High-risk members represent concentrated profitability** — small segment but major revenue impact

## Dashboard Features

- **Interactive Filtering**: Real-time analysis by age range, region, and smoker status with sticky navigation
- **Risk Scoring System**: Automated tier segmentation based on age (≥50), BMI (≥30), and smoking status
- **Dynamic Pricing Model**: Per-tier markup sliders showing real-time impact on premiums and profitability
- **Executive Summary**: KPI metric cards with live-computed metrics (smoker multiplier, tier spread, high-risk share)
- **Cost Driver Analysis**: Standardized OLS regression chart ranking factors by importance
- **Professional Visualizations**: Seaborn & Matplotlib charts with semantic color coding

## Skills Demonstrated

- **Data Analysis**: Pandas for data manipulation, NumPy for statistical regression
- **Data Visualization**: Seaborn & Matplotlib with custom styling and semantic coloring
- **Interactive UI/UX**: Streamlit app with sticky filters, KPI cards, responsive layout
- **Pricing Modeling**: Dynamic pricing simulation with scenario analysis
- **Statistical Analysis**: Risk tier classification and cost driver importance quantification

## Dataset

- **Size**: 1,338 insurance policy records
- **Features**: Age, BMI, region (4 regions), smoking status, medical charges
- **Type**: Synthetic data for demonstration
- **Purpose**: Understanding cost drivers and building pricing strategies

## How to View

1. **Click the live link** at the top to view the deployed dashboard
2. **Clone and run locally** — see [SETUP.md](SETUP.md) for instructions
3. **Explore the analysis** in [insurance_project.ipynb](insurance_project.ipynb) for detailed exploratory data analysis

## Project Structure

```
├── insurance_dashboard.py      # Main Streamlit application
├── insurance.csv              # Dataset (1,338 records)
├── insurance_project.ipynb    # Exploratory analysis & statistics
├── README.md                  # This file
├── SETUP.md                   # Setup & deployment instructions
├── requirements.txt           # Python dependencies
└── .streamlit/
    └── config.toml            # Streamlit theme configuration
```

## What Makes This Project Interesting

✨ **Interactive Pricing Simulator** — Adjust tier-based markups and see real-time profit impact

✨ **Sticky Filter Bar** — Filters stay visible when scrolling (UX best practice)

✨ **Evidence-Based Insights** — Metrics grounded in standardized regression, not guesswork

✨ **Professional Styling** — Semantic color palettes, metric cards, and responsive layout
