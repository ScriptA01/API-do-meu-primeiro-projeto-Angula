from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import json

app = FastAPI()

# Liberando acesso para o Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URL do Firebase
firebase_url = "https://meu-primeiro-projeto-angular-default-rtdb.firebaseio.com/imoveis"

# Endpoint para listar imóveis
@app.get("/imoveis")
def listar_imoveis():
    resposta = requests.get(f"{firebase_url}.json")
    return resposta.json()

# Endpoint para cadastrar imóvel com ID incremental
@app.post("/imoveis")
def cadastrar_imovel(imovel: dict):
    # 1. Pega o contador atual
    contador_resp = requests.get("https://meu-primeiro-projeto-angular-default-rtdb.firebaseio.com/contador_imoveis.json")
    contador = contador_resp.json() or 0
    novo_id = contador + 1

    # 2. Adiciona o id incremental no dicionário
    imovel["id"] = novo_id

    # 3. Salva o imóvel (Firebase vai gerar uma chave única)
    resposta = requests.post(f"{firebase_url}.json", data=json.dumps(imovel))
    firebase_key = resposta.json()["name"]

    # 4. Atualiza o próprio imóvel com a chave gerada (idFirebase)
    requests.patch(f"{firebase_url}/{firebase_key}.json", data=json.dumps({"idFirebase": firebase_key}))

    # 5. Atualiza o contador
    requests.put("https://meu-primeiro-projeto-angular-default-rtdb.firebaseio.com/contador_imoveis.json", data=json.dumps(novo_id))

    return {
        "mensagem": "Imóvel cadastrado com sucesso",
        "id": novo_id,
        "firebase_key": firebase_key
    }

# Endpoint para atualizar imóvel
@app.patch("/imoveis/{id}")
def atualizar_imovel(id: str, dados: dict):
    resposta = requests.patch(f"{firebase_url}/{id}.json", data=json.dumps(dados))
    return resposta.json()

# Endpoint para deletar imóvel
@app.delete("/imoveis/{id}")
def deletar_imovel(id: str):
    resposta = requests.delete(f"{firebase_url}/{id}.json")
    return {"mensagem": "Imóvel deletado com sucesso"}
