import re
from typing import List


def has_timestamp(text: str):
    pattern = re.compile(r'((?:\d{1,2}:)?\d{1,2}:\d{2})')
    match = re.search(pattern, text)
    return match


def extract_video_id(url: str) -> str:
    pattern = re.compile(r'(\/|v=)([a-zA-Z0-9-_]{11})(.*)')
    match = re.search(pattern, url)

    if match:
        return match.group(2)

    return 'Not a valid YouTube URL.'


def create_timestamped_url(video_url: str, timestamp: str) -> str:
    hour_pattern = re.compile(r'(\d{1,2}:\d{1,2}:\d{2})')
    minutes_pattern = re.compile(r'\d{1,2}:\d{2}')

    if re.match(hour_pattern, timestamp):
        url_timestamp = re.sub(r'(\d{1,2})(?::)(\d{1,2})(?::)(\d{2})', r'\1h\2m\3s', timestamp)
        timestamped_url = f'{video_url}&t={url_timestamp}'
        return timestamped_url
 
    if re.match(minutes_pattern, timestamp):
        url_timestamp = re.sub(r'(\d{1,2})(?::)(\d{2})', r'\1m\2s', timestamp)
        timestamped_url = f'{video_url}&t={url_timestamp}'
        return timestamped_url
 
    return 'timestamp could not be converted to URL'


def convert_yt_duration_to_seconds(yt_duration: str) -> str:
    pattern = re.compile(r'(?:(\d{1,2})H)?(?:(\d{1,2})M)?(\d{1,2})S')
    match = re.search(pattern, yt_duration)

    hours = match.group(1) if match.group(1) else 0
    minutes = match.group(2) if match.group(2) else 0
    seconds = match.group(3) if match.group(3) else 0

    total_seconds = int(seconds) + (int(minutes) * 60) + (int(hours) * 3600)

    return total_seconds


if __name__ == '__main__':
    pass