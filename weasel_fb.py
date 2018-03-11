#!/usr/bin/env python3
import argparse, facebook, json, copy
import pandas as pd
from functions import write_to_excel_file

parser = argparse.ArgumentParser(description='Download a users likes, posts and comments from Facebook')
parser.add_argument('-t', '--access_token', type=str, help='Facebook Access Token. Get one from the Graphi API Explorer')
parser.add_argument('-v', '--version', type=str, default="2.11", help='The version of the Facebook Graph API')
parser.add_argument('-l', '--limit', type=int, default=4000, help='The number of results to fetch per call to the Graph API')

args = parser.parse_args()

def get_graph(access_token, version):
    graph = facebook.GraphAPI(access_token=access_token, version=version)
    return graph

def get_generic_call(access_token, version, thing_to_call, limit):
    g = get_graph(access_token,version)
    thing_call_count = 1
    thing_count = 0
    things = g.get_object('me/{0}?limit={1}'.format(thing_to_call, limit))
    #print(things)
    dataset = []
    for entry in things["data"]:
        dataset.append(entry)
    while 'paging' in things:
        for thing in things["data"]:
            #print(thing)
            thing_count += 1
        if 'cursors' in things['paging']:
            after = things['paging']['cursors']['after']
        else:
            after = things['paging']['next']
        things = g.get_object('me/{0}?limit={1}&after={2}'.format(thing_to_call,
                                                                   limit,
                                                                   after))
        for entry in things["data"]:
            dataset.append(entry)
        thing_call_count += 1
    #print("The number of {0} calls performed was {1} and {2} {3} were retrieved.".format(thing_to_call,
    #                                                                                     thing_call_count,
    #                                                                                     thing_count,
    #                                                                                     thing_to_call))
    #print(dataset)
    return pd.DataFrame.from_dict(dataset)

def get_likes(access_token, version, limit):
    return get_generic_call(access_token, version, 'likes', limit)

def get_posts(access_token, version, limit):
    return get_generic_call(access_token, version, 'posts', limit)

def get_friends(access_token, version, limit):
    return get_generic_call(access_token, version, 'friends', limit)

def get_feed(access_token, version, limit):
    return get_generic_call(access_token, version, 'feed', limit)

def get_photos(access_token, version, limit):
    return get_generic_call(access_token, version, 'photos', limit)

def call_all_facebook(access_token, version, limit):
    list_of_df = []
    likes = get_likes(access_token, version, limit)
    list_of_df.append((likes, 'likes'))
    posts = get_posts(access_token, version, limit)
    list_of_df.append((posts, 'posts'))
    friends = get_friends(access_token, version, limit)
    list_of_df.append((friends, 'friends'))
    feed = get_feed(access_token, version, limit)
    list_of_df.append((feed, 'feed'))
    photos = get_photos(access_token, version, limit)
    list_of_df.append((photos, 'photos'))
    write_to_excel_file(list_of_df)

call_all_facebook(args.access_token, args.version, args.limit)
