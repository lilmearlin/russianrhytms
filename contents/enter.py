#определение класса для идентификация и проверки пользователей по e-mail

import smtplib
import flet as ft
import contents.enter_code_content
import contents.main_window
import random
import sqlite3
import contents.server_work
import contents.menu_bar


class EnterContent(ft.Column):
    #подготовка элементов управления
    def __init__(self, window, page):
        super().__init__()
        self.window = window
        self.page = page
        self.mail = ft.TextField(
            width=350,
            label='Почта',
            border_color=ft.colors.WHITE,
            color=ft.colors.WHITE,
            cursor_color='#708090',
            label_style=ft.TextStyle(color=ft.colors.WHITE)
        )
        self.password = ft.TextField(
            width=350,
            label='Пароль',
            border_color=ft.colors.WHITE,
            color=ft.colors.WHITE,
            cursor_color='#708090',
            label_style=ft.TextStyle(color=ft.colors.WHITE)
        )
        self.controls = [
            ft.Column(
                [
                self.mail,
                self.password,
                ],
                spacing=25
            ),
            ft.Column(
                [
                    ft.ElevatedButton(
                        width=250,
                        height=50,
                        content=ft.Text('Войти', size=20),
                        on_click=self.enter
                    ),
                    ft.ElevatedButton(
                        width=250,
                        height=50,
                        content=ft.Text('Войти по коду', size=20),
                        on_click=self.enter_by_code
                    )
                ]
            )
        ]
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = 'center'
        self.spacing = 75
    
    #функция проверки по e-mail и паролю зарегистрированных пользователей
    async def enter(self, e):
        if self.mail.value and self.password.value:
            try:
                data = contents.server_work.request(
                    f'enter {self.mail.value} {self.password.value}'.encode()
                )
                if data.decode() == 'true':
                    self.page.session.set('user', self.mail.value)
                    await contents.menu_bar.update_avatar()
                    self.window.content = contents.main_window.MainContent(self.window, self.page)
                    await self.page.update_async()
                else:
                    if not isinstance(self.controls[-1], ft.Text):
                        self.controls.append(ft.Text('Неправильный пароль или почта', size=20,color=ft.colors.RED_500))
                        await self.page.update_async()
            except Exception as e:
                pass
    
    #функция проверки по коду из e-mail
    async def enter_by_code(self, e):
        if self.mail.value:
            try:
                user = self.get_user()
                if user is not None:
                    code = random.randint(1000, 9999)
                    self.page.session.set('code', code)
                    self.page.session.set('email', self.mail.value)
                    self.page.session.set('type', 'enter')
                    smtp = smtplib.SMTP('smtp.mail.ru', 25)
                    smtp.starttls()
                    smtp.login('russianrhytms@mail.ru', 'SLaEqpVeNuaduQZa2wkV')
                    smtp.sendmail(
                        'russianrhytms@mail.ru',
                        self.mail.value,
                        f'Ваш код для подтверждения почты: {code}'.encode()
                    )
                    smtp.quit()
                    self.window.content = contents.enter_code_content.EnterCodeContent(self.window, self.page)
                    await self.page.update_async()
                else:
                    if not isinstance(self.controls[-1], ft.Text):
                        self.controls.append(ft.Text('Пользователя с такой почтой не сущевствует', size=20, color=ft.colors.RED_500))
                        await self.page.update_async()
            except Exception as e:
                await self.on_main(None)
    
    #получение учетных данных пользователя из базы данных
    def get_user(self):
        data = contents.server_work.request(f'check {self.mail.value}'.encode())
        if data.decode() == 'true':
            return True
        return None
