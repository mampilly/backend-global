from requests_oauthlib import OAuth1Session
import json
import logging
import time
import requests


def get_recent_posts_instagram(handle):
    """Api for basic details

    Arguments:
        handle {str}: username

    Returns:
        json -- returns basic details
    """
    result = None
    try:
        url = "https://www.instagram.com/{}/?__a=1".format(handle)
        response = requests.get(url)
        if (response.status_code != 200):
            return None
        result = response.json()
    except Exception as e:
        logging.error("error is {}".format(e))
    return result


def get_recent_posts_twitter(handle):
    """Api for basic details

    Arguments:
       handle

    Returns:
        json -- returns basic details
    """
    result = None
    try:

        url = "https://api.twitter.com/1.1/statuses/user_timeline.json?count=100&screen_name={}&count=10&exclude_replies=true&include_rts=false".format(
            handle)
        headers = {
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAAyQDAEAAAAAg1KcJ6Vghr4g8Jh%2FU5O6%2BwAwqm8%3DAIOa10IuJYpu7UF1Qnob79dxjP0Knd0PybNcbykTnid1jcQSzY',
        }

        response = requests.get(url, headers=headers)
        if (response.status_code != 200):
            return None
        result = response.json()
    except Exception as e:
        logging.error("error is {}".format(e))
    return result
