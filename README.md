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
│       ├── navigation.py
│       ├── question.py
│       ├── results.py
│       ├── sidebar.py
│       └── styles.py
├── Makefile
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── requirements.txt
```

## Executar

**Local:**

```bash
make install
make run
```

Ou manualmente:

```bash
pip install -r requirements.txt
PYTHONPATH=src streamlit run src/app.py
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

## Conteúdo

- Os quizzes ficam em `data/` (padrão e avançado).
- Os materiais de apoio ficam em `docs/`.
