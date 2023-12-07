from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from colorama import Fore, Style
import subprocess
import datetime
import time
import sys

BOLD = '\033[1m'
RESET = '\033[0m'

current_time = datetime.datetime.now()
current_hour = current_time.hour

# YouTube Data API Key
api_key = 'AIzaSyCcECKUjDXepi7YwTaPmIqM8t7aPXrjcyE'

# YouTube channel ID
channel_id = 'UCWsDFcIhY2DBi3GB5uykGXA'

# Array to store live stream video IDs
live_stream_video_ids = []
ids = ['UxoJYl5y4h8'] # test data
live_stream_video_ids.extend(ids)
print(live_stream_video_ids)
print()

youtube = build('youtube', 'v3', developerKey=api_key)


def get_live_stream_data(api_key, channel_id):
    response = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        eventType='live',
        type='video'
    ).execute()

    if 'items' in response and len(response['items']) > 0:
        video_id = response['items'][0]['id']['videoId']
        return video_id
    else:
        return None

def create_folder(title):
    folder_path = f'/run/media/robin/big-partition/Videos/yt-dlp/speed-live-streams/{title}'
    subprocess.run(['mkdir', '-p', folder_path])

def execute_command(command):
    subprocess.Popen(["gnome-terminal", "--", "bash", "-c", command])


while True:
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%H:%M:%S")

    try:
        live_stream_data = get_live_stream_data(api_key, channel_id)

        if live_stream_data and live_stream_data not in live_stream_video_ids:
            print(formatted_time, BOLD + f"- New Live Stream - Video ID: {live_stream_data}" + RESET)

            create_folder(live_stream_data)
            command = f"yt-dlp --live-from-start -P '/run/media/robin/big-partition/Videos/yt-dlp/speed-live-streams/{live_stream_data}' https://www.youtube.com/watch?v={live_stream_data}"
            execute_command(command)
            # Add the video ID to the array
            live_stream_video_ids.append(live_stream_data)
        else:
            print(formatted_time, BOLD + '- No new live stream currently.' + RESET)
            
            print("<=========================================================>")
            try:
                for video_id in live_stream_video_ids:
                    # Retrieve video details using videos().list() API endpoint
                    video_response = youtube.videos().list(
                        part='snippet',
                        id=video_id
                    ).execute()

                    if 'items' in video_response and len(video_response['items']) > 0:
                        print(f"Video with ID {BOLD}{video_id}{RESET}", Fore.GREEN + "Online", Style.RESET_ALL)
                    else:
                        print(f"Video with ID {BOLD}{video_id}{RESET}" + Fore.LIGHTYELLOW_EX + " Does not exist or has been deleted!" + Style.RESET_ALL)

            except HttpError as e:
                if e.resp.status == 404:
                    print(f"Video with ID {BOLD}{video_id}{RESET}", Fore.LIGHTYELLOW_EX + " Does not exist or has been deleted!", Style.RESET_ALL)
                else:
                    print("An error occurred:", e)

            print("<=========================================================>")

        # Check if the current time is between 7 PM and 2 AM
        if current_hour > 20 or current_hour <2:
            print("waiting 10 min before next check...")
            time.sleep(600)  # 10 minutes in seconds
        else:
            print("waiting 60 min before next check...")
            time.sleep(3200)  # 60 minutes in seconds

    except Exception as e:
        print(BOLD + Fore.RED + "something went wrong" + RESET)
        print(e)

        print("Trying again in 2 min")
        time.sleep(120)
