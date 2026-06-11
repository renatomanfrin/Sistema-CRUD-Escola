# Projeto API Escola

Este projeto é uma API escolar construída com FastAPI, SQLAlchemy e PostgreSQL. Ele permite gerenciar estudantes, perfis de estudantes, professores, disciplinas e matrículas, além de fornecer uma interface HTML simples para consulta, cadastro e exclusão. Desenvolvido como parte dos estudos e práticas realizadas nos cursos da Alura.

## Tecnologias usadas

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- HTML/CSS/JavaScript embutidos na homepage

## Estrutura do projeto

- `main.py` - define a aplicação FastAPI, endpoints REST e página inicial HTML interativa.
- `database.py` - configuração da conexão com o banco de dados PostgreSQL e criação da sessão SQLAlchemy.
- `models.py` - definição dos modelos ORM para `Estudante`, `Perfil`, `Professor`, `Disciplina` e `Matricula`.
- `schemas.py` - modelos Pydantic para validação e serialização de dados de entrada/saída.
- `.gitignore` - regras para proteger arquivos sensíveis e ignorar artefatos locais.

## Modelo de dados

### Estudante

- `id` - identificador único do estudante.
- `nome` - nome do estudante.
- `email` - email do estudante.
- `perfil` - relação de um para um com `Perfil`.

### Perfil

- Usa `estudante_id` como chave primária e chave estrangeira para `Estudante`.
- `idade` - idade do estudante.
- `endereco` - endereço do estudante.
- Isso faz com que o perfil compartilhe o ID do estudante, evitando IDs duplicados.

### Professor

- `id` - identificador único.
- `nome` - nome do professor.
- `email` - email do professor.

### Disciplina

- `id` - identificador único.
- `nome` - nome da disciplina.
- `professor_id` - referência opcional para o professor responsável.

### Matricula

- `id` - identificador único da matrícula.
- `estudante_id` - referência ao estudante.
- `disciplina_id` - referência à disciplina.
- Resposta da matrícula inclui os campos extras:
  - `estudante_nome`
  - `disciplina_nome`
  - `professor_nome`

## Endpoints disponíveis

### Estudantes

- `GET /estudantes/` - listar todos os estudantes.
- `POST /estudantes/` - cadastrar novo estudante com perfil.
- `DELETE /estudantes/{estudante_id}` - excluir estudante.

### Professores

- `GET /professores/` - listar todos os professores.
- `POST /professores/` - cadastrar novo professor.
- `DELETE /professores/{professor_id}` - excluir professor.

### Disciplinas

- `GET /disciplinas/` - listar todas as disciplinas.
- `POST /disciplinas/` - cadastrar nova disciplina.
- `DELETE /disciplinas/{disciplina_id}` - excluir disciplina.

### Matrículas

- `GET /matriculas/` - listar todas as matrículas com nomes de estudante, disciplina e professor.
- `POST /matriculas/` - cadastrar nova matrícula.
- `DELETE /matriculas/{matricula_id}` - excluir matrícula.

## Homepage interativa

A rota raiz `/` exibe um painel HTML com seções para:

- carregar listas de cada recurso
- cadastrar estudantes, professores, disciplinas e matrículas
- excluir registros por ID

O painel usa JavaScript embutido para chamar os endpoints da API.

## Configuração do banco de dados

A conexão com PostgreSQL está definida em `database.py`:

```python
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/escola"
```

> Recomenda-se manter credenciais fora do controle de versão usando variáveis de ambiente ou um arquivo `.env`.

## Como executar

1. Ative o ambiente virtual:

```powershell
& "d:\ALURA\1.python\Banco de dados\Projeto\venv\Scripts\Activate.ps1"
```

2. Instale as dependências:

```powershell
pip install -r requirements.txt
```

3. Execute a API:

```powershell
uvicorn main:app --reload
```

4. Acesse a homepage em:

```text
http://127.0.0.1:8000/
```

## Segurança e arquivos sensíveis

O arquivo `.gitignore` inclui regras para evitar o versionamento de:

- ambientes virtuais (`venv/`, `.venv/`, etc.)
- arquivos de configuração de ambiente (`.env`, `*.env`, `.env.*`)
- chaves e certificados (`*.key`, `*.pem`, `*.crt`, etc.)
- dumps e arquivos de banco de dados locais (`*.db`, `*.sqlite`, `*.sql`, `*.dump`)
- histórico de clientes SQL (`.pgpass`, `.psql_history`, `.mysql_history`)
- caches de ferramentas Python e relatórios de cobertura
- metadados de IDE/editor e arquivos temporários

