import flet as ft
from components.add_item_modal import AddItemModal
from components.items_list import ItemsList


def main(page: ft.Page):
    item_list = ItemsList(page)
    add_modal = AddItemModal(page, refresh_callback=item_list.refresh)

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=lambda e: add_modal.open()
    )

    page.title = "Flet CRUD Example"

    page.add(
        ft.SafeArea(
            expand=True,
            content=item_list.view,
        )
    )


ft.run(main)
