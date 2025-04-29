import flet as ft

def main(page: ft.Page):
    page.title = "공유형 To-Do 리스트"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 600
    page.window_height = 700

    # 전역 할 일 리스트 (진행률 공유용)
    todo_list = []

    # --------------------
    # ✅ 홈 화면
    # --------------------
    def home_view():
        return ft.Column([
            ft.Text("🏠 홈 페이지", size=30, weight="bold"),
            ft.Text("이곳은 홈입니다. 메뉴를 눌러 이동해보세요."),
        ])

    # --------------------
    # ✅ 프로젝트 화면 (예시용)
    # --------------------
    def project_view():
        return ft.Column([
            ft.Text("📁 프로젝트", size=30, weight="bold"),
            ft.Text("프로젝트 기능은 추후 구현 예정입니다."),
        ])

    # --------------------
    # ✅ 할 일 화면 (등록 + 진행률)
    # --------------------
    def todo_view():
        todo_column = ft.Column()
        progress_bar = ft.ProgressBar(width=400)
        progress_text = ft.Text("진행률: 0% (0/0)", size=16)

        def update_progress():
            total = len(todo_list)
            done = sum(1 for item in todo_list if item["checkbox"].value)
            progress = done / total if total else 0
            progress_bar.value = progress
            progress_text.value = f"진행률: {int(progress * 100)}% ({done}/{total})"
            page.update()

        def toggle_done(e):
            update_progress()

        def remove_todo(e):
            for item in todo_list:
                if item["row"] == e.control.parent:
                    todo_list.remove(item)
                    todo_column.controls.remove(item["row"])
                    break
            update_progress()
            page.update()

        def add_todo(e):
            task = todo_input.value.strip()
            if task:
                checkbox = ft.Checkbox(label=task, on_change=toggle_done)
                delete_btn = ft.IconButton(icon=ft.icons.DELETE, icon_color="red", on_click=remove_todo)
                row = ft.Row([checkbox, delete_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                todo_list.append({"checkbox": checkbox, "row": row})
                todo_column.controls.append(row)
                todo_input.value = ""
                update_progress()
                page.update()

        todo_input = ft.TextField(label="할 일을 입력하세요", expand=True, on_submit=add_todo)

        return ft.Column([
            ft.Text("📝 할 일", size=30, weight="bold"),
            ft.Row([todo_input, ft.ElevatedButton("등록", on_click=add_todo)], spacing=10),
            progress_text,
            progress_bar,
            ft.Divider(),
            todo_column,
        ])

    # --------------------
    # ✅ 내 정보 화면
    # --------------------
    def mypage_view():
        # 할 일 진행률 가져오기
        total = len(todo_list)
        done = sum(1 for item in todo_list if item["checkbox"].value)
        progress = done / total if total else 0

        return ft.Column([
            ft.Text("👤 내 정보", size=30, weight="bold"),
            ft.Text("닉네임: 사용자1"),
            ft.Text("가입일: 2025-01-01"),
            ft.Text("이메일: user@example.com"),
            ft.Divider(),
            ft.Text(f"총 할 일 수: {total}"),
            ft.Text(f"완료한 할 일 수: {done}"),
            ft.Text(f"진행률: {int(progress * 100)}%", size=20, weight="bold"),
            ft.ProgressBar(value=progress, width=400),
        ])

    # --------------------
    # ✅ 라우팅 처리
    # --------------------
    def route_change(e):
        page.views.clear()

        def get_view(route):
            if route == "/":
                return home_view()
            elif route == "/project":
                return project_view()
            elif route == "/todo":
                return todo_view()
            elif route == "/mypage":
                return mypage_view()
            else:
                return ft.Column([
                    ft.Text("404 - 페이지를 찾을 수 없습니다.")
                ])

        page.views.append(
            ft.View(
                route=page.route,
                controls=[
                    menu_bar,
                    ft.Divider(),
                    get_view(page.route)
                ]
            )
        )
        page.update()

    # --------------------
    # ✅ 상단 메뉴 바
    # --------------------
    menu_bar = ft.Row(
        [
            ft.TextButton("홈", on_click=lambda e: page.go("/")),
            ft.TextButton("프로젝트", on_click=lambda e: page.go("/project")),
            ft.TextButton("할 일", on_click=lambda e: page.go("/todo")),
            ft.TextButton("내 정보", on_click=lambda e: page.go("/mypage")),
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY
    )

    # --------------------
    # ✅ 앱 시작
    # --------------------
    page.on_route_change = route_change
    page.go("/")  # 홈에서 시작

ft.app(target=main)
