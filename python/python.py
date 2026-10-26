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
DEFAULT_XANO_PRODUCTS_URL = "https://x8ki-letl-twmt.n7.xano.io/api:nightfall-auth/produto"


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


class CartItem(TypedDict):
    name: str
    image_url: str
    price: float
    price_display: str
    quantity: int


def parse_catalog_data(data: list[Any]) -> list[Product]:
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


def load_catalog(path: Path = CATALOG_PATH) -> list[Product]:
    products_url = os.getenv("XANO_PRODUCTS_URL", DEFAULT_XANO_PRODUCTS_URL).strip()
    if products_url:
        try:
            response = httpx.get(products_url, timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                parsed = parse_catalog_data(data)
                if parsed:
                    return parsed
        except Exception:
            pass

    with path.open(encoding="utf-8") as catalog_file:
        data = json.load(catalog_file)
    return parse_catalog_data(data)


class CatalogState(rx.State):
    products: list[Product] = load_catalog()
    selected_category: str = "Todos"
    search_query: str = ""
    category_menu_open: bool = False
    product_details_open: bool = False
    selected_product_name: str = ""
    selected_product_image_url: str = ""
    selected_product_price_display: str = ""
    selected_product_description: str = ""
    selected_product_category: str = ""
    selected_product_specifications: list[Specification] = []

    min_price: str = ""
    max_price: str = ""
    selected_brand: str = "Todas"

    cart_items: list[CartItem] = []
    cart_open: bool = False

    @rx.event
    def set_cart_open(self, is_open: bool):
        self.cart_open = is_open

    @rx.event
    def add_to_cart(self, product_name: str):
        product = next(
            (item for item in self.products if item["name"] == product_name),
            None,
        )
        if product is None:
            return

        existing = next(
            (item for item in self.cart_items if item["name"] == product_name),
            None,
        )
        if existing:
            existing["quantity"] += 1
            self.cart_items = list(self.cart_items)
        else:
            self.cart_items = list(self.cart_items) + [{
                "name": product["name"],
                "image_url": product["image_url"],
                "price": product["price"],
                "price_display": product["price_display"],
                "quantity": 1,
            }]
        self.cart_open = True

    @rx.event
    def remove_from_cart(self, product_name: str):
        self.cart_items = [item for item in self.cart_items if item["name"] != product_name]

    @rx.event
    def update_quantity(self, product_name: str, delta: int):
        new_items = []
        for item in self.cart_items:
            if item["name"] == product_name:
                q = item["quantity"] + delta
                if q > 0:
                    item["quantity"] = q
                    new_items.append(item)
            else:
                new_items.append(item)
        self.cart_items = new_items

    @rx.event
    def clear_cart(self):
        self.cart_items = []

    @rx.var
    def cart_count(self) -> int:
        return sum(item["quantity"] for item in self.cart_items)

    @rx.var
    def cart_total(self) -> float:
        return sum(item["price"] * item["quantity"] for item in self.cart_items)

    @rx.var
    def cart_total_display(self) -> str:
        total = self.cart_total
        formatted = f"{Decimal(str(total)):,.2f}"
        formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {formatted}"

    coupon_code: str = ""
    discount_amount: float = 0.0
    coupon_message: str = ""
    coupon_applied: bool = False

    @rx.event
    def set_coupon_code(self, code: str):
        self.coupon_code = code

    @rx.event
    def apply_coupon(self):
        code = self.coupon_code.strip().upper()
        if code == "NIGHTFALL10":
            subtotal = sum(item["price"] * item["quantity"] for item in self.cart_items)
            self.discount_amount = subtotal * 0.10
            self.coupon_applied = True
            self.coupon_message = "Cupom NIGHTFALL10 aplicado (10% OFF)!"
        else:
            self.discount_amount = 0.0
            self.coupon_applied = False
            self.coupon_message = "Cupom inválido."

    @rx.event
    def remove_coupon(self):
        self.coupon_code = ""
        self.discount_amount = 0.0
        self.coupon_applied = False
        self.coupon_message = ""

    @rx.var
    def cart_discount_display(self) -> str:
        formatted = f"{Decimal(str(self.discount_amount)):,.2f}"
        formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"- R$ {formatted}"

    @rx.var
    def shipping_cost(self) -> float:
        subtotal = sum(item["price"] * item["quantity"] for item in self.cart_items)
        if subtotal >= 250.0 or subtotal == 0:
            return 0.0
        return 15.0

    @rx.var
    def shipping_display(self) -> str:
        cost = self.shipping_cost
        if cost == 0.0:
            return "Grátis"
        formatted = f"{Decimal(str(cost)):,.2f}"
        formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {formatted}"

    @rx.var
    def cart_final_total(self) -> float:
        subtotal = sum(item["price"] * item["quantity"] for item in self.cart_items)
        return max(0.0, subtotal - self.discount_amount + self.shipping_cost)

    @rx.var
    def cart_final_total_display(self) -> str:
        total = self.cart_final_total
        formatted = f"{Decimal(str(total)):,.2f}"
        formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {formatted}"

    @rx.event
    def set_min_price(self, value: str):
        self.min_price = value

    @rx.event
    def set_max_price(self, value: str):
        self.max_price = value

    @rx.event
    def set_selected_brand(self, value: str):
        self.selected_brand = value

    shipping_cep: str = ""
    shipping_address: str = ""
    shipping_number: str = ""
    shipping_complement: str = ""
    shipping_neighborhood: str = ""
    shipping_city: str = ""
    shipping_state: str = ""
    payment_method: str = "credit_card"
    card_number: str = ""
    card_name: str = ""
    card_expiry: str = ""
    card_cvv: str = ""
    order_success: bool = False
    order_id: str = ""

    @rx.event
    async def proceed_to_checkout(self):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_logged_in:
            auth_state.redirect_after_login = "/pagamento"
            return rx.redirect("/login")
        return rx.redirect("/pagamento")

    @rx.event
    async def set_shipping_cep(self, val: str):
        digits = "".join(filter(str.isdigit, val))[:8]
        if len(digits) <= 5:
            self.shipping_cep = digits
        else:
            self.shipping_cep = f"{digits[:5]}-{digits[5:]}"

        if len(digits) == 8:
            try:
                url = f"https://viacep.com.br/ws/{digits}/json/"
                response = httpx.get(url, timeout=3.0)
                if response.status_code == 200:
                    data = response.json()
                    if not data.get("erro"):
                        self.shipping_address = data.get("logradouro", "")
                        self.shipping_neighborhood = data.get("bairro", "")
                        self.shipping_city = data.get("localidade", "")
                        self.shipping_state = data.get("uf", "")
            except Exception:
                pass

    @rx.event
    def set_shipping_address(self, val: str):
        self.shipping_address = val

    @rx.event
    def set_shipping_number(self, val: str):
        self.shipping_number = "".join(filter(str.isdigit, val))

    @rx.event
    def set_shipping_complement(self, val: str):
        self.shipping_complement = val

    @rx.event
    def set_shipping_neighborhood(self, val: str):
        self.shipping_neighborhood = val

    @rx.event
    def set_shipping_city(self, val: str):
        self.shipping_city = val

    @rx.event
    def set_shipping_state(self, val: str):
        self.shipping_state = val

    @rx.event
    def set_payment_method(self, val: str):
        self.payment_method = val

    @rx.event
    def set_card_number(self, val: str):
        self.card_number = val

    @rx.event
    def set_card_name(self, val: str):
        self.card_name = val

    @rx.event
    def set_card_expiry(self, val: str):
        self.card_expiry = val

    @rx.event
    def set_card_cvv(self, val: str):
        self.card_cvv = val

    @rx.event
    def finalize_order(self):
        import random
        self.order_id = f"#NF-{random.randint(10000, 99999)}"
        self.order_success = True
        self.cart_items = []

    @rx.event
    def clear_filters(self):
        self.selected_category = "Todos"
        self.search_query = ""
        self.min_price = ""
        self.max_price = ""
        self.selected_brand = "Todas"
        self.category_menu_open = False

    @rx.event
    def show_all_products(self):
        self.selected_category = "Todos"
        self.search_query = ""
        self.category_menu_open = False

    @rx.event
    def select_category(self, category: str):
        self.selected_category = category
        self.category_menu_open = False

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

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
        prods = self.products
        if self.selected_category != "Todos":
            prods = [p for p in prods if p["category"] == self.selected_category]

        # Filtro por faixa de preço
        min_price = self.min_price.strip()
        max_price = self.max_price.strip()
        if min_price or max_price:
            try:
                min_val = float(min_price) if min_price else 0
                max_val = float(max_price) if max_price else float("inf")
                prods = [
                    p for p in prods
                    if min_val <= p["price"] <= max_val
                ]
            except ValueError:
                pass

        # Filtro por marca/especificações
        selected_brand = self.selected_brand.strip()
        if selected_brand and selected_brand != "Todas":
            prods = [
                p for p in prods
                if any(spec["value"].lower() == selected_brand.lower()
                       for spec in p["specifications"])
            ]

        q = self.search_query.strip().lower()
        if not q:
            return prods

        filtered = []
        for product in prods:
            searchable_text = " ".join(
                [product["name"], product["description"], product["category"]]
                + [
                    f"{specification['label']} {specification['value']}"
                    for specification in product["specifications"]
                ]
            ).lower()
            if q in searchable_text:
                filtered.append(product)
        return filtered

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

    @rx.var
    def brands(self) -> list[str]:
        seen: set[str] = set()
        brands: list[str] = []
        for product in self.products:
            for specification in product["specifications"]:
                if specification["label"].lower() == "marca":
                    brand = specification["value"].strip()
                    if brand and brand not in seen:
                        seen.add(brand)
                        brands.append(brand)
        return sorted(brands)


class AuthState(rx.State):
    is_logged_in: bool = False
    user_name: str = ""
    user_email: str = ""
    user_phone: str = "(11) 98888-7777"
    user_cpf: str = ""
    user_birth_date: str = ""
    profile_message: str = ""
    profile_tab: str = "dados"
    redirect_after_login: str = ""
    logout_dialog_open: bool = False

    @rx.event
    def set_profile_tab(self, tab: str):
        self.profile_tab = tab

    @rx.event
    def set_user_phone(self, phone: str):
        self.user_phone = phone
        self.profile_message = ""

    @rx.event
    def set_user_cpf(self, value: str):
        self.user_cpf = format_cpf(value)
        self.profile_message = ""

    @rx.event
    def set_user_birth_date(self, value: str):
        self.user_birth_date = value
        self.profile_message = ""

    @rx.event
    def update_profile(self, name: str):
        if name.strip():
            self.user_name = name.strip()
            self.profile_message = "Perfil atualizado com sucesso!"
        else:
            self.profile_message = "Informe um nome válido."

    @rx.event
    def set_logout_dialog_open(self, is_open: bool):
        self.logout_dialog_open = is_open

    @rx.event
    def confirm_logout(self):
        self.is_logged_in = False
        self.user_name = ""
        self.user_email = ""
        self.logout_dialog_open = False
        return rx.redirect("/")


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

                # Atualiza o estado de autenticação global e redireciona
                auth_state = await self.get_state(AuthState)
                auth_state.is_logged_in = True
                auth_state.user_email = email
                name_part = email.split("@")[0]
                auth_state.user_name = name_part.capitalize()

                target = auth_state.redirect_after_login if auth_state.redirect_after_login else "/"
                auth_state.redirect_after_login = ""

                # Limpa os campos de login para que da próxima vez venham limpos
                self.email = ""
                self.password = ""

                return rx.redirect(target)
            else:
                self.login_message = "Credenciais inválidas. Verifique seu e-mail e senha."
        except Exception:
            self.login_message = "Erro ao conectar com o serviço de autenticação."
        finally:
            self.is_submitting = False


def validate_cpf(cpf: str) -> bool:
    digits = "".join(filter(str.isdigit, cpf))
    if len(digits) != 11:
        return False
    if digits == digits[0] * 11:
        return False

    s = sum(int(digits[i]) * (10 - i) for i in range(9))
    digit1 = (s * 10) % 11
    if digit1 == 10:
        digit1 = 0
    if digit1 != int(digits[9]):
        return False

    s = sum(int(digits[i]) * (11 - i) for i in range(10))
    digit2 = (s * 10) % 11
    if digit2 == 10:
        digit2 = 0
    if digit2 != int(digits[10]):
        return False

    return True


def format_cpf(value: str) -> str:
    digits = "".join(filter(str.isdigit, value))[:11]
    if len(digits) <= 3:
        return digits
    elif len(digits) <= 6:
        return f"{digits[:3]}.{digits[3:]}"
    elif len(digits) <= 9:
        return f"{digits[:3]}.{digits[3:6]}.{digits[6:]}"
    else:
        return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"


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
        self.cpf = format_cpf(value)
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
        cpf = "".join(filter(str.isdigit, self.cpf))
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

        if not validate_cpf(cpf):
            self.registration_message = "CPF inválido. Verifique o número informado."
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
                self.registration_message = (
                    "Conta criada com sucesso. A verificação por e-mail ainda não está "
                    "disponível; não foi enviado nenhum código."
                )
                self.registration_succeeded = True
            else:
                self.registration_message = "O Xano não confirmou a criação da conta."
        finally:
            self.password = ""
            self.is_submitting = False


def category_item(category: rx.Var[Any]) -> rx.Component:
    return rx.cond(
        category["available"],
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
            min_height="48px",
            padding="10px 14px",
            justify="start",
            text_align="left",
            white_space="normal",
            line_height="1.4",
            border_radius="10px",
            font_size="14px",
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
        rx.hstack(
            rx.text(
                category["name"],
                color="#a1a1aa",
                font_size="14px",
                font_weight="500",
                line_height="1.4",
            ),
            rx.badge("Em breve", color_scheme="purple", variant="soft"),
            width="100%",
            min_height="48px",
            justify="between",
            align="center",
            padding="10px 14px",
            border_radius="10px",
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
        width="340px",
        flex="1 1 320px",
        max_width="420px",
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
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        _hover={
            "border": "1px solid rgba(196, 181, 253, 0.65)",
            "background": "linear-gradient(145deg, rgba(30, 24, 48, 0.95), rgba(20, 18, 30, 0.98))",
            "box_shadow": "0 28px 90px rgba(124, 58, 237, 0.35), 0 0 20px rgba(196, 181, 253, 0.2)",
            "transform": "translateY(-4px)",
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
                rx.button(
                    "Adicionar ao carrinho",
                    on_click=CatalogState.add_to_cart(CatalogState.selected_product_name),
                    color_scheme="purple",
                    size="3",
                    width="100%",
                    font_weight="700",
                    margin_top="8px",
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


def cart_item_row(item: rx.Var[CartItem]) -> rx.Component:
    return rx.hstack(
        rx.image(
            src=item["image_url"],
            alt=item["name"],
            width="60px",
            height="60px",
            object_fit="contain",
            background="#0b0b12",
            border_radius="10px",
        ),
        rx.vstack(
            rx.text(item["name"], color="#f5f3ff", font_size="14px", font_weight="600"),
            rx.text(item["price_display"], color="#e9d5ff", font_size="13px", font_weight="700"),
            rx.hstack(
                rx.button(
                    "-",
                    on_click=CatalogState.update_quantity(item["name"], -1),
                    size="1",
                    variant="soft",
                    color_scheme="purple",
                ),
                rx.text(item["quantity"], color="#f5f3ff", font_size="13px", font_weight="600"),
                rx.button(
                    "+",
                    on_click=CatalogState.update_quantity(item["name"], 1),
                    size="1",
                    variant="soft",
                    color_scheme="purple",
                ),
                spacing="2",
                align="center",
            ),
            spacing="1",
            align="start",
            flex="1",
        ),
        rx.button(
            rx.icon("trash", size=16),
            on_click=CatalogState.remove_from_cart(item["name"]),
            variant="ghost",
            color_scheme="red",
            size="1",
            aria_label="Remover item",
        ),
        width="100%",
        align="center",
        justify="between",
        padding_y="12px",
        border_bottom="1px solid rgba(167, 139, 250, 0.12)",
    )


def cart_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.link(
                    "← Voltar à loja",
                    href="/",
                    color="#c4b5fd",
                    font_size="14px",
                    font_weight="600",
                    text_decoration="none",
                    _hover={"color": "#f5f3ff"},
                ),
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
                    spacing="3",
                    align="center",
                ),
                width="100%",
                justify="between",
                align="center",
                padding_bottom="24px",
                border_bottom="1px solid rgba(167, 139, 250, 0.16)",
            ),
            # Content
            rx.vstack(
                rx.heading(
                    "Carrinho de Compras",
                    size="7",
                    color="#f5f3ff",
                    letter_spacing="-0.03em",
                    margin_y="16px",
                ),
                rx.cond(
                    CatalogState.cart_items.length() > 0,
                    rx.flex(
                        # Left: Items list
                        rx.vstack(
                            rx.foreach(CatalogState.cart_items, cart_item_row),
                            width="100%",
                            flex="2",
                            spacing="3",
                        ),
                        # Right: Summary card
                        rx.vstack(
                            rx.heading("Resumo do Pedido", size="5", color="#f5f3ff"),
                            rx.divider(border_color="rgba(167, 139, 250, 0.2)"),
                            rx.hstack(
                                rx.text("Subtotal", color="#a1a1aa", font_size="14px"),
                                rx.text(CatalogState.cart_total_display, color="#f5f3ff", font_size="15px", font_weight="600"),
                                width="100%",
                                justify="between",
                            ),
                            rx.cond(
                                CatalogState.coupon_applied,
                                rx.hstack(
                                    rx.text("Desconto (NIGHTFALL10)", color="#4ade80", font_size="14px"),
                                    rx.text(CatalogState.cart_discount_display, color="#4ade80", font_size="15px", font_weight="600"),
                                    width="100%",
                                    justify="between",
                                ),
                                rx.fragment(),
                            ),
                            rx.hstack(
                                rx.text("Frete", color="#a1a1aa", font_size="14px"),
                                rx.text(CatalogState.shipping_display, color="#f5f3ff", font_size="15px", font_weight="600"),
                                width="100%",
                                justify="between",
                            ),
                            rx.divider(border_color="rgba(167, 139, 250, 0.2)"),
                            rx.hstack(
                                rx.text("Total", color="#f5f3ff", font_size="16px", font_weight="700"),
                                rx.text(CatalogState.cart_final_total_display, color="#e9d5ff", font_size="20px", font_weight="800"),
                                width="100%",
                                justify="between",
                            ),
                            # Coupon Section
                            rx.vstack(
                                rx.text("Cupom de Desconto", color="#e4e4e7", font_size="13px", font_weight="600"),
                                rx.hstack(
                                    rx.input(
                                        placeholder="Ex: NIGHTFALL10",
                                        value=CatalogState.coupon_code,
                                        on_change=CatalogState.set_coupon_code,
                                        width="100%",
                                        height="42px",
                                        background="#11111a",
                                        border="1px solid rgba(167, 139, 250, 0.24)",
                                        border_radius="10px",
                                        color="#f5f3ff",
                                    ),
                                    rx.button(
                                        "Aplicar",
                                        on_click=CatalogState.apply_coupon,
                                        color_scheme="purple",
                                        height="42px",
                                        font_weight="600",
                                    ),
                                    width="100%",
                                    spacing="2",
                                ),
                                rx.cond(
                                    CatalogState.coupon_message != "",
                                    rx.text(
                                        CatalogState.coupon_message,
                                        color=rx.cond(CatalogState.coupon_applied, "#4ade80", "#f87171"),
                                        font_size="12px",
                                    ),
                                    rx.fragment(),
                                ),
                                width="100%",
                                spacing="2",
                                align="start",
                                margin_y="8px",
                            ),
                            rx.button(
                                "Ir para o Pagamento",
                                on_click=CatalogState.proceed_to_checkout,
                                color_scheme="purple",
                                size="3",
                                width="100%",
                                font_weight="700",
                                margin_top="12px",
                            ),
                            rx.button(
                                "Esvaziar Carrinho",
                                on_click=CatalogState.clear_cart,
                                variant="soft",
                                color_scheme="gray",
                                size="2",
                                width="100%",
                            ),
                            width="100%",
                            flex="1",
                            min_width="320px",
                            padding="24px",
                            background="linear-gradient(145deg, rgba(24, 20, 36, 0.96), rgba(15, 14, 22, 0.98))",
                            border="1px solid rgba(167, 139, 250, 0.18)",
                            border_radius="24px",
                            spacing="4",
                        ),
                        direction="row",
                        wrap="wrap",
                        spacing="6",
                        width="100%",
                        align="start",
                    ),
                    rx.vstack(
                        rx.text(
                            "Seu carrinho está vazio.",
                            color="#a1a1aa",
                            font_size="16px",
                            text_align="center",
                        ),
                        rx.link(
                            rx.button(
                                "Explorar Catálogo",
                                color_scheme="purple",
                                size="3",
                                font_weight="700",
                            ),
                            href="/",
                            text_decoration="none",
                        ),
                        width="100%",
                        align="center",
                        spacing="4",
                        padding="60px 0",
                    ),
                ),
                width="100%",
                align="stretch",
                spacing="5",
            ),
            width="100%",
            max_width="1120px",
            margin_x="auto",
            padding="28px clamp(20px, 5vw, 64px) 24px",
            align="stretch",
        ),
        min_height="100vh",
        width="100%",
        overflow_x="hidden",
        background="radial-gradient(ellipse at 50% 42%, rgba(91, 33, 182, 0.18), transparent 38%), radial-gradient(ellipse at 12% 8%, rgba(76, 29, 149, 0.12), transparent 28%), #0b0b12",
    )


def product_catalog() -> rx.Component:
    return rx.vstack(
        # Barra de pesquisa no topo, expansiva no foco
        rx.input(
            placeholder="Pesquisar produtos, marcas ou especificações...",
            value=CatalogState.search_query,
            on_change=CatalogState.set_search_query,
            width="100%",
            height="52px",
            background="#11111a",
            border="1px solid rgba(167, 139, 250, 0.3)",
            border_radius="14px",
            color="#f5f3ff",
            font_size="15px",
            padding_x="18px",
            transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
            _focus={
                "border_color": "#a78bfa",
                "box_shadow": "0 0 0 2px rgba(167, 139, 250, 0.4), 0 12px 40px rgba(139, 92, 246, 0.3)",
                "transform": "scale(1.01)",
            },
            aria_label="Pesquisar produtos",
        ),
        # Cabeçalho da seção com o título e categoria selecionada
        rx.hstack(
            rx.heading(
                rx.cond(
                    CatalogState.selected_category == "Todos",
                    "Todos os Produtos",
                    CatalogState.selected_category,
                ),
                size="6",
                color="#f5f3ff",
            ),
            rx.button(
                "Todos os produtos",
                on_click=CatalogState.show_all_products,
                variant="soft",
                color_scheme="purple",
                size="2",
            ),
            width="100%",
            justify="between",
            align="center",
            margin_y="4px",
        ),
        # Grid de produtos
        rx.cond(
            CatalogState.filtered_products.length() > 0,
            rx.flex(
                rx.foreach(CatalogState.filtered_products, product_card),
                direction="row",
                wrap="wrap",
                spacing="5",
                width="100%",
            ),
            rx.text(
                rx.cond(
                    CatalogState.search_query.strip() != "",
                    "Nenhum produto encontrado para essa pesquisa.",
                    "Nenhum produto disponível nesta categoria.",
                ),
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
    return rx.center(
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
                        max_length=11,
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
                rx.cond(
                    RegistrationState.registration_message != "",
                    rx.box(
                        rx.hstack(
                            rx.text(
                                rx.cond(RegistrationState.registration_succeeded, "✓", "⚠"),
                                color=rx.cond(RegistrationState.registration_succeeded, "#4ade80", "#f87171"),
                                font_weight="700",
                            ),
                            rx.text(
                                RegistrationState.registration_message,
                                color=rx.cond(RegistrationState.registration_succeeded, "#86efac", "#fca5a5"),
                                font_size="13px",
                                font_weight="600",
                                line_height="1.5",
                            ),
                            spacing="2",
                            align="center",
                        ),
                        padding="12px 16px",
                        background=rx.cond(
                            RegistrationState.registration_succeeded,
                            "rgba(34, 197, 94, 0.1)",
                            "rgba(239, 68, 68, 0.12)",
                        ),
                        border=rx.cond(
                            RegistrationState.registration_succeeded,
                            "1px solid rgba(74, 222, 128, 0.3)",
                            "1px solid rgba(248, 113, 113, 0.35)",
                        ),
                        border_radius="12px",
                        width="100%",
                        role="status",
                        aria_live="polite",
                    ),
                    rx.fragment(),
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
                    rx.cond(
                        AuthState.is_logged_in,
                        rx.hstack(
                            rx.link(
                                rx.text(
                                    AuthState.user_name,
                                    color="#f5f3ff",
                                    font_size="13px",
                                    font_weight="600",
                                ),
                                href="/perfil",
                                text_decoration="none",
                                _hover={"color": "#c4b5fd"},
                            ),
                            rx.button(
                                "Sair",
                                on_click=AuthState.set_logout_dialog_open(True),
                                variant="soft",
                                color_scheme="gray",
                                size="1",
                                cursor="pointer",
                            ),
                            rx.dialog.root(
                                rx.dialog.content(
                                    rx.vstack(
                                        rx.dialog.title("Confirmar Saída", color="#f5f3ff"),
                                        rx.dialog.description(
                                            "Tem certeza que deseja fazer o logout da sua conta?",
                                            color="#a1a1aa",
                                        ),
                                        rx.hstack(
                                            rx.dialog.close(
                                                rx.button(
                                                    "Cancelar",
                                                    variant="soft",
                                                    color_scheme="gray",
                                                    on_click=AuthState.set_logout_dialog_open(False),
                                                ),
                                            ),
                                            rx.button(
                                                "Sim, sair",
                                                color_scheme="red",
                                                on_click=AuthState.confirm_logout,
                                            ),
                                            spacing="3",
                                            justify="end",
                                            width="100%",
                                            margin_top="16px",
                                        ),
                                        spacing="4",
                                        align="start",
                                        width="100%",
                                    ),
                                    background="#101018",
                                    border="1px solid rgba(167, 139, 250, 0.2)",
                                    border_radius="20px",
                                    padding="24px",
                                    max_width="400px",
                                ),
                                open=AuthState.logout_dialog_open,
                                on_open_change=AuthState.set_logout_dialog_open,
                            ),
                            spacing="2",
                            align="center",
                            background="rgba(139, 92, 246, 0.18)",
                            border="1px solid rgba(167, 139, 250, 0.24)",
                            border_radius="999px",
                            padding_x="14px",
                            padding_y="6px",
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
                        rx.hstack(
                            rx.icon("shopping_cart", size=18),
                            rx.cond(
                                CatalogState.cart_count > 0,
                                rx.badge(
                                    CatalogState.cart_count,
                                    color_scheme="purple",
                                    variant="solid",
                                    size="1",
                                ),
                                rx.fragment(),
                            ),
                            spacing="2",
                            align="center",
                        ),
                        on_click=rx.redirect("/carrinho"),
                        variant="soft",
                        color_scheme="purple",
                        type="button",
                        aria_label="Carrinho de compras",
                        height="40px",
                        min_width="40px",
                        padding_x="12px",
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


def checkout_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.link(
                    "← Voltar ao Carrinho",
                    href="/carrinho",
                    color="#c4b5fd",
                    font_size="14px",
                    font_weight="600",
                    text_decoration="none",
                    _hover={"color": "#f5f3ff"},
                ),
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
                        "NightFall Checkout",
                        size="5",
                        color="#f5f3ff",
                        letter_spacing="-0.04em",
                    ),
                    spacing="3",
                    align="center",
                ),
                width="100%",
                justify="between",
                align="center",
                padding_bottom="24px",
                border_bottom="1px solid rgba(167, 139, 250, 0.16)",
            ),
            # Content / Auth Guard & Success cond
            rx.cond(
                AuthState.is_logged_in,
                rx.cond(
                    CatalogState.order_success,
                    # Success View
                    rx.vstack(
                        rx.box(
                            rx.icon("circle_check", size=48, color="#4ade80"),
                            padding="16px",
                            background="rgba(74, 222, 128, 0.1)",
                            border_radius="50%",
                            border="1px solid rgba(74, 222, 128, 0.3)",
                        ),
                        rx.heading("Pedido Realizado com Sucesso!", size="7", color="#f5f3ff"),
                        rx.text(
                            f"Número do Pedido: {CatalogState.order_id}",
                            color="#a78bfa",
                            font_size="16px",
                            font_weight="700",
                        ),
                        rx.text(
                            "Obrigado por comprar na NightFall! Seu pedido está sendo processado e enviado para o seu endereço.",
                            color="#a1a1aa",
                            font_size="14px",
                            text_align="center",
                            max_width="480px",
                        ),
                        rx.link(
                            rx.button(
                                "Voltar para a Loja",
                                color_scheme="purple",
                                size="3",
                                font_weight="700",
                            ),
                            href="/",
                            text_decoration="none",
                            margin_top="16px",
                        ),
                        width="100%",
                        align="center",
                        spacing="4",
                        padding="60px 24px",
                        background="linear-gradient(145deg, rgba(24, 20, 36, 0.96), rgba(15, 14, 22, 0.98))",
                        border="1px solid rgba(167, 139, 250, 0.18)",
                        border_radius="24px",
                    ),
                    # Checkout Form & Summary View
                    rx.flex(
                    # Left: Form (Address & Payment)
                    rx.vstack(
                        rx.heading("Endereço de Entrega", size="5", color="#f5f3ff"),
                        rx.flex(
                            rx.vstack(
                                rx.text("CEP", color="#e4e4e7", font_size="13px", font_weight="600"),
                                rx.input(
                                    placeholder="00000-000",
                                    value=CatalogState.shipping_cep,
                                    on_change=CatalogState.set_shipping_cep,
                                    width="100%",
                                    height="42px",
                                    background="#11111a",
                                    border="1px solid rgba(167, 139, 250, 0.24)",
                                    border_radius="10px",
                                    color="#f5f3ff",
                                ),
                                width="100%",
                                flex="1",
                                spacing="2",
                                align="start",
                            ),
                            rx.vstack(
                                rx.text("Estado (UF)", color="#e4e4e7", font_size="13px", font_weight="600"),
                                rx.input(
                                    placeholder="SP",
                                    value=CatalogState.shipping_state,
                                    on_change=CatalogState.set_shipping_state,
                                    width="100%",
                                    height="42px",
                                    background="#11111a",
                                    border="1px solid rgba(167, 139, 250, 0.24)",
                                    border_radius="10px",
                                    color="#f5f3ff",
                                ),
                                width="120px",
                                spacing="2",
                                align="start",
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        rx.flex(
                            rx.vstack(
                                rx.text("Endereço / Rua", color="#e4e4e7", font_size="13px", font_weight="600"),
                                rx.input(
                                    placeholder="Ex: Av. Paulista",
                                    value=CatalogState.shipping_address,
                                    on_change=CatalogState.set_shipping_address,
                                    width="100%",
                                    height="42px",
                                    background="#11111a",
                                    border="1px solid rgba(167, 139, 250, 0.24)",
                                    border_radius="10px",
                                    color="#f5f3ff",
                                ),
                                width="100%",
                                flex="3",
                                spacing="2",
                                align="start",
                            ),
                            rx.vstack(
                                rx.text("Número", color="#e4e4e7", font_size="13px", font_weight="600"),
                                rx.input(
                                    placeholder="1000",
                                    value=CatalogState.shipping_number,
                                    on_change=CatalogState.set_shipping_number,
                                    width="100%",
                                    height="42px",
                                    background="#11111a",
                                    border="1px solid rgba(167, 139, 250, 0.24)",
                                    border_radius="10px",
                                    color="#f5f3ff",
                                ),
                                width="120px",
                                spacing="2",
                                align="start",
                            ),
                            rx.vstack(
                                rx.text("Complemento", color="#e4e4e7", font_size="13px", font_weight="600"),
                                rx.input(
                                    placeholder="Apto, Bloco, etc.",
                                    value=CatalogState.shipping_complement,
                                    on_change=CatalogState.set_shipping_complement,
                                    width="100%",
                                    height="42px",
                                    background="#11111a",
                                    border="1px solid rgba(167, 139, 250, 0.24)",
                                    border_radius="10px",
                                    color="#f5f3ff",
                                ),
                                width="100%",
                                flex="1",
                                spacing="2",
                                align="start",
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        rx.flex(
                            rx.vstack(
                                rx.text("Bairro", color="#e4e4e7", font_size="13px", font_weight="600"),
                                rx.input(
                                    placeholder="Bairro",
                                    value=CatalogState.shipping_neighborhood,
                                    on_change=CatalogState.set_shipping_neighborhood,
                                    width="100%",
                                    height="42px",
                                    background="#11111a",
                                    border="1px solid rgba(167, 139, 250, 0.24)",
                                    border_radius="10px",
                                    color="#f5f3ff",
                                ),
                                width="100%",
                                flex="1",
                                spacing="2",
                                align="start",
                            ),
                            rx.vstack(
                                rx.text("Cidade", color="#e4e4e7", font_size="13px", font_weight="600"),
                                rx.input(
                                    placeholder="Cidade",
                                    value=CatalogState.shipping_city,
                                    on_change=CatalogState.set_shipping_city,
                                    width="100%",
                                    height="42px",
                                    background="#11111a",
                                    border="1px solid rgba(167, 139, 250, 0.24)",
                                    border_radius="10px",
                                    color="#f5f3ff",
                                ),
                                width="100%",
                                flex="1",
                                spacing="2",
                                align="start",
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        rx.divider(border_color="rgba(167, 139, 250, 0.16)", margin_y="8px"),
                        rx.heading("Forma de Pagamento", size="5", color="#f5f3ff"),
                        rx.hstack(
                            rx.button(
                                "Cartão de Crédito",
                                on_click=CatalogState.set_payment_method("credit_card"),
                                variant=rx.cond(CatalogState.payment_method == "credit_card", "solid", "soft"),
                                color_scheme="purple",
                                flex="1",
                            ),
                            rx.button(
                                "Pix",
                                on_click=CatalogState.set_payment_method("pix"),
                                variant=rx.cond(CatalogState.payment_method == "pix", "solid", "soft"),
                                color_scheme="purple",
                                flex="1",
                            ),
                            rx.button(
                                "Boleto",
                                on_click=CatalogState.set_payment_method("boleto"),
                                variant=rx.cond(CatalogState.payment_method == "boleto", "solid", "soft"),
                                color_scheme="purple",
                                flex="1",
                            ),
                            width="100%",
                            spacing="3",
                        ),
                        # Conditional Payment Inputs
                        rx.cond(
                            CatalogState.payment_method == "credit_card",
                            rx.vstack(
                                rx.vstack(
                                    rx.text("Número do Cartão", color="#e4e4e7", font_size="13px", font_weight="600"),
                                    rx.input(
                                        placeholder="0000 0000 0000 0000",
                                        value=CatalogState.card_number,
                                        on_change=CatalogState.set_card_number,
                                        width="100%",
                                        height="42px",
                                        background="#11111a",
                                        border="1px solid rgba(167, 139, 250, 0.24)",
                                        border_radius="10px",
                                        color="#f5f3ff",
                                    ),
                                    width="100%",
                                    spacing="2",
                                    align="start",
                                ),
                                rx.vstack(
                                    rx.text("Nome no Cartão", color="#e4e4e7", font_size="13px", font_weight="600"),
                                    rx.input(
                                        placeholder="Nome como impresso no cartão",
                                        value=CatalogState.card_name,
                                        on_change=CatalogState.set_card_name,
                                        width="100%",
                                        height="42px",
                                        background="#11111a",
                                        border="1px solid rgba(167, 139, 250, 0.24)",
                                        border_radius="10px",
                                        color="#f5f3ff",
                                    ),
                                    width="100%",
                                    spacing="2",
                                    align="start",
                                ),
                                rx.flex(
                                    rx.vstack(
                                        rx.text("Validade", color="#e4e4e7", font_size="13px", font_weight="600"),
                                        rx.input(
                                            placeholder="MM/AA",
                                            value=CatalogState.card_expiry,
                                            on_change=CatalogState.set_card_expiry,
                                            width="100%",
                                            height="42px",
                                            background="#11111a",
                                            border="1px solid rgba(167, 139, 250, 0.24)",
                                            border_radius="10px",
                                            color="#f5f3ff",
                                        ),
                                        width="100%",
                                        flex="1",
                                        spacing="2",
                                        align="start",
                                    ),
                                    rx.vstack(
                                        rx.text("CVV", color="#e4e4e7", font_size="13px", font_weight="600"),
                                        rx.input(
                                            placeholder="123",
                                            value=CatalogState.card_cvv,
                                            on_change=CatalogState.set_card_cvv,
                                            width="100%",
                                            height="42px",
                                            background="#11111a",
                                            border="1px solid rgba(167, 139, 250, 0.24)",
                                            border_radius="10px",
                                            color="#f5f3ff",
                                        ),
                                        width="120px",
                                        spacing="2",
                                        align="start",
                                    ),
                                    spacing="4",
                                    width="100%",
                                ),
                                width="100%",
                                spacing="3",
                            ),
                            rx.cond(
                                CatalogState.payment_method == "pix",
                                rx.vstack(
                                    rx.center(
                                        rx.vstack(
                                            rx.icon("qr_code", size=64, color="#c4b5fd"),
                                            rx.text("Escaneie o QR Code com o app do seu banco", color="#f5f3ff", font_size="14px", font_weight="600"),
                                            rx.text("Chave Pix Copia e Cola gerada com sucesso para pagamento instantâneo.", color="#a1a1aa", font_size="12px", text_align="center"),
                                            spacing="2",
                                            align="center",
                                        ),
                                        width="100%",
                                        padding="24px",
                                        background="#11111a",
                                        border="1px dashed rgba(167, 139, 250, 0.4)",
                                        border_radius="12px",
                                    ),
                                    width="100%",
                                    spacing="3",
                                ),
                                rx.vstack(
                                    rx.center(
                                        rx.vstack(
                                            rx.icon("file_text", size=48, color="#c4b5fd"),
                                            rx.text("Boleto Bancário gerado com sucesso!", color="#f5f3ff", font_size="14px", font_weight="600"),
                                            rx.text("O boleto vence em 3 dias úteis. A aprovação ocorre em até 48h após o pagamento.", color="#a1a1aa", font_size="12px", text_align="center"),
                                            spacing="2",
                                            align="center",
                                        ),
                                        width="100%",
                                        padding="24px",
                                        background="#11111a",
                                        border="1px solid rgba(167, 139, 250, 0.2)",
                                        border_radius="12px",
                                    ),
                                    width="100%",
                                    spacing="3",
                                ),
                            ),
                        ),
                        width="100%",
                        flex="2",
                        spacing="4",
                        padding="24px",
                        background="linear-gradient(145deg, rgba(24, 20, 36, 0.96), rgba(15, 14, 22, 0.98))",
                        border="1px solid rgba(167, 139, 250, 0.18)",
                        border_radius="24px",
                    ),
                    # Right: Order Summary card
                    rx.vstack(
                        rx.heading("Resumo do Pedido", size="5", color="#f5f3ff"),
                        rx.divider(border_color="rgba(167, 139, 250, 0.2)"),
                        rx.hstack(
                            rx.text("Subtotal", color="#a1a1aa", font_size="14px"),
                            rx.text(CatalogState.cart_total_display, color="#f5f3ff", font_size="15px", font_weight="600"),
                            width="100%",
                            justify="between",
                        ),
                        rx.cond(
                            CatalogState.coupon_applied,
                            rx.hstack(
                                rx.text("Desconto (NIGHTFALL10)", color="#4ade80", font_size="14px"),
                                rx.text(CatalogState.cart_discount_display, color="#4ade80", font_size="15px", font_weight="600"),
                                width="100%",
                                justify="between",
                            ),
                            rx.fragment(),
                        ),
                        rx.hstack(
                            rx.text("Frete", color="#a1a1aa", font_size="14px"),
                            rx.text(CatalogState.shipping_display, color="#f5f3ff", font_size="15px", font_weight="600"),
                            width="100%",
                            justify="between",
                        ),
                        rx.divider(border_color="rgba(167, 139, 250, 0.2)"),
                        rx.hstack(
                            rx.text("Total", color="#f5f3ff", font_size="16px", font_weight="700"),
                            rx.text(CatalogState.cart_final_total_display, color="#e9d5ff", font_size="20px", font_weight="800"),
                            width="100%",
                            justify="between",
                        ),
                        rx.button(
                            "Confirmar Pedido",
                            on_click=CatalogState.finalize_order,
                            color_scheme="purple",
                            size="3",
                            width="100%",
                            font_weight="700",
                            margin_top="16px",
                        ),
                        width="100%",
                        flex="1",
                        min_width="320px",
                        padding="24px",
                        background="linear-gradient(145deg, rgba(24, 20, 36, 0.96), rgba(15, 14, 22, 0.98))",
                        border="1px solid rgba(167, 139, 250, 0.18)",
                        border_radius="24px",
                        spacing="4",
                    ),
                    direction="row",
                    wrap="wrap",
                    spacing="6",
                    width="100%",
                    align="start",
                ),
            ),
            # Not logged in view
            rx.vstack(
                rx.box(
                    rx.icon("lock", size=48, color="#a78bfa"),
                    padding="16px",
                    background="rgba(167, 139, 250, 0.1)",
                    border_radius="50%",
                    border="1px solid rgba(167, 139, 250, 0.3)",
                ),
                rx.heading("Identificação Necessária", size="7", color="#f5f3ff"),
                rx.text(
                    "Você precisa estar logado na sua conta NightFall para acessar a página de pagamento.",
                    color="#a1a1aa",
                    font_size="14px",
                    text_align="center",
                    max_width="480px",
                ),
                rx.link(
                    rx.button(
                        "Fazer Login para Continuar",
                        color_scheme="purple",
                        size="3",
                        font_weight="700",
                    ),
                    href="/login",
                    text_decoration="none",
                    margin_top="16px",
                ),
                width="100%",
                align="center",
                spacing="4",
                padding="60px 24px",
                background="linear-gradient(145deg, rgba(24, 20, 36, 0.96), rgba(15, 14, 22, 0.98))",
                border="1px solid rgba(167, 139, 250, 0.18)",
                border_radius="24px",
            ),
        ),
            width="100%",
            max_width="1120px",
            margin_x="auto",
            padding="28px clamp(20px, 5vw, 64px) 24px",
            align="stretch",
        ),
        min_height="100vh",
        width="100%",
        overflow_x="hidden",
        background="radial-gradient(ellipse at 50% 42%, rgba(91, 33, 182, 0.18), transparent 38%), radial-gradient(ellipse at 12% 8%, rgba(76, 29, 149, 0.12), transparent 28%), #0b0b12",
    )


def profile_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.link(
                    "← Voltar à Loja",
                    href="/",
                    color="#c4b5fd",
                    font_size="14px",
                    font_weight="600",
                    text_decoration="none",
                    _hover={"color": "#f5f3ff"},
                ),
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
                        "NightFall Perfil",
                        size="5",
                        color="#f5f3ff",
                        letter_spacing="-0.04em",
                    ),
                    spacing="3",
                    align="center",
                ),
                width="100%",
                justify="between",
                align="center",
                padding_bottom="24px",
                border_bottom="1px solid rgba(167, 139, 250, 0.16)",
            ),
            # Content / Auth Guard
            rx.cond(
                AuthState.is_logged_in,
                rx.flex(
                    # Left Mini Menu
                    rx.vstack(
                        rx.heading("Painel", size="4", color="#f5f3ff", margin_bottom="8px"),
                        rx.button(
                            "Meus Dados",
                            on_click=AuthState.set_profile_tab("dados"),
                            variant=rx.cond(AuthState.profile_tab == "dados", "solid", "soft"),
                            color_scheme="purple",
                            width="100%",
                            justify_content="start",
                        ),
                        rx.button(
                            "Meus Pedidos",
                            on_click=AuthState.set_profile_tab("pedidos"),
                            variant=rx.cond(AuthState.profile_tab == "pedidos", "solid", "soft"),
                            color_scheme="purple",
                            width="100%",
                            justify_content="start",
                        ),
                        rx.button(
                            "Garantia",
                            on_click=AuthState.set_profile_tab("garantia"),
                            variant=rx.cond(AuthState.profile_tab == "garantia", "solid", "soft"),
                            color_scheme="purple",
                            width="100%",
                            justify_content="start",
                        ),
                        rx.button(
                            "Endereços",
                            on_click=AuthState.set_profile_tab("enderecos"),
                            variant=rx.cond(AuthState.profile_tab == "enderecos", "solid", "soft"),
                            color_scheme="purple",
                            width="100%",
                            justify_content="start",
                        ),
                        width="100%",
                        flex="1",
                        min_width="240px",
                        padding="20px",
                        background="linear-gradient(145deg, rgba(24, 20, 36, 0.96), rgba(15, 14, 22, 0.98))",
                        border="1px solid rgba(167, 139, 250, 0.18)",
                        border_radius="20px",
                        spacing="3",
                    ),
                    # Right Content Area
                    rx.box(
                        rx.cond(
                            AuthState.profile_tab == "dados",
                            rx.vstack(
                                rx.heading("Meus Dados Cadastrais", size="6", color="#f5f3ff"),
                                rx.text("Gerencie suas informações pessoais e de contato.", color="#a1a1aa", font_size="14px"),
                                rx.divider(border_color="rgba(167, 139, 250, 0.16)", margin_y="8px"),
                                rx.vstack(
                                    rx.text("Nome do Usuário", color="#e4e4e7", font_size="13px", font_weight="600"),
                                    rx.input(
                                        value=AuthState.user_name,
                                        on_change=AuthState.update_profile,
                                        width="100%",
                                        height="42px",
                                        background="#11111a",
                                        border="1px solid rgba(167, 139, 250, 0.24)",
                                        border_radius="10px",
                                        color="#f5f3ff",
                                    ),
                                    width="100%",
                                    spacing="2",
                                    align="start",
                                ),
                                rx.vstack(
                                    rx.text("CPF", color="#e4e4e7", font_size="13px", font_weight="600"),
                                    rx.input(
                                        value=AuthState.user_cpf,
                                        on_change=AuthState.set_user_cpf,
                                        placeholder="000.000.000-00",
                                        width="100%",
                                        height="42px",
                                        background="#11111a",
                                        border="1px solid rgba(167, 139, 250, 0.24)",
                                        border_radius="10px",
                                        color="#f5f3ff",
                                    ),
                                    width="100%",
                                    spacing="2",
                                    align="start",
                                ),
                                rx.vstack(
                                    rx.text("Data de Nascimento", color="#e4e4e7", font_size="13px", font_weight="600"),
                                    rx.input(
                                        type="date",
                                        value=AuthState.user_birth_date,
                                        on_change=AuthState.set_user_birth_date,
                                        width="100%",
                                        height="42px",
                                        background="#11111a",
                                        border="1px solid rgba(167, 139, 250, 0.24)",
                                        border_radius="10px",
                                        color="#f5f3ff",
                                    ),
                                    width="100%",
                                    spacing="2",
                                    align="start",
                                ),
                                rx.vstack(
                                    rx.text("E-mail (Cadastrado)", color="#e4e4e7", font_size="13px", font_weight="600"),
                                    rx.input(
                                        value=AuthState.user_email,
                                        is_read_only=True,
                                        width="100%",
                                        height="42px",
                                        background="#11111a",
                                        border="1px solid rgba(167, 139, 250, 0.24)",
                                        border_radius="10px",
                                        color="#a1a1aa",
                                    ),
                                    width="100%",
                                    spacing="2",
                                    align="start",
                                ),
                                rx.cond(
                                    AuthState.profile_message != "",
                                    rx.text(AuthState.profile_message, color="#4ade80", font_size="13px"),
                                    rx.fragment(),
                                ),
                                width="100%",
                                spacing="4",
                            ),
                            rx.cond(
                                AuthState.profile_tab == "pedidos",
                                rx.vstack(
                                    rx.heading("Meus Pedidos", size="6", color="#f5f3ff"),
                                    rx.text("Acompanhe o histórico e status das suas compras recentes.", color="#a1a1aa", font_size="14px"),
                                    rx.divider(border_color="rgba(167, 139, 250, 0.16)", margin_y="8px"),
                                    rx.vstack(
                                        rx.hstack(
                                            rx.vstack(
                                                rx.text("Pedido #NF-84920", color="#f5f3ff", font_weight="700", font_size="15px"),
                                                rx.text("Data: 26/10/2026 • 1 item", color="#a1a1aa", font_size="13px"),
                                                spacing="1",
                                                align="start",
                                            ),
                                            rx.vstack(
                                                rx.text("R$ 2.609,91", color="#e9d5ff", font_weight="700", font_size="15px"),
                                                rx.badge("Concluído", color_scheme="green", variant="solid", size="1"),
                                                spacing="1",
                                                align="end",
                                            ),
                                            width="100%",
                                            justify="between",
                                            align="center",
                                            padding="16px",
                                            background="#11111a",
                                            border="1px solid rgba(167, 139, 250, 0.2)",
                                            border_radius="12px",
                                        ),
                                        width="100%",
                                        spacing="3",
                                    ),
                                    width="100%",
                                    spacing="4",
                                ),
                                rx.cond(
                                    AuthState.profile_tab == "garantia",
                                    rx.vstack(
                                        rx.heading("Garantia de Produtos", size="6", color="#f5f3ff"),
                                        rx.text("Consulte a vigência e termos de garantia dos seus hardwares.", color="#a1a1aa", font_size="14px"),
                                        rx.divider(border_color="rgba(167, 139, 250, 0.16)", margin_y="8px"),
                                        rx.vstack(
                                            rx.hstack(
                                                rx.vstack(
                                                    rx.text("Processador AMD Ryzen 7 7800X3D", color="#f5f3ff", font_weight="700", font_size="15px"),
                                                    rx.text("Garantia de Fábrica: 3 Anos (Válida até Out/2029)", color="#4ade80", font_size="13px"),
                                                    spacing="1",
                                                    align="start",
                                                ),
                                                rx.badge("Ativa", color_scheme="purple", variant="solid", size="1"),
                                                width="100%",
                                                justify="between",
                                                align="center",
                                                padding="16px",
                                                background="#11111a",
                                                border="1px solid rgba(167, 139, 250, 0.2)",
                                                border_radius="12px",
                                            ),
                                            width="100%",
                                            spacing="3",
                                        ),
                                        width="100%",
                                        spacing="4",
                                    ),
                                    # Endereços
                                    rx.vstack(
                                        rx.heading("Endereços Cadastrados", size="6", color="#f5f3ff"),
                                        rx.text("Endereços salvos para entregas rápidas.", color="#a1a1aa", font_size="14px"),
                                        rx.divider(border_color="rgba(167, 139, 250, 0.16)", margin_y="8px"),
                                        rx.vstack(
                                            rx.hstack(
                                                rx.vstack(
                                                    rx.text("Endereço Principal", color="#f5f3ff", font_weight="700", font_size="15px"),
                                                    rx.text("Praça da Sé, 100 - Sé, São Paulo - SP", color="#a1a1aa", font_size="13px"),
                                                    rx.text("CEP: 01001-000", color="#a1a1aa", font_size="12px"),
                                                    spacing="1",
                                                    align="start",
                                                ),
                                                rx.badge("Principal", color_scheme="purple", variant="solid", size="1"),
                                                width="100%",
                                                justify="between",
                                                align="center",
                                                padding="16px",
                                                background="#11111a",
                                                border="1px solid rgba(167, 139, 250, 0.2)",
                                                border_radius="12px",
                                            ),
                                            width="100%",
                                            spacing="3",
                                        ),
                                        width="100%",
                                        spacing="4",
                                    ),
                                ),
                            ),
                        ),
                        width="100%",
                        flex="3",
                        padding="28px",
                        background="linear-gradient(145deg, rgba(24, 20, 36, 0.96), rgba(15, 14, 22, 0.98))",
                        border="1px solid rgba(167, 139, 250, 0.18)",
                        border_radius="24px",
                    ),
                    direction="row",
                    wrap="wrap",
                    spacing="6",
                    width="100%",
                    align="start",
                ),
                # Not logged in view
                rx.vstack(
                    rx.icon("lock", size=48, color="#a78bfa"),
                    rx.heading("Acesso Restrito", size="7", color="#f5f3ff"),
                    rx.text("Você precisa estar logado para acessar seu perfil.", color="#a1a1aa", font_size="14px"),
                    rx.link(
                        rx.button("Fazer Login", color_scheme="purple", size="3", font_weight="700"),
                        href="/login",
                        text_decoration="none",
                    ),
                    width="100%",
                    align="center",
                    spacing="4",
                    padding="60px 24px",
                    background="linear-gradient(145deg, rgba(24, 20, 36, 0.96), rgba(15, 14, 22, 0.98))",
                    border="1px solid rgba(167, 139, 250, 0.18)",
                    border_radius="24px",
                ),
            ),
            width="100%",
            max_width="1120px",
            margin_x="auto",
            padding="28px clamp(20px, 5vw, 64px) 24px",
            align="stretch",
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
app.add_page(cart_page, route="/carrinho", title="Carrinho de Compras | NightFall")
app.add_page(checkout_page, route="/pagamento", title="Pagamento | NightFall")
app.add_page(profile_page, route="/perfil", title="Meu Perfil | NightFall")
