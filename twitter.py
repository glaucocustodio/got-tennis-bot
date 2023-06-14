import pytwitter
import os
from dotenv import load_dotenv

load_dotenv()

def tweet(message):
  consumer_key = os.environ['TWITTER_CONSUMER_KEY']
  consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
  access_token = os.environ['TWITTER_ACCESS_TOKEN']
  access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

  twitter_api = pytwitter.Api(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_secret=access_token_secret
  )

  return twitter_api.create_tweet(text=message)
