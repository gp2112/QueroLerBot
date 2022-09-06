from requests_oauthlib import OAuth1
from querolerbot.config import read_config, check_config_file, HOME
from querolerbot import database
import requests
import time
import random
import os
import sys
import toml

check_config_file()
config = read_config()
username = config['twitter']['username']
api_url = config['twitter']['api_url']

consumer_key = os.environ.get('QUEROLER_CONSUMER_KEY', 'NO_CONSUMER_KEY')
consumer_secret = os.environ.get('QUEROLER_CONSUMER_SECRET', 'NO_CONSUMER_SECRET')
access_token_key = os.environ.get('QUEROLER_ACCESS_KEY', 'NO_A_TOKEN')
access_token_secret = os.environ.get('QUEROLER_ACCESS_SECRET', 'NO_A_TOKEN_SECRET')
token = os.environ.get('QUEROLER_BAERER_TOKEN', 'NO_TOKEN')

errors = config['messages']['error']

succ_msgs = config['messages']['success']

# delay entre cada checagem de menções em segundos
DELAY = config['general']['delay']

try:
    f = open(HOME+'/.auth', 'r')
    env = toml.load(f)
    f.close()
    consumer_key = env['QUEROLER_CONSUMER_KEY']
    consumer_secret = env['QUEROLER_CONSUMER_SECRET']
    access_token_key = env['QUEROLER_ACCESS_KEY']
    access_token_secret = env['QUEROLER_ACCESS_SECRET']
    token = env['QUEROLER_BAERER_TOKEN']
except FileNotFoundError:
    sys.exit(1)

try:
    f = open(HOME+'/'+config['database']['name'])
    f.close()
except FileNotFoundError:
    database.create_db()


def success(url):
    random.seed(time.time())
    i = random.randint(0, len(succ_msgs)-1)
    return succ_msgs[i]+'\n'+url


class Twitter:
    def __init__(self, token, id=None):
        self.token = token
        self.headers = {
            'Authorization': 'Bearer '+token
        }
        self.id = id

    def auth(self):
        r = requests.get(api_url+'2/users/by/username/'+username, headers=self.headers)
        try:
            data = r.json()['data']
            self.id = data['id']
        except KeyError:
            print(consumer_key, consumer_secret, access_token_key, access_token_secret, token)
            print(r.json())
            sys.exit(1)


    def oauth_header(self):
        oauth = OAuth1(consumer_key, consumer_secret,
                    access_token_key, access_token_secret,
                    signature_method="HMAC-SHA1")
        return oauth

    def get_mentions(self, since_id, user_id=None, fields=None):
        params = {}
        params['since_id'] = since_id

        if user_id is None:
            user_id = self.id
        if fields is not None:
            params['expansions'] = ','.join(fields)

        r = requests.get(api_url+f'2/users/{user_id}/mentions', headers=self.headers, params=params)
        # print(r.json())
        return r.json()

    def get_tweet(self, tweet_ids, fields=None):#referenced_tweets
        tweet_ids = ','.join(tweet_ids)
        params = {'ids': tweet_ids}

        if fields is not None:
            params['expansions'] = ','.join(fields)
        r = requests.get(api_url+'2/tweets', headers=self.headers, params=params)
        if 'data' not in r.json():
            return None
        return r.json()['data']

    def get_timeline(self, user_id, since_id=None):
        params = {}
        if since_id is not None:
            params['since_id'] = since_id
        r = requests.get(api_url+f'2/users/{user_id}/tweets', headers=self.headers, params=params)
        if 'data' not in r.json():
            return None
        print(r.json())
        return r.json()["data"]

    def send_tweet(self, content, reply_to=None):
        data = {'status': content}
        if reply_to is not None:
            data['in_reply_to_status_id'] = reply_to
        r = requests.post(api_url+'1.1/statuses/update.json', data=data, auth=self.oauth_header())
        return r.json()


# return real URL from Twitter's shortner
def real_url(url):
    r = requests.get(url)
    return r.url
