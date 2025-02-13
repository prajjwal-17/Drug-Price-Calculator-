import praw
import time
import csv
import os

# Reddit API setup
reddit = praw.Reddit(
    client_id="k-zzdMn5Dkay8lXPMBkDYg",
    client_secret="eAXhKrnujD_FG6BfCeRzqhNsWeLzJA",
    user_agent="Secure-Scratch2391"
)

# Ensure the `data/` directory exists
os.makedirs("data", exist_ok=True)

# Path to save the CSV file
csv_filepath = os.path.join("data", "medicine_demand.csv")

# Tracking API requests
request_count = 0
MAX_REQUESTS = 55  # Stay under 60 to be safe
POST_LIMIT = 100  # Stop after collecting 100 posts

data = []

try:
    for submission in reddit.subreddit("pharmacy+medicine").hot(limit=500):
        # Extract relevant data
        title = submission.title
        url = submission.url
        created_utc = submission.created_utc

        # Save the data
        data.append([title, url, created_utc])
        print(title)  # Print fetched titles
        
        request_count += 1

        # Check Reddit API rate limits
        remaining = reddit.auth.limits["remaining"]
        if remaining < 5:  # If only 5 requests left, pause
            print("Approaching API limit, sleeping for 60 seconds...")
            time.sleep(60)
            request_count = 0  # Reset request count

        # Stop if enough data is collected
        if len(data) >= POST_LIMIT:
            break

        time.sleep(1)  # Wait 1 second between requests to avoid hitting limits

except praw.exceptions.APIException as e:
    print("API error:", e)
    time.sleep(60)  # Wait & retry

# Save to CSV
with open(csv_filepath, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "URL", "Timestamp"])
    writer.writerows(data)

print(f"\n✅ Data has been saved to '{csv_filepath}'")
