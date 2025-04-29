import flet as ft
import calendar
from datetime import datetime

def create_calendar_with_tasks(year, month, tasks):
    cal = calendar.Calendar()
    month_days = list(cal.itermonthdays(year, month))
    weeks = [month_days[i:i + 7] for i in range(0, len(month_days), 7)]

    rows = []
    rows.append(
        ft.Row([
            ft.Container(ft.Text(day, weight="bold"), width=50, alignment=ft.alignment.center)
            for day in ['일', '월', '화', '수', '목', '금', '토']
        ])
    )

    # 날짜와 업무를 출력
    for week in weeks:
        date_row = []
        bar_rows = []

        for i, day in enumerate(week):
            if day == 0:
                date_row.append(ft.Container(width=50, height=24))
            else:
                color = "red" if i == 0 else None
                date_row.append(
                    ft.Container(
                        ft.Text(str(day), color=color),
                        width=50,
                        height=24,
                        alignment=ft.alignment.center
                    )
                )
        rows.append(ft.Row(date_row))

        # 각 task에 대해 작업이 시작되고 끝나는 날짜를 처리
        for task in tasks:
            start = datetime.strptime(task["start"], "%Y-%m-%d")
            end = datetime.strptime(task["end"], "%Y-%m-%d")

            # 해당 주의 날짜들에 대해 업무 막대 생성
            bar_row = []
            for i, day in enumerate(week):
                if day == 0:
                    bar_row.append(ft.Container(width=50, height=6))
                    continue

                current = datetime(year, month, day)

                # 작업이 이 날짜 범위에 포함되면
                if start <= current <= end:
                    # 막대가 생성될 위치 계산
                    bar_row.append(
                        ft.Container(
                            bgcolor=task['color'],
                            width=50,
                            height=6,
                            border_radius=3
                        )
                    )
                else:
                    bar_row.append(ft.Container(width=50, height=6))  # 해당 날짜는 빈 공간

            # 작업 바가 이어지게 처리
            rows.append(ft.Row(bar_row))

    return ft.Column(rows, spacing=2)

def main(page: ft.Page):
    page.title = "업무 달력 바 시각화"
    page.vertical_alignment = ft.MainAxisAlignment.START

    tasks = [
        {"title": "보고서 작성", "start": "2025-04-10", "end": "2025-04-15", "color": "#42a5f5"},
        {"title": "디자인 검토", "start": "2025-04-14", "end": "2025-04-21", "color": "#66bb6a"},
    ]

    calendar_ui = create_calendar_with_tasks(2025, 4, tasks)
    page.add(calendar_ui)

ft.app(target=main)
