import requests

url = "https://test-tg31.onrender.com/transcribe"
file_path = "sample.mp3"

with open(file_path, "rb") as f:
    files = {"file": (file_path, f, "audio/mpeg")}
    response = requests.post(url, files=files)

if response.status_code == 200:
    data = response.json()
    print("文字起こし結果:", data["text"])
else:
    print("エラー:", response.status_code, response.text)