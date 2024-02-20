#модуль определения класса проверки словарных слов

import flet as ft
import contents.main_window
import contents.settings_training
import random
import slovnik


class SlovnikTrainingContent(ft.Column):
    #начальная инициализация
    def __init__(self, window, page, count):
        super().__init__()
        self.scroll = ft.ScrollMode.ALWAYS
        self.window = window
        self.page = page
        self.words = random.sample(slovnik.slovnik, count)
        self.answers = []
        self.answer_options = ft.TextField(width=250,color=ft.colors.BLACK,border_color=ft.colors.BLACK)
        self.main_word = ft.Text(self.words[0][1].lower(), size=30,color=ft.colors.BLACK)
        self.count_done = ft.Text(f'1/{count}', size=25,color=ft.colors.BLACK)
        #настройка элементов управления
        if self.page.session.get('user') is not None:
            self.star_accents = contents.server_work.request(f'getwords {self.page.session.get("user")}'.encode()).decode().split()
        else:
            self.star_accents = []

        self.star_button = ft.IconButton(
            icon=ft.icons.STAR if self.words[0] in self.star_accents else ft.icons.STAR_OUTLINE,
            on_click=self.star_clicked
        )
        self.controls = [
            ft.Container(
                ft.Column(
                    [
                        ft.Row(
                            [
                                self.count_done,
                                self.star_button
                            ],
                            alignment='center'
                        ),
                        self.main_word,
                        self.answer_options,
                        ft.ElevatedButton(
                            content=ft.Text('Ответить', size=20), on_click=self.show_next_word, width=250, height=50
                        )
                    ],
                    horizontal_alignment='center',
                    spacing=25
                ),
                bgcolor=ft.colors.WHITE,
                padding=25,
                border_radius=10,
                width=min(self.page.width - 500, 600),
                margin=50
            )
        ]
        self.horizontal_alignment = 'center'
        self.spacing = 75
    
    #следующий  шаг проверки 
    async def show_next_word(self, e):
        self.answers.append(self.answer_options.value)
        if len(self.answers) == len(self.words):
            await self.show_result_table()
        else:
            self.main_word.value = self.words[len(self.answers)][1].lower()
            self.count_done.value = f'{len(self.answers) + 1}/{len(self.words)}'
            self.answer_options.value = ''
            self.star_button.icon=ft.icons.STAR if self.words[len(self.answers)][0] in self.star_accents else ft.icons.STAR_OUTLINE
            await self.page.update_async()
    
    #функция вывода результатов проверки
    async def show_result_table(self):
        self.height = self.page.height
        rows = []
        count_skip = 0
        count_true = 0
        count_false = 0
        for i in range(len(self.words)):
            if not self.answers[i]:
                res = '-'
                count_skip += 1
            elif self.words[i][0] == self.answers[i]:
                res = '+'
                count_true += 1
            else:
                count_false += 1
                res = '-'
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(self.words[i][0],font_family='Verdana',color=ft.colors.BLACK)),
                        ft.DataCell(ft.Text(self.answers[i],font_family='Verdana',color=ft.colors.GREEN_500 if res=='+' else ft.colors.RED_500)),
                        #ft.DataCell(ft.Text(res,font_family='Verdana',color=ft.colors.WHITE)),
                    ]
                )
            )
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text('Правильный ответ',font_family='Verdana',color=ft.colors.BLACK)),
                ft.DataColumn(ft.Text('Ваш ответ',font_family='Verdana',color=ft.colors.BLACK)),
                #ft.DataColumn(ft.Text('')),
            ],
            rows=rows,
        )
        table_height = self.page.height
        self.controls = [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Column(
                            [table], scroll=ft.ScrollMode.ALWAYS, height=table_height, alignment=ft.MainAxisAlignment.CENTER
                        ),
                    ],
                    height=self.page.height,
                    run_spacing=50,
                    spacing=200,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=ft.colors.WHITE,
                padding=25,
                border_radius=10,
                width=600,
                margin=50
            )
        ]
        self.scroll = ft.ScrollMode.HIDDEN
        await self.page.update_async()

    #на главный экран
    async def show_main_window(self, e):
        self.window.content = contents.main_window.MainContent(self.window, self.page)
        await self.page.update_async()
    
    #повторить проверку
    async def repeat_training(self, e):
        self.window.content = contents.settings_training.SettingsContent(self.window, self.page, SlovnikTrainingContent)
        await self.page.update_async()
    
    async def star_clicked(self, e):
        if self.star_button.icon == ft.icons.STAR:
            self.star_button.icon = ft.icons.STAR_OUTLINE
            if self.page.session.get('user') is not None:
                contents.server_work.request(f'delword {self.page.session.get("user")} {self.words[len(self.answers)][0]}'.encode())
        else:
            self.star_button.icon = ft.icons.STAR
            if self.page.session.get('user') is not None:
                contents.server_work.request(f'addword {self.page.session.get("user")} {self.words[len(self.answers)][0]}'.encode())
        await self.page.update_async()
