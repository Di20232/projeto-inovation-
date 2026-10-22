"""NightFall storefront landing page and auth flow."""

import asyncio
import json
import math
import os
from decimal import Decimal
from pathlib import Path
from typing import Any, TypedDict
from urllib.parse import urlparse

import httpx
import reflex as rx


CATEGORIES = ("Computadores", "Componentes", "Periféricos", "Acessórios")
CATALOG_PATH = Path(__file__).with_name("catalog.json")
DEFAULT_XANO_SIGNUP_URL = "https://x8ki-letl-twmt.n7.xano.io/api:nightfall-auth/signup"


class Specification(TypedDict):
    label: str
    value: str


class Product(TypedDict):
    name: str
    image_url: str
    source_url: str
    price: float
    price_display: str
    description: str
    category: str
    specifications: list[Specification]


class Category(TypedDict):
    name: str
    available: bool


def load_catalog(path: Path = CATALOG_PATH) -> list[Product]:
    with path.open(encoding="utf-8") as catalog_file:
        data = json.load(catalog_file)

    if not isinstance(data, list):
        raise ValueError("O catálogo deve ser uma lista JSON de produtos.")

    products: list[Product] = []
    required_fields = {
        "name",
        "image_url",
        "source_url",
        "price",
        "description",
        "category",
    }

    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Produto {index} deve ser um objeto JSON.")

        missing_fields = required_fields - item.keys()
        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise ValueError(f"Produto {index} sem os campos obrigatórios: {missing}.")

        for field in ("name", "image_url", "source_url", "description", "category"):
            if not isinstance(item[field], str) or not item[field].strip():
                raise ValueError(f"Campo '{field}' do produto {index} deve ser texto não vazio.")

        for field in ("image_url", "source_url"):
            product_url = urlparse(item[field])
            if product_url.scheme not in {"http", "https"} or not product_url.netloc:
                raise ValueError(
                    f"URL do campo '{field}' do produto {index} deve ser HTTP ou HTTPS."
                )

        price = item["price"]
        if (
            isinstance(price, bool)
            or not isinstance(price, (int, float))
            or not math.isfinite(price)
            or price < 0
        ):
            raise ValueError(f"Preço do produto {index} deve ser um número finito não negativo.")

        category = item["category"].strip()
        if category not in CATEGORIES:
            raise ValueError(
                f"Categoria do produto {index} deve ser uma destas: {', '.join(CATEGORIES)}."
            )

        raw_specifications = item.get("specifications", [])
        if not isinstance(raw_specifications, list):
            raise ValueError(
                f"Especificações do produto {index} devem ser uma lista de rótulos e valores."
            )

        specifications: list[Specification] = []
        for specification_index, specification in enumerate(raw_specifications, start=1):
            if not isinstance(specification, dict):
                raise ValueError(
                    f"Especificação {specification_index} do produto {index} deve ser um objeto."
                )

            label = specification.get("label")
            value = specification.get("value")
            if not isinstance(label, str) or not label.strip():
                raise ValueError(
                    f"Rótulo da especificação {specification_index} do produto {index} "
                    "deve ser texto não vazio."
                )
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"Valor da especificação {specification_index} do produto {index} "
                    "deve ser texto não vazio."
                )

            specifications.append({"label": label.strip(), "value": value.strip()})

        formatted_price = f"{Decimal(str(price)):,.2f}"
        formatted_price = formatted_price.replace(",", "X").replace(".", ",").replace("X", ".")
        products.append(
            {
                "name": item["name"].strip(),
                "image_url": item["image_url"].strip(),
                "source_url": item["source_url"].strip(),
                "price": price,
                "price_display": f"R$ {formatted_price}",
                "description": item["description"].strip(),
                "category": category,
                "specifications": specifications,
            }
        )

    return products


class CatalogState(rx.State):
    products: list[Product] = load_catalog()
    selected_category: str = "Todos"
    category_menu_open: bool = False
    product_details_open: bool = False
    selected_product_name: str = ""
    selected_product_image_url: str = ""
    selected_product_price_display: str = ""
    selected_product_description: str = ""
    selected_product_category: str = ""
    selected_product_specifications: list[Specification] = []

    @rx.event
    def select_category(self, category: str):
        self.selected_category = category
        self.category_menu_open = False

    @rx.event
    def show_all_products(self):
        self.selected_category = "Todos"
        self.category_menu_open = False

    @rx.event
    def set_category_menu_open(self, is_open: bool):
        self.category_menu_open = is_open

    @rx.event
    def open_product_details(self, product_name: str):
        product = next(
            (item for item in self.products if item["name"] == product_name),
            None,
        )
        if product is None:
            raise ValueError(f"Produto não encontrado no catálogo: {product_name}.")

        self.selected_product_name = product["name"]
        self.selected_product_image_url = product["image_url"]
        self.selected_product_price_display = product["price_display"]
        self.selected_product_description = product["description"]
        self.selected_product_category = product["category"]
        self.selected_product_specifications = product["specifications"]
        self.product_details_open = True

    @rx.event
    def set_product_details_open(self, is_open: bool):
        self.product_details_open = is_open
        if not is_open:
            self.selected_product_name = ""
            self.selected_product_image_url = ""
            self.selected_product_price_display = ""
            self.selected_product_description = ""
            self.selected_product_category = ""
            self.selected_product_specifications = []

    @rx.var
    def filtered_products(self) -> list[Product]:
        if self.selected_category == "Todos":
            return self.products
        return [
            product
            for product in self.products
            if product["category"] == self.selected_category
        ]

    @rx.var
    def categories(self) -> list[Category]:
        return [
            {
                "name": category,
                "available": any(
                    product["category"] == category for product in self.products
                ),
            }
            for category in CATEGORIES
        ]


