import os
from dotenv import load_dotenv
load_dotenv()
PROXY = os.getenv('PROXY')
proxies = {
                "http": PROXY,
                "https": PROXY
    }
import requests
import pandas as pd 
import string
from bs4 import BeautifulSoup
import re

def get_soup(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    r = requests.get(url, headers=headers, proxies=proxies)
    return BeautifulSoup(r.text, 'html.parser')

def prepare_keywords():
    return list(string.ascii_lowercase)

def scrape_duckduckgo(keyword):
    url = "https://duckduckgo.com/html/?q=" + keyword
    results = []
    try:
        soup = get_soup(url)
        links = soup.find_all("a",class_="result__snippet")

        for l in links:
            details = {"url": l["href"], "snippet": l.text}
            # extract email using regex from string snippet
            emails = re.findall(r'[\w\.-]+@[\w\.-]+', details["snippet"])
            details["email"] = emails[0].rstrip(".") if len(emails) > 0 else ""
            results.append(details)
    except:
        pass
    return results

def scrape_more_duckduckgo(keyword):
    helper_keywords = prepare_keywords()
    keywordlist = [keyword+" "+k for k in helper_keywords]
    # print(keywordlist)
    results = []
    for k in keywordlist[:4]:
        print(keywordlist.index(k),"/",len(keywordlist))
        try:
            results += scrape_duckduckgo(k)
        except:
            pass
    return results

if __name__ == "__main__":
    query = "site:instagram.com @gmail.com writer"
    data = scrape_more_duckduckgo(query)
    df = pd.DataFrame(data)
    df = df.drop_duplicates(subset=["url"])
    df.to_csv("insta_writers.csv",index=False)