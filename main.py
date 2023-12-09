from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from colorama import Fore, Style
import subprocess
import datetime
import time
import sys

BOLD = '\033[1m'
RESET = '\033[0m'

# Read the API key from api-key.txt file
with open('api-key.txt', 'r') as file:
    api_key = file.read().strip()  

# YouTube channel ID
channel_id = 'UCWsDFcIhY2DBi3GB5uykGXA'

# File to store live stream video IDs
video_ids_file = 'live_stream_video_ids.txt'

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

def read_video_ids_from_file():
    try:
        with open(video_ids_file, 'r') as file:
            lines = file.readlines()
            return [line.strip() for line in lines if line.strip()]
    except FileNotFoundError:
        return []

def write_video_id_to_file(video_id):
    with open(video_ids_file, 'a') as file:
        file.write(video_id + '\n')

def create_folder(title):
    folder_path = f'/run/media/robin/big-partition/Videos/yt-dlp/speed-live-streams/{title}'
    subprocess.run(['mkdir', '-p', folder_path])

def execute_command(command):
    subprocess.Popen(["gnome-terminal", "--", "bash", "-c", command])

while True:
    current_time = datetime.datetime.now()
    current_hour = current_time.hour
    formatted_time = current_time.strftime("%H:%M:%S")

    live_stream_video_ids = read_video_ids_from_file()
    try:
        live_stream_data = get_live_stream_data(api_key, channel_id)

        if live_stream_data and live_stream_data not in live_stream_video_ids:
            print(formatted_time, BOLD + f"- New Live Stream - Video ID: {live_stream_data}" + RESET)

            create_folder(live_stream_data)
            command = f"yt-dlp --live-from-start -P '/run/media/robin/big-partition/Videos/yt-dlp/speed-live-streams/{live_stream_data}' https://www.youtube.com/watch?v={live_stream_data}"
            execute_command(command)
            write_video_id_to_file(live_stream_data)  # Add the video ID to the file
        else:
            print(formatted_time, BOLD + '- No new live stream currently.' + RESET)
            
            print("<=========================================================>")
            try:
                if live_stream_video_ids:
                    video_id = live_stream_video_ids[-1]  # Get the last video ID from the file
                    video_response = youtube.videos().list(part='snippet', id=video_id).execute()

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
        if current_hour > 20 or current_hour < 2:
            print("waiting 10 min before next check...")
            time.sleep(600)  # 10 minutes in seconds
        else:
            print("waiting 60 min before next check...")
            time.sleep(3600)  # 60 minutes in seconds

    except Exception as e:
        print(BOLD + Fore.RED + "something went wrong" + RESET)
        print(formatted_time, "-", e)

        print("Trying again in 2 min")
        time.sleep(120)
