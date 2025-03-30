import requests
import json

def F_to_C(f:float)->float:
    return (f-32) / (5/9)

def get_mars_weather():
    url = "https://api.nasa.gov/insight_weather/?api_key=Q1OWchfuFGEh9l08Ax5kSSrwjWoD9yfuTbip0Bpr&feedtype=json&ver=1.0"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()

weather = get_mars_weather()

sol_keys = weather["sol_keys"]
for sol in sol_keys:
    current_sol = weather[sol]
    temps = {}
    temps["avg"] = current_sol["AT"]["av"]
    temps["min"] = current_sol["AT"]["mn"]
    temps["max"] = current_sol["AT"]["mx"]
    print("Sol: " + sol)
    print("Average temp:", round(F_to_C(temps["avg"]), 2), "°C")
    print("Min temp:", round(F_to_C(temps["min"]), 2), "°C")
    print("Max temp:", round(F_to_C(temps["max"]), 2), "°C")
    print("Date: ", current_sol["Last_UTC"])
    print()
    
