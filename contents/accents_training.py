#определение класса для проверки ударения слов

import flet as ft
import contents.server_work
import random
import accents


class AccentsTrainingContent(ft.Column):
    #определение начальных параметров и элементов на форме
    def __init__(self, window, page, count):
        super().__init__()
        self.window = window
        self.page = page
        self.words = random.sample(accents.words, count)
        self.answers = []

        self.answer_options = ft.RadioGroup(
            content=self.get_answer_options(self.words[0])
        )
        self.main_word = ft.Text(self.words[0].lower(), size=30, color=ft.colors.BLACK)
        self.count_done = ft.Text(f'1/{count}', size=25, color=ft.colors.BLACK)

        if self.page.session.get('user') is not None:
            self.star_accents = contents.server_work.request(f'getaccents {self.page.session.get("user")}'.encode()).decode().split()
        else:
            self.star_accents = []

        self.star_button = ft.IconButton(
            icon=ft.icons.STAR if self.words[0] in self.star_accents else ft.icons.STAR_OUTLINE,
            on_click=self.star_clicked
        )

        self.controls = [
            ft.Container(
                bgcolor=ft.colors.WHITE,
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                self.count_done,
                                self.star_button
                            ],
                            width=min(self.page.width - 500, 600),
                            alignment='center'
                        ),
                        self.main_word,
                        self.answer_options,
                        ft.ElevatedButton(
                            content=ft.Text('Ответить', size=20), on_click=self.show_next_word, width=250, height=50
                        )
                    ],
                    horizontal_alignment='center',
                    spacing=25,
                    height=600,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                border_radius=10,
                width=min(self.page.width - 500, 600),
                padding=5
            ),
        ]
        self.scroll = ft.ScrollMode.ALWAYS

    def get_answer_options(self, word):
        word = word.lower()
        options = []
        for i in range(len(word)):
            if word[i] in 'ёуеыаоэяию':
                s = word[:i] + word[i].upper() + word[i + 1 :]
                options.append(ft.Row([ft.Radio(value=s), ft.Text(s, size=20, color=ft.colors.BLACK)]))
        return ft.Row([ft.Column(options)], alignment='center')

    #следующий шаг проверки
    async def show_next_word(self, e):
        self.answers.append(self.answer_options.value)
        if len(self.answers) == len(self.words):
            await self.show_result_table()
        else:
            self.main_word.value = self.words[len(self.answers)].lower()
            self.count_done.value = f'{len(self.answers) + 1}/{len(self.words)}'
            self.answer_options.content = self.get_answer_options(
                self.words[len(self.answers)]
            )
            self.answer_options.value = ''
            self.star_button.icon=ft.icons.STAR if self.words[len(self.answers)] in self.star_accents else ft.icons.STAR_OUTLINE
            await self.page.update_async()
    
    #показать итоговую таблицу
    async def show_result_table(self):
        self.height = self.page.height
        rows = []
        count_skip = 0
        count_true = 0
        count_false = 0
        for i in range(len(self.words)):
            res = '+' if self.words[i] == self.answers[i] else '-'
            if not self.words[i]:
                res = '-'
                count_skip += 1
            elif self.words[i] == self.answers[i]:
                res = '+'
                count_true += 1
            else:
                count_false += 1
                res = '-'
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(self.words[i],font_family='Verdana',color=ft.colors.BLACK)),
                        ft.DataCell(ft.Text(self.answers[i],font_family='Verdana',color=ft.colors.GREEN_500 if res=='+' else ft.colors.RED_500)),
                        #ft.DataCell(ft.Text(res,font_family='Verdana',color=ft.colors.GREEN_500 if res=='+' else ft.colors.RED_500)),
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
        table_height = self.page.height - 200
        self.controls = [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Column(
                            [table], height=table_height, alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.ALWAYS
                        ),
                    ],
                    height=self.page.height,
                    run_spacing=50,
                    spacing=200,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=ft.colors.WHITE,
                padding=5,
                border_radius=10,
                width=600,
                margin=50
            )
        ]
        self.scroll = ft.ScrollMode.HIDDEN
        await self.page.update_async()
    
    async def star_clicked(self, e):
        if self.star_button.icon == ft.icons.STAR:
            self.star_button.icon = ft.icons.STAR_OUTLINE
            if self.page.session.get('user') is not None:
                contents.server_work.request(f'delaccent {self.page.session.get("user")} {self.words[len(self.answers)]}'.encode())
        else:
            self.star_button.icon = ft.icons.STAR
            if self.page.session.get('user') is not None:
                contents.server_work.request(f'addaccent {self.page.session.get("user")} {self.words[len(self.answers)]}'.encode())
        await self.page.update_async()
