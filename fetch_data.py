import os
import requests
from dotenv import load_dotenv

# .env 파일에서 비밀 키들을 불러옴
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# 노션 API에 보낼 요청 주소와 인증 헤더
url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

response = requests.post(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(f"연결 성공! 행 개수: {len(data['results'])}개")
    # 첫 번째 행이 어떤 모양인지 확인
    print(data["results"][0]["properties"])
else:
    print("연결 실패:", response.status_code, response.text)