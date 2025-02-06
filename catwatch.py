import requests
import re
import subprocess
import argparse
import time

# Function to fetch the current livestream URL from a YouTube channel
def get_current_livestream(channel_url):
    # Send a request to the channel's URL
    response = requests.get(channel_url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error: Unable to fetch channel page. Status code: {response.status_code}")
        return None

    # Use regex to search for the video ID of the livestream
    # The pattern will look for "liveData" and extract the video ID from the URL
    match = re.search(r'liveData".*watch\?v=(\w+)', response.text)

    if match:
        video_id = match.group(1)
        livestream_url = f"https://www.youtube.com/watch?v={video_id}"
        return livestream_url
    else:
        print("No livestream found.")
        return None

# Function to play the stream using mpv
def play_stream(livestream_url):
    try:
        # Run the mpv player with the YouTube stream URL
        subprocess.run([
            'mpv', 
            '--cache=yes', 
            '--cache-secs=60', 
            '--ytdl-format=bestvideo+bestaudio/best',  # Force best quality video and audio
            '--no-audio', 
            livestream_url
        ])
    except Exception as e:
        print(f"Error playing stream: {e}")

# Function to check and monitor the stream status
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
        
        # Wait for a while before checking again (e.g., 30 seconds)
        time.sleep(30)

# Main execution
if __name__ == "__main__":
    # Argument parser for channel name
    parser = argparse.ArgumentParser(description="YouTube Livestream Monitor")
    parser.add_argument(
        'channel_name', 
        nargs='?', 
        default='gletu', 
        help="YouTube channel name (default: gletu)"
    )
    args = parser.parse_args()

    monitor_stream(args.channel_name)
