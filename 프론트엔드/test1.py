import flet as ft
import calendar
from datetime import datetime, timedelta

def create_calendar_with_tasks(year, month, tasks):
    cal = calendar.Calendar()
    month_days = list(cal.itermonthdays(year, month))

    # 날짜를 7일씩 자름 (주 단위)
    weeks = [month_days[i:i+7] for i in range(0, len(month_days), 7)]

    # 날짜별 배경 표시용 dict
    date_to_bar = {}

    # 작업 구간을 색깔로 저장
    for task in tasks:
        start_date = datetime.strptime(task['start'], "%Y-%m-%d")
        end_date = datetime.strptime(task['end'], "%Y-%m-%d")
        current = start_date
        while current <= end_date:
            if current.month == month and current.year == year:
                date_to_bar[current.day] = task['color']
            current += timedelta(days=1)

    # UI 생성
    rows = []
    rows.append(
        ft.Row([ft.Text(day, width=50, weight="bold") for day in ['일', '월', '화', '수', '목', '금', '토']])
    )

    for week in weeks:
        row = []
        for day in week:
            if day == 0:
                row.append(ft.Container(width=50, height=50))
            else:
                color = date_to_bar.get(day, None)
                cell = ft.Column([
                    ft.Text(str(day)),
                    ft.Container(
                        bgcolor=color if color else None,
                        height=6,
                        width=40,
                        border_radius=5
                    )
                ])
                row.append(ft.Container(content=cell, width=50, height=50))
        rows.append(ft.Row(row))

    return ft.Column(rows)

def main(page: ft.Page):
    page.title = "업무 달력 바 시각화"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # 샘플 작업 데이터
    tasks = [
        {"title": "보고서 작성", "start": "2025-04-10", "end": "2025-04-15", "color": "#42a5f5"},
        {"title": "디자인 검토", "start": "2025-04-18", "end": "2025-04-21", "color": "#66bb6a"},
    ]

    calendar_ui = create_calendar_with_tasks(2025, 4, tasks)
    page.add(calendar_ui)

ft.app(target=main)
