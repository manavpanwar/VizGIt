from crawler import Crawler


url = "https://www.moneycontrol.com/india/stockpricequote/online-services/zomato/Z"
start_anchor = "/"
urls = crawler(url, start_anchor)
print(len(urls), urls)