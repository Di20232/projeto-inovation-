import { index, route } from "@react-router/dev/routes";

export default [
  // Node does not classify OneDrive placeholder files as regular files.
  index("routes/_index.jsx"),
  route("login", "routes/[login]._index.jsx", { index: true }),
  route("cadastro", "routes/[cadastro]._index.jsx", { index: true }),
  route("carrinho", "routes/[carrinho]._index.jsx", { index: true }),
  route("pagamento", "routes/[pagamento]._index.jsx", { index: true }),
  route("perfil", "routes/[perfil]._index.jsx", { index: true }),
  route("admin", "routes/[admin]._index.jsx", { index: true }),
  route("*", "routes/[404]._index.jsx"),
];
