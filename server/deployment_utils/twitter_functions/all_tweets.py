import tweepy 
from .config import BEARER_TOKEN
from .sentiment import getSentimentalAnalysis

def getAllTweets() :
    client = tweepy.Client(BEARER_TOKEN)
    query = f"(#cybersecurity OR cybersecurity OR #CyberSecurity OR CyberSecurity) is:verified "
    responseCollection = []
    response = client.search_recent_tweets(query=query,
                              tweet_fields = ['public_metrics', 'context_annotations', 'created_at'], expansions = ['author_id','attachments.media_keys','referenced_tweets.id'], max_results=50,
                              media_fields=['preview_image_url','url'])
    responseCollection.append(response)
    metadata = response.meta
    next_token = metadata.get("next_token")

    for  x in range(2):
        response = client.search_recent_tweets(query=query,
                              tweet_fields = ['public_metrics', 'context_annotations', 'created_at'], expansions = ['author_id','attachments.media_keys','referenced_tweets.id'] , max_results=50, 
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
                if tweet.referenced_tweets: 
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
                retweet_count = int(response.data.public_metrics[key])

            new_tweet = {
                    'text' : response.data.text.replace("\n", ''),
                    "username" : client.get_user(id = response.data.author_id).data['username'],
                    'retweets' : retweet_count,
                    'sentiment' : sentiments[count]['sentiment'],
                    'score' : sentiments[count]['score'],
                    'date_created' : (response.data.created_at).strftime('%m/%d/%Y'),
                    'media_url' : mediaUrl
                }
            all_tweets.append(new_tweet)
        all_tweets = sorted(all_tweets, key=lambda x: x['retweets'], reverse=True)[:50]

        msg = 'all tweets retrieved successfully'
    except Exception as e :
        status_code = 400
        error = str(e)
        is_ok = False
        msg = 'failed to retrieve tweets'
        all_tweets = ''
    
    response_dict = {
    'tweets' : all_tweets,
    'statusCode' : status_code,
    'message' : msg,
    'error' : error,
    'isOk' : is_ok
    }

    return response_dict, status_code

if __name__ == "__main__":
    response, status_code = getAllTweets()
    print(response)