class LoginState(rx.State):
    email: str = ""
    password: str = ""
    login_message: str = ""
    login_succeeded: bool = False
    is_submitting: bool = False

    @rx.event
    def set_email(self, value: str):
        self.email = value
        self.login_message = ""
        self.login_succeeded = False

    @rx.event
    def set_password(self, value: str):
        self.password = value
        self.login_message = ""
        self.login_succeeded = False

    @rx.event
    async def login(self):
        email = self.email.strip().lower()
        password = self.password

        if not email or not password:
            self.login_message = "Informe e-mail e senha."
            self.login_succeeded = False
            return

        self.login_message = ""
        self.login_succeeded = False
        self.is_submitting = True
        try:
            await asyncio.sleep(0.8)
            if "@" in email and len(password) >= 6:
                self.login_message = "Login realizado com sucesso!"
                self.login_succeeded = True
            else:
                self.login_message = "Credenciais inválidas. Verifique seu e-mail e senha."
        except Exception:
            self.login_message = "Erro ao conectar com o serviço de autenticação."
        finally:
            self.is_submitting = False


class RegistrationState(rx.State):
    name: str = ""
    cpf: str = ""
    birth_date: str = ""
    email: str = ""
    password: str = ""
    registration_message: str = ""
    registration_succeeded: bool = False
    is_submitting: bool = False

    @rx.event
    def set_name(self, value: str):
        self.name = value
        self.registration_message = ""
        self.registration_succeeded = False

    @rx.event
    def set_cpf(self, value: str):
        self.cpf = value
        self.registration_message = ""
        self.registration_succeeded = False

    @rx.event
    def set_birth_date(self, value: str):
        self.birth_date = value
        self.registration_message = ""
        self.registration_succeeded = False

    @rx.event
    def set_email(self, value: str):
        self.email = value
        self.registration_message = ""
        self.registration_succeeded = False

    @rx.event
    def set_password(self, value: str):
        self.password = value
        self.registration_message = ""
        self.registration_succeeded = False

    @rx.event
    async def register(self):
        name = self.name.strip()
        cpf = self.cpf.strip()
        birth_date = self.birth_date.strip()
        email = self.email.strip().lower()
        password = self.password

        if not name:
            self.registration_message = "Informe seu nome completo."
            self.registration_succeeded = False
            return

        if not cpf:
            self.registration_message = "Informe seu CPF."
            self.registration_succeeded = False
            return

        if not birth_date:
            self.registration_message = "Informe sua data de nascimento."
            self.registration_succeeded = False
            return

        if not email:
            self.registration_message = "Informe um e-mail válido."
            self.registration_succeeded = False
            self.password = ""
            return

        if len(password) < 8:
            self.registration_message = "A senha deve conter pelo menos 8 caracteres."
            self.registration_succeeded = False
            self.password = ""
            return

        signup_url = os.getenv("XANO_SIGNUP_URL", DEFAULT_XANO_SIGNUP_URL).strip()
        try:
            parsed_signup_url = urlparse(signup_url)
        except ValueError:
            parsed_signup_url = None

        if (
            parsed_signup_url is None
            or parsed_signup_url.scheme != "https"
            or not parsed_signup_url.netloc
        ):
            self.registration_message = "Cadastro indisponível: configure o endpoint do Xano."
            self.registration_succeeded = False
            self.password = ""
            return

        self.registration_message = ""
        self.registration_succeeded = False
        self.is_submitting = True
        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=False) as client:
                response = await client.post(
                    signup_url,
                    json={
                        "name": name,
                        "cpf": cpf,
                        "birth_date": birth_date,
                        "email": email,
                        "password": password,
                    },
                )
                response.raise_for_status()
                signup_result = response.json()
        except httpx.HTTPStatusError as error:
            if error.response.status_code == 403:
                self.registration_message = "Este e-mail já está cadastrado."
            elif error.response.status_code in {400, 422}:
                self.registration_message = (
                    "Dados inválidos. Verifique as informações preenchidas."
                )
            else:
                self.registration_message = (
                    f"O Xano recusou o cadastro (HTTP {error.response.status_code}). "
                    "Tente novamente."
                )
        except httpx.InvalidURL:
            self.registration_message = "A URL de cadastro do Xano está inválida."
        except httpx.RequestError:
            self.registration_message = "Não foi possível conectar ao Xano. Tente novamente."
        except ValueError:
            self.registration_message = "O Xano retornou uma resposta inválida."
        else:
            if isinstance(signup_result, dict) and signup_result.get("success") is True:
                self.registration_message = "Conta criada com sucesso!"
                self.registration_succeeded = True
            else:
                self.registration_message = "O Xano não confirmou a criação da conta."
        finally:
            self.password = ""
            self.is_submitting = False


