import csv
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load environment variables from .env file
load_dotenv()
# Get the YouTube API key from the environment variables
api_key = os.getenv('YOUTUBE_API_KEY')
# Check if the API key is available
if not api_key:
    raise ValueError('YouTube API key not found. Make sure to set the YOUTUBE_API_KEY environment variable in the .env file.')

youtube = build('youtube', 'v3', developerKey=api_key)

# Make a request to the API for trending videos
request = youtube.videos().list(part='snippet,statistics', chart='mostPopular', regionCode='IN', maxResults=10)
response = request.execute()

# Create a CSV file and write the header
csv_file = 'trending_videos.csv'
fieldnames = ['Video Title', 'Channel', 'View Count', 'Comment Count']

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    # Write the trending videos with view count and comment count to the CSV file
    for item in response['items']:
        video_title = item['snippet']['title']
        video_channel = item['snippet']['channelTitle']
        view_count = item['statistics']['viewCount']
        comment_count = item['statistics']['commentCount']
        writer.writerow({
            'Video Title': video_title,
            'Channel': video_channel,
            'View Count': view_count,
            'Comment Count': comment_count
        })

print(f'Trending videos saved to {csv_file}')
