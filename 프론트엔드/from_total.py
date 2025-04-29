# main.py
import flet as ft
from views.login import login_view
from views.menu import menu_bar
from views.mypage import mypage_view
from views.running import running_view


def main(page: ft.Page):
    page.title = "공유형 To-Do 리스트"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 600
    page.window_height = 700

    # --------------------
    # ✅ 홈 화면
    # --------------------
    def home_view():
        return ft.Column([
            ft.Text("🏠 홈 페이지", size=30, weight="bold"),
            ft.ElevatedButton("로그인", on_click=lambda e: page.go("/login")),
            ft.ElevatedButton("상단 메뉴", on_click=lambda e: page.go("/menu")),
            ft.ElevatedButton("내 정보", on_click=lambda e: page.go("/mypage")),
            ft.ElevatedButton("할 일 진행률", on_click=lambda e: page.go("/running")),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # --------------------
    # ✅ 라우팅 처리
    # --------------------
    def route_change(e):
        page.views.clear()

        def get_view(route):
            if route == "/":
                return home_view()
            elif route == "/login":
                return login_view()
            elif route == "/menu":
                return menu_bar(page)
            elif route == "/mypage":
                return mypage_view()
            elif route == "/running":
                return running_view(page)
            else:
                return ft.Column([
                    ft.Text("404 - 페이지를 찾을 수 없습니다.")
                ])

        page.views.append(
            ft.View(
                route=page.route,
                controls=[
                    get_view(page.route)
                ]
            )
        )
        page.update()

    # --------------------
    # ✅ 앱 시작
    # --------------------
    page.on_route_change = route_change
    page.go("/")  # 홈에서 시작

ft.app(target=main)
