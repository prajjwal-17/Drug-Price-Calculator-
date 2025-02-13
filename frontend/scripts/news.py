import requests
import xml.etree.ElementTree as ET
import csv
import os

# Define the RSS feed URL
rss_url = "https://www.pharmacytimes.com/rss"

# Ensure the `data/` directory exists
os.makedirs("data", exist_ok=True)

# Path to save the CSV file
csv_filepath = os.path.join("data", "pharmaceutical_news.csv")

# Send a request to fetch the RSS feed
response = requests.get(rss_url)

# Parse the XML content
root = ET.fromstring(response.content)

# Create a CSV file to save the data
with open(csv_filepath, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(["Title", "Link", "Description", "Publish Date"])
    
    # Extract information from each RSS item and write to the CSV file
    for item in root.findall(".//item"):
        title = item.find("title").text
        link = item.find("link").text
        description = item.find("description").text
        pub_date = item.find("pubDate").text
        
        # Write each article's data as a new row in the CSV
        writer.writerow([title, link, description, pub_date])

print(f"✅ Data has been saved to '{csv_filepath}'")
