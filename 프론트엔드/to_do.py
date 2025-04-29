import flet as ft

def main(page: ft.Page):
    page.title = "공유형 To-Do 리스트"
    page.window_width = 500
    page.window_height = 600

    todo_list = ft.Column()

    todo_input = ft.TextField(
        label="할 일을 입력하세요",
        expand=True,
        on_submit=lambda e: add_todo(e)
    )

    def add_todo(e):
        text = todo_input.value.strip()
        if text:
            todo_item = ft.Row(
                [
                    ft.Checkbox(label=text, value=False, on_change=toggle_done),
                    ft.IconButton(icon=ft.icons.DELETE, icon_color="red", on_click=remove_todo)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            todo_list.controls.append(todo_item)
            todo_input.value = ""
            page.update()

    def toggle_done(e):
        checkbox = e.control
        if checkbox.value:
            checkbox.label.style = ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH)
        else:
            checkbox.label.style = None
        page.update()

    def remove_todo(e):
        todo_list.controls.remove(e.control.parent)
        page.update()

    page.add(
        ft.Column(
            [
                ft.Text("📋 To-Do 리스트", size=28, weight="bold"),
                ft.Row([todo_input, ft.ElevatedButton("등록", on_click=add_todo)], spacing=10),
                ft.Divider(),
                ft.Container(todo_list, expand=True, padding=10, bgcolor="#f5f5f5", border_radius=10),
            ],
            spacing=20,
            expand=True
        )
    )

ft.app(target=main)
