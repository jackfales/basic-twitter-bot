import tweepy
import config
import time

auth = tweepy.OAuthHandler(config.API_KEY, config.API_SECRET_KEY)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_SECRET_TOKEN)
api = tweepy.API(auth)

# Helper functions ------------------------------

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

# -----------------------------------------------

"""
Follows all followers
"""
def followAll():
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()

"""
Replies to 20 most recent mentions if not interacted with before in chronological order
"""
def replyToMentions():
    last_seen_id = retrieveLastSeenId(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')
    for mention in reversed(mentions):
        last_seen_id = mention.id
        storeLastSeenId(last_seen_id, FILE_NAME)

        # Functionality
        text = ''
        api.update_status('@' + mention.user.screen_name + ' ' + text, mention.id)

"""
Direct messages 20 most recent mentions if not interacted with before in chronological order
"""
def directMessageMentions():
    last_seen_id = retrieveLastSeenId(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')
    for mention in reversed(mentions):
        last_seen_id = mention.id
        storeLastSeenId(last_seen_id, FILE_NAME)

        # Functionality
        text = ''
        api.send_direct_message(mention.user.id, text)

# Infinite loop to keep running the bot
while True:
    followAll()
    replyToMentions()
    time.sleep(10)