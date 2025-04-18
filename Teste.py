from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)

@patch("main.requests.get")
def test_listar_imoveis(mock_get):
    mock_get.return_value.json.return_value = {
        "id1": {"endereco": "Rua X", "valor": 123456}
    }

    response = client.get("/imoveis")
    assert response.status_code == 200
    assert response.json() == {"id1": {"endereco": "Rua X", "valor": 123456}}

@patch("main.requests.post")
@patch("main.requests.put")
@patch("main.requests.get")
@patch("main.requests.patch")
def test_cadastrar_imovel(mock_patch, mock_get, mock_put, mock_post):
    mock_get.return_value.json.return_value = 5  # contador atual
    mock_post.return_value.json.return_value = {"name": "abc123"}

    novo_imovel = {
        "imagem": "img-teste.jpg",
        "endereco": "Rua Teste",
        "valor": 123456,
        "tipo": "venda",
        "numero": "101",
        "descricao": "Descrição teste"
    }

    response = client.post("/imoveis", json=novo_imovel)
    data = response.json()

    assert response.status_code == 200
    assert data["mensagem"] == "Imóvel cadastrado com sucesso"
    assert data["id"] == 6
    assert data["firebase_key"] == "abc123"

@patch("main.requests.patch")
def test_atualizar_imovel(mock_patch):
    mock_patch.return_value.json.return_value = {"valor": 999999}
    firebase_key = "abc123"

    dados = {"valor": 999999}
    response = client.patch(f"/imoveis/{firebase_key}", json=dados)

    assert response.status_code == 200
    assert response.json()["valor"] == 999999

@patch("main.requests.delete")
def test_deletar_imovel(mock_delete):
    mock_delete.return_value.json.return_value = None  # Firebase retorna None na exclusão

    firebase_key = "abc123"
    response = client.delete(f"/imoveis/{firebase_key}")

    assert response.status_code == 200
    assert response.json()["mensagem"] == "Imóvel deletado com sucesso"


    "Comandos usados para testar: pytest Teste.py, pytest -v Teste.py e instalei a biblioteca: pip install httpx."