import flet as ft

def main(page: ft.Page):
    page.title = "To-Do List 프로젝트"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 600
    page.window_height = 700

    # --------------------
    # ✅ 할 일 뷰 구성 함수
    # --------------------
    def todo_view():
        todo_list = []
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
    # ✅ 라우팅 함수
    # --------------------
    def route_change(e):
        page.views.clear()

        def get_view(route):
            if route == "/todo":
                return todo_view()
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
    # ✅ 초기 화면 설정
    # --------------------
    page.on_route_change = route_change
    page.go("/todo")  # 시작을 todo 페이지로 해볼게

ft.app(target=main)
