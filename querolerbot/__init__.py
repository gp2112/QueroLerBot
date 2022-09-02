from requests_oauthlib import OAuth1
from urllib.parse import urlparse
from datetime import datetime, timedelta
import antipay
import requests
import database
import time
import re
import random
import os
import toml


with open('config.toml') as f:
    config = toml.load(f)

username = config['twitter']['username']
api_url = config['twitter']['api_url']

consumer_key = os.environ.get('QUEROLER_CONSUMER_KEY', '')
consumer_secret = os.environ.get('QUEROLER_CONSUMER_SECRET', '')
access_token_key = os.environ.get('QUEROLER_ACCESS_KEY', '')
access_token_secret = os.environ.get('QUEROLER_ACCESS_SECRET', '')
token = os.environ.get('QUEROLER_TOKEN', '')

errors = config['messages']['errors']

succ_msgs = config['messages']['success']

# delay entre cada checagem de menções em segundos
DELAY = config['general']['delay']


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
        data = r.json()['data']
        self.id = data['id']

    def oauth_header(self):
        oauth = OAuth1(consumer_key, consumer_secret,
                    access_token_key, access_token_secret,
                    signature_method="HMAC-SHA1")
        return oauth

    def get_mentions(self, start_time=None, user_id=None, fields=None):
        params = {}
        if start_time is not None:
            params['start_time'] = start_time
        if user_id is None:
            user_id = self.id
        if fields is not None:
            params['expansions'] = ','.join(fields)

        r = requests.get(api_url+f'2/users/{user_id}/mentions', headers=self.headers, params=params)
        # print(r.json())
        return r.json()

    def get_tweet(self, tweet_ids, fields=None):#referenced_tweets
        tweet_ids = ','.join(tweet_ids)
        params = {'ids':tweet_ids}

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
        data = {'status':content}
        if reply_to is not None:
            data['in_reply_to_status_id'] = reply_to
        r = requests.post(api_url+'1.1/statuses/update.json', data=data, auth=self.oauth_header())
        return r.json()


# return real URL from Twitter's shortner
def real_url(url):
   r = requests.get(url)
   return r.url

def main():
   twitter = Twitter(token)
   twitter.auth() #get user ID

   print('Bot rodando...')

   l_time = datetime.now()
   while True:
      mentions = twitter.get_mentions(start_time=l_time.isoformat()+'Z', fields=['referenced_tweets.id', 'author_id'])
      if 'data' in mentions:

         print(mentions)
         for i, tweet in enumerate(mentions['data']):
            user_name = mentions['includes']['users'][i]['username']
            if 'referenced_tweets' not in tweet:
               url = re.search("(?P<url>https?://[^\s]+)", tweet['text'])
               if url is None:
                  continue
               url = url.group("url")
            else:
               t = twitter.get_tweet([tweet['referenced_tweets'][0]['id']])
               if t is None: continue
               print(f"{tweet['id']} {t[0]['text']} ")

               url = re.search("(?P<url>https?://[^\s]+)", t[0]['text']) # Gets the first URL
               if url is None:
                  #twitter.send_tweet(f'@{user_name} '+errors['url_not_found'], reply_to=tweet['id'])
                  continue
               url = url.group('url')
            url = real_url(url) # change Twitter's URL for the original one
            url = urlparse(url)
            url = f'{url.scheme}://{url.netloc}{url.path}' # erase GET params ;)
            article = database.get_article(main_url=url)
            if article is not None:
               r = twitter.send_tweet(f'@{user_name} '+success(article[0]), reply_to=tweet['id'])
               #print(r)
            else:
               article = antipay.break_paywall(url)
               if article is None:
                  twitter.send_tweet(f'@{user_name} '+errors['text_not_found'], reply_to=tweet['id'])
               else:
                  database.insert_article(**article)
                  r = twitter.send_tweet(f'@{user_name} '+success(article['telegraph']), reply_to=tweet['id'])
                     #print(r)
         print('Aguardando Tweets...')
      time.sleep(DELAY)
      l_time = datetime.now()-timedelta(seconds=DELAY)

if __name__ == '__main__':
   main()
   
