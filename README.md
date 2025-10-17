📊 Reddit Social Media Data Analysis

A comprehensive data analysis project that extracts, processes, and visualizes technology discussion trends from Reddit. This project demonstrates end-to-end data analysis skills from web scraping to interactive dashboard creation.

🎯 Project Overview

This project analyzes technology-related discussions across multiple Reddit communities to identify trending topics, sentiment patterns, and engagement metrics. The analysis provides actionable insights for understanding tech community interests and sentiment dynamics.

📈 Key Business Insights

- 65% positive sentiment in AI-related discussions vs **45%** in career topics
- Peak engagement time: 2-5 PM UTC (40% higher interaction)
- Most discussed topics: AI advancements, programming tools, career opportunities
- Highest sentiment: Programming tools discussions (72% positive)

🛠️ Technical Stack

Data Collection & Processing
- Python, PRAW API, Pandas, Data Cleaning

Analysis & NLP
- Sentiment Analysis (VADER), Topic Modeling, Statistical Analysis

Visualization & Reporting
- Power BI, Streamlit, Data Visualization, Interactive Dashboards

Tools & Platforms
- Jupyter Notebook, VS Code, Microsoft Power BI

📁 Project Structure
reddit-social-media-analytics/
│
├── 1_reddit_scraper.py # Data collection from Reddit API
├── 2_data_cleaner.py # Data cleaning and preprocessing
├── 3_analysis.py # Sentiment analysis and EDA
├── 4_dashboard.py # Streamlit interactive dashboard
├── reddit_credentials.py # API configuration template
├── requirements.txt # Python dependencies
├── cleaned_tech_posts.csv # Sample dataset
└── images/ # Dashboard screenshots
├── dashboard-screenshot.png
├── sentiment-analysis.png
└── wordcloud.png


## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Reddit API credentials

Step 1: Clone Repository

git clone https://github.com/DeepAgre/reddit-social-media-analytics.git
cd reddit-social-media-analytics

Step 2: Install Dependencies
bash
pip install -r requirements.txt

Step 3: Configure API Credentials
Create a Reddit app at https://www.reddit.com/prefs/apps

Update reddit_credentials.py with your credentials:

python
client_id = "your_client_id_here"
client_secret = "your_secret_here"
user_agent = "reddit_tech_analytics_v1"

Step 4: Run the Analysis Pipeline
bash
1. Data Collection
python 1_reddit_scraper.py

2. Data Cleaning
python 2_data_cleaner.py

3. Analysis & Visualization
python 3_analysis.py

4. Launch Interactive Dashboard
streamlit run 4_dashboard.py
