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

    def get_user_by_id(self, user_id: str):
        try:
            return self.api.get_user(user_id)
        except TweepError as e:
            # logging.warning(user_id + ' - ' + e.args[0][0]['message'])
            pass

    def get_tweet_by_user_id(self, user_id: str, n: int):
        try:
            return self.api.user_timeline(user_id, count=n, tweet_mode="extended", exclude_replies=False,
                                          include_rts=False)
        except TweepError as e:
            # logging.warning(user_id + ' - ' + e.args[0][0]['message'])
            pass

    def get_followers_by_user_id(self, user_id: str, n: int):
        try:
            return self.api.followers(user_id, count=n)
        except TweepError as e:
            # logging.warning(user_id + ' - ' + e.args[0][0]['message'])
            pass

    def get_following_by_user_id(self, user_id: str, n: int):
        try:
            return self.api.friends(user_id, count=n)
        except TweepError as e:
            # logging.warning(user_id + ' - ' + e.args[0][0]['message'])
            pass

    def get_subscribed_lists(self, user_id: str, n: int):
        try:
            return self.api.lists_all(user_id=user_id, count=n)
        except TweepError as e:
            # logging.warning(user_id + ' - ' + e.args[0][0]['message'])
            pass
