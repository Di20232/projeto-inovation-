Estou criando uma plataforma de e-commerce chamada NightFall de alto desempenho, robusta, escalável e focada na venda de hardware e periféricos (estilo KaBuM! e Pichau). O objetivo principal é proporcionar uma experiência de compra ágil, com buscas e filtros técnicos precisos, precificação dinâmica (descontos em PIX/boleto) e uma ferramenta integrada de montagem de computadores com verificação de compatibilidade.

--escopo do projeto--
Catálogo de produtos com categorização profunda de hardware e periféricos.

Filtros de busca avançados por especificações técnicas.

Carrinho de compras e checkout integrado com meios de pagamento (PIX, Cartão de Crédito) e cálculo de frete.

Área do cliente (cadastro, histórico de pedidos, rastreamento).

Monte Seu PC (versão inicial com validação básica de compatibilidade).

Painel administrativo básico para gestão de produtos, estoque, preços e pedidos.

--funcionalidades--
Monte Seu PC (Custom Builder): Montador passo a passo de computadores que filtra automaticamente componentes compatíveis conforme as seleções anteriores.

Precificação Dupla Dinâmica: Exibição clara de preço à vista (ex: 15% de desconto no PIX/Boleto) vs. preço parcelado no cartão.

Cálculo de Frete e Prazo: Integração com APIs de logística para cotação em tempo real.

Sistema de Avaliações e Reviews: Depoimentos e notas de compradores por produto.

Alertas de Estoque: Notificação de "Avise-me quando chegar" para itens esgotados.

--algumas restrições--
Precisão de Estoque: Impedir a venda de produtos sem estoque real (evitar overbooking em promoções de alta demanda).

Integridade das Regras de Compatibilidade: A lógica de montagem não pode permitir combinações fisicamente ou tecnicamente inviáveis.

Compliance e LGPD: Tratamento rigoroso de dados pessoais e de pagamento dos usuários.

Orçamento / Prazos de Infraestrutura: Dependência de gateways de pagamento e APIs de frete terceirizadas com limites de rate-limiting.

--algumas das tecnologias--
Front-end: reflex.

Back-end: Node.js (NestJS/Express) ou Python/Go para APIs RESTful / GraphQL.

Banco de Dados: PostgreSQL / MySQL (dados relacionais para pedidos e estoque) + Redis (cache de catálogo e sessões).

Infraestrutura: Docker, hospedagem em nuvem (AWS / Vercel / Render).