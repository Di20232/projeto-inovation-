## Context

Consulte `proposal.md` para a motivação e `specs/identidade-inicial-loja/spec.md` para o comportamento esperado. A aplicação é uma página Reflex sem backend de catálogo; o menu lateral já apresenta as categorias e o estado “Em breve”.

## Goals / Non-Goals

**Goals:**
- Manter os dados iniciais editáveis sem criar um serviço ou infraestrutura de persistência.
- Reaproveitar o menu existente para filtrar produtos por categoria e oferecer retorno a todos os produtos.
- Preencher o catálogo com um produto real pesquisado para cada categoria definida.

**Non-Goals:**
- Criar cadastro administrativo, autenticação, carrinho, checkout ou ações de compra.
- Consultar APIs externas ou integrar Xano.
- Inventar produtos ou usar conteúdo de demonstração para preencher a listagem.

## Decisions

1. **Manter os produtos em `python/catalog.json`.** Um arquivo próximo ao módulo Reflex mantém os dados versionáveis e fáceis de revisar, sem uma base de dados ou API. Cada produto conterá nome, URL da imagem, preço, descrição, categoria e URL da página de origem.
2. **Pesquisar produtos reais em lojas públicas.** Com autorização da pessoa usuária, selecionar um produto real para cada uma das quatro categorias existentes e registrar sua página de origem no campo `source_url`. Não usar placeholders ou produtos fictícios.
3. **Carregar o arquivo local no app e filtrar pelo valor da categoria.** Isso mantém a implementação simples para um catálogo inicial pequeno. Um filtro “Todos” restaura a listagem completa; categorias sem produtos permanecem indisponíveis e identificadas como “Em breve”.
4. **Exibir preços e URLs conforme os dados cadastrados.** A interface não calcula preços nem substitui imagens por dados inventados. Valores ausentes ou inconsistentes devem ser tratados explicitamente durante a validação dos dados, em vez de produzir cards incompletos silenciosamente. Preços promocionais condicionados a pagamento via Pix serão identificados na descrição do produto.
5. **Não introduzir infraestrutura adicional.** O JSON local é adequado enquanto a lista é mantida manualmente; um banco ou API poderá ser especificado em uma change futura se a administração dinâmica se tornar necessária.

## Risks / Trade-offs

- [URLs externas de imagem podem ficar indisponíveis ou lentas] → Manter o endereço como dado explícito e validar a apresentação de cards quando os produtos reais forem fornecidos.
- [Edição manual do JSON pode gerar dados malformados] → Validar a estrutura e os campos obrigatórios antes de considerar o catálogo pronto.
- [Preços e disponibilidade de lojas podem mudar] → Registrar a página de origem em cada produto e tratar os preços como um retrato da pesquisa; revisar antes de usar comercialmente.

## Migration Plan

Não há migração de dados existentes. A mudança adiciona a fonte JSON local e substitui a apresentação vazia somente quando ela contiver produtos reais; pode ser revertida removendo o carregamento do arquivo e restaurando o estado vazio anterior.
