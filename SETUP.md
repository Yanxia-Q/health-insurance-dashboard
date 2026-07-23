# Setup & Deployment Instructions

## Run Locally

### Requirements
- Python 3.11+
- pip or conda

### Installation

```bash
# Clone the repository
git clone https://github.com/Yanxia-Q/health-insurance-dashboard.git
cd health-insurance-dashboard

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run insurance_dashboard.py
```

The dashboard will open at `http://localhost:8501`

## Deploy to Streamlit Cloud (Recommended)

### Why Streamlit Cloud?
- ✅ Free tier available
- ✅ Automatic deployment from GitHub
- ✅ Live URL to share with others
- ✅ Perfect for portfolio/CV
- ✅ No server management needed

### Steps

1. **Push to GitHub** (if not already done)
   ```bash
   git init
   git add .
   git commit -m "Initial commit: health insurance analytics dashboard"
   git remote add origin https://github.com/Yanxia-Q/health-insurance-dashboard
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Sign in with GitHub
   - Select your repository, branch (`main`), and main file (`insurance_dashboard.py`)
   - Click "Deploy"

## Project Dependencies

See [requirements.txt](requirements.txt) for the full list of packages and pinned versions.

## Troubleshooting

### Dashboard won't start
```bash
# Verify Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Run with verbose logging
streamlit run insurance_dashboard.py --logger.level=debug
```

### Port 8501 already in use
```bash
# Use a different port
streamlit run insurance_dashboard.py --server.port 8502
```

### Data file not found
Ensure `insurance.csv` is in the same directory as `insurance_dashboard.py`

## For Interviewers/Reviewers

Quick-start command for running locally:
```bash
git clone https://github.com/Yanxia-Q/health-insurance-dashboard.git && \
cd health-insurance-dashboard && \
pip install -r requirements.txt && \
streamlit run insurance_dashboard.py
```

Or just visit the live deployment link at the top of the README.
