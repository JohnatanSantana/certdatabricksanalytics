## Databricks Cert Prep

App em Streamlit para praticar o quiz de `Databricks Certified Data Analyst Associate`.

Antes leia o docs/resumo-estudo.md

## Estrutura

```text
.
├── data/
│   ├── quiz-data-analyst-associate.md
│   └── quiz-advanced.md
├── docs/
│   ├── databricks-certified-data-analyst-associate-oct-2025.pdf
│   └── resumo-estudo.md
├── src/
│   ├── app.py
│   ├── database/
│   │   └── repository.py
│   ├── quiz/
│   │   └── loader.py
│   ├── schema/
│   │   └── models.py
│   ├── state/
│   │   └── session.py
│   └── ui/
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

## Executar

**Local:**

```bash
make install   # uv sync
make run       # uv run streamlit run src/app.py
```

Ou manualmente:

```bash
uv sync
PYTHONPATH=src uv run streamlit run src/app.py
```

**Docker Compose:**

```bash
make docker-up
```

Acesse em [http://localhost:8501](http://localhost:8501).

```bash
make docker-down   # encerrar
make docker-logs   # ver logs
make docker-build  # rebuild da imagem
```

## Outros comandos

```bash
make lock    # atualizar uv.lock
make clean   # remover __pycache__ e .pyc
```

## Conteúdo

- Os quizzes ficam em `data/` (padrão e avançado).
- Os materiais de apoio ficam em `docs/`.
