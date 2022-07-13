import re
import tweepy 
from config import BEARER_TOKEN
from sentiment import getSentimentalAnalysis

def testGetAllTweets():

    client = tweepy.Client(BEARER_TOKEN)
    query = f"(#cybersecurity OR cybersecurity OR #CyberSecurity OR CyberSecurity) is:retweet "
    highest_retweet = 0 
    responseCollection = []
    response = client.search_recent_tweets(query=query,
                              tweet_fields = ['public_metrics', 'context_annotations', 'created_at'], expansions = ['author_id','attachments.media_keys','referenced_tweets.id'], max_results=10,
                              media_fields=['preview_image_url','url'])
    responseCollection.append(response)
    metadata = response.meta
    next_token = metadata.get("next_token")

    for  x in range(2):
        response = client.search_recent_tweets(query=query,
                              tweet_fields = ['public_metrics', 'context_annotations', 'created_at'], expansions = ['author_id','attachments.media_keys','referenced_tweets.id'] , max_results=10, 
                              media_fields=['preview_image_url','url'], next_token = next_token)
        responseCollection.append(response)
        metadata = response.meta
        next_token = metadata.get("next_token")
        
    try: 
        status_code = 200
        error = None
        is_ok = True
        referenced_tweets = []
        all_tweets =[]
        media = {}
    #get a list of tweets referenced in retrieved tweets
        for response in responseCollection:
            for tweet in response.data :
                tweet_id = tweet.referenced_tweets[0]['id']
                referenced_tweet = client.get_tweet(tweet_id, tweet_fields = ['public_metrics', 'context_annotations', 'created_at'], 
                expansions = ['author_id', 'attachments.media_keys'], media_fields = ['preview_image_url', 'url']) 
                referenced_tweets.append(referenced_tweet)
    # get a dict of all media within referenced tweets, with the media_key as the key and a list of the media keys as the fields. 
        for response in referenced_tweets:
            for key in response.includes:
                if key == 'media' :
                    media[response.includes[key][0].media_key] = response.includes[key][0]
    # get a list of all tweets 
        text = [response.data for response in referenced_tweets]
        sentiments = getSentimentalAnalysis(text)

        for count, response in enumerate(referenced_tweets) : 
            attachments = response.data.attachments
            if attachments != None :
                media_keys = attachments['media_keys']
                if media[media_keys[0]].url :
                    mediaUrl = (media[media_keys[0]].url)
                else :
                    mediaUrl = None
            else :
                    mediaUrl = None
            for key in response.data.public_metrics:
              if key == 'retweet_count':
                retweet_count = response.data.public_metrics[key]

            new_tweet = {
                    'text' : tweet.text.replace("\n", ''),
                    "username" : client.get_user(id = response.data.author_id).data['username'],
                    'retweets' : retweet_count,
                    'sentiment' : sentiments[count]['sentiment'],
                    'score' : sentiments[count]['score'],
                    'date_created' : (response.data.created_at).strftime('%m/%d/%Y'),
                    'media_url' : mediaUrl
                }
            all_tweets.append(new_tweet)
    
        msg = 'all tweets retrieved successfully'
    except Exception as e :
        status_code = 400
        error = str(e)
        is_ok = False
        msg = 'failed to retrieve articles'
        all_tweets = ''

    response_dict = {
    'tweets' : all_tweets,
    'statusCode' : status_code,
    'message' : msg,
    'error' : error,
    'isOk' : is_ok
    }

    return response_dict, status_code

def testGetTopTweet() :
    client = tweepy.Client(BEARER_TOKEN)
    query = f"(#cybersecurity OR cybersecurity OR #CyberSecurity OR CyberSecurity) is:retweet "
    responseCollection = []
    response = client.search_recent_tweets(query=query,
                              tweet_fields = ['public_metrics', 'context_annotations', 'created_at'], expansions = ['author_id','attachments.media_keys','referenced_tweets.id'], max_results=100,
                              media_fields=['preview_image_url','url'])
    responseCollection.append(response)
    metadata = response.meta
    next_token = metadata.get("next_token")

    for  x in range(2):
        response = client.search_recent_tweets(query=query,
                              tweet_fields = ['public_metrics', 'context_annotations', 'created_at'], expansions = ['author_id','attachments.media_keys','referenced_tweets.id'] , max_results=100, 
                              media_fields=['preview_image_url','url'], next_token = next_token)
        responseCollection.append(response)
        metadata = response.meta
        next_token = metadata.get("next_token")
        
    try: 
        status_code = 200
        error = None
        is_ok = True
        referenced_tweets = []
        highest_retweets = 0
        media = {}
        for response in responseCollection:
            for tweet in response.data :
                tweet_id = tweet.referenced_tweets[0]['id']
                referenced_tweet = client.get_tweet(tweet_id, tweet_fields = ['public_metrics', 'context_annotations', 'created_at'], 
                expansions = ['author_id', 'attachments.media_keys'], media_fields = ['preview_image_url', 'url']) 
                referenced_tweets.append(referenced_tweet)
    # get a dict of all media within referenced tweets, with the media_key as the key and a list of the media keys as the fields. 
            
        for response in referenced_tweets:
            for key in response.includes:
                if key == 'media' :
                    media[response.includes[key][0].media_key] = response.includes[key][0]
    
        for response in referenced_tweets :
            if response.data.public_metrics['retweet_count'] > highest_retweets :
                highest_retweets = response.data.public_metrics['retweet_count']
                current_top_tweet = response 
        sentiment,score = getSentimentalAnalysis(current_top_tweet.data['text'])
        attachments = current_top_tweet.data.attachments
        if attachments != None :
            media_keys = attachments['media_keys']
            if media[media_keys[0]].preview_image_url :
                mediaUrl = (media[media_keys[0]].preview_image_url)
            else :
                mediaUrl = None
        else :
                mediaUrl = None

        top_tweet = {
                   'text' : current_top_tweet.data['text'].replace("\n", ''),
                   "username" : client.get_user(id = current_top_tweet.data.author_id).data['username'],
                   'retweets' : highest_retweets,
                   'sentiment' : sentiment,
                   'score' : score,
                   'mediaUrl' : mediaUrl
               } 
        msg = "top tweet successfully retrieved"

    except Exception as e :
        status_code = 400
        error = str(e)
        is_ok = False
        msg = 'failed to retrieve articles'
        top_tweet = ''

    response_dict = {
    'tweet' : top_tweet,
    'statusCode' : status_code,
    'message' : msg,
    'error' : error,
    'isOk' : is_ok
    }

    return response_dict, status_code
if __name__ == '__main__':
    print(testGetAllTweets())