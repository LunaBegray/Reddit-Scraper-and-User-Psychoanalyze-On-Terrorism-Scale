import asyncio
import praw
import sys
import os
import json

# PRAW credentials
CLIENT_ID = ""
CLIENT_SECRET = ""
USER_AGENT = ""

# Ensure the directory exists for saving data
os.makedirs("./data", exist_ok=True)

# Function to initialize the PRAW Reddit client
def init_reddit_client():
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
    )
    return reddit

# Function to extract comments from a post
def extract_user_data(post):
    user_data = {}

    # Fetch comments and make sure they are sorted by 'best' or 'top'
    post.comments.replace_more(limit=0)  # Remove "More comments" placeholder
    for comment in post.comments:
        if comment.author and comment.author.name != "AutoModerator":
            username = comment.author.name
            comment_text = comment.body

            # If user already exists in user_data, append the new comment text
            if username in user_data:
                user_data[username].append(comment_text)
            else:
                user_data[username] = [comment_text]

    return user_data

async def scrape_subreddit(subreddit_id: str, skip_posts: int = 6, max_posts: int = 3):
    """Scrape the comments of a subreddit."""
    reddit = init_reddit_client()

    user_db = {}

    # Get the subreddit
    subreddit = reddit.subreddit(subreddit_id)

    # Fetch the posts and skip the initial 'skip_posts' posts
    posts = subreddit.new(limit=skip_posts + max_posts)  # Get posts starting from the first one
    
    post_list = list(posts)[skip_posts:]  # Skip the first `skip_posts` posts
    print(f"Found {len(post_list)} regular posts to scrape after skipping {skip_posts}.")

    # Scrape the next `max_posts` posts
    for count, post in enumerate(post_list[:max_posts]):
        print(f"Scraping post: {post.url}")
        
        # Extract comments from the post
        user_comments = extract_user_data(post)

        # For each user, store their list of comments
        for username, comments in user_comments.items():
            if username in user_db:
                user_db[username].extend(comments)
            else:
                user_db[username] = comments

        # Print progress and move to the next post
        print(f"Moving to next post, {count + 1} out of {max_posts}")
    
    return user_db

async def run(max_posts):
    """Run the scraper with a specific maximum number of posts."""
    # Scrape subreddit 'Palestine' and get comment data
    data = await scrape_subreddit(subreddit_id="YouChoose", skip_posts=6, max_posts=max_posts)

    # Write the extracted data into the user_db.json file in JSON format
    with open("./data/user_db.json", "w", encoding="utf-8") as f:
        # Convert the data to a JSON string and write it
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("User comment data saved to user_db.json!")

if __name__ == "__main__":
    # Ensure that an argument is provided
    if len(sys.argv) != 2:
        print("Usage: python reddit_scraper.py <number_of_posts>")
        sys.exit(1)

    try:
        max_posts = int(sys.argv[1])
        if max_posts < 1:
            raise ValueError("Number of posts must be at least 1.")
    except ValueError as e:
        print(f"Invalid argument: {e}")
        sys.exit(1)

    asyncio.run(run(max_posts))
