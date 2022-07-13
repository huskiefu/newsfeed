from types import NoneType
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree 
from dateutil import parser 

def getHackerNewsArticles():
    try:
        status_code = 200
        error = None
        is_ok = True
        articleList = []
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        browser = webdriver.Chrome(options = options)
        url = "https://thehackernews.com/"
        browser.get(url)
        articles = browser.find_elements(By.CLASS_NAME, 'story-link')
        article_count = len(articles)
        condition = True

        while (condition == True): 
            browser2 = webdriver.Chrome(options = options)
            browser2.get(url)
            for i in range(article_count):
                articles = browser2.find_elements(By.CLASS_NAME, 'story-link')
                article, status = retrieveArticle(articles[i],browser2)
                
                if article['title'] != "":
                    articleList.append(article)
                if status == 1 :
                    break
            if (len(articleList) == article_count and status == 0 ):
                condition = False
                msg = 'articles successfully retrieved'
    
    except Exception as e : 
        status_code = 400
        error = str(e)
        is_ok = False
        articleList = []

    response_dict = {
            'articles' : articleList,
            'statusCode' : status_code,
            'message' : msg,
            'error' : error,
            'isOk' : is_ok
        }
    
    return response_dict, status_code

def retrieveArticle(article,browser):
    article.click()
    tree = etree.HTML(browser.page_source)
    title = tree.find('.//h1[@class = "story-title"]/a')

    #check for ads
    if type(title) == NoneType:
        print('ad found')
        articleList = []
        browser.quit()
        return articleList,1

    contents = browser.find_elements(By.XPATH,'.//div[@id = "articlebody"]/p')  
    articleContent = ''
    for i in range(3):
        articleContent = articleContent + contents[i].text
    newArticle = {
        'title' : "",
        'content' : "",
        'date': "",
        'link' : ""
    }
    newArticle['title'] = title.text
    # newArticle['content'] = articleContent.replace("\"", "'") for visibility as " shows as \" because content is stored as a string.
    newArticle['content'] = articleContent
    newArticle['link'] = title.get('href')
    newArticle['date'] = parser.parse(tree.find('.//div[@class = "postmeta"]/span').text).strftime('%m/%d/%Y')
    browser.execute_script("window.history.go(-1)")
    return newArticle,0

if __name__ == "__main__":
    articleList, status_code = getHackerNewsArticles()
    print(articleList['articles'])

   
        
    