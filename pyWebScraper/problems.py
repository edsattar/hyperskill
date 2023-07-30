import requests

from bs4 import BeautifulSoup

act = int(input())
url = input()
# act = 3
# url = "https://cogniterra.org/media/attachments/lesson/24996/4._Pygmalion.htm" 

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

a_tags = soup.find_all('a')

for tag in a_tags:
    # print(tag.text.endswith(str(2)))
    if tag.text.endswith(str(act - 1)):
        print(tag.get('href'))
