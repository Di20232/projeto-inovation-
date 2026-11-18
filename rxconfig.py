import reflex as rx

config = rx.Config(
    app_name="python",
    backend_port=8003,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(),
    ]
)