def category_item(category: rx.Var[Any]) -> rx.Component:
    return rx.cond(
        category["available"],
        rx.dialog.close(
            rx.button(
                category["name"],
                on_click=CatalogState.select_category(category["name"]),
                variant="ghost",
                color=rx.cond(
                    CatalogState.selected_category == category["name"],
                    "#f5f3ff",
                    "#d4d4d8",
                ),
                background=rx.cond(
                    CatalogState.selected_category == category["name"],
                    "rgba(139, 92, 246, 0.18)",
                    "transparent",
                ),
                border_left=rx.cond(
                    CatalogState.selected_category == category["name"],
                    "3px solid #a78bfa",
                    "3px solid transparent",
                ),
                aria_pressed=CatalogState.selected_category == category["name"],
                width="100%",
                min_height="52px",
                padding="12px 16px",
                justify="start",
                text_align="left",
                white_space="normal",
                line_height="1.4",
                border_radius="12px",
                font_size="15px",
                font_weight=rx.cond(
                    CatalogState.selected_category == category["name"],
                    "600",
                    "500",
                ),
                transition="background-color 160ms ease, color 160ms ease",
                _hover={
                    "background": "rgba(139, 92, 246, 0.12)",
                    "color": "#f5f3ff",
                },
                _focus_visible={
                    "outline": "2px solid #c4b5fd",
                    "outline_offset": "2px",
                },
            ),
        ),
        rx.hstack(
            rx.text(
                category["name"],
                color="#a1a1aa",
                font_size="15px",
                font_weight="500",
                line_height="1.4",
            ),
            rx.badge("Em breve", color_scheme="purple", variant="soft"),
            width="100%",
            min_height="52px",
            justify="between",
            align="center",
            padding="12px 16px",
            border_radius="12px",
            background="rgba(255, 255, 255, 0.025)",
        ),
    )


def product_card(product: rx.Var[Product]) -> rx.Component:
    return rx.button(
        rx.vstack(
            rx.image(
                src=product["image_url"],
                alt=product["name"],
                width="100%",
                height="220px",
                object_fit="contain",
                background="#0b0b12",
                border_radius="16px",
            ),
            rx.text(
                product["category"],
                color="#c4b5fd",
                font_size="12px",
                font_weight="700",
                letter_spacing="0.08em",
                text_transform="uppercase",
            ),
            rx.heading(product["name"], size="4", color="#f5f3ff"),
            rx.text(
                product["description"],
                color="#a1a1aa",
                font_size="14px",
                line_height="1.6",
            ),
            rx.text(
                product["price_display"],
                color="#e9d5ff",
                font_size="18px",
                font_weight="700",
            ),
            width="100%",
            align="start",
            spacing="3",
        ),
        on_click=CatalogState.open_product_details(product["name"]),
        aria_label=f"Ver detalhes de {product['name']}",
        variant="ghost",
        width="100%",
        height="100%",
        padding="18px",
        color="#f5f3ff",
        text_align="left",
        white_space="normal",
        align_items="stretch",
        justify_content="flex-start",
        background="linear-gradient(145deg, rgba(24, 20, 36, 0.92), rgba(15, 14, 22, 0.96))",
        border="1px solid rgba(167, 139, 250, 0.16)",
        border_radius="24px",
        box_shadow="0 24px 80px rgba(0, 0, 0, 0.2)",
        _hover={
            "border_color": "rgba(196, 181, 253, 0.5)",
            "box_shadow": "0 24px 80px rgba(0, 0, 0, 0.3)",
        },
    )


def specification_row(specification: rx.Var[Specification]) -> rx.Component:
    return rx.hstack(
        rx.text(
            specification["label"],
            color="#a1a1aa",
            font_size="14px",
            flex="1",
            min_width="0",
            overflow_wrap="anywhere",
        ),
        rx.text(
            specification["value"],
            color="#f5f3ff",
            font_size="14px",
            font_weight="600",
            text_align="right",
            flex="1",
            min_width="0",
            overflow_wrap="anywhere",
        ),
        width="100%",
        align="start",
        spacing="4",
        padding_y="12px",
        border_bottom="1px solid rgba(167, 139, 250, 0.12)",
    )


