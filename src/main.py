import flet as ft


def main(page: ft.Page):
    # установка заголовка
    page.title = "Привет мир"

    # функция, которая будет вызываться при изменении значения текстового поля
    def change_name(e):
        print(name_input.value)

    # функция, которая будет вызываться при нажатии кнопки
    def click_button(e):
        print(name_input.value)

    # создание текстового поля
    name_input = ft.TextField(
        label="введите ваше имя",  # текст подсказки
        on_change=change_name,  # функция, которая будет вызываться при изменении значения
    )

    # создание кнопки
    button = ft.ElevatedButton(
        "сохранить",  # текст на кнопке
        on_click=click_button,  # функция, которая будет вызываться при нажатии
        color=ft.Colors.PINK,  # цвет текста на кнопке
        bgcolor=ft.Colors.AMBER,  # цвет фона кнопки
    )

    # добавление элементов на страницу(окно)
    page.add(name_input, button)


ft.app(main)
