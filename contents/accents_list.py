import flet as ft
import contents.server_work
import accents


class AccentsListContent(ft.Column):
    def __init__(self, win, page):
        super().__init__()
        self.window = win
        self.page = page
        self.button = ft.IconButton(
            icon=ft.icons.STAR_OUTLINE,
            on_click=self.button_clicked,
            width=50,
            height=50
        )
        self.update_controls()
        self.scroll = ft.ScrollMode.ALWAYS
    
    def add_word(self, e):
        if e.control.value:
            contents.server_work.request(f'addaccent {self.page.session.get("user")} {e.control.key}'.encode())
        else:
            contents.server_work.request(f'delaccent {self.page.session.get("user")} {e.control.key}'.encode())
    
    async def button_clicked(self, e):
        if self.button.icon == ft.icons.STAR_OUTLINE:
            self.button.icon = ft.icons.STAR
        else:
            self.button.icon = ft.icons.STAR_OUTLINE
        self.update_controls()
        await self.page.update_async()
    
    def update_controls(self):
        controls = [ft.Row([self.button], alignment='center', width=300)]
        if self.page.session.get('user') is not None:
            accents_main = contents.server_work.request(f'getaccents {self.page.session.get("user")}'.encode()).decode().split()
        else:
            accents_main = []
        for i in range(len(accents.words)):
            if self.button.icon == ft.icons.STAR_OUTLINE or accents.words[i] in accents_main:
                row = ft.Row(
                    controls=[
                        ft.Text(str(i + 1) + ') ' + accents.words[i], size=20, color=ft.colors.BLACK),
                        ft.Checkbox(
                            value=True if accents.words[i] in accents_main else False,
                            on_change=self.add_word,
                            key=accents.words[i]
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    width=300
                )
                controls.append(row)

        self.controls = [
            ft.Container(
                content=ft.Column(
                    controls
                ),
                bgcolor=ft.colors.WHITE,
                margin=20,
                border_radius=10
            )
        ]
