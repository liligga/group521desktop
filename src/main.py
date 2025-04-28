import flet as ft
from database import Database
from pprint import pprint


def main(page: ft.Page):
    # установка заголовка
    page.title = "Приложение для управления списком дел"
    # Задаем ширину окна
    page.window.width = 1024

    # data - свойство объекта page, которое может хранить любые данные
    # которые будут использоваться в любом месте прилижения, работает как глобальная переменная
    page.data = 0  # храним ID задачи, которую собираемся удалить или редактировать

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
                            on_click=open_update_modal,
                            data=t[0],
                        ),
                        # кнопка для удаления задачи
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINED,
                            icon_color=ft.Colors.RED,
                            icon_size=20,
                            on_click=open_delete_modal,
                            data=t[0],
                            # data - свойство кнопки, в которое можем сохранить
                            # любые данные, в данном случае ID задачи для удаления
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

    # функция в которой открываем модальное окно для редактирования
    def open_update_modal(e):
        todo_id = e.control.data
        print(f"Нажали на todo с ID {todo_id}")
        page.data = todo_id
        todo = database.get_one_todo(todo_id)
        print(todo)
        todo_input.value = todo[1]
        category_input.value = todo[2]
        page.open(update_modal)

    # обработчик кнопки 'Отменить' при редактировании
    def close_update_modal(e):
        todo_input.value = ""
        category_input.value = ""
        page.close(update_modal)

    # обработчик кнопки 'Сохранить' в модальном окне при редактировании
    def update_todo(e):
        # берем ID задачи из глобального свойства data
        todo_id = page.data
        # обновляем задачу в БД
        database.update_todo(
            todo_id=todo_id,
            todo=todo_input.value,
            category=category_input.value,
        )
        # закрываем модальное окно
        page.close(update_modal)
        # очищаем поля ввода
        todo_input.value = ""
        category_input.value = ""

        # отображаем обновленный список задач в интерфейсе
        todo_list_area.controls = build_rows()
        page.update()

    # функция в которой открываем модальное окно для удаления
    def open_delete_modal(e):
        print("Todo ID на который нажали", e.control.data)
        # устанавливаем ID удаляемой задачи в качестве значения
        # глобального свойства data у объекта page
        page.data = e.control.data
        page.open(delete_modal)

    # обработчик кнопки 'Отменить' при удалении
    def close_delete_modal(e):
        page.close(delete_modal)  # закрываем модальное окно

    # обработчик кнопки 'Удалить' в модальном окне
    def delete_todo(e):
        # делаем запрос в БД на удаление
        database.delete_todo(todo_id=page.data)
        page.close(delete_modal)

        # отображаем обновленный список в интерфейсе
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

    # модальное окно, используется для подтверждения удаления
    delete_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Подтвердите удаление"),  # заголовок модального окна
        content=ft.Text("Вы действительно хотите удалить задачу?"),
        actions=[  # кнопки 'Удалить' и 'Отменить'
            ft.ElevatedButton(
                "Удалить",
                on_click=delete_todo,
                bgcolor=ft.Colors.RED,
                color=ft.Colors.WHITE,
            ),
            ft.ElevatedButton("Отменить", on_click=close_delete_modal),
        ],
        actions_alignment=ft.MainAxisAlignment.END,  # расположение кнопок, в данном случае справа
    )

    # модальное окно, используется для редактирования задачи
    update_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Хотите изменить задачу?"),
        # текстовые поля для редактирования задачи
        content=ft.Column(
            controls=[
                todo_input,
                category_input,
            ]
        ),
        actions=[  # кнопки 'Сохранить' и 'Отменить'
            ft.ElevatedButton(
                "Сохранить",
                on_click=update_todo,
                bgcolor=ft.Colors.BLUE,
                color=ft.Colors.WHITE,
            ),
            ft.ElevatedButton("Отменить", on_click=close_update_modal),
        ],
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
