#класс регистрации пользователя

import smtplib
import flet as ft
import contents.enter_code_content
import contents.main_window
import random
import sqlite3


class RegistrationContent(ft.Column):
    #задания начальных значений, настройка элементов управления на форме
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
                        content=ft.Text('Зарегистрироваться', size=20),
                        on_click=self.registration
                    )
                ]
            )
        ]
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = 'center'
        self.spacing = 75
    
    #функция регистрация пользователя по e-mail
    async def registration(self, e):
        if self.mail.value and self.password.value:
            try:
                if self.get_user() is None:
                    code = random.randint(1000, 9999)
                    self.page.session.set('code', code)
                    self.page.session.set('email', self.mail.value)
                    self.page.session.set('password', self.password.value)
                    self.page.session.set('type', 'registration')
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
                        self.controls.append(ft.Text('Пользователь с такой почтой уже существует', size=20,color=ft.colors.RED_500))
                        await self.page.update_async()
            except Exception as e:
                raise e
                await self.on_main(None)
    # возврат к главному экрану
    async def on_main(self, e):
        self.window.content = contents.main_window.MainContent(self.window, self.page)
        await self.page.update_async()
    
    #проверка существования пользователя в базе данных
    def get_user(self):
        data = contents.server_work.request(f'check {self.mail.value}'.encode())
        if data.decode() == 'true':
            return True
        return None
