## Documentação da API - Backend FastAPI

### 🔧 Iniciando a API

Para iniciar o servidor backend com FastAPI e Uvicorn:

```bash
uvicorn main:app --reload
```

A aplicação estará disponível em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Acesse também a documentação automática gerada pelo FastAPI:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### 🌐 Endpoints da API

#### `GET /imoveis`

Retorna todos os imóveis cadastrados no Firebase.

**Exemplo de resposta:**

```json
{
  "-Nabc123": {
    "id": 1,
    "endereco": "Rua das Flores",
    "valor": 250000,
    "idFirebase": "-Nabc123"
  },
  ...
}
```

#### `POST /imoveis`

Cadastra um novo imóvel com ID incremental e chave do Firebase.

**Body (exemplo):**

```json
{
  "endereco": "Av. Brasil",
  "valor": 300000,
  "descricao": "Imóvel de alto padrão"
}
```

**Resposta:**

```json
{
  "mensagem": "Imóvel cadastrado com sucesso",
  "id": 4,
  "firebase_key": "-Nxyz456"
}
```

#### `PATCH /imoveis/{id}`

Atualiza os dados de um imóvel existente pelo ID Firebase.

**Body (exemplo):**

```json
{
  "valor": 320000,
  "descricao": "Preço atualizado"
}
```

#### `DELETE /imoveis/{id}`

Remove um imóvel existente com base em seu ID Firebase.

**Resposta:**

```json
{
  "mensagem": "Imóvel deletado com sucesso"
}
```

### 🔐 CORS Middleware

Para permitir que o frontend Angular se comunique com a API, foi adicionado middleware de CORS liberando todas as origens:

```python
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
```

### 📌 Observações

- Os dados são persistidos no Firebase Realtime Database.
- O ID do imóvel é controlado separadamente via `contador_imoveis`.
- O Firebase gera uma chave única (`idFirebase`) usada para editar e excluir registros.
- A API está pronta para ser consumida por qualquer frontend, especialmente o Angular usado neste projeto.

---

