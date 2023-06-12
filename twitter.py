import requests
from requests_oauthlib import OAuth1
import json, os

def tweet(message):
    url = "https://api.twitter.com/2/tweets"

    payload = json.dumps({"text": message})

    consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
    consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
    access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

    oauth = OAuth1(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    )

    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.post(url, headers=headers, data=payload, auth=oauth)

    print(response)

    return response