# 3_analysis.py - Complete Reddit Tech Post Analyzer
import pandas as pd
import numpy as np
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def load_and_prepare_data():
    """Load and preprocess the Reddit data"""
    df = pd.read_csv("cleaned_tech_posts.csv")
    
    # Convert all content to strings and handle missing values
    df['clean_content'] = df['clean_content'].astype(str).replace('nan', np.nan).fillna('')
    df['clean_title'] = df['clean_title'].astype(str).replace('nan', np.nan).fillna('')
    
    return df

def analyze_sentiment(df):
    """Calculate sentiment polarity for each post"""
    df['sentiment'] = df['clean_content'].apply(
        lambda x: TextBlob(x).sentiment.polarity if x.strip() else 0
    )
    return df

def calculate_engagement(df):
    """Compute engagement score"""
    df['popularity'] = df['upvotes'] + (df['comments'] * 2)
    return df

def generate_visualizations(df):
    """Create EDA visualizations"""
    # Posts per subreddit
    plt.figure(figsize=(12,6))
    df['subreddit'].value_counts().plot(
        kind='bar',
        title='Number of Posts per Tech Subreddit',
        color='skyblue'
    )
    plt.xlabel('Subreddit')
    plt.ylabel('Post Count')
    plt.tight_layout()
    plt.savefig('posts_per_subreddit.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Sentiment distribution
    plt.figure(figsize=(12,6))
    df['sentiment'].plot(
        kind='hist',
        bins=20,
        title='Sentiment Distribution of Tech Posts',
        color='lightgreen',
        edgecolor='black'
    )
    plt.xlabel('Sentiment Score (-1 to 1)')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig('sentiment_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Word cloud from titles (more concise than content)
    text = ' '.join(df['clean_title'][df['clean_title'].str.strip() != ''])
    if text:
        wordcloud = WordCloud(
            width=1200,
            height=600,
            background_color='white',
            colormap='viridis',
            max_words=200
        ).generate(text)
        plt.figure(figsize=(15,8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Most Frequent Words in Tech Post Titles', pad=20)
        plt.savefig('tech_wordcloud.png', dpi=300, bbox_inches='tight')
        plt.close()

def main():
    print("🚀 Starting Reddit Tech Post Analysis...")
    
    # Load and prepare data
    df = load_and_prepare_data()
    
    # Perform analysis
    df = analyze_sentiment(df)
    df = calculate_engagement(df)
    
    # Save analyzed data
    df.to_csv("cleaned_tech_posts.csv", index=False)
    
    # Generate visualizations
    generate_visualizations(df)
    
    print("✅ Analysis Complete! Created:")
    print("- cleaned_tech_posts.csv (with sentiment and popularity)")
    print("- posts_per_subreddit.png")
    print("- sentiment_distribution.png")
    print("- tech_wordcloud.png")

if __name__ == "__main__":
    main()