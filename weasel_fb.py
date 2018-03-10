#!/usr/bin/env python3
import argparse, facebook

parser = argparse.ArgumentParser(description='Download your likes, posts and comments from Facebook')
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


call_all_facebook(args.access_token, args.version, args.limit)
