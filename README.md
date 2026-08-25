# OceanWatch API

API para cadastrar boias de monitoramento oceânico, desenvolvida com FastAPI, SQLAlchemy e SQLite.

## Como rodar o sistema

1. Crie e ative um ambiente virtual:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Instale as dependências:

   ```powershell
   pip install -r requirements.txt
   ```

3. Crie o banco de dados e as tabelas. Execute uma vez, na raiz do projeto:

   ```powershell
   python -c "from app.database.base import Base; from app.database.database import engine; import app.models.boia; Base.metadata.create_all(bind=engine)"
   ```

4. Inicie a API:

   ```powershell
   uvicorn app.main:app --reload
   ```

5. Acesse a documentação interativa em [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

## Estrutura do projeto

```text
app/
├── main.py                  # Inicializa a aplicação FastAPI
├── boia.py                  # Rotas HTTP de boias
├── schemas/                 # Validação dos dados recebidos
├── services/                # Regras de negócio
├── repositories/            # Persistência de dados
├── models/                  # Modelos do banco de dados
└── database/                # Configuração e sessão do SQLite
tests/                       # Testes automatizados
```

## API

### Cadastrar uma boia

`POST /boias`

Exemplo de requisição:

```json
{
  "nome": "Boia RJ-001",
  "numero_serie": "OW-0002",
  "latitude": -22.90,
  "longitude": -43.20
}
```

Exemplo com PowerShell:

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/boias" -ContentType "application/json" -Body '{"nome":"Boia RJ-001","numero_serie":"OW-0002","latitude":-22.90,"longitude":-43.20}'
```

Em caso de sucesso, a API responde com os dados cadastrados, incluindo o `id`. O campo `numero_serie` deve ser único; se já existir, a API retorna `409 Conflict`.

## Testes

Com o ambiente virtual ativado, instale o executor de testes e execute:

```powershell
pip install pytest
pytest
```
