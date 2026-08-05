from datetime import date, timedelta
from count_by_date import fetch_all_pages, extract_date

# 빈칸 + 상태 3단계. 배경(#ebedf0)이랑 헷갈리던 가장 연한 색은 빼고
# 세 가지 진하기로만 씀 → 눈으로 구분이 훨씬 잘 됨
STATUS_COLOR = {
    None: "#ebedf0",       # 그날 항목 없음
    "시작 전": "#c4bee2",
    "진행 중": "#9986b3",
    "완료": "#6c5a72",
}


def extract_status(page):
    """'상태' 속성(status 타입)에서 이름만 꺼냄. 비어있으면 None."""
    status_prop = page["properties"]["상태"]["status"]
    if not status_prop:
        return None
    return status_prop["name"]


def build_svg(status_by_date, start_date, end_date=None):
    if end_date is None:
        end_date = date.today()

    # 시작일을 그 주의 일요일로 앞당김 (weekday(): 월=0 ... 일=6)
    aligned_start = start_date - timedelta(days=(start_date.weekday() + 1) % 7)

    # 정렬 때문에 당겨진 만큼을 포함해서 실제로 그릴 총 일수를 계산.
    # 끝은 무조건 end_date까지 채워야 하니, 여기서 주 수를 역산함.
    total_days = (end_date - aligned_start).days + 1
    weeks = -(-total_days // 7)  # 올림 나눗셈 (7로 나눠떨어지지 않으면 한 주 더)

    cell = 12   # 칸 크기(px)
    gap = 3     # 칸 사이 간격(px)
    width = weeks * (cell + gap)
    height = 7 * (cell + gap)

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']

    current = aligned_start
    for week in range(weeks):
        for weekday in range(7):  # 0=일요일 ... 6=토요일
            if start_date <= current <= end_date:
                status = status_by_date.get(current)
                color = STATUS_COLOR[status]
                label = status if status else "기록 없음"
                x = week * (cell + gap)
                y = weekday * (cell + gap)
                svg.append(
                    f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
                    f'rx="3" fill="{color}"><title>{current} · {label}</title></rect>'
                )
            current += timedelta(days=1)

    svg.append("</svg>")
    return "\n".join(svg)


if __name__ == "__main__":
    START_DATE = date(2026, 6, 1)  # 강의 시작일

    pages = fetch_all_pages()

    status_by_date = {}
    for p in pages:
        d = extract_date(p)
        if d is not None:
            status_by_date[d] = extract_status(p)

    svg_code = build_svg(status_by_date, start_date=START_DATE)

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>study heatmap</title>
<style>
  html, body {{
    margin: 0;
    padding: 0;
    background: transparent;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    font-family: -apple-system, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
  }}
  .card {{
    background: transparent;
    border: 1.5px solid #c4bee2;
    border-radius: 16px;
    padding: 20px 24px;
  }}
</style>
</head>
<body>
<div class="card">
{svg_code}
</div>
</body>
</html>"""

    with open("heatmap.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("heatmap.html 생성 완료! 브라우저로 열어서 확인해보세요.")