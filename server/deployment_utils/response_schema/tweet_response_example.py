from pydantic import BaseModel
from typing import Optional


class TweetResponse(BaseModel):
    tweet : object
    statusCode: int
    message : str 
    message: str
    error: Optional[str] = None
    isOk: bool

    class Config:
        schema_extra = {
            'tweet' : {
                    'text' : 'the quick brown fox jumps over the lazy fox',
                    'username' : 'brown_fox',
                    'retweets' : 222,
                    'sentiment': 'neutral',
                    'score' : 0.7,
                },
            'statusCode' : 200,
            'message' : 'tweet successfully retrieved',
            'error' : 'error',
            'isOk' : True
        }