import flet as ft

def main(page: ft.Page):
    page.title = "To-Do 리스트 진행률"
    page.window_width = 500
    page.window_height = 650

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
        control = e.control
        for item in todo_list:
            if item["row"] == control.parent:
                todo_list.remove(item)
                todo_column.controls.remove(control.parent)
                break
        update_progress()
        page.update()

    def add_todo(e):
        text = todo_input.value.strip()
        if text:
            checkbox = ft.Checkbox(label=text, value=False, on_change=toggle_done)
            delete_button = ft.IconButton(icon=ft.icons.DELETE, icon_color="red", on_click=remove_todo)
            row = ft.Row([checkbox, delete_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            todo_list.append({"checkbox": checkbox, "row": row})
            todo_column.controls.append(row)
            todo_input.value = ""
            update_progress()
            page.update()

    todo_input = ft.TextField(label="할 일을 입력하세요", expand=True, on_submit=add_todo)

    page.add(
        ft.Column(
            [
                ft.Text("📋 To-Do 리스트 진행률", size=28, weight="bold"),
                ft.Row([todo_input, ft.ElevatedButton("등록", on_click=add_todo)], spacing=10),
                progress_text,
                progress_bar,
                ft.Divider(),
                ft.Container(todo_column, expand=True, padding=10, bgcolor="#f9f9f9", border_radius=10),
            ],
            spacing=20,
            expand=True,
        )
    )

ft.app(target=main)
