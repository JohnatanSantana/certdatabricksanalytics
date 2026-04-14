# 🧱 Databricks Cert Prep

> App  em Streamlit para praticar o quiz da certificação **Databricks Certified Data Analyst Associate**.

📖 Antes de começar, leia o [`docs/resumo-estudo.md`](docs/resumo-estudo.md)

---

## ✨ Funcionalidades

- 🧪 **80 questões** divididas em modo Padrão e Avançado
- ✅ Feedback imediato com conceito-chave por questão
- 📊 Progresso em tempo real por seção
- 🕐 Histórico de sessões com revisão completa das respostas
- 🧭 Navegação rápida entre questões
- 💾 Persistência local via SQLite

---

## 🗂️ Estrutura

```text
.
├── 📁 data/
│   ├── quiz-data-analyst-associate.md   # 40 questões padrão
│   └── quiz-advanced.md                 # 40 questões avançado
├── 📁 docs/
│   ├── databricks-certified-data-analyst-associate-oct-2025.pdf
│   └── resumo-estudo.md                 # guia de estudo completo
├── 📁 src/
│   ├── app.py                           # orquestração principal
│   ├── database/repository.py           # SQLite
│   ├── quiz/loader.py                   # parser do markdown
│   ├── schema/models.py                 # dataclasses
│   ├── state/session.py                 # session state
│   └── ui/                             # componentes Streamlit
│       ├── history.py
│       ├── navigation.py
│       ├── question.py
│       ├── results.py
│       ├── sidebar.py
│       └── styles.py
├── Makefile
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── uv.lock
```

---

## 🚀 Executar

### ⚡ Local (recomendado)

Requer [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
make install   # uv sync
make run       # abre em http://localhost:8501
```

<details>
<summary>Ou manualmente</summary>

```bash
uv sync
PYTHONPATH=src uv run streamlit run src/app.py
```
</details>

### 🐳 Docker Compose

```bash
make docker-up          # sobe em background
```

Acesse em **[http://localhost:8501](http://localhost:8501)**

```bash
make docker-down        # encerrar
make docker-logs        # acompanhar logs
make docker-build       # rebuild da imagem
```

---

## 🛠️ Outros comandos

```bash
make lock    # atualizar uv.lock após mudar dependências
make clean   # remover __pycache__ e .pyc
```

---

## 📚 Conteúdo de estudo

| Arquivo | Descrição |
|---|---|
| [`data/quiz-data-analyst-associate.md`](data/quiz-data-analyst-associate.md) | 40 questões nível padrão |
| [`data/quiz-advanced.md`](data/quiz-advanced.md) | 40 questões nível avançado |
| [`docs/resumo-estudo.md`](docs/resumo-estudo.md) | Resumo completo com SQL, Unity Catalog, Delta Lake e mais |
| [`docs/databricks-certified-data-analyst-associate-oct-2025.pdf`](docs/databricks-certified-data-analyst-associate-oct-2025.pdf) | Guia oficial do exame (out/2025) |

---

## 🧰 Stack

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.44+-red?logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-local-lightgrey?logo=sqlite)
![uv](https://img.shields.io/badge/uv-package%20manager-purple)
![Docker](https://img.shields.io/badge/Docker-compose-2496ED?logo=docker&logoColor=white)
