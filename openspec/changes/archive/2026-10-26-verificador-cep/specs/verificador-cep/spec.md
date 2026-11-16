# Especificação: Verificador de CEP

## Requisitos
1. **Formatação de CEP**: O CEP inserido deve ser formatado automaticamente no padrão `00000-000`.
2. **Consulta ViaCEP**: Ao atingir 8 dígitos, o sistema deve consultar a API ViaCEP em segundo plano.
3. **Autopreenchimento**: Caso o CEP seja válido, os campos de endereço (rua, bairro, cidade e uf) devem ser preenchidos automaticamente.
