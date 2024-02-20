# класс для установки параметров проверки

import flet as ft
import contents.accents_training


class SettingsContent(ft.Column):
    # определение начальных значений, настройка элементов управления
    def __init__(self, window, page, training):
        self.window = window
        self.page = page
        self.training = training
        self.counter = ft.Slider(
            min=10, max=200, divisions=19, label='{value}', width=350, value=50
        )
        super().__init__()
        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Column(
                            [
                                ft.Text(
                                    'Количество заданий',
                                    size=25,
                                    width=350,
                                    color=ft.colors.BLACK,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                self.counter,
                            ],
                            horizontal_alignment='center'
                        ),
                        ft.ElevatedButton(
                            content=ft.Text('Начать', size=20),
                            width=250,
                            height=50,
                            on_click=self.set_training_content
                        )
                    ],
                    horizontal_alignment='center',
                    spacing=50
                ),
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                padding=25
            )
        ]
        self.alignment = ft.MainAxisAlignment.CENTER
        self.spacing = 100

    #приступить к проверке
    async def set_training_content(self, e):
        self.window.content = self.training(
            self.window, self.page, int(self.counter.value)
        )
        await self.page.update_async()
