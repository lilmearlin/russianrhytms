import flet as ft


class MainContent(ft.Column):
    #определение элементов управления
    def __init__(self, window, page):
        super().__init__()
        self.page = page
        self.alignment = 'center'
        self.horizontal_alignment = 'center'
        
        self.controls = [
            ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        'Рады вас видеть в приложении Russian rhythms! В приложении вы можете найти полный список словарных слов и ударений, которые взяты из сборников ФИПИ. А также потренировать свои полученные знания в разделах тренировок, которые приближены к формату экзамена.',
                        size=20,
                        text_align=ft.TextAlign.CENTER,
                        width=500,
                        color=ft.colors.BLACK
                    )
                ],
            ),
            bgcolor=ft.colors.WHITE,
            padding=25,
            width=600,
            border_radius=10
            )
        ]
