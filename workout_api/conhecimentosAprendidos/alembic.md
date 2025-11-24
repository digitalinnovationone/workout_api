### **O que é Alembic**

Alembic é uma **ferramenta de migração de banco de dados** para projetos que usam SQLAlchemy (ou ORMs baseados nele).
Ela serve para **controlar alterações no esquema do banco** (tabelas, colunas, índices, constraints) ao longo do tempo, sem precisar apagar e recriar o banco inteiro.

---

### **Comando: `alembic init alembic`**

* **Função:** inicializa um diretório de migração dentro do seu projeto.
* **O que ele cria:**

  1. Uma pasta chamada `alembic`
  2. Um arquivo de configuração `alembic.ini`
  3. Um diretório `versions` dentro de `alembic`, onde cada arquivo de migração futura será salvo

> Exemplo de estrutura depois do `alembic init alembic`:

```
seu_projeto/
│
├─ alembic.ini
├─ alembic/
│   ├─ env.py
│   ├─ script.py.mako
│   └─ versions/
```

* **`alembic.ini`**: contém a URL do banco e configurações gerais do Alembic.
* **`env.py`**: é o script que conecta o Alembic ao seu banco (você configura aqui a URL e importa os modelos).
* **`versions/`**: cada alteração no banco será registrada aqui como um script Python separado.

---

### **Quando usar Alembic**

Use Alembic quando você:

1. **Quer evoluir o banco** sem perder dados.

   * Ex: adicionar uma coluna nova, mudar um tipo de dado, criar índices.
2. **Tem equipes trabalhando juntas** e precisam sincronizar alterações do banco.
3. **Quer versionar seu banco** de forma controlada, junto com o código.

> Sem Alembic, cada mudança exigiria apagar o banco ou escrever SQL manual. Com Alembic, você mantém histórico de mudanças, reverte alterações, e aplica automaticamente em diferentes ambientes (desenvolvimento, teste, produção).

---

### **Próximos passos após `alembic init`**

1. Configurar `alembic.ini` para apontar para seu banco (Neon ou local).
2. Editar `alembic/env.py` para importar seus modelos (`Base.metadata`).
3. Criar migração inicial:

   ```bash
   alembic revision --autogenerate -m "Criando tabelas iniciais"
   ```
4. Aplicar migração no banco:

   ```bash
   alembic upgrade head
   ```

---

