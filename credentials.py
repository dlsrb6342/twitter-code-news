import os


# twitter credential
twitter_credential = {
    'TWITTER_APP_KEY': os.environ['TWITTER_APP_KEY'],
    'TWITTER_APP_SECRET': os.environ['TWITTER_APP_SECRET'],
    'TWITTER_OAUTH_TOKEN': os.environ['TWITTER_OAUTH_TOKEN'],
    'TWITTER_OAUTH_TOKEN_SECRET': os.environ['TWITTER_OAUTH_TOKEN_SECRET']
}
# gmail credential

gmail_credential = {
    'GMAIL_ID': os.environ['GMAIL_ID'],
    'GMAIL_PASSWORD': os.environ['GMAIL_PASSWORD']
}
