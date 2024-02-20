import flet as ft
import contents.main_window
from contents.menu_bar import rail, appbar


#настройка главного окна
async def main(page: ft.Page):
    page.title = 'Russian rhytms'
    page.appbar = appbar
    page.padding = 0

    async def page_resize(e):
        main_container.height = page.height
        main_container.width = page.width - 200
        rail.height = page.height
        await page.update_async()

    page.on_resize = page_resize
    main_container = ft.Container(
        image_src="IMG_1259.JPG",
        image_fit=ft.ImageFit.COVER,
        expand=True,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.BLACK,
        theme_mode=ft.ThemeMode.DARK
    )
    main_container.content = contents.main_window.MainContent(main_container, page)
    await page.add_async(
        ft.Row(
            controls=[
                rail,
                ft.VerticalDivider(
                    width=1
                ),
                main_container
            ]
        )
    )
    rail.win = main_container
    appbar.win = main_container
    rail.page = page
    appbar.page = page
    await page_resize(None)


#старт
ft.app(main)
