## Databricks Cert Prep

App simples em Streamlit para praticar o quiz de `Databricks Certified Data Analyst Associate`.

## Estrutura

```text
.
├── app.py
├── data/
│   └── quiz-data-analyst-associate.md
├── docs/
│   ├── databricks-certified-data-analyst-associate-oct-2025.pdf
│   └── resumo-estudo.md
├── main.py
├── pyproject.toml
├── requirements.txt
└── src/
    └── databrickscertprep/
        ├── __init__.py
        └── app.py
```

## Executar

**Local:**

```bash
pip install -r requirements.txt
streamlit run app.py
```

**Docker Compose:**

```bash
docker-compose up
```

Acesse em [http://localhost:8501](http://localhost:8501).

Para rodar em background:

```bash
docker-compose up -d
docker-compose down  # para encerrar
```

## Conteúdo

- O quiz fica em `data/quiz-data-analyst-associate.md`.
- Os materiais de apoio ficam em `docs/`.
