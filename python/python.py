"""Public catalog for computer components."""

from typing import TypedDict

import reflex as rx


class Product(TypedDict):
    slug: str
    category: str
    name: str
    brand: str
    image_url: str
    price: str
    availability: str
    specifications: dict[str, str]


CATEGORIES = (
    "Todas",
    "Placas de vídeo",
    "Processadores",
    "Memória RAM",
    "Armazenamento",
    "Refrigeração",
)

PRODUCTS: tuple[Product, ...] = (
    {
        "slug": "geforce-rtx-4060-8gb",
        "category": "Placas de vídeo",
        "name": "GeForce RTX 4060 8 GB",
        "brand": "MSI",
        "image_url": "https://images.unsplash.com/photo-1591488320449-011701bb6704?auto=format&fit=crop&w=640&q=80",
        "price": "R$ 2.199,90",
        "availability": "Em estoque",
        "specifications": {
            "Memória": "8 GB GDDR6",
            "Interface": "PCI Express 4.0",
            "Conexões": "3x DisplayPort, 1x HDMI",
        },
    },
    {
        "slug": "radeon-rx-7600-8gb",
        "category": "Placas de vídeo",
        "name": "Radeon RX 7600 8 GB",
        "brand": "Sapphire",
        "image_url": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=640&q=80",
        "price": "R$ 1.899,90",
        "availability": "Em estoque",
        "specifications": {
            "Memória": "8 GB GDDR6",
            "Interface": "PCI Express 4.0",
            "Conexões": "3x DisplayPort, 1x HDMI",
        },
    },
    {
        "slug": "ryzen-5-5600",
        "category": "Processadores",
        "name": "Ryzen 5 5600",
        "brand": "AMD",
        "image_url": "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?auto=format&fit=crop&w=640&q=80",
        "price": "R$ 849,90",
        "availability": "Em estoque",
        "specifications": {
            "Núcleos / threads": "6 / 12",
            "Clock boost": "Até 4,4 GHz",
            "Soquete": "AM4",
        },
    },
    {
        "slug": "core-i5-12400f",
        "category": "Processadores",
        "name": "Core i5-12400F",
        "brand": "Intel",
        "image_url": "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?auto=format&fit=crop&w=640&q=80",
        "price": "R$ 899,90",
        "availability": "Em estoque",
        "specifications": {
            "Núcleos / threads": "6 / 12",
            "Clock boost": "Até 4,4 GHz",
            "Soquete": "LGA 1700",
        },
    },
    {
        "slug": "corsair-vengeance-16gb",
        "category": "Memória RAM",
        "name": "Vengeance LPX 16 GB",
        "brand": "Corsair",
        "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=640&q=80",
        "price": "R$ 289,90",
        "availability": "Em estoque",
        "specifications": {
            "Capacidade": "16 GB (2x 8 GB)",
            "Tipo": "DDR4",
            "Frequência": "3.200 MHz",
        },
    },
    {
        "slug": "kingston-nv2-1tb",
        "category": "Armazenamento",
        "name": "SSD NV2 1 TB",
        "brand": "Kingston",
        "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=640&q=80",
        "price": "R$ 399,90",
        "availability": "Em estoque",
        "specifications": {
            "Capacidade": "1 TB",
            "Formato": "M.2 2280",
            "Interface": "NVMe PCIe 4.0",
        },
    },
)


class CatalogState(rx.State):
    selected_category: str = CATEGORIES[0]

    @rx.event
    def select_category(self, category: str) -> None:
        self.selected_category = category

    @rx.var
    def has_products(self) -> bool:
        return self.selected_category == CATEGORIES[0] or any(
            product["category"] == self.selected_category for product in PRODUCTS
        )


