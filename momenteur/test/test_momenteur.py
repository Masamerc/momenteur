import os

from ..utils import extract_video_id, create_timestamped_url, convert_yt_duration_to_seconds
from ..main import Momenteur
from pytest import fixture

m = Momenteur('https://www.youtube.com/watch?v=tFjNH9l6-sQ')


@fixture
def response_items():
    return m._load_items(os.path.join(os.getcwd(), 'momenteur/sample_data/sample_items.pkl'))


@fixture
def video_urls():
    video_urls = ('https://www.youtube.com/watch?v=NPMn2WCiQSk', 'https://www.youtube.com/watch?v=e-ORhEE9VVg',
                 'https://www.youtube.com/watch?v=60ItHLz5WEA', 'https://www.youtube.com/watch?v=hvYLQM_fMMw',
                 'https://www.youtube.com/watch?v=hvYLQM-fMMw')
    return video_urls


def test_extract_video_id(video_urls):

    extracted_video_ids = [extract_video_id(url) for url in video_urls]

    expected_results = ['NPMn2WCiQSk','e-ORhEE9VVg','60ItHLz5WEA','hvYLQM_fMMw', 'hvYLQM-fMMw']

    for extracted_video_id, expected_result in zip(extracted_video_ids, expected_results):
        assert expected_result == extracted_video_id, f"Failed: {extracted_video_id} != {expected_result}"


def test_create_timestamped_url(video_urls):
    time_stamps = ('9:23', '45:55', '1:02:22','02:22:43', '00:45')

    results = [create_timestamped_url(video_url, time_stamp) for video_url, time_stamp in zip(video_urls, time_stamps)]

    expected_results = ('https://www.youtube.com/watch?v=NPMn2WCiQSk&t=9m23s', 'https://www.youtube.com/watch?v=e-ORhEE9VVg&t=45m55s',
                 'https://www.youtube.com/watch?v=60ItHLz5WEA&t=1h02m22s', 'https://www.youtube.com/watch?v=hvYLQM_fMMw&t=02h22m43s',
                 'https://www.youtube.com/watch?v=hvYLQM-fMMw&t=00m45s')
    
    for result, expected_result in zip(results, expected_results):
        assert result == expected_result, f"Failed: {result} != {expected_result}"


def test_find_timestamped_comments(response_items):
    results = m.find_timestamped_comments(response_items)
    assert len(results) > 0
    assert type(results[0]['comment']) == str
    assert type(results[0]['timestamp']) == str


def test_rank_sort_timestamps(response_items):
    timestamp_comment_pairs = m.find_timestamped_comments(response_items)
    results = m.rank_sort_timestamps(timestamp_comment_pairs)
    assert len(results) > 0

    first_result = results[0]
    second_result = results[1]
    assert first_result['comment_count'] >= second_result['comment_count'], f"Failed: {first_result['comment_count']} !>= {second_result['comment_count']}"


def test_add_timestamped_url(response_items):
    timestamp_comment_pairs = m.find_timestamped_comments(response_items)
    ranked_timestamps = m.rank_sort_timestamps(timestamp_comment_pairs)

    results = m.add_timestamped_url(ranked_timestamps)
    assert len(results) > 0
    
    for result in results:
        expected = create_timestamped_url(m.video_url, result['timestamp'])
        assert result['url'] == expected, f"Failed: {result['url']} != {expected}"


def test_convert_yt_duration_to_seconds():
    yt_durations = ['PT3M45S', 'PT1H12M33S', 'PT56S']
    
    expected = [(3*60)+45, (1*3600)+(12*60)+33, 56]
    results = [convert_yt_duration_to_seconds(yt_duration) for yt_duration in yt_durations]

    for expected_result, actual_result in zip(expected, results):
        assert expected_result == actual_result, f"Failed: {expected_result} != {actual_result}"
