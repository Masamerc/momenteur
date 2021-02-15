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
    pattern = re.compile(r'\?v=([a-zA-Z0-9-]+)')
    match = re.search(pattern, url)

    if match:
        return match.group(1)

    print('Not a valide youtube url.')
    return


if __name__ == '__main__':

    # extract_timestamp
    # with open('comments_dump.txt') as f:
    #     text = f.read()

    # result = extract_timestamp(text)
    # print(result)


    # extract_vide_id
    video_urls = ('https://www.youtube.com/watch?v=NPMn2WCiQSk', 'https://www.youtube.com/watch?v=e-ORhEE9VVg',
                 'https://www.youtube.com/watch?v=60ItHLz5WEA')

    for video_url in video_urls:
        video_id = extract_video_id(video_url)
        print(video_id)

