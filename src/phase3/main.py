import json

from src.config import *
from src.logic.api import API
from src.phase1.tweet_database_helper import TweetDatabaseHelper


def get_personal_info(user):
    result = api.get_user_by_id(user)
    related_url = None
    profile_banner = None

    try:
        related_url = result.entities['url']['urls'][0]['expanded_url']
    except:
        pass

    try:
        profile_banner = result.profile_banner_url
    except:
        pass

    return {
        'id': result.id,
        'name': result.name,
        'username': result.screen_name,
        'location': result.location,
        'bio': result.description,
        'like_count': result.favourites_count,
        'followers_count': result.followers_count,
        'following_count': result.friends_count,
        'list_count': result.listed_count,  # The number of public lists that this user is a member of
        'tweet_count': result.statuses_count,  # The number of Tweets (including retweets) issued by the user
        'created_at': result.created_at.isoformat(),  # the UTC datetime that the user account was created on Twitter
        'profile_background_image': result.profile_background_image_url_https,
        'profile_image_url_https': result.profile_image_url_https,
        'isProtected': result.protected,
        'verified': result.verified,
        'related_url': related_url,
        'profile_banner': profile_banner,
    }


def get_tweets(user, n):
    result = api.get_tweet_by_user_id(user, n)

    result_list = []
    for tweet in result:
        medias = []
        try:
            medias = [item['url'] for item in tweet.entities['media']]
        except:
            pass

        result_list.append({
            'tweet_id': tweet.id,
            'tweet_text': tweet.full_text,
            'tweet_created_at': tweet.created_at.isoformat(),
            'tweet_source': tweet.source,
            'tweet_fav_count': tweet.favorite_count,
            'tweet_ret_count': tweet.retweet_count,
            'tweet_geo': tweet.geo,
            'tweet_coordinates': tweet.coordinates,
            'is_quote': tweet.is_quote_status,
            'lang': tweet.lang,
            'user_mentions': [
                {
                    'id': item['id'],
                    'screen_name': item['screen_name']
                } for item in tweet.entities['user_mentions']
            ],
            'hashtags': [item['text'] for item in tweet.entities['hashtags']],
            'urls': [item['url'] for item in tweet.entities['urls']],
            'medias': medias
        })

    return result_list


def get_followers(user, n):
    result = api.get_followers_by_user_id(user, n)

    return [
        {
            'id': item.id,
            'name': item.name,
            'username': item.screen_name,
            'followers_count': item.followers_count,
            'following_count': item.friends_count,
        }
        for item in result
    ]


def get_following(user, n):
    result = api.get_following_by_user_id(user, n)

    return [
        {
            'id': item.id,
            'name': item.name,
            'username': item.screen_name,
            'followers_count': item.followers_count,
            'following_count': item.friends_count,
        }
        for item in result
    ]


def get_subscribed_lists(user, n):
    result = api.get_subscribed_lists(user, n)

    return [
        {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'member_count': item.member_count,
            'subscriber_count': item.subscriber_count,
            'mode': item.mode,
            'created_at': item.created_at.isoformat(),
        }
        for item in result
    ]


if __name__ == '__main__':
    # Initialize
    api = API()
    database = TweetDatabaseHelper(train_csv)

    for item in database.get_distinct_users()[85 + 2:]:
        user_id = item[0]

        personal_info = get_personal_info(user_id)
        tweets = get_tweets(user_id, 100)
        followers = get_followers(user_id, 100)
        following = get_following(user_id, 100)
        lists = get_subscribed_lists(user_id, 100)

        json_result = json.dumps({
            'user': personal_info,
            'tweets': tweets,
            'followers': followers,
            'following': following,
            'lists': lists,
        })
        print(json_result + ',')
