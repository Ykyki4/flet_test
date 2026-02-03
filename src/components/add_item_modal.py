import flet as ft
import httpx
from typing import Callable, Optional


class AddItemModal:
    def __init__(self, page: ft.Page, on_save: Optional[Callable[[dict], None]] = None, refresh_callback: Optional[Callable] = None):
        self.page = page
        self.on_save = on_save
        self.refresh_callback = refresh_callback

        self.item_name = ft.TextField(label="Item Name", width=300)
        self.description = ft.TextField(label="Description", width=300)
        self.price = ft.TextField(label="Price", width=300)

        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add Item"),
            content=ft.Column([
                self.item_name,
                self.description,
                self.price,
            ], tight=True),
            actions=[
                ft.TextButton("Отмена", on_click=self._close),
                ft.Button("Сохранить", on_click=self._save),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def open(self):
        self.page.show_dialog(self.dialog)

    def _close(self, e=None):
        self.dialog.open = False
        self.page.update()

    def _save(self, e=None):
        data = {
            "name": self.item_name.value,
            "description": self.description.value,
            "price": self.price.value,
        }
        if self.on_save:
            try:
                self.on_save(data)
            finally:
                self._close()
            return

        try:
            response = httpx.post("http://localhost:8001/items/", json=data)
            if response.status_code == 201:
                snack_bar = ft.SnackBar(ft.Text("Item added successfully!"))
                self.page.show_dialog(snack_bar)
                self._close()
                if self.refresh_callback:
                    self.refresh_callback()
            else:
                snack_bar = ft.SnackBar(ft.Text(f"Failed to add item: {response.text}"))
                self.page.show_dialog(snack_bar)
        except Exception as ex:
            snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"))
            self.page.show_dialog(snack_bar)
        finally:
            self.page.update()
