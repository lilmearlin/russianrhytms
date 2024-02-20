import flet as ft
import contents.registrations
import contents.enter
import contents.accents_training
import contents.slovnik_training
import contents.settings_training
import contents.main_window
import contents.accents_list
import contents.slovnik_list


async def reg(e):
    appbar.win.content = contents.registrations.RegistrationContent(appbar.win, appbar.page)
    await appbar.page.update_async()


async def enter(e):
    appbar.win.content = contents.enter.EnterContent(appbar.win, appbar.page)
    await appbar.page.update_async()


async def update_avatar():
    appbar.actions = [
        ft.CircleAvatar(
            content=ft.Text(appbar.page.session.get('user')[0])
        )
    ]
    await appbar.page.update_async()


async def click(e):
    i = e.control.selected_index
    if i == 0:
        appbar.win.content = contents.slovnik_list.SlovnikListContent(
            appbar.win,
            appbar.page
        )
    elif i == 1:
        appbar.win.content = contents.accents_list.AccentsListContent(
            appbar.win,
            appbar.page
        )
    elif i == 2:
        appbar.win.content = contents.settings_training.SettingsContent(
            appbar.win,
            appbar.page,
            contents.slovnik_training.SlovnikTrainingContent
        )
    elif i == 3:
        appbar.win.content = contents.settings_training.SettingsContent(
            appbar.win,
            appbar.page,
            contents.accents_training.AccentsTrainingContent
        )
    elif i == 4:
        appbar.win.content = contents.main_window.MainContent(appbar.win, appbar.page)
    await appbar.page.update_async()


rail = ft.NavigationRail(
    selected_index=0,
    label_type=ft.NavigationRailLabelType.ALL,
    min_extended_width=400,
    group_alignment=-0.9,
    destinations=[
        ft.NavigationRailDestination(
            icon_content=ft.Icon(ft.icons.MENU_BOOK),
            selected_icon_content=ft.Icon(ft.icons.MENU_BOOK),
            label="Словарные слова",
        ),
        ft.NavigationRailDestination(
            icon=ft.icons.SPELLCHECK,
            selected_icon_content=ft.Icon(ft.icons.SPELLCHECK),
            label="Ударения",
        ),
        ft.NavigationRailDestination(
            icon=ft.icons.BORDER_COLOR,
            selected_icon_content=ft.Icon(ft.icons.BORDER_COLOR),
            label="Тренировка слов"
        ),
        ft.NavigationRailDestination(
            icon=ft.icons.AUTOFPS_SELECT,
            label='Тренировка ударений'
        ),
        ft.NavigationRailDestination(
            icon=ft.icons.HOME,
            label='Главная'
        ),
    ],
    on_change=click,
)
rail.selected_index = 4


appbar = ft.AppBar(
    title=ft.Text("RussianRhytms"),
    center_title=False,
    bgcolor=ft.colors.SURFACE_VARIANT,
    actions=[
        ft.PopupMenuButton(
            icon=ft.icons.ACCOUNT_CIRCLE,
            items=[
                ft.PopupMenuItem(
                    text="Вход",
                    on_click=enter
                ),
                ft.PopupMenuItem(
                    text="Регистрация",
                    on_click=reg
                ),
            ]
        ),
    ],
)
