import requests
import time

def get_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)
    
    if response.status_code == 200:
        joke = response.json()
        return joke
    else:
        return None

while True:
    joke = get_joke()
    print(joke["setup"])
    input()
    print(joke["punchline"])
    input()