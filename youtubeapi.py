import os
import csv
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load environment variables from .env file
load_dotenv()

# Get the YouTube API key from the environment variables
api_key = os.getenv('YOUTUBE_API_KEY')

# Check if the API key is present
if not api_key:
    raise ValueError(
        'YouTube API key not found. Make sure to set the YOUTUBE_API_KEY environment variable in the .env file.')

# Set up the YouTube Data API client
youtube = build('youtube', 'v3', developerKey=api_key)

# Make a request to the API for trending videos
request = youtube.videos().list(part='snippet,statistics',
                                chart='mostPopular', regionCode='IN', maxResults=50)
response = request.execute()

# Open a CSV file for writing
with open('trending_videos.csv', 'w', newline='', encoding='utf-8') as file:
    # Create a CSV writer
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['Video Title', 'Channel', 'Views', 'Comments', 'Tags'])

    # Process and save the trending videos
    for item in response['items']:
        video_title = item['snippet']['title']
        video_channel = item['snippet']['channelTitle']
        video_views = item['statistics']['viewCount']
        video_comments = item['statistics']['commentCount']
        video_tags = item['snippet']['tags'] if 'tags' in item['snippet'] else []

        # Write the data to the CSV file
        writer.writerow([video_title, video_channel, video_views,
                        video_comments, ', '.join(video_tags)])

# Notify the user that the data is saved
print('Trending videos data saved to trending_videos.csv')