def store_header() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.link(
                rx.heading("byte.", size="6", color="#f97316"),
                href="/",
                text_decoration="none",
            ),
            rx.spacer(),
            rx.text(
                "Hardware para suas próximas ideias",
                color="#cbd5e1",
                font_size="14px",
            ),
            align="center",
            width="100%",
            max_width="1180px",
            margin_x="auto",
            padding="16px 24px",
        ),
        background_color="#111827",
        border_bottom="1px solid #293548",
        width="100%",
    )


def product_card(product: Product) -> rx.Component:
    availability_color = (
        "#4ade80" if product["availability"] == "Em estoque" else "#fbbf24"
    )
    return rx.link(
        rx.box(
            rx.vstack(
                rx.box(
                    rx.text(
                        product["category"].upper(),
                        color="#fb923c",
                        font_size="11px",
                        font_weight="700",
                        letter_spacing="1px",
                    ),
                    padding="7px 10px",
                    background_color="#342417",
                    border_radius="999px",
                ),
                rx.image(
                    src=product["image_url"],
                    alt=product["name"],
                    width="100%",
                    height="140px",
                    border_radius="12px",
                    object_fit="cover",
                ),
                rx.vstack(
                    rx.text(product["brand"], color="#94a3b8", font_size="13px"),
                    rx.heading(
                        product["name"],
                        size="4",
                        color="#f8fafc",
                        min_height="52px",
                    ),
                    align="start",
                    spacing="2",
                    width="100%",
                ),
                rx.hstack(
                    rx.text(
                        product["availability"],
                        color=availability_color,
                        font_size="12px",
                    ),
                    rx.spacer(),
                    rx.text(
                        product["price"],
                        color="#f8fafc",
                        font_size="18px",
                        font_weight="700",
                    ),
                    width="100%",
                    align="center",
                ),
                align="start",
                spacing="4",
                width="100%",
            ),
            padding="18px",
            background_color="#151f2e",
            border="1px solid #293548",
            border_radius="16px",
            width="100%",
            height="100%",
            _hover={
                "border_color": "#f97316",
                "transform": "translateY(-3px)",
                "transition": "all 150ms ease",
            },
        ),
        href=f"/produto/{product['slug']}",
        text_decoration="none",
        width="100%",
    )


def empty_category() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Nenhum produto por aqui ainda", size="5", color="#f8fafc"),
            rx.text(
                "Esta categoria ainda não tem componentes cadastrados.",
                color="#94a3b8",
                text_align="center",
            ),
            spacing="3",
            align="center",
        ),
        padding="64px 24px",
        background_color="#151f2e",
        border="1px solid #293548",
        border_radius="16px",
        width="100%",
    )


def index() -> rx.Component:
    product_cards = [
        rx.cond(
            (CatalogState.selected_category == CATEGORIES[0])
            | (CatalogState.selected_category == product["category"]),
            product_card(product),
            rx.fragment(),
        )
        for product in PRODUCTS
    ]

    return rx.box(
        store_header(),
        rx.box(
            rx.vstack(
                rx.box(
                    rx.text(
                        "PEÇAS PARA IR MAIS LONGE",
                        color="#fb923c",
                        font_size="12px",
                        font_weight="700",
                        letter_spacing="2px",
                    ),
                    rx.heading(
                        "Monte seu próximo setup.",
                        size="8",
                        color="#f8fafc",
                        line_height="1.1",
                    ),
                    rx.text(
                        "Componentes selecionados para jogar, criar e trabalhar.",
                        color="#94a3b8",
                        font_size="17px",
                    ),
                    spacing="4",
                    align="start",
                    padding_y="44px",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.heading("Componentes", size="6", color="#f8fafc"),
                        rx.spacer(),
                        rx.text(
                            f"{len(PRODUCTS)} produtos de demonstração",
                            color="#94a3b8",
                            font_size="13px",
                        ),
                        align="center",
                        width="100%",
                        flex_wrap="wrap",
                        gap="12px",
                    ),
                    rx.flex(
                        *[
                            rx.button(
                                category,
                                on_click=CatalogState.select_category(category),
                                background_color=rx.cond(
                                    CatalogState.selected_category == category,
                                    "#ea580c",
                                    "#1e293b",
                                ),
                                color="#f8fafc",
                                border="1px solid #334155",
                                border_radius="999px",
                                _hover={"background_color": "#c2410c"},
                            )
                            for category in CATEGORIES
                        ],
                        gap="10px",
                        flex_wrap="wrap",
                        width="100%",
                    ),
                    rx.cond(
                        CatalogState.has_products,
                        rx.grid(
                            *product_cards,
                            grid_template_columns="repeat(auto-fit, minmax(230px, 1fr))",
                            gap="18px",
                            width="100%",
                        ),
                        empty_category(),
                    ),
                    spacing="5",
                    align="start",
                    width="100%",
                ),
                spacing="6",
                align="start",
                width="100%",
            ),
            max_width="1180px",
            margin_x="auto",
            padding="0 24px 64px",
        ),
        min_height="100vh",
        background_color="#0b1220",
    )


