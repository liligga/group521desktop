import flet as ft


def main(page: ft.Page):
    # установка заголовка
    page.title = "Приложение для управления списком дел"

    title = ft.Text(
        value="Список дел на день", size=30, weight=ft.FontWeight.BOLD, italic=True
    )

    # функция, которая будет вызываться при нажатии кнопки
    def click_button(e):
        print(todo_input.value)

        todo_list_area.controls.append(
            ft.Row(
                controls=[
                    ft.Text(value=todo_input.value, size=20, color=ft.Colors.PINK),
                    ft.Text(value=category_input.value, size=20),
                    ft.IconButton(
                        icon=ft.Icons.EDIT_OUTLINED,
                        icon_color=ft.Colors.BLUE,
                        icon_size=20,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINED,
                        icon_color=ft.Colors.RED,
                        icon_size=20,
                    ),
                ]
            )
        )  # добавляем новый текстовый элемент с новым делом в колонку
        todo_input.value = ""  # очищаем поле ввода
        category_input.value = ""
        todo_input.focus()
        page.update()  # обновляем страницу, обязательно а то не будет работать

    # создание текстового поля
    todo_input = ft.TextField(
        label="Введите что-нибудь",  # текст подсказки
    )
    category_input = ft.TextField(
        label="Введите категорию",  # текст подсказки
    )

    # создание кнопки
    add_button = ft.ElevatedButton(
        "Добавить",  # текст на кнопке
        on_click=click_button,  # функция, которая будет вызываться при нажатии
        color=ft.Colors.PINK,  # цвет текста на кнопке
        bgcolor=ft.Colors.AMBER,  # цвет фона кнопки
    )

    form_area = ft.Row(controls=[todo_input, category_input, add_button])

    # создание колонки
    todo_list_area = ft.Column(
        expand=True, scroll="always"
    )  # место, где будет отображаться список

    # добавление элементов на страницу(окно)
    page.add(
        title, form_area, todo_list_area
    )  # от того, в каком порядке они тут добавляются, зависит в каком порядке они отображаются


ft.app(main)
