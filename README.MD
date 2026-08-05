# 노션 수업정리노트용 히트맵

노션 데이터베이스(수업일 + 상태)를 읽어와 깃허브 잔디밭 스타일의 
히트맵을 그려서 노션 페이지에 임베드하기 위한 스크립트.

_개인 사용 목적으로 제작함_
   
   
   
## 실행 방법

1. `.env`에 NOTION_TOKEN, NOTION_DATABASE_ID 설정
2. `py generate_heatmap.py` 실행 → heatmap.html 생성
3. 깃허브 push → GitHub Pages로 배포된 URL을 노션에 /embed