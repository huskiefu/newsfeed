from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import etree 
from dateutil import parser

def getCywareArticles():
    try: 
        status_code = 200
        error = None
        is_ok = True
        articleList = []
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        browser = webdriver.Chrome(options = options)
        url = "https://cyware.com/hacker-news"
        browser.get(url)
        articles = browser.find_elements(By.XPATH,'.//div[@class = "cy-panel__body"]')
        article_count = len(articles)
        
        for i in range(article_count):
            articles = browser.find_elements(By.XPATH,'.//div[@class = "cy-panel__body"]')
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
    
    return response_dict,status_code

def retrieveArticle(article,browser):
    article.click()
    browser.switch_to.window(browser.window_handles[1])
    newArticle = {
        'title' : "",
        'content' : "",
        'link' : "",
        'date' : ""
    }
    textContainers = browser.find_elements(By.XPATH, './/div[@class = "cy-alert__description col-md-7 col-12"]/div/div/div/span')
    newArticle['title'] = browser.find_element(By.XPATH, './/h1[@class = "cy-alert__title font-weight-800 mt-2"]').text
    newArticle['content'] = textContainers[0].text + " " + textContainers[-1].text
    newArticle['date'] = parser.parse(browser.find_elements(By.XPATH, './/ul[@class = "cy-card__list list-inline cy-alert__info m-0"]/li/a')[1].text).strftime('%m/%d/%Y')
    newArticle['link'] = browser.current_url

    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    return newArticle 

if __name__ == "__main__":
    articleList,status_code = getCywareArticles()
    print(articleList['articles'])
