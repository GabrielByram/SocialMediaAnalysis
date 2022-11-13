import os

import tweepy
from datetime import date
from dotenv import load_dotenv

load_dotenv('.env')

client = None

def getClient():
    global client

    if(client != None):
        return client

    client = tweepy.Client(bearer_token =  os.environ['AUTH_BEARER_TOKEN'],consumer_key= os.environ['AUTH_CONSUMER_KEY'], 
       consumer_secret= os.environ['AUTH_COSUMER_SECRET'], access_token= os.environ['AUTH_ACCESS_TOKEN'],
        access_token_secret=os.environ['AUTH_ACCESS_TOKEN_SECRET'],return_type='json')
        
    return client




