# Design: Busca no Catálogo NightFall

## Arquitetura
- **Estado**: `CatalogState.search_query` armazena o texto; `set_search_query` atualiza somente esse campo para preservar o filtro de categoria.
- **Filtragem**: `filtered_products` primeiro aplica a categoria ativa e depois compara o termo normalizado com nome, descrição, categoria, rótulos e valores das especificações.
- **Interface**: O input é controlado pelo estado (`value`) e dispara `on_change`; o catálogo apresenta mensagem distinta quando a consulta não tem resultados.

## Decisões
- A busca é local e reativa, sem novas APIs ou dependências.
- Limpar o texto mantém a categoria ativa e mostra novamente os produtos daquela categoria.
- O botão “Todos os produtos” restaura a categoria “Todos” e limpa a consulta.

## Verificação
A compilação Reflex pode ser executada localmente. A confirmação de interação no browser depende de atualizar o servidor local, que está executando uma versão anterior ao código atual.
