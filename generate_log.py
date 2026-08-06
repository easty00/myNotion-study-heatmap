from datetime import date
from count_by_date import fetch_all_pages, extract_date

# 상태별 점(dot) 색 — 히트맵이랑 같은 팔레트 계열
STATUS_DOT = {
    "시작 전": "#c4bee2",
    "진행 중": "#9986b3",
    "완료": "#6c5a72",
}


def extract_title(page):
    title_prop = page["properties"]["제목"]["title"]
    if not title_prop:
        return "(제목 없음)"
    return title_prop[0]["plain_text"]


def extract_status(page):
    status_prop = page["properties"]["상태"]["status"]
    if not status_prop:
        return None
    return status_prop["name"]


def kst_date(utc_str):
    """노션이 주는 UTC 시각 문자열을 한국 시간 기준 날짜로 변환."""
    from datetime import datetime, timedelta
    utc_dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
    return (utc_dt + timedelta(hours=9)).strftime("%Y-%m-%d")


def extract_created(page):
    """페이지가 실제로 만들어진 날 (노션 자동 기록)."""
    return kst_date(page["created_time"])


def extract_last_edited(page):
    """마지막으로 수정한 날 (노션 자동 기록)."""
    return kst_date(page["last_edited_time"])


def build_rows(entries):
    """entries: [(수업일, 제목, 상태, 발행일, 수정일), ...] 최신순 정렬"""
    rows = []
    for d, title, status, created, edited in entries:
        dot_color = STATUS_DOT.get(status, "#555")
        status_label = status or "미정"
        short = lambda s: s[5:].replace("-", ".")
        rows.append(f"""
        <div class="row">
          <div class="row-top">
            <span class="dot" style="background:{dot_color}"></span>
            <span class="date">{d.strftime('%m.%d')}</span>
            <span class="title">{title}</span>
          </div>
          <div class="row-bottom">
            <span class="status-badge" style="color:{dot_color}">{status_label}</span>
            <span class="dates">
              <span class="date-item">발행 {short(created)}</span>
              {f'<span class="date-item">수정 {short(edited)}</span>' if edited != created else ''}
            </span>
          </div>
        </div>""")
    return "\n".join(rows)


if __name__ == "__main__":
    pages = fetch_all_pages()

    entries = []
    for p in pages:
        d = extract_date(p)
        if d is None:
            continue
        entries.append((
            d,
            extract_title(p),
            extract_status(p),
            extract_created(p),
            extract_last_edited(p),
        ))

    entries.sort(key=lambda x: x[0], reverse=True)  # 최신 날짜가 위로

    rows_html = build_rows(entries)

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>study log</title>
<style>
  html, body {{
    margin: 0;
    padding: 0;
    background: transparent;
    display: flex;
    justify-content: center;
    font-family: -apple-system, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
  }}
  .card {{
    width: 100%;
    max-width: 760px;
    background: #ffffff;
    border: 1.5px solid #c4bee2;
    border-radius: 16px;
    padding: 18px 22px;
    box-sizing: border-box;
  }}
  .header {{
    display: flex;
    align-items: center;
    gap: 8px;
    color: #6c5a72;
    font-weight: 600;
    font-size: 15px;
    margin-bottom: 14px;
  }}
  .header .dot {{
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #9986b3;
  }}
  .row {{
    padding: 7px 0;
    border-bottom: 1px solid #ece8f2;
    font-size: 13px;
  }}
  .row:last-child {{
    border-bottom: none;
  }}
  .row-top {{
    display: flex;
    align-items: center;
    gap: 8px;
    min-width: 0;   /* 자식이 넘칠 때 title이 줄임표로 잘리도록 허용 */
  }}
  .row .dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }}
  .row .date {{
    color: #a39cae;
    font-family: "SFMono-Regular", Consolas, monospace;
    width: 38px;
    flex-shrink: 0;
  }}
  .row .title {{
    color: #3a3441;
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }}
  .row-bottom {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 6px;
    font-size: 11.5px;
    padding-left: 16px;
    margin-top: 2px;
  }}
  .status-badge {{
    font-weight: 600;
  }}
  .dates {{
    display: flex;
    gap: 8px;
    color: #b3abbf;
    font-family: "SFMono-Regular", Consolas, monospace;
  }}
  .log-list {{
    max-height: 252px;   /* 대략 7행 높이 */
    overflow-y: auto;
  }}
  .log-list::-webkit-scrollbar {{
    width: 6px;
  }}
  .log-list::-webkit-scrollbar-thumb {{
    background: #d9d1e8;
    border-radius: 3px;
  }}
</style>
</head>
<body>
<div class="card">
  <div class="header"><span class="dot"></span>학습 로그 정리 현황</div>
  <div class="log-list">
  {rows_html}
  </div>
</div>
</body>
</html>"""

    with open("log.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("log.html 생성 완료!")