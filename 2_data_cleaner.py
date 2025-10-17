import pandas as pd
import re

def clean_text(text):
    if pd.isna(text): return ""
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)  # Remove URLs
    text = re.sub(r'\@\w+|\#\w+', '', text)  # Remove mentions/hashtags
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text.strip().lower()

df = pd.read_csv("raw_tech_posts.csv")
df['clean_content'] = df['content'].apply(clean_text)
df['clean_title'] = df['title'].apply(clean_text)
df.to_csv("cleaned_tech_posts.csv", index=False)
print("Saved cleaned data!")