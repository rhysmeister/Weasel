#!/usr/bin/env python3
import argparse, facebook, Menoetius
import pandas as pd

parser = argparse.ArgumentParser(description='Download your likes, posts and comments from Facebook')
parser.add_argument('-t', '--access_token', type=str, help='Facebook Access Token. Get one from the Graphi API Explorer')
parser.add_argument('-v', '--version', type=str, default="2.11", help='The version of the Facebook Graph API')
parser.add_argument('-l', '--limit', type=int, default=4000, help='The number of results to fetch per call to the Graph API')
parser.add_argument('-u', '--tweeter', type=str, help='Twitter username to download the timeline of.')
parser.add_argument('-a', '--no_analysis', action="store_true", default=False, help="Don't run analysis on the datas.")


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

def get_graph(access_token, version):
    graph = facebook.GraphAPI(access_token=access_token, version=version)
    return graph

def get_generic_call(access_token, version, thing_to_call, limit):
    g = get_graph(access_token,version)
    thing_call_count = 1
    thing_count = 0
    things = g.get_object('me/{0}?limit={1}'.format(thing_to_call, limit))
    print(things)
    while 'paging' in things:
        for thing in things["data"]:
            print(thing)
            thing_count += 1
        if 'cursors' in things['paging']:
            after = things['paging']['cursors']['after']
        else:
            after = things['paging']['next']
        things = g.get_object('me/{0}?limit={1}&after={2}'.format(thing_to_call,
                                                                  limit,
                                                                  after))
        thing_call_count += 1
    print("The number of {0} calls performed was {1} and {2} {3} were retrieved.".format(thing_to_call,
                                                                                         thing_call_count,
                                                                                         thing_count,
                                                                                         thing_to_call))

def get_likes(access_token, version, limit):
    get_generic_call(access_token, version, 'likes', limit)

def get_posts(access_token, version, limit):
    get_generic_call(access_token, version, 'posts', limit)

def get_friends(access_token, version, limit):
    get_generic_call(access_token, version, 'friends', limit)

def get_feed(access_token, version, limit):
    get_generic_call(access_token, version, 'feed', limit)

def get_photos(access_token, version, limit):
    get_generic_call(access_token, version, 'photos', limit)

def call_all_facebook(access_token, version, limit):
    get_likes(access_token, version, limit)
    get_posts(access_token, version, limit)
    get_friends(access_token, version, limit)
    get_feed(access_token, version, limit)
    get_photos(access_token, version, limit)

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

if args.access_token is not None:
    call_all_facebook(args.access_token, args.version, args.limit)
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
except Exception as e:
    raise e
