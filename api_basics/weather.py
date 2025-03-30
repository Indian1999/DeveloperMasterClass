import requests

def get_weather(city:str) -> dict:
    url = f"https://wttr.in/{city}?format=%t&lang=hu"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    else:
        print("Error: ", response.status_code)
        
weather = get_weather("budapest")
print("Budapest:", weather)
weather = get_weather("Melbourne")
print("Melbourne:", weather)