from pydantic import BaseModel
from typing import Optional

class AllTweetsResponse(BaseModel):
    tweets : list[object]
    statusCode: int
    message : str 
    error: Optional[str] = None
    isOk: bool

    class Config:
        schema_extra = {
            'tweets' : [
                {
                    'text' : 'the quick brown fox jumps over the lazy fox',
                    'username' : 'brown_fox',
                    'retweets' : 222,
                    'sentiment': 'neutral',
                    'score' : 0.7,
                    'date_created' : 270321
                },
                {
                    'text' : 'the quick brown fox jumps over the lazy fox',
                    'username' : 'brown_fox',
                    'retweets' : 222,
                    'sentiment': 'neutral',
                    'score' : 0.7,
                    'date_created' : 270321
                },
            ],
            'statusCode' : 200,
            'message' : 'tweet successfully retrieved',
            'error' : 'error',
            'isOk' : True
        }