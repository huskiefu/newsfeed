from inspect import getcallargs
from fastapi import FastAPI, Request
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from deployment_utils import (
    getCveArticles,
    getHackerNewsArticles,
    getCywareArticles,
    getArticles,
    getHashtags,
    getTopTweet,
    getAllTweets,
    ArticleResponse,
    HashtagResponse,
    TweetResponse,
    AllTweetsResponse
)

application = FastAPI()

origins = [
    "http://localhost",
    "https://localhost:5002",
    "http://localhost:3001",
]

application.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@application.get("/All_articles", response_model = ArticleResponse)
def allArticles():
    response,status_code = getArticles()
    return JSONResponse(content= jsonable_encoder(response), status_code=status_code)
    
@application.get("/All_tweets", response_model = AllTweetsResponse)
def AllTweets():
    response,status_code = getAllTweets()
    return JSONResponse(content = jsonable_encoder(response),status_code = status_code)

@application.get("/Top_tweet", response_model =TweetResponse)
def topTweet():
    response,status_code = getTopTweet()
    return JSONResponse(content = jsonable_encoder(response),status_code = status_code)

@application.get("/Hashtags", response_model = HashtagResponse)
def hashTags():
    response,status_code = getHashtags()
    return JSONResponse(content = jsonable_encoder(response),status_code = status_code)

@application.get("/Hackernews_articles", response_model = ArticleResponse)
def hackerNewsArticles():
    response,status_code = getHackerNewsArticles()
    return JSONResponse(content= jsonable_encoder(response), status_code=status_code)

@application.get("/Cyware_articles", response_model = ArticleResponse)
def cywareArticles():
    response,status_code = getCywareArticles()
    return JSONResponse(content= jsonable_encoder(response), status_code=status_code)

@application.get("/Cve_articles", response_model = ArticleResponse)
def cveArticles():
    response,status_code = getCveArticles()
    return JSONResponse(content= jsonable_encoder(response), status_code=status_code)



if __name__ == '__main__':
    uvicorn.run('main:application', host='0.0.0.0', port=5002, reload=True)


    