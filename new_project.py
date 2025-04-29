import flet as ft

def main(page: ft.Page):
    page.title = "내 프로젝트"
    project_list_view = ft.ListView(expand=True, spacing=10)
    name_input = ft.TextField(label="프로젝트 이름", width=300)
    desc_input = ft.TextField(label="설명", width=300, multiline=True)

    # 역할 선택 드롭다운
    role_dropdown = ft.Dropdown(
        label="역할 선택",
        width=300,
        options=[
            ft.dropdown.Option("리더"),
            ft.dropdown.Option("멤버"),
        ],
        value="멤버"  # 기본값 설정
    )

    # 프로젝트를 담을 리스트
    projects = []

    def render_projects():
        project_list_view.controls.clear()
        for project in projects:
            title = ft.Text(project["name"], size=16, weight="bold")
            desc = ft.Text(project["description"], color=ft.colors.GREY_700)
            role = project["role"]

            project_list_view.controls.append(
                ft.Container(
                    content=ft.Column([
                        title,
                        desc,
                        ft.Text(f"역할: {role}", italic=True, size=12)
                    ]),
                    bgcolor=ft.colors.WHITE,
                    padding=10,
                    border_radius=10,
                    shadow=ft.BoxShadow(blur_radius=4, color=ft.colors.GREY_300)
                )
            )
        page.update()

    def on_create_click(e):
        name = name_input.value.strip()
        desc = desc_input.value.strip()
        role = role_dropdown.value

        if not name:
            page.snack_bar = ft.SnackBar(ft.Text("프로젝트 이름을 입력해주세요"))
            page.snack_bar.open = True
            page.update()
            return

        if not role:
            page.snack_bar = ft.SnackBar(ft.Text("역할을 선택해주세요"))
            page.snack_bar.open = True
            page.update()
            return

        # 새 프로젝트 추가
        new_project = {
            "name": name,
            "description": desc,
            "role": role
        }
        projects.append(new_project)

        # 입력값 초기화
        name_input.value = ""
        desc_input.value = ""
        role_dropdown.value = "멤버"  # 기본값으로 리셋

        # 목록 갱신
        render_projects()

    page.add(
        ft.Column([
            ft.Text("내 프로젝트", size=30, weight="bold"),
            name_input,
            desc_input,
            role_dropdown,
            ft.ElevatedButton("새 프로젝트 만들기", on_click=on_create_click),
            ft.Divider(),
            ft.Text("전체 프로젝트 목록", size=18, weight="w600"),
            project_list_view
        ])
    )

ft.app(target=main)
