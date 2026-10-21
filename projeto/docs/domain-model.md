Vendas, Carrinho e Checkout (Sales & Checkout Context)
Cart (Raiz do Agregado): Carrinho de compras associado ao cliente ou sessão anônima.

CartItem (Entidade): SKU vinculado ao carrinho, quantidade e preço congelado na adição.

Order (Raiz do Agregado): O pedido formalizado após a confirmação do checkout.

OrderItem (Objeto de Valor): Snapshots do produto/SKU no momento da compra (garante que alterações futuras no catálogo não alterem o histórico do pedido).

Payment (Entidade): Estado da transação (Método: PIX/Cartão, Valor, Status: Pendente, Aprovado, Recusado).

ShippingQuote (Objeto de Valor): Informação de entrega (Transportadora, Preço, Prazo estimado).

D. Usuário e Clientes (Customer Context)
Customer (Raiz do Agregado): Dados do cliente (Nome, CPF/CNPJ, E-mail, Telefone).

Address (Objeto de Valor): Endereço imutável de entrega e cobrança.

Uma Category possui N Products: Exemplo: A categoria Placas-Mãe contém diversos modelos.

Um Product possui N SKUs: Um mesmo modelo de memória RAM pode ter variações de frequência/capacidade (SKUs diferentes).

Um SKU possui N TechnicalSpecifications: Essencial para o motor de busca e regras de compatibilidade.

Um PCBuild agrupa N SKUs: O cliente seleciona 1 CPU, 1 Placa-Mãe, 2 Pentes de RAM, 1 Fonte, etc.

Um PCBuild valida suas escolhas contra N CompatibilityRules: Cada adição ao build dispara a verificação das especificações técnicas.

Um PCBuild pode ser transformado em um Cart: Todos os itens validados do monte-seu-PC são transferidos para o carrinho como itens individuais ou como um bundle.

Um Cart gera um Order: Ao finalizar a compra, o estado do carrinho é congelado e transformado em um pedido imutável com Payment e ShippingQuote.

Quando um cliente inicia o processo de pagamento no checkout, é criada uma Reserva de Estoque válida por X minutos.

Se o pagamento for Aprovado, a reserva é convertida em Baixa Definitiva de Estoque.

Se o pagamento for Recusado ou o tempo do PIX/Boleto Expirar, a reserva é cancelada e os itens retornam ao estoque disponível.