# yt-live-stream-downloader
A Python bot designed to automate the process of detecting live streams from specified YouTube channels using the Google YouTube API. Once a new live stream is detected, the bot automatically initiates the download process using [yt-dlp](https://github.com/yt-dlp/yt-dlp), a feature-rich command-line downloader for media content on YouTube.

<br>

## Setup

- YouTube API Key: Create a project in the [google clound console](https://console.cloud.google.com/apis/api/youtube.googleapis.com) and obtain a YouTube Data API key and save it in a file named 'api-key.txt' in the project directory.
- Dependencies: Install necessary Python libraries using `pip install -r requirements.txt`.

## Configuration

- Channel ID: Set the desired YouTube channel ID to monitor for live streams by updating the `channel_id` variable in the main.py script.

## Requirements

- Python 3.x
- yt-dlp library (https://github.com/yt-dlp/yt-dlp)
- YouTube API queries key (stored in 'api-key.txt')
