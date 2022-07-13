import tweepy 
from .config import BEARER_TOKEN
from collections import Counter
def getHashtags() :
    #Get most popular hashtags relevant to cybersecurity 
    try: 
        status_code = 200
        error = None
        is_ok = True
        client = tweepy.Client(BEARER_TOKEN)
        #Get most recent relevant tweets (1000)

        query = "(#cybersecurity) is:verified lang:en"

        #Iterate through the tweets and retrieve hashtags, place into an array
        response = tweepy.Paginator(client.search_recent_tweets, query=query,
                              tweet_fields = ["public_metrics", "created_at"], expansions = ['author_id'] , max_results=100).flatten(limit = 500)

        hashtags = []
        for tweet in response:
            for key in tweet.entities :
                if key == 'hashtags':
                    for hashtagobject in tweet.entities['hashtags']:
                        if hashtagobject['tag'].lower() != 'cybersecurity':
                            hashtags.append(hashtagobject['tag'])
        msg = "hashtags successfully retrieved"
    except Exception as e:
        status_code = 400
        error = str(e)
        is_ok = False
        msg = 'failed to retrieve hashtags'

    #Count each hashtag and sort according to most to least with a count beside 
    sortedHashtags = Counter(hashtags).most_common(10)
    response_dict = {
        'hashtags' : sortedHashtags,
        'statusCode' : status_code,
        'message' : msg,
        'error' : error,
        'isOk' : is_ok
    }
    
    return response_dict,status_code

if __name__ == "__main__":
    print(getHashtags())