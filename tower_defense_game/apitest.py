import requests

url = "https://vincebence-500c0-default-rtdb.europe-west1.firebasedatabase.app/highscores.json"

response = requests.get(url)

print(type(response.json()))