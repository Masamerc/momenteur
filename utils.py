import re
from typing import List

def extract_timestamp(text: str) -> List[str]:
    pattern = re.compile(r'(?:\d{1,2}:)?\d{2}:\d{2}')
    match = re.findall(pattern, text)
    return match


def has_timestamp(text: str) -> re.Match:
    pattern = re.compile(r'((?:\d{1,2}:)?\d{1,2}:\d{2})')
    match = re.search(pattern, text)
    return match


def extract_video_id(url: str) -> str:
    pattern = re.compile(r'(\/|v=)([a-zA-Z0-9-_]{11})(.*)')
    match = re.search(pattern, url)

    if match:
        return match.group(2)

    print('Not a valide youtube url.')
    return


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
    

if __name__ == '__main__':

    # extract_timestamp
    # with open('comments_dump.txt') as f:
    #     text = f.read()

    # result = extract_timestamp(text)
    # print(result)


    # extract_vide_id
    video_urls = ('https://www.youtube.com/watch?v=NPMn2WCiQSk', 'https://www.youtube.com/watch?v=e-ORhEE9VVg',
                 'https://www.youtube.com/watch?v=60ItHLz5WEA', 'https://www.youtube.com/watch?v=hvYLQM_fMMw')

    for video_url in video_urls:
        video_id = extract_video_id(video_url)
        print(video_id)

