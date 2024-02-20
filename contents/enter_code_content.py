#определение класса функционала входа по коду

import flet as ft
import contents.menu_bar
import contents.main_window
import contents.server_work

class EnterCodeContent(ft.Column):
    #начальная инициализация
    def __init__(self, window, page):
        super().__init__()
        self.window = window
        self.page = page
        self.code = ft.TextField(label='Код', width=350, border_color=ft.colors.WHITE, color=ft.colors.WHITE, cursor_color='#708090', label_style=ft.TextStyle(color=ft.colors.WHITE))
        self.controls = [
            ft.Text(f'Код был отправлен на почту {self.page.session.get("email")}', size=17,color=ft.colors.WHITE),
            self.code,
            ft.ElevatedButton(content=ft.Text('Подтвердить'), width=250, height=50, on_click=self.enter)
        ]
        self.spacing = 75
        self.alignment = 'center'
        self.horizontal_alignment = 'center'
    
    #функция проверки пользователя по коду на основе e-mail
    async def enter(self, e):
        if self.code.value == str(self.page.session.get('code')):
            if self.page.session.get('type') == 'registration':
                self.add_user()
                self.page.session.set('user', self.page.session.get('email'))
                await contents.menu_bar.update_avatar()
                self.window.content = contents.main_window.MainContent(self.window, self.page)
            else:
                self.page.session.set('user', self.page.session.get('email'))
                await contents.menu_bar.update_avatar()
                self.window.content = contents.main_window.MainContent(self.window, self.page)
            await self.page.update_async()
        else:
            self.controls = [
                ft.Text(f'Код был отправлен на почту {self.page.session.get("email")}', size=17, color=ft.colors.WHITE),
                self.code,
                ft.ElevatedButton(content=ft.Text('Подтвердить'), width=350, height=75, on_click=self.enter),
                ft.Text('Неверный код подтверждения', size=20,color=ft.colors.RED_500)
            ]
            await self.page.update_async()


    #функция добавления нового пользователя в бд
    def add_user(self):
        contents.server_work.request(
            f'add {self.page.session.get("email")} {self.page.session.get("password")}'.encode()
        )
