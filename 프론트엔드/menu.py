import flet as ft

def main(page: ft.Page):
    page.title = "공유형 To-Do 리스트"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 600
    page.window_height = 700

    # --------------------
    # ✅ 각 화면 함수 정의
    # --------------------
    def home_view():
        return ft.Column([
            ft.Text("🏠 홈 페이지", size=30, weight="bold"),
            ft.Text("환영합니다! 이곳은 홈입니다.")
        ])

    def project_view():
        return ft.Column([
            ft.Text("📁 프로젝트", size=30, weight="bold"),
            ft.Text("진행 중인 프로젝트 목록이 여기에 표시됩니다.")
        ])

    def todo_view():
        return ft.Column([
            ft.Text("📝 할 일", size=30, weight="bold"),
            ft.Text("할 일 목록 및 등록 화면입니다.")
        ])

    def mypage_view():
        return ft.Column([
            ft.Text("👤 내 정보", size=30, weight="bold"),
            ft.Text("마이페이지입니다. 개인 정보와 활동을 확인할 수 있어요.")
        ])

    # --------------------
    # ✅ 화면 전환 함수
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
                return ft.Text("404 - 페이지를 찾을 수 없습니다.")

        # 메뉴 바를 유지하면서 내용만 바뀜
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
    # ✅ 메뉴 바 (상단 고정)
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
    # ✅ 초기 설정
    # --------------------
    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
