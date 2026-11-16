---
name: auto-archive-change
description: Arquiva automaticamente uma change do OpenSpec para openspec/changes/archive/ após a conclusão e verificação do desenvolvimento.
---

# Auto Archive Change Skill

Esta skill automatiza o arquivamento de mudanças (changes) do OpenSpec assim que o seu desenvolvimento, testes e verificações forem concluídos com sucesso.

## Quando executar

Execute esta skill ao finalizar e verificar completamente uma change do OpenSpec que estava em andamento em `openspec/changes/<nome-da-change>/`.

## Passos para arquivar

1. **Verificar Conclusão**:
   - Confirme que todos os itens em `tasks.md` da change estão concluídos.
   - Certifique-se de que os testes e a compilação (`reflex compile --dry`, testes locais, etc.) passaram com sucesso.
   - Confirme que as alterações de código foram commitadas no git.

2. **Mover para o Archive**:
   - Mova a pasta da change de `openspec/changes/<nome-da-change>/` para `openspec/changes/archive/<nome-da-change>/`.
   - Se a pasta de destino `openspec/changes/archive/` não existir, crie-a.

3. **Atualizar Documentação e Git**:
   - Faça commit da movimentação no git.
   - Atualize a nota do projeto no cofre do Obsidian se necessário.