def product_details_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.hstack(
                    rx.dialog.title(
                        CatalogState.selected_product_name,
                        color="#f5f3ff",
                        font_size="22px",
                        font_weight="700",
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Fechar",
                            variant="soft",
                            color_scheme="gray",
                            aria_label="Fechar detalhes do produto",
                        ),
                    ),
                    width="100%",
                    justify="between",
                    align="start",
                    spacing="4",
                ),
                rx.image(
                    src=CatalogState.selected_product_image_url,
                    alt=CatalogState.selected_product_name,
                    width="100%",
                    height="clamp(180px, 34vh, 300px)",
                    object_fit="contain",
                    background="#0b0b12",
                    border_radius="16px",
                ),
                rx.badge(
                    CatalogState.selected_product_category,
                    color_scheme="purple",
                    variant="soft",
                ),
                rx.text(
                    CatalogState.selected_product_price_display,
                    color="#e9d5ff",
                    font_size="22px",
                    font_weight="700",
                ),
                rx.dialog.description(
                    "Preços e disponibilidade podem mudar. Confirme essas informações na loja.",
                    color="#c4b5fd",
                    font_size="14px",
                    line_height="1.6",
                ),
                rx.text(
                    CatalogState.selected_product_description,
                    color="#d4d4d8",
                    font_size="15px",
                    line_height="1.7",
                ),
                rx.heading(
                    "Especificações",
                    size="4",
                    color="#f5f3ff",
                    margin_top="8px",
                ),
                rx.cond(
                    CatalogState.selected_product_specifications.length() > 0,
                    rx.vstack(
                        rx.foreach(
                            CatalogState.selected_product_specifications,
                            specification_row,
                        ),
                        width="100%",
                        align="stretch",
                        spacing="0",
                    ),
                    rx.text(
                        "Não há especificações adicionais disponíveis para este produto.",
                        color="#a1a1aa",
                        font_size="14px",
                        line_height="1.6",
                    ),
                ),
                width="100%",
                align="start",
                spacing="4",
            ),
            width="min(92vw, 760px)",
            max_width="calc(100vw - 24px)",
            max_height="88vh",
            overflow_y="auto",
            overflow_x="hidden",
            overscroll_behavior="contain",
            padding="24px",
            background="#101018",
            border="1px solid rgba(167, 139, 250, 0.2)",
            border_radius="24px",
            box_shadow="0 24px 80px rgba(0, 0, 0, 0.45)",
            outline="none",
            visibility=rx.cond(
                CatalogState.product_details_open,
                "visible",
                "hidden",
            ),
            pointer_events=rx.cond(
                CatalogState.product_details_open,
                "auto",
                "none",
            ),
        ),
        open=CatalogState.product_details_open,
        on_open_change=CatalogState.set_product_details_open,
    )


def product_catalog() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("Catálogo", size="6", color="#f5f3ff"),
            rx.button(
                "Todos os produtos",
                on_click=CatalogState.show_all_products,
                variant="soft",
                color_scheme="purple",
            ),
            width="100%",
            justify="between",
            align="center",
        ),
        rx.cond(
            CatalogState.filtered_products.length() > 0,
            rx.grid(
                rx.foreach(CatalogState.filtered_products, product_card),
                columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                spacing="5",
                width="100%",
            ),
            rx.text(
                "Nenhum produto disponível nesta categoria.",
                color="#a1a1aa",
                text_align="center",
                width="100%",
                padding="32px 16px",
            ),
        ),
        width="100%",
        align="stretch",
        spacing="5",
    )


def empty_catalog_state() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.box(
                rx.text(
                    "N",
                    color="#c4b5fd",
                    font_size="25px",
                    font_weight="700",
                    text_align="center",
                    line_height="64px",
                ),
                width="64px",
                height="64px",
                background="radial-gradient(circle at 35% 30%, #31234f, #171322 72%)",
                border="1px solid rgba(167, 139, 250, 0.24)",
                border_radius="20px",
                box_shadow="0 0 48px rgba(124, 58, 237, 0.16)",
            ),
            rx.text(
                "CATÁLOGO EM PREPARAÇÃO",
                color="#e9d5ff",
                font_size="12px",
                font_weight="700",
                letter_spacing="0.12em",
                text_align="center",
            ),
            rx.text(
                "Em breve, novidades por aqui.",
                color="#a1a1aa",
                font_size="14px",
                text_align="center",
            ),
            spacing="3",
            align="center",
        ),
        width="100%",
        max_width="420px",
        padding="28px 24px",
        background="linear-gradient(145deg, rgba(24, 20, 36, 0.92), rgba(15, 14, 22, 0.96))",
        border="1px solid rgba(167, 139, 250, 0.16)",
        border_radius="24px",
        box_shadow="0 24px 80px rgba(0, 0, 0, 0.28)",
    )


