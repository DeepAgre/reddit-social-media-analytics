import praw
import pandas as pd
from datetime import datetime
from reddit_credentials import client_id, client_secret, user_agent

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

tech_subs = ["technology", "programming", "datascience", "artificial"]

def scrape_posts():
    posts = []
    for sub in tech_subs:
        print(f"Scraping r/{sub}...")
        for post in reddit.subreddit(sub).hot(limit=50):
            posts.append({
                "subreddit": sub,
                "title": post.title,
                "content": post.selftext,
                "upvotes": post.score,
                "comments": post.num_comments,
                "created": datetime.fromtimestamp(post.created_utc),
                "author": str(post.author),
                "url": f"https://reddit.com{post.permalink}"
            })
    return pd.DataFrame(posts)

if __name__ == "__main__":
    df = scrape_posts()
    df.to_csv("raw_tech_posts.csv", index=False)
    print("Saved to raw_tech_posts.csv")