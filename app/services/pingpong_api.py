import requests
from app.config import pingpong

def ping_pong_reply(query: str):
    url = pingpong.PINGPONG_HOST + "10"
    data = {"request": {"query": f"{query}"}}
    header = {"Authorization": f"{pingpong.PINGPONG_API_KEY}"}
    res = requests.post(url=url ,headers=header, json=data).json()
    return res['response']['replies'][0]['text']

if __name__ == "__main__":
    print(ping_pong_reply("너 이름이 뭐야?"))