def login_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.link(
                "← Voltar à loja",
                href="/",
                color="#c4b5fd",
                font_size="14px",
                font_weight="600",
                text_decoration="none",
                align_self="start",
                _hover={"color": "#f5f3ff"},
                _focus_visible={
                    "outline": "2px solid #c4b5fd",
                    "outline_offset": "4px",
                },
            ),
            rx.vstack(
                rx.box(
                    rx.text(
                        "N",
                        color="#f5f3ff",
                        font_size="18px",
                        font_weight="800",
                        text_align="center",
                        line_height="40px",
                    ),
                    width="40px",
                    height="40px",
                    background="linear-gradient(145deg, #a78bfa, #6d28d9)",
                    border="1px solid rgba(196, 181, 253, 0.35)",
                    border_radius="12px",
                    box_shadow="0 8px 28px rgba(139, 92, 246, 0.25)",
                ),
                rx.heading(
                    "Entrar",
                    size="7",
                    color="#f5f3ff",
                    text_align="center",
                    letter_spacing="-0.045em",
                ),
                rx.text(
                    "Acesse sua conta na NightFall.",
                    color="#a1a1aa",
                    font_size="14px",
                    text_align="center",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            rx.vstack(
                rx.vstack(
                    rx.text(
                        "E-mail",
                        color="#e4e4e7",
                        font_size="13px",
                        font_weight="600",
                    ),
                    rx.input(
                        type="email",
                        value=LoginState.email,
                        on_change=LoginState.set_email,
                        placeholder="voce@exemplo.com",
                        aria_label="E-mail",
                        required=True,
                        width="100%",
                        height="48px",
                        background="#11111a",
                        border="1px solid rgba(167, 139, 250, 0.24)",
                        border_radius="12px",
                        color="#f5f3ff",
                        _focus={
                            "border_color": "#a78bfa",
                            "box_shadow": "0 0 0 1px #a78bfa",
                        },
                    ),
                    spacing="2",
                    align="stretch",
                    width="100%",
                ),
                rx.vstack(
                    rx.text(
                        "Senha",
                        color="#e4e4e7",
                        font_size="13px",
                        font_weight="600",
                    ),
                    rx.input(
                        type="password",
                        value=LoginState.password,
                        on_change=LoginState.set_password,
                        placeholder="Sua senha",
                        aria_label="Senha",
                        required=True,
                        width="100%",
                        height="48px",
                        background="#11111a",
                        border="1px solid rgba(167, 139, 250, 0.24)",
                        border_radius="12px",
                        color="#f5f3ff",
                        _focus={
                            "border_color": "#a78bfa",
                            "box_shadow": "0 0 0 1px #a78bfa",
                        },
                    ),
                    spacing="2",
                    align="stretch",
                    width="100%",
                ),
                rx.button(
                    rx.cond(
                        LoginState.is_submitting,
                        "Entrando...",
                        "Entrar",
                    ),
                    type="button",
                    on_click=LoginState.login,
                    disabled=LoginState.is_submitting,
                    variant="solid",
                    color_scheme="purple",
                    width="100%",
                    height="48px",
                    border_radius="12px",
                    font_size="14px",
                    font_weight="700",
                ),
                rx.text(
                    LoginState.login_message,
                    color=rx.cond(
                        LoginState.login_succeeded,
                        "#86efac",
                        "#fca5a5",
                    ),
                    font_size="13px",
                    line_height="1.5",
                    role="status",
                    aria_live="polite",
                ),
                rx.hstack(
                    rx.text("Não tem uma conta?", color="#a1a1aa", font_size="14px"),
                    rx.link("Cadastre-se", href="/cadastro", color="#c4b5fd", font_size="14px", font_weight="600", text_decoration="none", _hover={"color": "#f5f3ff"}),
                    justify="center",
                    width="100%",
                    spacing="2",
                    margin_top="12px",
                ),
                spacing="5",
                align="stretch",
                width="100%",
            ),
            spacing="7",
            align="stretch",
            width="100%",
            max_width="420px",
            padding="32px clamp(22px, 6vw, 40px)",
            background="linear-gradient(145deg, rgba(24, 20, 36, 0.96), rgba(15, 14, 22, 0.98))",
            border="1px solid rgba(167, 139, 250, 0.18)",
            border_radius="24px",
            box_shadow="0 24px 80px rgba(0, 0, 0, 0.35)",
        ),
        min_height="100vh",
        width="100%",
        padding="24px",
        display="flex",
        align_items="center",
        justify_content="center",
        overflow_x="hidden",
        background="radial-gradient(ellipse at 50% 42%, rgba(91, 33, 182, 0.18), transparent 38%), #0b0b12",
    )


