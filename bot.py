# -----------------------------------------------------------
# A basic Twitter bot used to teach others about interacting
# with APIs 
#
# Built by Jack Fales
# -----------------------------------------------------------

import tweepy
import config
import time

# Authentication --------------------------------------------

auth = tweepy.OAuthHandler(config.API_KEY, config.API_SECRET_KEY)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_SECRET_TOKEN)
api = tweepy.API(auth)

# Helper functions ------------------------------------------

FILE_NAME = 'last_seen_id.txt'

def retrieveLastSeenId(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def storeLastSeenId(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

# Main functions --------------------------------------------

def followAll():
    """Follows all followers"""
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()

def replyToMentions():
    """Replies to 20 most recent mentions if not interacted with before in chronological order"""
    last_seen_id = retrieveLastSeenId(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')
    for mention in reversed(mentions):
        last_seen_id = mention.id
        storeLastSeenId(last_seen_id, FILE_NAME)

        # Functionality
        text = 'Hello World!'
        api.update_status('@' + mention.user.screen_name + ' ' + text, mention.id)

def directMessageMentions():
    """Direct messages 20 most recent mentions if not interacted with before in chronological order"""
    last_seen_id = retrieveLastSeenId(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')
    for mention in reversed(mentions):
        last_seen_id = mention.id
        storeLastSeenId(last_seen_id, FILE_NAME)

        # Functionality
        text = 'Hello World!'
        api.send_direct_message(mention.user.id, text)

def likeRecentTweets():
    """Likes 20 most recent tweets (including retweets) on timeline if not interacted with before in chronological order"""
    last_seen_id = retrieveLastSeenId(FILE_NAME)
    recent_tweets = api.home_timeline(last_seen_id, tweet_mode='extended')
    for tweet in reversed(recent_tweets):
        last_seen_id = tweet.id
        storeLastSeenId(last_seen_id, FILE_NAME)

        # Functionality
        if not tweet.favorited:
            tweet.favorite()


# Loop to run the bot ---------------------------------------

while True:
    followAll()
    replyToMentions()
    likeRecentTweets()
    directMessageMentions()
    time.sleep(10)