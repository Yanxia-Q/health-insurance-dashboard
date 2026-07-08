# Setup & Deployment Instructions

## Run Locally

### Requirements
- Python 3.11+
- pip or conda

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/health-insurance-dashboard.git
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
   git remote add origin https://github.com/YOUR_USERNAME/health-insurance-dashboard
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Sign in with GitHub
   - Select your repository, branch (`main`), and main file (`insurance_dashboard.py`)
   - Click "Deploy"

3. **Share your live dashboard**
   - Your URL will be: `https://YOUR_USERNAME-health-insurance.streamlit.app`
   - Add this to your CV and portfolio

## Deploy with Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "insurance_dashboard.py"]
```

### Build and Run Locally

```bash
docker build -t health-insurance-dashboard .
docker run -p 8501:8501 health-insurance-dashboard
```

### Deploy to Cloud Platforms

Once built, you can deploy the Docker image to:
- **AWS ECS** or **Elastic Beanstalk**
- **Google Cloud Run**
- **Azure Container Instances**
- **DigitalOcean**
- **Heroku** (using container registry)

## Project Dependencies

```
streamlit==1.35.0        # Interactive web framework
pandas==2.1.4            # Data manipulation
numpy==1.26.3            # Numerical computing & regression
matplotlib==3.8.2        # Data visualization
seaborn==0.13.1          # Statistical visualization
```

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
git clone https://github.com/YOUR_USERNAME/health-insurance-dashboard.git && \
cd health-insurance-dashboard && \
pip install -r requirements.txt && \
streamlit run insurance_dashboard.py
```

Or just visit the live deployment link at the top of the README.
