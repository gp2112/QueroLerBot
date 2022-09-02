from querolerbot import *

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

