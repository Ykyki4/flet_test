import json
import flet as ft
import httpx
from typing import List, Dict, Any


class ItemsList:
    """Component that displays items from backend in a DataTable.

    Usage: create `items = ItemsList(page)` and add `items.view` to the page.
    Call `items.refresh()` to reload data.
    """

    def __init__(self, page: ft.Page, api_url: str = "http://localhost:8001/items/"):
        self.page = page
        self.api_url = api_url

        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Description")),
                ft.DataColumn(ft.Text("Price")),
            ],
            rows=[],
            visible=False,
            width=800,
        )

        self.refresh_btn = ft.IconButton(icon=ft.icons.Icons.REFRESH, tooltip="Refresh", on_click=self._on_refresh)

        self.view = ft.Column([
            ft.Row([ft.Text("Items from backend", size=16), self.refresh_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            self.table,
        ])

        # initial load
        self.refresh()

    def _on_refresh(self, e):
        self.refresh()

    def refresh(self):
        items = self._fetch_items()
        self._populate_table(items)
        self.page.update()

    def _fetch_items(self) -> List[Dict[str, Any]]:
        try:
            resp = httpx.get(self.api_url, timeout=5.0)
            resp.raise_for_status()
            try:
                return resp.json()
            except json.JSONDecodeError:
                return []
        except Exception:
            return []

    def _populate_table(self, items: List[Dict[str, Any]]):
        rows = []
        for it in items:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(it.get("id", "")))),
                        ft.DataCell(ft.Text(it.get("name", ""))),
                        ft.DataCell(ft.Text(it.get("description", ""))),
                        ft.DataCell(ft.Text(str(it.get("price", "")))),
                    ]
                )
            )

        self.table.rows = rows
        self.table.visible = True if rows else False
