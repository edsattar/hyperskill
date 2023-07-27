import requests

from bs4 import BeautifulSoup

act = input()
url = input()

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

a_tags = soup.find_all('a')

for tag in a_tags:
    print(tag.text)
