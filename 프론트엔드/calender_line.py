import flet as ft
import calendar
from datetime import datetime, timedelta

def create_calendar_with_tasks(year, month, tasks):
    cal = calendar.Calendar()
    month_days = list(cal.itermonthdays(year, month))
    weeks = [month_days[i:i + 7] for i in range(0, len(month_days), 7)]

    rows = []
    rows.append(
        ft.Row([ft.Text(day, width=50, weight="bold") for day in ['일', '월', '화', '수', '목', '금', '토']])
    )

    for week in weeks:
        date_row = []
        bar_row = []

        for i, day in enumerate(week):
            if day == 0:
                date_row.append(ft.Container(width=50, height=24))
            else:
                color = "red" if i == 0 else None  # 일요일은 빨강
                date_row.append(ft.Container(content=ft.Text(str(day), color=color), width=50, height=24))

        rows.append(ft.Row(date_row))

        # 막대(bar)는 task마다 생성
        task_bars = []
        for task in tasks:
            start = datetime.strptime(task['start'], "%Y-%m-%d")
            end = datetime.strptime(task['end'], "%Y-%m-%d")

            # 현재 week의 날짜 리스트에서 start와 end 위치 계산
            positions = []
            for i, day in enumerate(week):
                if day == 0:
                    continue
                current_date = datetime(year, month, day)
                if start <= current_date <= end:
                    positions.append(i)

            if positions:
                left_padding = positions[0]
                span = len(positions)

                bar_row = []
                i = 0
                while i < 7:
                    if i in positions:
                        if i == positions[0]:  # 바의 시작점
                            span = positions[-1] - positions[0] + 1
                            bar_row.append(
                                ft.Container(
                                    bgcolor=task['color'],
                                    width=50 * span,
                                    height=6,
                                    border_radius=3
                                )
                            )
                            i += span  # span만큼 건너뛰기
                        else:
                            i += 1  # 이미 처리했거나 중간 부분은 건너뜀
                    else:
                        bar_row.append(ft.Container(width=50, height=6))
                        i += 1

                rows.append(ft.Row(bar_row))

    return ft.Column(rows)

def main(page: ft.Page):
    page.title = "업무 달력 바 시각화"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # 샘플 작업 데이터
    tasks = [
        {"title": "보고서 작성", "start": "2025-04-10", "end": "2025-04-15", "color": "#42a5f5"},
        {"title": "디자인 검토", "start": "2025-04-14", "end": "2025-04-21", "color": "#66bb6a"},
    ]

    calendar_ui = create_calendar_with_tasks(2025, 4, tasks)
    page.add(calendar_ui)

ft.app(target=main)
