import requests

url = input("Input the URL:")

r = requests.get(url)

if r:
    try:
        print(r.json()['content'])
    except KeyError:
        print("Invalid quote resource!")
else:
    print("Invalid quote resource!")
