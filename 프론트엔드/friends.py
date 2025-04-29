import flet as ft

def main(page: ft.Page):
    page.title = "친구 추가 기능"
    page.window_width = 500
    page.window_height = 650

    friend_list = []  # 친구 목록

    def update_friend_list():
        friend_column.controls.clear()  # 기존 목록 초기화
        for friend in friend_list:
            # 친구 이름과 삭제 버튼 추가
            friend_column.controls.append(
                ft.Row([
                    ft.Text(friend, size=16),
                    ft.IconButton(icon=ft.icons.DELETE, icon_color="red", on_click=lambda e, friend=friend: remove_friend(friend)),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            )
        page.update()

    def remove_friend(friend):
        """친구 목록에서 친구 삭제"""
        if friend in friend_list:
            friend_list.remove(friend)
            update_friend_list()

    def add_friend(e):
        """새 친구 추가"""
        friend_name = friend_input.value.strip()
        if friend_name and friend_name not in friend_list:
            friend_list.append(friend_name)
            update_friend_list()
            friend_input.value = ""  # 입력 필드 초기화
            page.update()

    # 친구 목록을 표시할 컬럼
    friend_column = ft.Column()

    # 친구 이름 입력 필드
    friend_input = ft.TextField(label="친구의 이름을 입력하세요", expand=True, on_submit=add_friend)

    # 화면에 표시할 내용
    page.add(
        ft.Column(
            [
                ft.Text("👫 친구 추가", size=28, weight="bold"),
                ft.Row([friend_input, ft.ElevatedButton("친구 추가", on_click=add_friend)], spacing=10),
                ft.Divider(),
                ft.Container(friend_column, expand=True, padding=10, bgcolor="#f9f9f9", border_radius=10),
            ],
            spacing=20,
            expand=True,
        )
    )

ft.app(target=main)
