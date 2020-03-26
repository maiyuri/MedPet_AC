from twython import Twython
import pandas as pd
import json

pd.set_option('display.max_colwidth', 0)

def tweets():
    # Instantiate an object
    python_tweets = Twython('fiOffIFd7f1U4F1xmzLQGuDEL','DyJb9VneX1YUkjBqm1M1YZbMtLjFsqTo6KDYe3XNWidkEFNnll')

    # Create our query
    query = {'q': 'MEDPET', 
            'result_type': '',
            'count': 10,
            'lang': '',
            }

    dict_ = list()
    for status in python_tweets.search(**query)['statuses']:
        tweet = dict()
        tweet['Usuário'] = status['user']['screen_name']
        tweet['Data'] = status['created_at']
        tweet['Tweet'] = status['text']
        tweet['Likes']= status['favorite_count']
        dict_.append(tweet)

    return dict_