def product_details(product: Product) -> rx.Component:
    return rx.vstack(
        rx.link(
            rx.text("<  Voltar ao catálogo", color="#fb923c", font_weight="600"),
            href="/",
            text_decoration="none",
        ),
        rx.box(
            rx.vstack(
                rx.text(
                    product["category"].upper(),
                    color="#fb923c",
                    font_size="12px",
                    font_weight="700",
                    letter_spacing="1px",
                ),
                rx.heading(product["name"], size="8", color="#f8fafc"),
                rx.text(product["brand"], color="#94a3b8", font_size="18px"),
                rx.image(
                    src=product["image_url"],
                    alt=product["name"],
                    width="100%",
                    max_width="560px",
                    height="320px",
                    border_radius="16px",
                    object_fit="cover",
                ),
                rx.hstack(
                    rx.text(
                        product["price"],
                        color="#f8fafc",
                        font_size="28px",
                        font_weight="700",
                    ),
                    rx.text(
                        product["availability"],
                        color="#4ade80"
                        if product["availability"] == "Em estoque"
                        else "#fbbf24",
                    ),
                    gap="16px",
                    align="center",
                    flex_wrap="wrap",
                ),
                rx.divider(border_color="#293548"),
                rx.heading("Especificações técnicas", size="5", color="#f8fafc"),
                rx.vstack(
                    *[
                        rx.hstack(
                            rx.text(label, color="#94a3b8"),
                            rx.spacer(),
                            rx.text(value, color="#f8fafc", text_align="right"),
                            width="100%",
                            gap="16px",
                        )
                        for label, value in product["specifications"].items()
                    ],
                    spacing="4",
                    width="100%",
                ),
                align="start",
                spacing="5",
                width="100%",
                max_width="680px",
            ),
            padding="32px",
            background_color="#151f2e",
            border="1px solid #293548",
            border_radius="20px",
            width="100%",
        ),
        align="start",
        spacing="6",
        width="100%",
    )


def product_not_found() -> rx.Component:
    return rx.vstack(
        rx.heading("Produto não encontrado", size="7", color="#f8fafc"),
        rx.text(
            "Este componente não está disponível no catálogo.",
            color="#94a3b8",
        ),
        rx.link(
            rx.button("Voltar ao catálogo", background_color="#ea580c", color="white"),
            href="/",
        ),
        align="center",
        spacing="4",
        padding="64px 24px",
        width="100%",
    )


def product_page() -> rx.Component:
    product_cases = [
        (product["slug"], product_details(product)) for product in PRODUCTS
    ]
    return rx.box(
        store_header(),
        rx.box(
            rx.match(rx.State.slug, *product_cases, product_not_found()),
            max_width="1180px",
            margin_x="auto",
            padding="40px 24px 64px",
            width="100%",
        ),
        min_height="100vh",
        background_color="#0b1220",
    )


app = rx.App()
app.add_page(product_page, route="/produto/[slug]")
app.add_page(index, route="/")
