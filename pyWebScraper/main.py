import string
import requests
from bs4 import BeautifulSoup

def remove_punc(text: str):
    return text.translate(str.maketrans('','',string.punctuation))

def format_title(title: str):
    return remove_punc(title).strip().replace(" ", "_")

def stage1():
    url = input("Input the URL:")
    r = requests.get(url)
    if r:
        try:
            print(r.json()['content'])
        except KeyError:
            print("Invalid quote resource!")
    else:
        print("Invalid quote resource!")

def stage2():
    # url = input()
    url = "https://www.nature.com/articles/d41586-023-00103-3"
    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(r.content, 'html.parser')
    if r and "articles" in url:
        title = soup.find('title').text
        desc = soup.find('meta', {'name': 'description'})['content']
        if title and desc:
            print({"title": title, "description": desc})
        else:
            print('Invalid page!')
    else:
        print("Invalid page!")

def stage3():
    url = input()
    r = requests.get(url)
    if r:
        page_content = r.content
        with open("source.html", "wb") as f:
            f.write(page_content)
        print("Content saved.")
    else:
        print(f"The URL returned {r.status_code}!")

def stage4():
    page_url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3"
    r = requests.get(page_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(r.content, 'html.parser')
    if r:
        articles = soup.find_all('article')
        for e in articles:
            article_type = e.find("span", {"data-test": "article.type"}).text
            if article_type == "News":
                a_tag = e.find('a')
                title = format_title(a_tag.text)
                link = "https://www.nature.com/nature" + a_tag.get("href")
                r = requests.get(link, headers={'Accept-Language': 'en-US,en;q=0.5'})
                
                # page_content = BeautifulSoup(r.content, "html.parser")
                print(title)
                print(link)
                with open("source.html", "wb") as f:
                    f.write(r.content)
                # b = page_content.find_all('p')
                # for a in b:
                #     print(a.prettify())
                break
    else:
        print(f"The URL returned {r.status_code}!")

if __name__ == "__main__":
    stage4()
