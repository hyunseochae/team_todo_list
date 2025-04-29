# views/home.py
import flet as ft

def home_view(page: ft.Page):
    return ft.Column([
        ft.Text("🏠 홈 페이지", size=30, weight="bold"),
        ft.Text("여기는 홈입니다. 메뉴를 눌러 이동해보세요.")
    ])
