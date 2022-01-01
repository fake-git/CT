
import requests
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession
import collections
import time


proxies = {
 'https': 'http:////129.213.120.175:3128'
}



url = 'https://www.ynet.co.il/home/0,7340,L-184,00.html'
request = requests.get(url, proxies=proxies)
soup = BeautifulSoup(request.text, 'html.parser')
urls = [f'https://www.ynet.co.il{item.get("href")}' for item in soup.select('a.smallheader')] # a.smallheader = (tag.class)



word_counter = collections.Counter()

def parse_ynet_article_(resp, *args, **kwargs):
    page = BeautifulSoup(resp.text, 'html.parser')
    text = page.select('.art_body span')[0].text
    word_counter.update(text.split())  # probably take ' ' (space) by default


session = FuturesSession()
# we pass the function reference, and that's mean: on every response that we get, we will activate
# the function "parse_ynet_article" on the respond
session.hooks['response'] = parse_ynet_article_

print(session.hooks)
# sending all the requests with thread-pool
q = [session.get(url) for url in urls]



results = [f.result() for f in q]


print(q)
print(results)


print(len(results))
print(word_counter)
print(sorted(word_counter))
print(type(word_counter))
for key, value in word_counter.items():
    print(f' {key}  -->  {value}')



# This is DEV branch
