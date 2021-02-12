import re

def extract_timestamp(text: str) -> str:
    pattern = re.compile(r'\s?(?:\d{1,2}:)?\d{2}:\d{2}\s')
    match = re.findall(pattern, text)
    return match

if __name__ == '__main__':
    with open('comments_dump.txt') as f:
        text = f.read()

    result = extract_timestamp(text)
    print(result)
