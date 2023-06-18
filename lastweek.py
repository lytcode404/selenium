import os
import csv
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load environment variables from .env file
load_dotenv()

# Get the YouTube API key from the environment variables
api_key = os.getenv('YOUTUBE_API_KEY')

# Check if the API key is present
if not api_key:
    raise ValueError('YouTube API key not found. Make sure to set the YOUTUBE_API_KEY environment variable in the .env file.')

# Set up the YouTube Data API client
youtube = build('youtube', 'v3', developerKey=api_key)

# Calculate the date 1 week ago
one_week_ago = datetime.now(timezone.utc) - timedelta(weeks=1)

# Make a request to the API for trending videos
request = youtube.videos().list(part='snippet,statistics', chart='mostPopular', regionCode='IN', maxResults=50)
response = request.execute()

# Filter the videos based on their published date
trending_videos = []
for item in response['items']:
    video_published_at = datetime.fromisoformat(item['snippet']['publishedAt'].replace('Z', '+00:00'))
    if video_published_at >= one_week_ago:
        trending_videos.append(item)

# Open a CSV file for writing
with open('last_week.csv', 'w', newline='', encoding='utf-8') as file:
    # Create a CSV writer
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['Video Title', 'Channel', 'Views', 'Comments', 'Tags'])

    # Process and save the trending videos
    for video in trending_videos:
        video_title = video['snippet']['title']
        video_channel = video['snippet']['channelTitle']
        video_views = video['statistics']['viewCount']
        video_comments = video['statistics']['commentCount']
        video_tags = video['snippet']['tags'] if 'tags' in video['snippet'] else []

        # Write the data to the CSV file
        writer.writerow([video_title, video_channel, video_views, video_comments, ', '.join(video_tags)])

# Notify the user that the data is saved
print('Trending videos data from the last 1 week saved to last_week.csv')