def registration_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.link(
                "← Voltar ao login",
                href="/login",
                color="#c4b5fd",
                font_size="14px",
                font_weight="600",
                text_decoration="none",
                align_self="start",
                _hover={"color": "#f5f3ff"},
                _focus_visible={
                    "outline": "2px solid #c4b5fd",
                    "outline_offset": "4px",
                },
            ),
            rx.vstack(
                rx.box(
                    rx.text(
                        "N",
                        color="#f5f3ff",
                        font_size="18px",
                        font_weight="800",
                        text_align="center",
                        line_height="40px",
                    ),
                    width="40px",
                    height="40px",
                    background="linear-gradient(145deg, #a78bfa, #6d28d9)",
                    border="1px solid rgba(196, 181, 253, 0.35)",
                    border_radius="12px",
                    box_shadow="0 8px 28px rgba(139, 92, 246, 0.25)",
                ),
                rx.heading(
                    "Crie sua conta",
                    size="7",
                    color="#f5f3ff",
                    text_align="center",
                    letter_spacing="-0.045em",
                ),
                rx.text(
                    "Cadastre-se na NightFall com suas informações.",
                    color="#a1a1aa",
                    font_size="14px",
                    text_align="center",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            rx.vstack(
                rx.vstack(
                    rx.text(
                        "Nome completo",
                        color="#e4e4e7",
                        font_size="13px",
                        font_weight="600",
                    ),
                    rx.input(
                        type="text",
                        value=RegistrationState.name,
                        on_change=RegistrationState.set_name,
                        placeholder="Seu nome completo",
                        aria_label="Nome completo",
                        required=True,
                        width="100%",
                        height="48px",
                        background="#11111a",
                        border="1px solid rgba(167, 139, 250, 0.24)",
                        border_radius="12px",
                        color="#f5f3ff",
                        _focus={
                            "border_color": "#a78bfa",
                            "box_shadow": "0 0 0 1px #a78bfa",
                        },
                    ),
                    spacing="2",
                    align="stretch",
                    width="100%",
                ),
                rx.vstack(
                    rx.text(
                        "CPF",
                        color="#e4e4e7",
                        font_size="13px",
                        font_weight="600",
                    ),
                    rx.input(
                        type="text",
                        value=RegistrationState.cpf,
                        on_change=RegistrationState.set_cpf,
                        placeholder="000.000.000-00",
                        aria_label="CPF",
                        required=True,
                        width="100%",
                        height="48px",
                        background="#11111a",
                        border="1px solid rgba(167, 139, 250, 0.24)",
                        border_radius="12px",
                        color="#f5f3ff",
                        _focus={
                            "border_color": "#a78bfa",
                            "box_shadow": "0 0 0 1px #a78bfa",
                        },
                    ),
                    spacing="2",
                    align="stretch",
                    width="100%",
                ),
                rx.vstack(
                    rx.text(
                        "Data de Nascimento",
                        color="#e4e4e7",
                        font_size="13px",
                        font_weight="600",
                    ),
                    rx.input(
                        type="date",
                        value=RegistrationState.birth_date,
                        on_change=RegistrationState.set_birth_date,
                        aria_label="Data de Nascimento",
                        required=True,
                        width="100%",
                        height="48px",
                        background="#11111a",
                        border="1px solid rgba(167, 139, 250, 0.24)",
                        border_radius="12px",
                        color="#f5f3ff",
                        _focus={
                            "border_color": "#a78bfa",
                            "box_shadow": "0 0 0 1px #a78bfa",
                        },
                    ),
                    spacing="2",
                    align="stretch",
                    width="100%",
                ),
                rx.vstack(
                    rx.text(
                        "E-mail",
                        color="#e4e4e7",
                        font_size="13px",
                        font_weight="600",
                    ),
                    rx.input(
                        type="email",
                        value=RegistrationState.email,
                        on_change=RegistrationState.set_email,
                        placeholder="voce@exemplo.com",
                        aria_label="E-mail",
                        required=True,
                        width="100%",
                        height="48px",
                        background="#11111a",
                        border="1px solid rgba(167, 139, 250, 0.24)",
                        border_radius="12px",
                        color="#f5f3ff",
                        _focus={
                            "border_color": "#a78bfa",
                            "box_shadow": "0 0 0 1px #a78bfa",
                        },
                    ),
                    spacing="2",
                    align="stretch",
                    width="100%",
                ),
                rx.vstack(
                    rx.text(
                        "Senha",
                        color="#e4e4e7",
                        font_size="13px",
                        font_weight="600",
                    ),
                    rx.input(
                        type="password",
                        value=RegistrationState.password,
                        on_change=RegistrationState.set_password,
                        placeholder="Mínimo de 8 caracteres",
                        aria_label="Senha",
                        required=True,
                        width="100%",
                        height="48px",
                        background="#11111a",
                        border="1px solid rgba(167, 139, 250, 0.24)",
                        border_radius="12px",
                        color="#f5f3ff",
                        _focus={
                            "border_color": "#a78bfa",
                            "box_shadow": "0 0 0 1px #a78bfa",
                        },
                    ),
                    spacing="2",
                    align="stretch",
                    width="100%",
                ),
                rx.button(
                    rx.cond(
                        RegistrationState.is_submitting,
                        "Criando conta...",
                        "Criar conta",
                    ),
                    type="button",
                    on_click=RegistrationState.register,
                    disabled=RegistrationState.is_submitting,
                    variant="solid",
                    color_scheme="purple",
                    width="100%",
                    height="48px",
                    border_radius="12px",
                    font_size="14px",
                    font_weight="700",
                ),
                rx.text(
                    RegistrationState.registration_message,
                    color=rx.cond(
                        RegistrationState.registration_succeeded,
                        "#86efac",
                        "#fca5a5",
                    ),
                    font_size="13px",
                    line_height="1.5",
                    role="status",
                    aria_live="polite",
                ),
                rx.hstack(
                    rx.text("Já tem uma conta?", color="#a1a1aa", font_size="14px"),
                    rx.link("Faça login", href="/login", color="#c4b5fd", font_size="14px", font_weight="600", text_decoration="none", _hover={"color": "#f5f3ff"}),
                    justify="center",
                    width="100%",
                    spacing="2",
                    margin_top="12px",
                ),
                spacing="5",
                align="stretch",
                width="100%",
            ),
            spacing="7",
            align="stretch",
            width="100%",
            max_width="420px",
            padding="32px clamp(22px, 6vw, 40px)",
            background="linear-gradient(145deg, rgba(24, 20, 36, 0.96), rgba(15, 14, 22, 0.98))",
            border="1px solid rgba(167, 139, 250, 0.18)",
            border_radius="24px",
            box_shadow="0 24px 80px rgba(0, 0, 0, 0.35)",
        ),
        min_height="100vh",
        width="100%",
        padding="24px",
        display="flex",
        align_items="center",
        justify_content="center",
        overflow_x="hidden",
        background="radial-gradient(ellipse at 50% 42%, rgba(91, 33, 182, 0.18), transparent 38%), #0b0b12",
    )


