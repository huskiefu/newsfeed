from pydantic import BaseModel
from typing import Optional

class ArticleResponse(BaseModel):
    articles = list[object]
    statusCode: int
    message : str 
    error: Optional[str] = None
    isOk: bool

    class Config:
        schema_extra = {
            'articles' : 
                [
                    {
                        'title' : 'article1',
                        'content' : 'article text article text article text article text article text',
                        'date' : '2022-06-08T00:00:00',
                        'link' : 'https://website/article',
                            }],
            'statusCode' : 200,
            'message' : 'article successfully retrieved',
            'error' : 'error',
            'isOk' : True
        }