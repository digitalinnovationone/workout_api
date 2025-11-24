# 🏋️ Workout API - API de Gestão de Atletas

Uma API completa para gerenciamento de atletas, categorias e centros de treinamento desenvolvida em FastAPI com PostgreSQL.

## 🚀 Tecnologias Utilizadas

- **Python 3.11+**
- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM para banco de dados
- **PostgreSQL** - Banco de dados relacional
- **Alembic** - Migrações de banco de dados
- **Docker** - Containerização (opcional)
- **Pydantic** - Validação de dados

## 📋 Pré-requisitos

- Python 3.11 ou superior
- PostgreSQL 15 ou superior
- Git

## 🛠️ Instalação e Configuração

### 1. Clone o repositório
```bash
git clone https://github.com/Xavier-sa/workout_api.git
cd workout_api
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o Banco de Dados

#### Opção A: PostgreSQL Local
```bash
# Crie o banco de dados
createdb -U postgres workout

# Ou via SQL
psql -U postgres -c "CREATE DATABASE workout;"
```

#### Opção B: Docker (Recomendado)
```bash
docker run --name workout-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=workout \
  -p 5432:5432 \
  -d postgres:15
```

### 5. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
DB_URL=postgresql+asyncpg://postgres:postgres@localhost/workout
```

### 6. Execute as migrações
```bash
alembic upgrade head
```

### 7. Execute a aplicação
```bash
uvicorn workout_api.main:app --reload
```

A API estará disponível em: http://127.0.0.1:8000

## 📚 Documentação da API

### Swagger UI
http://127.0.0.1:8000/docs

### Redoc
http://127.0.0.1:8000/redoc

## 🎯 Endpoints Principais

### Atletas
- `GET /atletas/` - Listar todos os atletas
- `POST /atletas/` - Criar novo atleta
- `GET /atletas/{id}` - Buscar atleta por ID
- `PATCH /atletas/{id}` - Atualizar atleta
- `DELETE /atletas/{id}` - Deletar atleta

### Categorias
- `GET /categorias/` - Listar categorias
- `POST /categorias/` - Criar categoria

### Centros de Treinamento
- `GET /centros_treinamento/` - Listar centros
- `POST /centros_treinamento/` - Criar centro

## 💡 Fluxo de Uso

### 1. Primeiro crie uma categoria
```json
{
  "nome": "Scale"
}
```

### 2. Depois crie um centro de treinamento
```json
{
  "nome": "CT King",
  "endereco": "Rua X, Q02",
  "proprietario": "Marcos"
}
```

### 3. Finalmente crie o atleta
```json
{
  "nome": "João Silva",
  "cpf": "12345678900",
  "idade": 25,
  "peso": 75.5,
  "altura": 1.80,
  "sexo": "M",
  "categoria": {
    "nome": "Scale"
  },
  "centro_treinamento": {
    "nome": "CT King"
  }
}
```

## 🐛 Problemas Comuns e Soluções

### Erro: "connection was closed in the middle of operation"
- Verifique se o PostgreSQL está rodando
- Confirme as credenciais no `.env`

### Erro: "Table doesn't exist"
- Execute `alembic upgrade head`

### Erro: "UUID não suportado"
- Use PostgreSQL (MySQL/MariaDB não suportam UUID nativo)

### Erro no PowerShell com PSReadLine
- Use comandos em uma linha ou arquivos `.py` separados

## 🗄️ Estrutura do Banco

### Tabelas Principais
- `atletas` - Dados dos atletas
- `categorias` - Categorias dos atletas
- `centros_treinamento` - Centros de treinamento

### Relacionamentos
- Atleta → Categoria (N:1)
- Atleta → Centro de Treinamento (N:1)

## 🚧 Desenvolvimento

### Criando novas migrações
```bash
alembic revision --autogenerate -m "Descrição da migração"
alembic upgrade head
```

### Testando a API
```bash
# Teste de conexão com o banco
python -c "
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

async def test():
    engine = create_async_engine('postgresql+asyncpg://postgres:postgres@localhost/workout')
    async with engine.connect() as conn:
        print('✅ Conexão bem-sucedida!')

asyncio.run(test())
"
```

## 📸 Capturas de Tela

*(Adicione aqui suas imagens de teste)*

### Swagger UI em Funcionamento
![Swagger Interface](workout_api/diolabluiza_passos/navegador-.PNG)

### Dados no PostgreSQL
![Dados no pgAdmin](workout_api/diolabluiza_passos/passo-3.PNG)

### Testes de API
![Testes com curl](workout_api/diolabluiza_passos/postman-api.PNG)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Seu Nome**
- GitHub: [@Xavier-sa](https://github.com/Xavier-sa)

## 🙏 Agradecimentos

- Equipe DIO pelos desafios propostos
- Comunidade Python Brasil
- Documentação do FastAPI e SQLAlchemy

---

**⭐️ Se este projeto foi útil, deixe uma estrela no repositório!**


