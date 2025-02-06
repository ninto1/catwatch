import requests
import re
import subprocess
import argparse
import time

def get_current_livestream(channel_url):
        response = requests.get(channel_url)

        if response.status_code != 200:
        print(f"Error: Unable to fetch channel page. Status code: {response.status_code}")
        return None

            match = re.search(r'liveData".*watch\?v=(\w+)', response.text)

    if match:
        video_id = match.group(1)
        livestream_url = f"https://www.youtube.com/watch?v={video_id}"
        return livestream_url
    else:
        print("No livestream found.")
        return None

def play_stream(livestream_url):
    try:
                subprocess.run([
            'mpv', 
            '--cache=yes', 
            '--cache-secs=60', 
            '--ytdl-format=bestvideo+bestaudio/best',              '--no-audio', 
            livestream_url
        ])
    except Exception as e:
        print(f"Error playing stream: {e}")

def monitor_stream(channel_name):
    channel_url = f"https://www.youtube.com/@{channel_name}"

    while True:
        print(f"Checking for a livestream on channel: {channel_url}")
        
        livestream_url = get_current_livestream(channel_url)

        if livestream_url:
            print(f"Current Livestream URL: {livestream_url}")
            print(f"Starting the stream. This may take a while...")
            play_stream(livestream_url)
            print("Stream ended or was closed. Rechecking for new stream...")
        else:
            print("No livestream currently active. Retrying...")
        
                time.sleep(30)

if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="YouTube Livestream Monitor")
    parser.add_argument(
        'channel_name', 
        nargs='?', 
        default='gletu', 
        help="YouTube channel name (default: gletu)"
    )
    args = parser.parse_args()

    monitor_stream(args.channel_name)
