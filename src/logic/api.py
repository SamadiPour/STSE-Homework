import logging

import tweepy as tweepy
from tweepy import TweepError

from src.env import *


class API:
    def __init__(self) -> None:
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)

    # Attribute needed:
    # .full_text
    # .created_at
    # .lang
    # .id_str
    # .user.screen_name --username
    # .user.id
    def get_tweet_by_id(self, tweet_id: str):
        try:
            return self.api.get_status(tweet_id, tweet_mode='extended')
        except TweepError as e:
            logging.warning(tweet_id + ' - ' + e.args[0][0]['message'])
            pass