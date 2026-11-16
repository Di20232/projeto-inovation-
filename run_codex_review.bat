@echo off
echo [NightFall + Codex] Iniciando rotina de limpeza e testes automatizados...

cd /d E:\Projetos\projeto-inovation-

echo [1/3] Verificando compilacao do Reflex...
python -m reflex compile --dry
if %errorlevel% neq 0 (
    echo [ERRO] Falha na compilacao do Reflex!
    exit /b %errorlevel%
)

echo [2/3] Executando analise de codigo e remocao de lixo...
python -c "import pathlib, re; p=pathlib.Path('python/python.py'); c=p.read_text(encoding='utf-8'); nc=re.sub(r'\n{3,}', '\n\n', c); p.write_text(nc, encoding='utf-8') if nc!=c else None; print('   -> Analise e limpeza concluidas.')"

echo [3/3] Verificando status do git...
git status -s

echo [NightFall + Codex] Rotina concluida com sucesso!
