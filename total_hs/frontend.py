import flet as ft
import requests
import json
from datetime import datetime

class TodoApp:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.token = None
        self.current_user = None

    def main(self, page: ft.Page):
        page.title = "팀 투두리스트"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20
        page.window_width = 800
        page.window_height = 600

        # 로그인 폼
        def login(e):
            try:
                response = requests.post(
                    f"{self.base_url}/token",
                    data={
                        "username": username.value,
                        "password": password.value,
                        "grant_type": "password"
                    },
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                )
                if response.status_code == 200:
                    self.token = response.json()["access_token"]
                    self.current_user = username.value
                    page.clean()
                    show_main_content()
                    page.update()
                else:
                    page.snack_bar = ft.SnackBar(content=ft.Text("로그인 실패"))
                    page.snack_bar.open = True
                    page.update()
            except Exception as e:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"오류 발생: {str(e)}"))
                page.snack_bar.open = True
                page.update()

        # 회원가입 폼
        def show_signup():
            page.clean()
            
            signup_username = ft.TextField(label="사용자명", width=300)
            signup_email = ft.TextField(label="이메일", width=300)
            signup_password = ft.TextField(label="비밀번호", password=True, width=300)
            
            def do_signup(e):
                try:
                    response = requests.post(
                        f"{self.base_url}/users/",
                        params={
                            "username": signup_username.value,
                            "email": signup_email.value,
                            "password": signup_password.value
                        }
                    )
                    if response.status_code == 200:
                        page.snack_bar = ft.SnackBar(content=ft.Text("회원가입 성공! 로그인해주세요."))
                        page.snack_bar.open = True
                        show_login()
                    else:
                        page.snack_bar = ft.SnackBar(content=ft.Text("회원가입 실패"))
                        page.snack_bar.open = True
                except Exception as e:
                    page.snack_bar = ft.SnackBar(content=ft.Text(f"오류 발생: {str(e)}"))
                    page.snack_bar.open = True
                page.update()

            def back_to_login(e):
                show_login()

            page.add(
                ft.Column([
                    ft.Text("회원가입", size=30, weight=ft.FontWeight.BOLD),
                    signup_username,
                    signup_email,
                    signup_password,
                    ft.Row([
                        ft.ElevatedButton("회원가입", on_click=do_signup),
                        ft.OutlinedButton("로그인으로 돌아가기", on_click=back_to_login)
                    ]),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )

        # 로그인 화면
        def show_login():
            page.clean()
            login_username = ft.TextField(label="사용자명", width=300)
            login_password = ft.TextField(label="비밀번호", password=True, width=300)
            
            def go_to_signup(e):
                show_signup()

            def handle_login(e):
                print("로그인 시도:", login_username.value, login_password.value)  # 디버깅용
                try:
                    response = requests.post(
                        f"{self.base_url}/token",
                        data={
                            "username": login_username.value,
                            "password": login_password.value,
                            "grant_type": "password"
                        },
                        headers={
                            "Content-Type": "application/x-www-form-urlencoded"
                        }
                    )
                    print("응답:", response.status_code, response.text)  # 디버깅용
                    if response.status_code == 200:
                        self.token = response.json()["access_token"]
                        self.current_user = login_username.value
                        page.clean()
                        show_main_content()
                        page.update()
                    else:
                        page.snack_bar = ft.SnackBar(content=ft.Text("로그인 실패"))
                        page.snack_bar.open = True
                        page.update()
                except Exception as e:
                    print("오류:", str(e))  # 디버깅용
                    page.snack_bar = ft.SnackBar(content=ft.Text(f"오류 발생: {str(e)}"))
                    page.snack_bar.open = True
                    page.update()

            login_button = ft.ElevatedButton("로그인", on_click=handle_login)
            signup_button = ft.OutlinedButton("회원가입", on_click=go_to_signup)

            page.add(
                ft.Column([
                    ft.Text("팀 투두리스트", size=30, weight=ft.FontWeight.BOLD),
                    login_username,
                    login_password,
                    ft.Row([
                        login_button,
                        signup_button
                    ]),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
            page.update()

        # 메인 콘텐츠
        def show_main_content():
            page.clean()  # 페이지 초기화
            
            # 네비게이션 바 스타일
            nav_style = {
                "height": 40,
                "bgcolor": ft.colors.BLUE_GREY_50,
                "style": ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=0),
                    padding=ft.padding.symmetric(horizontal=20, vertical=0),
                    color=ft.colors.BLACK
                )
            }
            
            # 네비게이션 바
            nav_bar = ft.Container(
                content=ft.Row([
                    ft.ElevatedButton(
                        "홈",
                        on_click=lambda e: show_home(),
                        **nav_style
                    ),
                    ft.ElevatedButton(
                        "프로젝트",
                        on_click=lambda e: show_projects(),
                        **nav_style
                    ),
                    ft.ElevatedButton(
                        "할 일",
                        on_click=lambda e: show_tasks(),
                        **nav_style
                    ),
                    ft.ElevatedButton(
                        "내 정보",
                        on_click=lambda e: show_profile(),
                        **nav_style
                    )
                ], alignment=ft.MainAxisAlignment.CENTER),
                bgcolor=ft.colors.BLUE_GREY_50,
                padding=ft.padding.symmetric(vertical=10)
            )
            
            # 홈 화면
            def show_home():
                page.clean()
                page.add(
                    ft.Column([
                        nav_bar,
                        ft.Container(
                            content=ft.Column([
                                ft.Text("환영합니다!", size=30, weight=ft.FontWeight.BOLD),
                                ft.Text(f"{self.current_user}님의 대시보드", size=20),
                                ft.Text("왼쪽 상단의 메뉴를 선택하여 이동하세요.", size=16)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=20
                        )
                    ])
                )
                page.update()

            # 프로젝트 화면
            def show_projects():
                page.clean()
                projects = ft.ListView(expand=1, spacing=10, padding=20)
                
                def load_projects():
                    try:
                        response = requests.get(
                            f"{self.base_url}/projects/",
                            headers={"Authorization": f"Bearer {self.token}"}
                        )
                        if response.status_code == 200:
                            projects.controls.clear()
                            for project in response.json():
                                project_card = ft.Card(
                                    content=ft.Container(
                                        content=ft.Column([
                                            ft.Text(project["name"], size=16, weight=ft.FontWeight.BOLD),
                                            ft.Text(project["description"]),
                                            ft.ProgressBar(value=project["progress"]/100),
                                            ft.Text(f"{project['progress']}%")
                                        ]),
                                        padding=10
                                    )
                                )
                                projects.controls.append(project_card)
                            page.update()
                    except Exception as e:
                        page.snack_bar = ft.SnackBar(content=ft.Text(f"오류 발생: {str(e)}"))
                        page.snack_bar.open = True
                        page.update()

                # 새 프로젝트 추가
                new_project_name = ft.TextField(label="프로젝트 이름", width=300)
                new_project_desc = ft.TextField(label="프로젝트 설명", width=300, multiline=True)
                
                def add_project(e):
                    try:
                        response = requests.post(
                            f"{self.base_url}/projects/",
                            params={
                                "name": new_project_name.value,
                                "description": new_project_desc.value,
                                "user_id": 1  # 현재 로그인한 사용자 ID
                            },
                            headers={"Authorization": f"Bearer {self.token}"}
                        )
                        if response.status_code == 200:
                            page.snack_bar = ft.SnackBar(content=ft.Text("프로젝트가 성공적으로 추가되었습니다."))
                            page.snack_bar.open = True
                            new_project_name.value = ""
                            new_project_desc.value = ""
                            load_projects()
                            page.update()
                        else:
                            page.snack_bar = ft.SnackBar(content=ft.Text("프로젝트 추가 실패"))
                            page.snack_bar.open = True
                            page.update()
                    except Exception as e:
                        page.snack_bar = ft.SnackBar(content=ft.Text(f"오류 발생: {str(e)}"))
                        page.snack_bar.open = True
                        page.update()

                page.add(
                    ft.Column([
                        nav_bar,
                        ft.Container(
                            content=ft.Column([
                                ft.Text("프로젝트 관리", size=30, weight=ft.FontWeight.BOLD),
                                ft.Container(
                                    content=ft.Column([
                                        new_project_name,
                                        new_project_desc,
                                        ft.ElevatedButton("프로젝트 추가", on_click=add_project)
                                    ]),
                                    padding=10
                                ),
                                projects
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=20
                        )
                    ])
                )
                load_projects()
                page.update()

            # 할 일 화면
            def show_tasks():
                page.clean()
                
                # 할 일 입력 폼
                new_task_title = ft.TextField(label="할 일 명", width=300)
                new_task_desc = ft.TextField(label="내용", width=300, multiline=True, min_lines=3)
                
                # 할 일 목록을 담을 컨테이너
                tasks_container = ft.Container(
                    content=ft.ListView(spacing=10, padding=10, height=400),
                    bgcolor=ft.colors.WHITE,
                    border=ft.border.all(1, ft.colors.BLUE_GREY_100),
                    border_radius=10,
                    padding=10,
                    expand=True
                )

                def load_tasks():
                    try:
                        response = requests.get(
                            f"{self.base_url}/tasks/",
                            params={"user_id": 1},  # 현재 로그인한 사용자 ID
                            headers={"Authorization": f"Bearer {self.token}"}
                        )
                        print("할 일 목록 응답:", response.status_code, response.text)  # 디버깅용
                        if response.status_code == 200:
                            tasks = response.json()
                            tasks_container.content.controls.clear()
                            for task in tasks:
                                task_item = ft.Container(
                                    content=ft.Row([
                                        ft.Checkbox(
                                            value=task["is_completed"],
                                            on_change=lambda e, task_id=task["id"]: complete_task(e, task_id)
                                        ),
                                        ft.Column([
                                            ft.Text(
                                                task["title"],
                                                size=16,
                                                weight=ft.FontWeight.BOLD,
                                                style=ft.TextStyle(
                                                    decoration=ft.TextDecoration.LINE_THROUGH if task["is_completed"] else None
                                                )
                                            ),
                                            ft.Text(
                                                task["description"],
                                                size=14,
                                                style=ft.TextStyle(
                                                    decoration=ft.TextDecoration.LINE_THROUGH if task["is_completed"] else None
                                                )
                                            )
                                        ], expand=True)
                                    ]),
                                    padding=10,
                                    bgcolor=ft.colors.BLUE_50,
                                    border=ft.border.all(1, ft.colors.BLUE_GREY_100),
                                    border_radius=5
                                )
                                tasks_container.content.controls.append(task_item)
                            page.update()
                    except Exception as e:
                        print("할 일 목록 로드 오류:", str(e))  # 디버깅용
                        page.snack_bar = ft.SnackBar(content=ft.Text(f"오류 발생: {str(e)}"))
                        page.snack_bar.open = True
                        page.update()

                def complete_task(e, task_id):
                    try:
                        response = requests.put(
                            f"{self.base_url}/tasks/{task_id}/complete",
                            headers={"Authorization": f"Bearer {self.token}"}
                        )
                        if response.status_code == 200:
                            load_tasks()
                        else:
                            page.snack_bar = ft.SnackBar(content=ft.Text("할 일 완료 처리 실패"))
                            page.snack_bar.open = True
                            page.update()
                    except Exception as e:
                        page.snack_bar = ft.SnackBar(content=ft.Text(f"오류 발생: {str(e)}"))
                        page.snack_bar.open = True
                        page.update()
                
                def add_task(e):
                    try:
                        print("할 일 추가 시도:", new_task_title.value, new_task_desc.value)  # 디버깅용
                        response = requests.post(
                            f"{self.base_url}/tasks/?title={new_task_title.value}&description={new_task_desc.value}&user_id=1",
                            headers={"Authorization": f"Bearer {self.token}"}
                        )
                        print("응답:", response.status_code, response.text)  # 디버깅용
                        if response.status_code == 200:
                            page.snack_bar = ft.SnackBar(content=ft.Text("할 일이 성공적으로 추가되었습니다."))
                            page.snack_bar.open = True
                            new_task_title.value = ""
                            new_task_desc.value = ""
                            load_tasks()
                            page.update()
                        else:
                            page.snack_bar = ft.SnackBar(content=ft.Text("할 일 추가 실패"))
                            page.snack_bar.open = True
                            page.update()
                    except Exception as e:
                        print("오류:", str(e))  # 디버깅용
                        page.snack_bar = ft.SnackBar(content=ft.Text(f"오류 발생: {str(e)}"))
                        page.snack_bar.open = True
                        page.update()
                
                page.add(
                    ft.Column([
                        nav_bar,
                        ft.Container(
                            content=ft.Column([
                                ft.Text("할 일 관리", size=30, weight=ft.FontWeight.BOLD),
                                ft.Container(
                                    content=ft.Column([
                                        new_task_title,
                                        new_task_desc,
                                        ft.ElevatedButton("할 일 추가", on_click=add_task)
                                    ]),
                                    padding=10
                                ),
                                ft.Divider(),
                                tasks_container
                            ]),
                            padding=20,
                            expand=True
                        )
                    ])
                )
                load_tasks()
                page.update()

            # 내 정보 화면
            def show_profile():
                page.clean()
                page.add(
                    ft.Column([
                        nav_bar,
                        ft.Container(
                            content=ft.Column([
                                ft.Text("내 정보", size=30, weight=ft.FontWeight.BOLD),
                                ft.Text(f"사용자명: {self.current_user}", size=20),
                                ft.ElevatedButton("로그아웃", on_click=lambda e: show_login())
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=20
                        )
                    ])
                )
                page.update()

            # 초기 화면은 홈으로 설정
            show_home()
            page.update()  # 페이지 업데이트 추가

        # 초기 로그인 화면 표시
        show_login()

app = TodoApp()
ft.app(target=app.main, view=ft.WEB_BROWSER) 