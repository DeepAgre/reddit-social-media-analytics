# 4_dashboard.py - Fully Working Version
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, date
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk

# Download required NLTK data
nltk.download('vader_lexicon')

# Configure page
st.set_page_config(
    page_title="Reddit Tech Analytics Pro",
    layout="wide",
    page_icon="🧠"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-label {
        font-size: 14px;
        color: #cccccc; /* light gray for labels */
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #ffcc00; /* gold for numbers */
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_tech_posts.csv")
    # Ensure datetime conversion and normalization
    df['created'] = pd.to_datetime(df['created'], errors='coerce').dt.normalize()
    return df.dropna(subset=['created', 'clean_content'])

def analyze_sentiment_vader(text):
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)['compound']

def extract_topics(texts, n_topics=3):
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    dtm = vectorizer.fit_transform(texts)
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(dtm)
    return lda, vectorizer

def show_wordcloud(text):
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

def main():
    st.title("🧠 Reddit Tech Analytics Pro")
    st.markdown("Advanced NLP analysis of tech subreddit discussions")
    
    # Load data
    df = load_data()
    
    # ===== SIDEBAR =====
    with st.sidebar:
        st.header("Analysis Controls")
        
        # Sentiment Analysis
        st.subheader("Sentiment Options")
        use_vader = st.checkbox("Use VADER (for social media)", True)
        
        # Topic Modeling
        st.subheader("Topic Modeling")
        do_topic_modeling = st.checkbox("Enable Topic Analysis", False)
        n_topics = st.slider("Number of topics", 2, 5, 3) if do_topic_modeling else 3
        
        # Filters
        st.subheader("Filters")
        selected_subs = st.multiselect(
            "Subreddits",
            df['subreddit'].unique(),
            default=df['subreddit'].unique()[:2]
        )
        
        # Convert min/max dates to datetime.date for the date_input
        min_date = df['created'].min().date()
        max_date = df['created'].max().date()
        selected_dates = st.date_input(
            "Date Range",
            value=[min_date, max_date],
            min_value=min_date,
            max_value=max_date
        )
    
    # ===== DATA PROCESSING =====
    # Convert selected dates to datetime64[ns] for comparison
    start_date = pd.to_datetime(selected_dates[0]) if len(selected_dates) > 0 else pd.to_datetime(min_date)
    end_date = pd.to_datetime(selected_dates[1]) if len(selected_dates) > 1 else pd.to_datetime(max_date)
    
    filtered_df = df[
        (df['subreddit'].isin(selected_subs)) &
        (df['created'] >= start_date) &
        (df['created'] <= end_date)
    ].copy()
    
    # Enhanced Sentiment Analysis
    if use_vader:
        filtered_df['sentiment'] = filtered_df['clean_content'].apply(analyze_sentiment_vader)
    else:
        from textblob import TextBlob
        filtered_df['sentiment'] = filtered_df['clean_content'].apply(
            lambda x: TextBlob(x).sentiment.polarity
        )
    
    # ===== DASHBOARD =====
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card">📊 Total Posts<br><h3>{}</h3></div>'.format(
            len(filtered_df)), unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">😃 Avg Sentiment<br><h3>{:.2f}</h3></div>'.format(
            filtered_df['sentiment'].mean()), unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">🔥 Avg Engagement<br><h3>{:.0f}</h3></div>'.format(
            filtered_df['popularity'].mean()), unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card">💬 Top Subreddit<br><h3>{}</h3></div>'.format(
            filtered_df['subreddit'].mode()[0]), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ===== TABS =====
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Trends", "🧠 NLP Insights", "Raw Data"])
    
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.pie(
                filtered_df,
                names='subreddit',
                title='Post Distribution by Subreddit'
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.box(
                filtered_df,
                x='subreddit',
                y='sentiment',
                title='Sentiment Distribution by Subreddit'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Count posts per day instead of using non-existent 'id' column
        daily_stats = filtered_df.resample('D', on='created').agg({
            'sentiment': 'mean',
            'subreddit': 'count'  # Count posts per day
        }).rename(columns={'subreddit': 'post_count'}).reset_index()
        
        fig = px.line(
            daily_stats,
            x='created',
            y=['sentiment', 'post_count'],
            title='Daily Activity & Sentiment',
            labels={'value': 'Metric', 'variable': 'Legend'},
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.header("Advanced Text Analysis")
        
        # Word Cloud
        st.subheader("Most Frequent Words")
        show_wordcloud(' '.join(filtered_df['clean_content']))
        
        # Topic Modeling
        if do_topic_modeling:
            st.subheader("Topic Modeling Results")
            lda_model, vectorizer = extract_topics(filtered_df['clean_content'], n_topics)
            
            for idx, topic in enumerate(lda_model.components_):
                st.markdown(f"**Topic {idx+1}**: " + ", ".join(
                    [vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-5:]]
                ))
        
        # Sentiment Deep Dive
        st.subheader("Sentiment Analysis")
        pos = filtered_df.nlargest(3, 'sentiment')
        neg = filtered_df.nsmallest(3, 'sentiment')
        
        st.write("**Most Positive Posts**")
        st.dataframe(pos[['title', 'sentiment']], hide_index=True)
        st.write("**Most Negative Posts**")
        st.dataframe(neg[['title', 'sentiment']], hide_index=True)
    
    with tab4:
        st.dataframe(
            filtered_df.sort_values('created', ascending=False),
            column_config={
                "url": st.column_config.LinkColumn("Post URL"),
                "created": st.column_config.DatetimeColumn("Date")
            },
            hide_index=True,
            use_container_width=True,
            height=600
        )

if __name__ == "__main__":
    main()