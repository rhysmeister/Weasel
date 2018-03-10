#!/usr/bin/env python3
import argparse, facebook, Menoetius
import pandas as pd

parser = argparse.ArgumentParser(description='Retrieve a Twitter users timeline and run some Analysis on it.')
parser.add_argument('-u', '--tweeter', type=str, help='Twitter username to download the timeline of.')
parser.add_argument('-a', '--no_analysis', action="store_true", default=False, help="Don't run analysis on the data.")


args = parser.parse_args()

def run_Menoetius_analysis(text):
    m = Menoetius.Menoetius(text)
    data = { "original_text": m.original_text,
             "lowercase_text": m.lowercase_text,
             "stems": m.stems,
             "pos_tags": m.pos_tags,
             "sentiment_scores": m.sentiment_scores,
             "text_stats": m.text_stats }
    return data

def get_twitter_timeline(twitter_auth, username):
    if 'consumer_key' in twitter_auth.keys():
        import twitter
        api = twitter.Api(consumer_key=twitter_auth['consumer_key'],
                          consumer_secret=twitter_auth['consumer_secret'],
                          access_token_key=twitter_auth['access_token_key'],
                          access_token_secret=twitter_auth['access_token_secret'])
        max_id = None
        tweet_count = 0
        call_count = 0
        data = []
        # Initial batch of most recent tweets
        statuses = api.GetUserTimeline(screen_name=username, count=200, max_id=max_id)
        while len(statuses) > 0:
            data += statuses
            call_count += 1
            for s in statuses:
                #print(s)
                tweet_count += 1
                if max_id is None:
                    max_id = s.id - 1
                elif max_id > int(s.id):
                    max_id = int(s.id) - 1
            #max_id = int(min([s.id for s in statuses]) - 1)
            statuses = api.GetUserTimeline(screen_name=username, count=200, max_id=max_id)
        print("The number of calls performed was {0} and {1} tweets were retrieved.".format(call_count,
                                                                                            tweet_count))
        return data

# TODO? https://github.com/t-davidson/hate-speech-and-offensive-language/tree/master/lexicons

try:
    data = []
    twitter_auth = dict = eval(open("./twitter_auth.dict").read())
    tweets = get_twitter_timeline(twitter_auth, args.tweeter)
    if not args.no_analysis:
        for tweet in tweets:
            d = run_Menoetius_analysis(tweet.text)
            data.append(d)
        tweet_df = pd.DataFrame(data)
        print(tweet_df)
        print(tweet_df.dtypes)
except Exception as e:
    raise e
