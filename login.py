import flet as ft


def main(page: ft.Page):
    page.title = "공유형 To-Do 리스트 - 로그인 / 회원가입"
    page.window_width = 400
    page.window_height = 500

    # 공통 상태
    username = ft.TextField(label="아이디", autofocus=True)
    password = ft.TextField(label="비밀번호", password=True, can_reveal_password=True)
    confirm_password = ft.TextField(label="비밀번호 확인", password=True, can_reveal_password=True, visible=False)
    message = ft.Text()

    is_signup = False

    def toggle_mode(e):
        nonlocal is_signup
        is_signup = not is_signup
        if is_signup:
            submit_btn.text = "회원가입"
            switch_btn.text = "이미 계정이 있나요? 로그인"
            confirm_password.visible = True
        else:
            submit_btn.text = "로그인"
            switch_btn.text = "계정이 없나요? 회원가입"
            confirm_password.visible = False
        page.update()

    def submit(e):
        if is_signup:
            if not username.value or not password.value or not confirm_password.value:
                message.value = "모든 항목을 입력하세요."
            elif password.value != confirm_password.value:
                message.value = "비밀번호가 일치하지 않습니다."
            else:
                # 여기에 회원가입 처리 로직
                message.value = f"'{username.value}' 님 회원가입 완료!"
        else:
            if not username.value or not password.value:
                message.value = "아이디와 비밀번호를 입력하세요."
            else:
                # 여기에 로그인 처리 로직
                message.value = f"'{username.value}' 님 로그인 시도 중..."
        page.update()

    submit_btn = ft.ElevatedButton(text="로그인", on_click=submit)
    switch_btn = ft.TextButton(text="계정이 없나요? 회원가입", on_click=toggle_mode)

    form = ft.Column(
        [
            ft.Text("To-Do List", size=30, weight="bold"),
            username,
            password,
            confirm_password,
            submit_btn,
            switch_btn,
            message
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    page.add(ft.Container(form, alignment=ft.alignment.center, padding=30))


ft.app(target=main)
