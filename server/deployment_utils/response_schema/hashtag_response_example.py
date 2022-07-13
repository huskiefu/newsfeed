from pydantic import BaseModel
from typing import Optional


class HashtagResponse(BaseModel):
    hashtags : list[tuple]
    statusCode: int
    message : str 
    message: str
    error: Optional[str] = None
    isOk: bool

    class Config:
        schema_extra = {
            'hashtags' : 
                    [('BizTalks', 19), ('AI', 5), ('RSAC', 5), ('research', 4), ('infosec', 4), ('Security', 4), ('splunkconf22', 4), ('MachineLearning', 3), ('tech', 3), ('technology', 3)],
            'statusCode' : 200,
            'message' : 'hashtags successfully retrieved',
            'error' : 'error',
            'isOk' : True
        }