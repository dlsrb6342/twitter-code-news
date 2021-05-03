from email_utils import connectSmtp, makeMsg, sendEmail
from requests_oauthlib import OAuth1
from credentials import twitter_credential
import requests, datetime, sys


def getTweets():
    auth = OAuth1(twitter_credential['TWITTER_APP_KEY'],
            twitter_credential['TWITTER_APP_SECRET'],
            twitter_credential['TWITTER_OAUTH_TOKEN'], 
            twitter_credential['TWITTER_OAUTH_TOKEN_SECRET'])

    response = requests.request(
            "GET", 'https://api.twitter.com/1.1/statuses/user_timeline.json',
            params = { 'count': 50 }, auth = auth)

    tweets = list()
    for tweet in response.json():
        aggregated = dict()
        aggregated['tweet_id'] = tweet['id']
        aggregated['created_at_string'] = tweet['created_at']
        aggregated['created_at'] = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
        aggregated['text'] = tweet['text']
        aggregated['urls'] = tweet['entities']['urls']
        aggregated['user'] = tweet['user']['screen_name']

        if len(aggregated['urls']) == 0:
            continue
        aggregated['url'] = aggregated['urls'][0]['expanded_url']
        aggregated['tweet_url'] = f'https://twitter.com/{aggregated["user"]}/status/{aggregated["tweet_id"]}'
        tweets.append(aggregated)
    return tweets


def filterTweets(tweets):
    today = datetime.datetime.today() \
                    .replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=datetime.timezone.utc)
    yesterday = today - datetime.timedelta(days=1)
    return list(filter(lambda t: t['created_at'] >= yesterday and t['created_at'] <= today, tweets))


def crawlTweets():
    tweets = getTweets()
    filtered_tweets = filterTweets(tweets)
    if len(filtered_tweets) == 0:
        sys.exit()

    smtp = connectSmtp()
    msg = makeMsg(filtered_tweets)
    sendEmail(smtp, msg)
