import os
from datetime import datetime
from collections import Counter
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


def fetch_all_pages():
    """노션은 한 번에 최대 100개까지만 주기 때문에,
    다음 페이지가 있으면 계속 이어서 받아온다."""
    all_pages = []
    payload = {}
    while True:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        all_pages.extend(data["results"])

        if data.get("has_more"):
            payload["start_cursor"] = data["next_cursor"]
        else:
            break
    return all_pages


def extract_date(page):
    """'수업일' 속성(진짜 Date 타입)에서 날짜 값을 꺼내 변환.
    값이 비어있으면 None 반환."""
    date_prop = page["properties"]["수업일"]["date"]
    if not date_prop:
        return None
    # date_prop["start"]는 이미 'YYYY-MM-DD' 형식의 문자열
    return datetime.strptime(date_prop["start"], "%Y-%m-%d").date()


if __name__ == "__main__":
    pages = fetch_all_pages()
    print(f"총 {len(pages)}개 행 가져옴")

    dates = [extract_date(p) for p in pages]
    dates = [d for d in dates if d is not None]  # 파싱 실패한 것 제거

    counts = Counter(dates)

    for date, count in sorted(counts.items()):
        print(date, "->", count, "개")