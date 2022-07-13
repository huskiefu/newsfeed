from .hackernews import getHackerNewsArticles
from .cyware import getCywareArticles
from .cve import getCveArticles
import threading

def getHacker(articleSet):
    articles,status_code = getHackerNewsArticles()
    for article in articles['articles'] :
        articleSet.append(article)
    return articleSet


def getCyware(articleSet):
    articles,status_code = getCywareArticles()
    for article in articles['articles'] : 
        articleSet.append(article)
    return articleSet

def getCve(articleSet):
    articles,status_code = getCveArticles()
    for article in articles['articles'] :
        articleSet.append(article)
    return articleSet

def getArticles(): 
    articleSet = []
    # start = timer()

    # getHacker(hackerSet)
    # getCyware(cywareSet)
    # getCve(cveSet)

    # hacker = mp.Process(target = getHacker, args = (hackerSet,))
    # cyware = mp.Process(target = getCyware, args = (cywareSet,))
    # cve = mp.Process(target = getCve, args = (cveSet,))
    try :
        error = None
        is_ok = True 
        status_code = 200
        hacker = threading.Thread(target = getHacker, args = (articleSet,))
        cyware = threading.Thread(target = getCyware, args = (articleSet,))
        cve = threading.Thread(target = getCve, args = (articleSet,))

        hacker.start()
        cyware.start()
        cve.start()

        hacker.join()
        cyware.join()
        cve.join()

        # end = timer()
        articleSet.sort(key=lambda x : x['date'], reverse = True)
        # print(f'HackerSet ====== {hackerSet}')
        # print(f'CywareSet ====={cywareSet}')
        # print(f'CveSet ====== {cveSet} ')
        # print(end - start)
        msg = 'successfully retrieved articles'
    except Exception as e: 
        error = str(e)
        is_ok = False
        status_code = 400
        msg = 'error retrieving articles'

    response_dict = {
            'articles' : articleSet,
            'statusCode' : status_code,
            'message' : msg,
            'error' : error,
            'isOk' : is_ok
        }

    return response_dict, status_code

if __name__ == "__main__":
    articles,status_code = getArticles()
    print(articles)

    
    