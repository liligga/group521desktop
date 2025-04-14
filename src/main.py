import flet as ft


def main(page: ft.Page):
    # установка заголовка
    page.title = "Приложение для управления списком дел"
    todo_list = []  # список дел

    title = ft.Text(
        value="Список дел на день", size=30, weight=ft.FontWeight.BOLD, italic=True
    )

    # функция, которая будет вызываться при изменении значения текстового поля
    def change_todo(e):
        # print(todo_input.value)
        pass

    # функция, которая будет вызываться при нажатии кнопки
    def click_button(e):
        print(todo_input.value)
        new_todo = f"{todo_input.value}, {category_input.value}"  # делаем строку для отображения, состоящий из двух полей
        new_text = ft.Text(
            value=new_todo, size=20, color=ft.Colors.PINK
        )  # создаем текстовый элемент
        todo_list_area.controls.append(
            new_text
        )  # добавляем новый текстовый элемент с новым делом в колонку

        page.update()  # обновляем страницу, обязательно а то не будет работать

    # создание текстового поля
    todo_input = ft.TextField(
        label="Введите что-нибудь",  # текст подсказки
        on_change=change_todo,  # функция, которая будет вызываться при изменении значения
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

    # создание колонки
    todo_list_area = ft.Column()  # место, где будет отображаться список

    # добавление элементов на страницу(окно)
    page.add(
        title, todo_input, category_input, add_button, todo_list_area
    )  # от того, в каком порядке они тут добавляются, зависит в каком порядке они отображаются


ft.app(main)
