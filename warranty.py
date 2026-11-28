"""Garantia dos produtos comprados no NightFall.

O prazo (em meses) é cadastrado no produto pelo painel administrativo. Cada
pedido guarda o prazo vigente na compra; a aba "Garantia" do perfil calcula a
validade a partir da data do pedido.
"""

from __future__ import annotations

import calendar
import json
from datetime import date, datetime
from pathlib import Path
from typing import TypedDict

from order_persistence import ORDERS_FILE

MAX_WARRANTY_MONTHS = 120


class WarrantyItem(TypedDict):
    product_name: str
    order_id: str
    purchase_date: str
    expiry_date: str
    months_display: str
    status: str
    active: bool


def parse_warranty_months(text: str) -> int:
    """Converte o campo do painel em meses. Vazio = sem garantia (0)."""
    text = (text or "").strip()
    if not text:
        return 0
    if not (text.isascii() and text.isdigit()) or int(text) > MAX_WARRANTY_MONTHS:
        raise ValueError(
            f"Garantia inválida. Informe os meses, de 0 a {MAX_WARRANTY_MONTHS}."
        )
    return int(text)


def add_months(start: date, months: int) -> date:
    """Soma meses ao calendário; 31/01 + 1 mês vira o último dia de fevereiro."""
    year, month_index = divmod(start.year * 12 + start.month - 1 + months, 12)
    month = month_index + 1
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(start.day, last_day))


def load_warranties_for_email(
    email: str,
    catalog_months: dict[str, int],
    *,
    path: Path = ORDERS_FILE,
    today: date | None = None,
) -> list[WarrantyItem]:
    """Garantias do cliente, das compras mais recentes para as mais antigas.

    `catalog_months` (nome do produto -> meses) só vale para pedidos antigos, que
    não guardaram o prazo. Pedido que guardou 0 continua sem garantia.
    """
    email = (email or "").strip().lower()
    if not email or not path.exists():
        return []
    try:
        orders = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    if not isinstance(orders, list):
        return []

    today = today or date.today()
    warranties: list[WarrantyItem] = []
    for order in reversed(orders):
        if not isinstance(order, dict):
            continue
        if str(order.get("user_email", "")).strip().lower() != email:
            continue
        try:
            purchased = datetime.strptime(str(order.get("date", "")), "%d/%m/%Y").date()
        except ValueError:
            continue
        for item in order.get("items") or []:
            if not isinstance(item, dict):
                continue
            name = str(item.get("name", ""))
            months = item.get("warranty_months", catalog_months.get(name, 0))
            if type(months) is not int or not 0 < months <= MAX_WARRANTY_MONTHS:
                continue
            expiry = add_months(purchased, months)
            active = today <= expiry
            warranties.append(
                {
                    "product_name": name,
                    "order_id": str(order.get("id", "")),
                    "purchase_date": purchased.strftime("%d/%m/%Y"),
                    "expiry_date": expiry.strftime("%d/%m/%Y"),
                    "months_display": "1 mês" if months == 1 else f"{months} meses",
                    "status": "Ativa" if active else "Expirada",
                    "active": active,
                }
            )
    return warranties
