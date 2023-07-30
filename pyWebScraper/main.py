import requests
from bs4 import BeautifulSoup

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
            # print(f'{{"title": "{title}", "description": "{desc}"}}')
            # print(str({"title": title, "description": desc}).replace("'", '"'))
            print({"title": title, "description": desc})
        else:
            print('Invalid page!')
    else:
        print("Invalid page!")

def stage3():
    # url = input()
    url = "http://google.com/asdfg"
    r = requests.get(url)
    if r:
        page_content = r.content
        with open("source.html", "wb") as f:
            f.write(page_content)
        print("Content saved.")
    else:
        print(f"The URL returned {r.status_code}!")

if __name__ == "__main__":
    stage3()