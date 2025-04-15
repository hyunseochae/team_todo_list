import flet as ft

def main(page: ft.Page):
    page.title = "마이페이지"
    page.window_width = 500
    page.window_height = 600

    # 예시 유저 데이터
    user_info = {
        "nickname": "홍길동",
        "email": "gildong@example.com",
        "joined": "2024-03-15",
        "todo_total": 10,
        "todo_done": 7
    }

    progress = user_info["todo_done"] / user_info["todo_total"] if user_info["todo_total"] else 0

    # 유저 정보 카드
    user_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("👤 사용자 정보", size=20, weight="bold"),
                    ft.Text(f"닉네임: {user_info['nickname']}"),
                    ft.Text(f"이메일: {user_info['email']}"),
                    ft.Text(f"가입일: {user_info['joined']}"),
                    ft.Row([
                        ft.ElevatedButton("비밀번호 변경"),
                        ft.OutlinedButton("로그아웃")
                    ])
                ],
                spacing=10
            ),
            padding=20
        )
    )

    # 할 일 진행률
    progress_section = ft.Column(
        [
            ft.Text("📊 진행률", size=20, weight="bold"),
            ft.Text(f"{user_info['todo_done']} / {user_info['todo_total']} 완료"),
            ft.ProgressBar(value=progress, width=400),
            ft.Text(f"진행률: {int(progress * 100)}%", size=16),
        ],
        spacing=10
    )

    # 최근 할 일 활동 (예시 데이터)
    recent_todos = ["팀 회의 준비", "보고서 제출", "스터디 일정 공유"]
    recent_section = ft.Column(
        [ft.Text("📝 최근 활동", size=20, weight="bold")] +
        [ft.Text(f"- {todo}") for todo in recent_todos],
        spacing=5
    )

    page.add(
        ft.Column(
            [
                ft.Text("📂 마이페이지", size=30, weight="bold"),
                user_card,
                ft.Divider(),
                progress_section,
                ft.Divider(),
                recent_section
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO
        )
    )

ft.app(target=main)
