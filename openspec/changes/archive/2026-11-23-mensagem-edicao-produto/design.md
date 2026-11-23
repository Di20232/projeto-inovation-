# Design

`save_edited_product` chama `_admin_feedback(...)` com a mensagem detalhada e, em seguida, define `self.admin_message = "Produto atualizado."`. A segunda atribuição prevalece, então a tela mostra só o texto curto.

Efeito colateral conhecido: o nome do produto editado deixa de aparecer no aviso. Se isso fizer falta, basta remover a linha para voltar à mensagem detalhada.
