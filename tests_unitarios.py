"""Testes unitários e de integração para o projeto NightFall (Reflex + Xano)."""

import math
import sys
import os

# Adiciona o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Imports do módulo da aplicação
from python import python as app_module

parse_catalog_data = app_module.parse_catalog_data
Product = app_module.Product
Specification = app_module.Specification
CATEGORIES = app_module.CATEGORIES
validate_cpf = app_module.validate_cpf
format_cpf = app_module.format_cpf
format_birth_date = app_module.format_birth_date


def test_parse_catalog_data_estrutura_valida():
    """Deve aceitar uma lista de produtos com todos os campos obrigatórios."""
    data = [
        {
            "name": "Placa de Vídeo RTX 4070",
            "image_url": "https://exemplo.com/img.jpg",
            "source_url": "https://exemplo.com/produto",
            "price": 3499.90,
            "description": "Placa de vídeo dedicada.",
            "category": "Componentes",
            "specifications": [
                {"label": "Marca", "value": "NVIDIA"},
                {"label": "VRAM", "value": "12GB"},
            ],
        }
    ]
    resultado = parse_catalog_data(data)
    assert len(resultado) == 1
    assert resultado[0]["name"] == "Placa de Vídeo RTX 4070"
    assert resultado[0]["price"] == 3499.90
    assert resultado[0]["price_display"].startswith("R$")
    assert resultado[0]["category"] == "Componentes"
    assert len(resultado[0]["specifications"]) == 2


def test_parse_catalog_data_campos_obrigatorios():
    """Deve lançar ValueError quando campos obrigatórios faltarem."""
    data_invalida = [
        {
            "name": "Produto Sem Descrição",
            "image_url": "https://exemplo.com/img.jpg",
            "source_url": "https://exemplo.com/produto",
            "price": 100.0,
            # "description" faltando
            "category": "Componentes",
        }
    ]
    try:
        parse_catalog_data(data_invalida)
        assert False, "Deveria ter lançado ValueError"
    except ValueError as e:
        assert "description" in str(e)


def test_parse_catalog_data_preco_negativo():
    """Deve lançar ValueError para preço negativo."""
    data_invalida = [
        {
            "name": "Produto",
            "image_url": "https://exemplo.com/img.jpg",
            "source_url": "https://exemplo.com/produto",
            "price": -50.0,
            "description": "Desc",
            "category": "Componentes",
        }
    ]
    try:
        parse_catalog_data(data_invalida)
        assert False, "Deveria ter lançado ValueError"
    except ValueError:
        pass


def test_parse_catalog_data_categoria_invalida():
    """Deve lançar ValueError para categoria fora da lista permitida."""
    data_invalida = [
        {
            "name": "Produto",
            "image_url": "https://exemplo.com/img.jpg",
            "source_url": "https://exemplo.com/produto",
            "price": 100.0,
            "description": "Desc",
            "category": "Categoria Inexistente",
        }
    ]
    try:
        parse_catalog_data(data_invalida)
        assert False, "Deveria ter lançado ValueError"
    except ValueError as e:
        assert "Categoria" in str(e)


def test_formato_preco_brasileiro():
    """Verifica se o preço é formatado no padrão brasileiro (R$ 1.234,56)."""
    from decimal import Decimal
    preco = 1234.5
    formatado = f"{Decimal(str(preco)):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    assert formatado == "1.234,50"


def test_categorias_permitidas():
    """Verifica se as categorias esperadas estão definidas."""
    assert "Computadores" in CATEGORIES
    assert "Componentes" in CATEGORIES
    assert "Periféricos" in CATEGORIES
    assert "Acessórios" in CATEGORIES


def test_validar_cpf_valido():
    """Verifica a validação de CPF válido."""
    assert validate_cpf("123.456.789-09") == True
    assert validate_cpf("11144477735") == True  # CPF válido de exemplo


def test_validar_cpf_invalido():
    """Verifica a validação de CPF inválido."""
    assert validate_cpf("000.000.000-00") == False
    assert validate_cpf("123") == False
    assert validate_cpf("") == False


def test_formatar_cpf():
    """Verifica a formatação de CPF."""
    assert format_cpf("12345678909") == "123.456.789-09"
    assert format_cpf("123") == "123"
    assert format_cpf("1234567") == "123.456.7"


def test_formatar_data_nascimento():
    """Verifica a formatação de data de nascimento."""
    assert format_birth_date("15051995") == "15/05/1995"
    assert format_birth_date("150519") == "15/05/19"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])