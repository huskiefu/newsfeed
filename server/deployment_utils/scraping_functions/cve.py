from selenium import webdriver
from selenium.webdriver.common.by import By
from dateutil import parser

def getCveArticles():
    try:
        status_code = 200
        error = None
        is_ok = True
        articleList = []
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        browser = webdriver.Chrome(options = options)
        url = "https://www.cve.org/Media/News/AllNews"
        browser.get(url)
        articles = browser.find_elements(By.XPATH,'.//h2[@class = "title mt-4 mb-1 is-size-4"]/a')
        article_count = len(articles)
        for i in range(article_count):
            articles = browser.find_elements(By.XPATH,'.//h2[@class = "title mt-4 mb-1 is-size-4"]/a')
            article = retrieveArticle(articles[i],browser)
            articleList.append(article)
        msg = 'articles successfully retrieved'
        
    except Exception as e :
        status_code = 400
        error = str(e)
        is_ok = False
        msg = 'failed to retrieve articles'

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
    newArticle = {
        'title' : "",
        'content' : "",
        'link' : "",
        'date' : ""
    }
    textContainers = browser.find_elements(By.CLASS_NAME,'block')
    newArticle['title'] = browser.find_element(By.CLASS_NAME,'title').text
    newArticle['link'] = browser.current_url
    newArticle['date'] = parser.parse(browser.find_element(By.TAG_NAME,'time').text).strftime('%m/%d/%Y')
    if len(textContainers) > 3 :
        for i in range(3):
            newArticle['content'] = newArticle['content'] + textContainers[i].text
    else :
        for i in range(len(textContainers)) :
            newArticle['content'] = newArticle['content'] + textContainers[i].text
    
    browser.execute_script("window.history.go(-1)")
    return newArticle




if __name__ == "__main__":
    articleList, status_code = getCveArticles()
    print(articleList['articles'])

    

