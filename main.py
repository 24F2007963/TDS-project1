import requests

url = "http://127.0.0.1:8000/ask"
data = {
    "question": " I know Docker but have not used Podman before. Should I use Docker for this course?"
}
response = requests.post(url, json=data)

print("Response:", response.json())
