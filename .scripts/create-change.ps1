#!/usr/bin/env pwsh

param(
    [string]$tipo,
    [string]$descricao
)

$data = Get-Date -Format "yyyy-MM-dd"
$baseDir = "C:\Users\Diego\OneDrive\Documentos\04 - Estudos e Faculdade\Projeto faculdade\projeto-inovation"
$changesDir = Join-Path $baseDir "openspec\changes"
$changeName = "$data-$tipo"
$changeDir = Join-Path $changesDir $changeName

if (Test-Path $changeDir) {
    Write-Host "Change ja existe: $changeDir" -ForegroundColor Yellow
    return
}

New-Item -ItemType Directory -Path $changeDir -Force | Out-Null

$proposalContent = @"
# Proposta: $descricao

## Visao Geral
Implementacao de $descricao no projeto NightFall.

## Objetivos
1. Detalhe os objetivos principais da mudanca.
2. Liste os beneficios ou impactos esperados.
"@

$designContent = @"
# Design: $descricao

## Arquitetura e Componentes
- Detalhe os componentes afetados.
- Explique como as alteracoes se integram ao sistema existente.
"@

$tasksContent = @"
# Tarefas: $descricao

- [ ] Tarefa 1: Descricao da tarefa
- [ ] Tarefa 2: Descricao da tarefa
- [ ] Tarefa 3: Descricao da tarefa
"@

foreach ($fileName in @("proposal.md", "design.md", "tasks.md")) {
    $filePath = Join-Path $changeDir $fileName
    $content = switch ($fileName) {
        "proposal.md" { $proposalContent }
        "design.md" { $designContent }
        default { $tasksContent }
    }
    Set-Content -Path $filePath -Value $content -Encoding UTF8
    Write-Host "Criado: $filePath"
}

Write-Host "Change criado: $changeDir"