import flet as ft
from database import Database
from pprint import pprint


def main(page: ft.Page):
    # установка заголовка
    page.title = "Приложение для управления списком дел"
    page.window.width = 1024
    page.data = 0

    # создание объекта Database для работы с БД
    database = Database("database.sqlite")
    # создание таблиц
    database.create_tables()
    pprint(database.all_todos())

    title = ft.Text(
        value="Список дел на день", size=30, weight=ft.FontWeight.BOLD, italic=True
    )

    # функция, которая будет возвращать список Row с задачами из БД
    def build_rows():
        rows = []
        # проход по всем записям из таблицы todos
        for t in database.all_todos():
            print(t)
            # каждую запись отображаем в виде строки Row
            rows.append(
                ft.Row(
                    controls=[
                        ft.Text(value=str(t[0]), size=20),
                        ft.Text(value=t[1], size=20, color=ft.Colors.PINK),  # текст
                        ft.Text(value=t[2], size=20),  # категория
                        # кнопка для редактирования задачи
                        ft.IconButton(
                            icon=ft.Icons.EDIT_OUTLINED,
                            icon_color=ft.Colors.BLUE,
                            icon_size=20,
                        ),
                        # кнопка для удаления задачи
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINED,
                            icon_color=ft.Colors.RED,
                            icon_size=20,
                            on_click=before_delete,
                            data=t[0],
                        ),
                    ]
                )
            )
        return rows

    # функция, которая будет вызываться при нажатии кнопки "Добавить"
    def add_todo(e):
        print(todo_input.value)
        # добавляем задачу в БД через вызов метода add_todo
        database.add_todo(todo_input.value, category_input.value)

        todo_list_area.controls = build_rows()  # обновляем отображаемый список
        todo_input.value = ""  # очищаем поле ввода
        category_input.value = ""
        todo_input.focus()
        page.update()  # обновляем страницу, обязательно а то не будет работать

    def before_delete(e):
        print("Todo ID на который нажали", e.control.data)
        page.data = e.control.data
        page.open(delete_modal)

    def handle_close_delete(e):
        page.close(delete_modal)

    def delete_todo(e):
        database.delete_todo(todo_id=page.data)
        page.close(delete_modal)
        #
        todo_list_area.controls = build_rows()
        page.update()

    # создание текстового поля
    todo_input = ft.TextField(
        label="Введите что-нибудь",  # текст подсказки
    )
    category_input = ft.TextField(
        label="Введите категорию",  # текст подсказки
    )

    # создание кнопки для добавления задачи
    add_button = ft.ElevatedButton(
        "Добавить",  # текст на кнопке
        on_click=add_todo,  # функция, которая будет вызываться при нажатии
        color=ft.Colors.PINK,  # цвет текста на кнопке
        bgcolor=ft.Colors.AMBER,  # цвет фона кнопки
    )

    form_area = ft.Row(controls=[todo_input, category_input, add_button])

    delete_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Подтвердите удаление"),
        content=ft.Text("Вы действительно хотите удалить задачу?"),
        actions=[
            ft.ElevatedButton(
                "Удалить",
                on_click=delete_todo,
                bgcolor=ft.Colors.RED,
                color=ft.Colors.WHITE,
            ),
            ft.ElevatedButton("Отменить", on_click=handle_close_delete),
        ],
        # actions_alignment=ft.MainAxisAlignment.END,
    )

    # создание колонки
    todo_list_area = ft.Column(
        expand=True,
        scroll="always",
        controls=build_rows(),  # список элементов, которые будут в колонке
    )  # место, где будет отображаться список

    # добавление элементов на страницу(окно)
    page.add(
        title, form_area, todo_list_area
    )  # от того, в каком порядке они тут добавляются, зависит в каком порядке они отображаются


ft.app(main)