def index() -> rx.Component:
    return rx.box(
        product_details_dialog(),
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.box(
                        rx.text(
                            "N",
                            color="#f5f3ff",
                            font_size="18px",
                            font_weight="800",
                            text_align="center",
                            line_height="40px",
                        ),
                        width="40px",
                        height="40px",
                        background="linear-gradient(145deg, #a78bfa, #6d28d9)",
                        border="1px solid rgba(196, 181, 253, 0.35)",
                        border_radius="12px",
                        box_shadow="0 8px 28px rgba(139, 92, 246, 0.25)",
                    ),
                    rx.heading(
                        "NightFall",
                        size="5",
                        color="#f5f3ff",
                        letter_spacing="-0.04em",
                    ),
                    rx.link(
                        "Login",
                        href="/login",
                        color="#f5f3ff",
                        background="rgba(139, 92, 246, 0.18)",
                        border="1px solid rgba(167, 139, 250, 0.24)",
                        border_radius="999px",
                        padding_x="16px",
                        padding_y="8px",
                        font_size="13px",
                        font_weight="600",
                        text_decoration="none",
                        transition="background-color 160ms ease, border-color 160ms ease",
                        _hover={
                            "background": "rgba(139, 92, 246, 0.28)",
                            "border_color": "rgba(196, 181, 253, 0.5)",
                        },
                        _focus_visible={
                            "outline": "2px solid #c4b5fd",
                            "outline_offset": "2px",
                        },
                    ),
                    spacing="3",
                    align="center",
                ),
                rx.hstack(
                    rx.dialog.root(
                        rx.dialog.trigger(
                            rx.button(
                                "Categorias",
                                variant="soft",
                                color_scheme="purple",
                                aria_label="Abrir menu de categorias",
                            ),
                        ),
                        rx.dialog.content(
                            rx.vstack(
                                rx.hstack(
                                    rx.vstack(
                                        rx.dialog.title(
                                            "Categorias",
                                            color="#f5f3ff",
                                            font_size="24px",
                                            font_weight="700",
                                            letter_spacing="-0.025em",
                                        ),
                                        rx.dialog.description(
                                            "NIGHTFALL  /  EXPLORE POR CATEGORIA",
                                            color="#a1a1aa",
                                            font_size="11px",
                                            font_weight="600",
                                            letter_spacing="0.09em",
                                            line_height="1.6",
                                        ),
                                        align="start",
                                        spacing="3",
                                    ),
                                    rx.dialog.close(
                                        rx.button(
                                            "Fechar",
                                            variant="soft",
                                            color_scheme="gray",
                                            aria_label="Fechar menu de categorias",
                                        ),
                                    ),
                                    width="100%",
                                    justify="between",
                                    align="start",
                                    spacing="4",
                                ),
                                rx.vstack(
                                    rx.cond(
                                        CatalogState.products.length() > 0,
                                        rx.dialog.close(
                                            rx.button(
                                                "Todos os produtos",
                                                on_click=CatalogState.show_all_products,
                                                variant="ghost",
                                                color=rx.cond(
                                                    CatalogState.selected_category == "Todos",
                                                    "#f5f3ff",
                                                    "#d4d4d8",
                                                ),
                                                background=rx.cond(
                                                    CatalogState.selected_category == "Todos",
                                                    "rgba(139, 92, 246, 0.18)",
                                                    "transparent",
                                                ),
                                                border_left=rx.cond(
                                                    CatalogState.selected_category == "Todos",
                                                    "3px solid #a78bfa",
                                                    "3px solid transparent",
                                                ),
                                                aria_pressed=(
                                                    CatalogState.selected_category == "Todos"
                                                ),
                                                width="100%",
                                                min_height="52px",
                                                padding="12px 16px",
                                                justify="start",
                                                text_align="left",
                                                white_space="normal",
                                                line_height="1.4",
                                                border_radius="12px",
                                                font_size="15px",
                                                font_weight=rx.cond(
                                                    CatalogState.selected_category == "Todos",
                                                    "600",
                                                    "500",
                                                ),
                                                transition=(
                                                    "background-color 160ms ease, color 160ms ease"
                                                ),
                                                _hover={
                                                    "background": "rgba(139, 92, 246, 0.12)",
                                                    "color": "#f5f3ff",
                                                },
                                                _focus_visible={
                                                    "outline": "2px solid #c4b5fd",
                                                    "outline_offset": "2px",
                                                },
                                            ),
                                        ),
                                        rx.fragment(),
                                    ),
                                    rx.foreach(CatalogState.categories, category_item),
                                    width="100%",
                                    spacing="2",
                                    margin_top="32px",
                                ),
                                width="100%",
                                align="start",
                                spacing="5",
                            ),
                            position="fixed",
                            top="0",
                            left="0",
                            bottom="0",
                            right="auto",
                            transform="none",
                            width="min(88vw, 360px)",
                            max_width="100vw",
                            height="100vh",
                            margin="0",
                            padding="32px 24px",
                            background="#101018",
                            border="1px solid rgba(167, 139, 250, 0.2)",
                            border_radius="0 24px 24px 0",
                            box_shadow="0 0 0 100vmax rgba(3, 3, 8, 0.72), 24px 0 80px rgba(0, 0, 0, 0.45)",
                            overflow_y="auto",
                            outline="none",
                            font_family=(
                                '"Inter", "Segoe UI", ui-sans-serif, system-ui, sans-serif'
                            ),
                            visibility=rx.cond(
                                CatalogState.category_menu_open,
                                "visible",
                                "hidden",
                            ),
                            pointer_events=rx.cond(
                                CatalogState.category_menu_open,
                                "auto",
                                "none",
                            ),
                        ),
                        open=CatalogState.category_menu_open,
                        on_open_change=CatalogState.set_category_menu_open,
                    ),
                    rx.button(
                        rx.icon("shopping_cart", size=18),
                        variant="soft",
                        color_scheme="purple",
                        type="button",
                        aria_label="Carrinho de compras (apenas visual)",
                        width="40px",
                        height="40px",
                        min_width="40px",
                        padding="0",
                        flex_shrink="0",
                        _focus_visible={
                            "outline": "2px solid #c4b5fd",
                            "outline_offset": "2px",
                        },
                    ),
                    spacing="2",
                    align="center",
                    flex_shrink="0",
                ),
                spacing="3",
                align="center",
                justify="between",
                width="100%",
                flex_wrap="wrap",
            ),
            rx.spacer(),
            rx.center(
                rx.vstack(
                    rx.box(
                        width="48px",
                        height="3px",
                        background_color="#a78bfa",
                        border_radius="999px",
                        box_shadow="0 0 20px rgba(167, 139, 250, 0.75)",
                    ),
                    rx.text(
                        "NIGHTFALL  /  HARDWARE",
                        color="#c4b5fd",
                        font_size="12px",
                        font_weight="700",
                        letter_spacing="0.16em",
                    ),
                    rx.heading(
                        "Tecnologia para ir além.",
                        size="8",
                        color="#f5f3ff",
                        text_align="center",
                        letter_spacing="-0.055em",
                        line_height="1.08",
                    ),
                    rx.text(
                        "Estamos preparando uma nova experiência para quem vive tecnologia.",
                        color="#a1a1aa",
                        font_size="16px",
                        line_height="1.7",
                        text_align="center",
                        max_width="520px",
                    ),
                    rx.cond(
                        CatalogState.products.length() > 0,
                        product_catalog(),
                        empty_catalog_state(),
                    ),
                    spacing="6",
                    align="center",
                    width="100%",
                ),
                width="100%",
                flex="1",
            ),
            rx.text(
                "NIGHTFALL",
                color="#52525b",
                font_size="11px",
                font_weight="600",
                letter_spacing="0.2em",
            ),
            min_height="100vh",
            width="100%",
            max_width="1120px",
            margin_x="auto",
            padding="28px clamp(20px, 5vw, 64px) 24px",
            align="center",
        ),
        min_height="100vh",
        width="100%",
        overflow_x="hidden",
        background="radial-gradient(ellipse at 50% 42%, rgba(91, 33, 182, 0.18), transparent 38%), radial-gradient(ellipse at 12% 8%, rgba(76, 29, 149, 0.12), transparent 28%), #0b0b12",
    )


app = rx.App()
app.add_page(index, route="/")
app.add_page(login_page, route="/login", title="Entrar | NightFall")
app.add_page(registration_page, route="/cadastro", title="Criar conta | NightFall")
