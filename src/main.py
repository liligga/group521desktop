import flet as ft


def main(page: ft.Page):
    # установка заголовка
    page.title = "Привет мир"

    # функция, которая будет вызываться при изменении значения текстового поля
    def change_name(e):
        print(name_input.value)

    # создание текстового поля
    name_input = ft.TextField(
        label="введите ваше имя",  # текст подсказки
        on_change=change_name,  # функция, которая будет вызываться при изменении значения
    )

    # добавление текстового поля на страницу(окно)
    page.add(name_input)


ft.app(main)
