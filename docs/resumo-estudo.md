# Resumo de Estudo — Databricks Certified Data Analyst Associate
> Novidades pós-2023, trade-offs de escolha, comandos SQL e Databricks Assistant
> Atualizado com base no Exam Guide (Oct 2025) + documentação oficial

---

## 1. DATABRICKS ASSISTANT (Genie Code)

O assistente foi renomeado de **Databricks Assistant** para **Genie Code**. Disponível no SQL Editor e Notebooks.

### Slash Commands (Notebooks)

| Comando | O que faz |
|---|---|
| `/` | Exibe a lista de comandos disponíveis |
| `/explain` | Explica o código da célula atual em linguagem natural |
| `/fix` | Propõe correção de erros em **diff view** (Accept/Reject — não executa automaticamente) |
| `/optimize` | Avalia e melhora SQL, Python e PySpark. Disponível também no **SQL Editor** |
| `/doc` | Adiciona comentários/docstrings ao código em **diff view** |
| `/prettify` | Formata o código (indentação, espaçamento) sem alterar a lógica |
| `/findTables` | Busca tabelas relevantes no Unity Catalog. Use "feature tables" para feature tables de ML |
| `/findQueries` | Busca queries salvas relevantes no Unity Catalog |
| `/rename` | Sugere novos nomes para células e outros elementos |
| `/repairEnvironment` | Diagnostica falhas de ambiente (ex: erro de instalação de library) |

> **Importante para a prova:**
> - `/fix` e `/doc` sempre abrem **diff view** — você aceita ou rejeita, nunca são aplicados automaticamente
> - `/optimize` é o único slash command disponível tanto em **Notebooks quanto no SQL Editor**
> - Use `@catalog.schema.tabela` para referenciar tabelas Unity Catalog em qualquer prompt
> - **Quick Fix** (automático ao errar uma célula) e **Diagnose Error** (botão no output de erro) executam `/fix` automaticamente

### Quando usar cada comando — trade-off

| Situação | Comando certo |
|---|---|
| Query retornando resultado inesperado | `/explain` → entenda o que está fazendo |
| Query com erro de sintaxe ou lógica | `/fix` |
| Query lenta ou mal escrita | `/optimize` |
| Código sem documentação | `/doc` |
| Código desformatado | `/prettify` |
| Não sabe qual tabela usar | `/findTables` |

---

## 2. NOVIDADES SQL PÓS-2023

### QUALIFY — Filtrar resultados de Window Functions

`QUALIFY` é para window functions o que `HAVING` é para aggregations.

**Sintaxe:**
```sql
SELECT coluna, window_function(...) OVER (...) AS alias
FROM tabela
QUALIFY boolean_expression;
```

**Exemplo: manter apenas o 1º lugar por categoria**
```sql
-- Com window function no SELECT
SELECT cidade, modelo, RANK() OVER (PARTITION BY modelo ORDER BY quantidade) AS rank
FROM estoque
QUALIFY rank = 1;

-- Com window function diretamente no QUALIFY
SELECT cidade, modelo
FROM estoque
QUALIFY RANK() OVER (PARTITION BY modelo ORDER BY quantidade) = 1;
```

**Por que usar QUALIFY em vez de subquery?**
```sql
-- Sem QUALIFY (verboso)
SELECT cidade, modelo FROM (
  SELECT cidade, modelo, RANK() OVER (PARTITION BY modelo ORDER BY quantidade) AS rank
  FROM estoque
) WHERE rank = 1;

-- Com QUALIFY (limpo)
SELECT cidade, modelo
FROM estoque
QUALIFY RANK() OVER (PARTITION BY modelo ORDER BY quantidade) = 1;
```

> **Regra:** não pode usar aggregation no QUALIFY. Requer ao menos uma window function no SELECT ou no próprio QUALIFY.

---

### PIVOT — Transformar linhas em colunas

```sql
SELECT *
FROM vendas_trimestrais
PIVOT (SUM(vendas) FOR trimestre IN ('Q1', 'Q2', 'Q3', 'Q4'));
```

---

### UNPIVOT — Transformar colunas em linhas (inverso do PIVOT)

```sql
-- EXCLUDE NULLS é o padrão; use INCLUDE NULLS para manter linhas nulas
SELECT *
FROM vendas_trimestrais
UNPIVOT INCLUDE NULLS (vendas FOR trimestre IN (q1 AS 'Q1', q2 AS 'Q2', q3 AS 'Q3', q4 AS 'Q4'));
```

---

### Window Functions — Referência completa

```sql
SELECT
  cliente_id,
  valor,
  data,

  -- Ranking
  ROW_NUMBER() OVER (PARTITION BY regiao ORDER BY valor DESC) AS row_num,
  RANK()       OVER (PARTITION BY regiao ORDER BY valor DESC) AS rank,       -- gaps nos empates
  DENSE_RANK() OVER (PARTITION BY regiao ORDER BY valor DESC) AS dense_rank, -- sem gaps

  -- Navegação
  LAG(valor, 1)  OVER (PARTITION BY cliente_id ORDER BY data) AS valor_anterior,
  LEAD(valor, 1) OVER (PARTITION BY cliente_id ORDER BY data) AS proximo_valor,
  FIRST_VALUE(valor) OVER (PARTITION BY cliente_id ORDER BY data) AS primeiro_valor,
  LAST_VALUE(valor)  OVER (PARTITION BY cliente_id ORDER BY data
                           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS ultimo_valor,

  -- Agregação com janela
  SUM(valor) OVER (PARTITION BY regiao ORDER BY data
                   ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS acumulado,
  AVG(valor) OVER (PARTITION BY regiao) AS media_regiao

FROM pedidos;
```

**QUALIFY com window functions — casos de uso típicos na prova:**

```sql
-- Top 3 produtos por categoria
SELECT categoria, produto, total_vendas
FROM resumo
QUALIFY ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY total_vendas DESC) <= 3;

-- Remover duplicatas, manter o registro mais recente
SELECT *
FROM eventos
QUALIFY ROW_NUMBER() OVER (PARTITION BY id ORDER BY timestamp DESC) = 1;
```

---

### RANK vs ROW_NUMBER vs DENSE_RANK

| Função | Empates | Gaps | Resultado exemplo (3 empates no 1º lugar) |
|---|---|---|---|
| `ROW_NUMBER()` | Desempata aleatoriamente | Sem gaps | 1, 2, 3 |
| `RANK()` | Mesma posição | **Com gaps** | 1, 1, 1, 4 |
| `DENSE_RANK()` | Mesma posição | **Sem gaps** | 1, 1, 1, 2 |

---

## 3. TRADE-OFFS PRINCIPAIS

### Managed Table vs External Table

| | Managed Table | External Table |
|---|---|---|
| Gerenciado por | Unity Catalog | Você (storage externo) |
| `DROP TABLE` remove dados? | **Sim** (metadados + arquivos) | **Não** (só metadados) |
| Ideal para | Dados novos criados no Databricks | Dados pré-existentes no cloud storage |

> **Questão frequente:** DROP TABLE executado e arquivos ainda existem no S3 → **External Table**

---

### Streaming Table vs Materialized View vs Dynamic View

| | Streaming Table | Materialized View | Dynamic View |
|---|---|---|---|
| Armazena fisicamente? | Sim | Sim | Não |
| Atualização | Incremental (novos eventos) | Batch refresh (periódico) | Sempre em tempo real |
| Caso de uso | IoT, clickstream, eventos contínuos | Aggregations pesadas para BI | Mascaramento de PII, row-level security |
| Suporta Column Masks? | Sim (desde 2024) | Sim (desde 2024) | Sim (nativo via CASE/is_member) |

> **Regra simples:**
> - Dados chegando continuamente → **Streaming Table**
> - Query pesada pré-computada → **Materialized View**
> - Mascarar colunas por grupo → **Dynamic View** ou Column Mask

---

### Liquid Clustering vs Particionamento vs ZORDER

| | Partitioning | ZORDER | Liquid Clustering |
|---|---|---|---|
| Sintaxe | `PARTITIONED BY (col)` | `OPTIMIZE ... ZORDER BY (col)` | `CLUSTER BY (col)` |
| Flexibilidade | Baixa (fixo na criação) | Média (muda por operação) | Alta (pode alterar depois) |
| Ideal para | Colunas de baixa cardinalidade, filtros fixos | Filtragem secundária após partição | Filtros variáveis, alta cardinalidade |
| Atualização | Recriar tabela | Rodar OPTIMIZE manualmente | Incremental e automático |
| Suporta streaming | Limitado | Não | **Sim** |

```sql
-- Criar com Liquid Clustering
CREATE TABLE catalog.schema.eventos CLUSTER BY (regiao, categoria);

-- Alterar tabela existente
ALTER TABLE catalog.schema.eventos CLUSTER BY (regiao, categoria);

-- Clustering automático (Databricks decide as colunas)
ALTER TABLE catalog.schema.eventos CLUSTER BY AUTO;
```

---

### UNION vs UNION ALL

| | UNION | UNION ALL |
|---|---|---|
| Remove duplicatas? | Sim (mais lento) | Não (mais rápido) |
| Quando usar | Resultado precisa ser único | Performance ou duplicatas são esperadas |

---

### WHERE vs HAVING vs QUALIFY

| Cláusula | Filtra | Pode usar aggregate? | Pode usar window function? |
|---|---|---|---|
| `WHERE` | Linhas **antes** do GROUP BY | **Não** | Não |
| `HAVING` | Grupos **após** o GROUP BY | **Sim** | Não |
| `QUALIFY` | Resultados de window functions | Não | **Sim** |

```sql
-- WHERE: filtro simples de linhas
SELECT * FROM pedidos WHERE status = 'ativo';

-- HAVING: filtro em resultado de agregação
SELECT cliente_id, COUNT(*) FROM pedidos GROUP BY cliente_id HAVING COUNT(*) > 5;

-- QUALIFY: filtro em resultado de window function
SELECT cliente_id, valor FROM pedidos QUALIFY ROW_NUMBER() OVER (PARTITION BY cliente_id ORDER BY data DESC) = 1;
```

---

### SQL Alert vs Dashboard Refresh vs Job

| Cenário | Ferramenta |
|---|---|
| Notificar quando valor ultrapassa threshold | **SQL Alert** |
| Atualizar dados do dashboard automaticamente | **Scheduled Dashboard Refresh** |
| Executar pipeline/notebook em horário fixo | **Lakeflow Job** |

---

### SQL Alert — Estados e Mensagens de Notificação

#### Estados do alerta

| Estado | Quando ocorre |
|---|---|
| **`TRIGGERED`** | Última execução: coluna avaliada **satisfez** a condição + threshold configurados |
| **`OK`** | Última execução: condição **não** foi satisfeita (valor voltou ao normal) |
| **`ERROR`** | Ocorreu um erro durante a avaliação do alerta |

> A versão atual **não possui** o estado `UNKNOWN` (existia em versões legadas).

#### Quando a notificação é disparada

- **Padrão:** apenas quando o estado muda para `TRIGGERED`
- **Opção "Notify when OK":** envia notificação também quando o estado volta para `OK`
- **Opção "Notify periodically":** reenvio periódico enquanto permanecer `TRIGGERED` (útil para alertas críticos que precisam de ação)

#### Tipos de condição

| Operador | Exemplo |
|---|---|
| `>` maior que | vendas > 10000 |
| `>=` maior ou igual | erros >= 5 |
| `<` menor que | estoque < 50 |
| `<=` menor ou igual | uptime <= 0.99 |
| `=` igual a | status = 0 |
| `!=` diferente de | status != 'ok' |

Agregações suportadas no valor avaliado: `SUM`, `AVERAGE`, ou o valor da primeira linha/coluna.

> **Queries com parâmetros não são suportadas** em SQL Alerts.

#### Template de mensagem personalizada

As notificações aceitam **variáveis de template** entre `{{ }}`:

| Variável | Conteúdo |
|---|---|
| `{{ALERT_NAME}}` | Nome do alerta |
| `{{ALERT_STATUS}}` | Estado atual: `TRIGGERED`, `OK` ou `ERROR` |
| `{{ALERT_CONDITION}}` | Operador da condição configurada |
| `{{ALERT_THRESHOLD}}` | Valor do threshold configurado |
| `{{ALERT_COLUMN}}` | Coluna avaliada |
| `{{ALERT_URL}}` | Link direto para o alerta no workspace |
| `{{QUERY_RESULT_VALUE}}` | Valor encontrado na última execução |
| `{{QUERY_RESULT_ROWS}}` | Número de linhas retornadas |
| `{{QUERY_RESULT_COLS}}` | Número de colunas retornadas |
| `{{QUERY_RESULT_TABLE}}` | Primeiras 100 linhas em formato HTML (só e-mail) |

**Exemplo de mensagem:**
```
Alerta: {{ALERT_NAME}} está {{ALERT_STATUS}}
Valor atual: {{QUERY_RESULT_VALUE}} (threshold: {{ALERT_CONDITION}} {{ALERT_THRESHOLD}})
Ver detalhes: {{ALERT_URL}}
```

> Formatação **HTML** é suportada apenas para destinos do tipo **e-mail**.

Ref: [sql/user/alerts](https://docs.databricks.com/aws/en/sql/user/alerts/)

---

### Auto Loader vs COPY INTO vs Delta Sharing

| | Auto Loader | COPY INTO | Delta Sharing |
|---|---|---|---|
| Detecta arquivos novos automaticamente? | **Sim** | Não (precisa de job) | N/A |
| Tipo de ingestão | Contínua, incremental | Batch, pontual | Compartilhamento cross-platform |
| Suporta streaming | **Sim** | Não | Não |
| Ideal para | S3 com novos arquivos chegando continuamente | Carga inicial ou batch periódica | Parceiros externos sem copiar dados |

---

### Photon vs Cache vs Liquid Clustering

| Problema | Solução |
|---|---|
| SQL/DataFrame lento em geral | **Photon** (engine C++, transparente) |
| Mesma query rodada várias vezes | **Result Cache** do SQL Warehouse |
| Filtros lentos em tabela grande | **Liquid Clustering** nas colunas de filtro |
| Shuffle excessivo, join caro | **Query Profiler** para diagnosticar |

---

### Query Profile — Analisar performance com o DAG

O **Query Profile** exibe a execução de uma query como um **DAG (Directed Acyclic Graph)** — um grafo onde cada nó é um operador e as arestas representam o fluxo de dados.

> Acesse via: SQL Editor → resultado da query → aba **Query Profile**

**O que o DAG mostra:**

| Operador | O que significa |
|---|---|
| **Scan** | Leitura de dados de uma fonte (tabela, arquivo) |
| **Filter** | Aplicação de condição WHERE — reduz linhas |
| **Join** | Combinação de linhas de múltiplas fontes |
| **Shuffle** | Redistribuição de dados entre executores — **operação cara** |
| **Hash / Sort** | Agrupamento e agregação por chave |
| **Union** | Concatenação de linhas com mesmo schema |

**Métricas disponíveis por nó (clique no operador):**
- **Time spent** — tempo de execução do operador
- **Rows processed** — quantidade de linhas processadas/emitidas
- **Memory peak** — pico de memória consumida

**Como identificar gargalos:**
1. Localize operadores com **alto tempo** ou **muitas linhas inesperadas**
2. **Shuffle excessivo** → considere Liquid Clustering ou broadcast join
3. **Scan com muitas linhas** → filtros não estão sendo aplicados no storage (revisar particionamento/clustering)
4. **Join caro** → verificar se a ordem dos joins está otimizada

> **Atenção:** Query Profile **não está disponível para resultados em cache**. Para forçar re-execução, modifique ou remova o `LIMIT` da query.

Ref: [query-profile#explore-the-dag](https://docs.databricks.com/aws/en/sql/user/queries/query-profile#explore-the-dag)

---

### ANALYZE TABLE — Coletar estatísticas para o otimizador

Coleta estatísticas estimadas de uma tabela para que o **query optimizer** gere planos de execução mais eficientes.

> Para Unity Catalog managed tables, prefira habilitar **Predictive Optimization** — ele executa `ANALYZE` automaticamente.

**Sintaxe:**
```sql
-- Tabela inteira (row count + size em bytes)
ANALYZE TABLE tabela COMPUTE STATISTICS;

-- Apenas tamanho em bytes (sem full scan — rápido)
ANALYZE TABLE tabela COMPUTE STATISTICS NOSCAN;

-- Estatísticas por coluna (min, max, nulls, distinct count, avg length)
ANALYZE TABLE tabela COMPUTE STATISTICS FOR COLUMNS col1, col2;
ANALYZE TABLE tabela COMPUTE STATISTICS FOR ALL COLUMNS;

-- Estatísticas Delta (recomputa no Delta log — Runtime 14.3 LTS+)
ANALYZE TABLE tabela COMPUTE DELTA STATISTICS;

-- Todas as tabelas de um schema
ANALYZE TABLES IN schema_name COMPUTE STATISTICS;
```

**O que cada opção coleta:**

| Opção | Coleta | Custo |
|---|---|---|
| *(padrão)* | Row count + size em bytes | Full scan |
| `NOSCAN` | Apenas size em bytes | Sem scan — muito rápido |
| `FOR COLUMNS` | Min, max, nulls, distinct count, avg/max length | Full scan + extra |
| `FOR ALL COLUMNS` | Igual acima para todas as colunas | Full scan + extra |
| `COMPUTE DELTA STATISTICS` | Estatísticas no Delta log para data skipping | Incremental |

> **Limitações:**
> - `FOR COLUMNS` é incompatível com `PARTITION`
> - `PARTITION` não é suportado em tabelas Delta
> - Após definir novas colunas de estatísticas Delta, rode `COMPUTE DELTA STATISTICS` **e depois** `COMPUTE STATISTICS` em sequência

**Quando usar:**
- Antes de queries críticas após grandes modificações de dados
- Quando o Query Profile mostrar planos de join ruins ou scans inesperadamente grandes
- Ao adicionar novas colunas para Delta data skipping

Ref: [sql-ref-syntax-aux-analyze-compute-statistics](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-aux-analyze-compute-statistics)

---

### WATERMARK — Controle de atraso em streaming

Disponível a partir do **Databricks Runtime 12.0**. A cláusula `WATERMARK` define um **limiar de atraso** para dados que chegam fora de ordem em pipelines de streaming stateful (stream-stream joins, agregações por janela de tempo).

**Sintaxe (dentro do FROM):**
```sql
FROM tabela
  WATERMARK named_expression DELAY OF interval
```

**Exemplos:**
```sql
-- Usando coluna de timestamp já existente
SELECT window(ts, '1 minute'), COUNT(*)
FROM eventos
  WATERMARK ts DELAY OF INTERVAL 10 SECONDS
GROUP BY window(ts, '1 minute');

-- Derivando timestamp a partir de coluna string
SELECT window(event_time, '5 minutes'), SUM(valor)
FROM vendas
  WATERMARK to_timestamp(event_ts) DELAY OF INTERVAL 30 SECONDS
GROUP BY window(event_time, '5 minutes');

-- Stream-stream join com watermark nos dois lados
SELECT a.id, b.descricao
FROM pedidos
    WATERMARK ts DELAY OF INTERVAL 1 MINUTES AS a
JOIN pagamentos
    WATERMARK ts DELAY OF INTERVAL 1 MINUTES AS b
ON a.id = b.pedido_id;
```

**Parâmetros:**

| Parâmetro | Regra |
|---|---|
| `named_expression` | Deve ser do tipo **timestamp** — referência a coluna existente ou transformação determinística (ex: `to_timestamp()`) |
| `DELAY OF interval` | Valor positivo, **menor que 1 mês** — define a "janela de tolerância" para dados atrasados |

**Como funciona:**
- O watermark avança conforme o **maior timestamp visto** menos o `DELAY`
- Dados que chegam com timestamp **anterior ao watermark atual** são descartados
- Operações stateful (aggregation, join) só fecham a janela quando o watermark ultrapassa o limite da janela

> **Trade-off delay alto vs baixo:**
> | | Delay pequeno | Delay grande |
> |---|---|---|
> | Latência | Baixa | Alta |
> | Tolerância a atraso | Pouca | Muita |
> | Estado mantido em memória | Menos | Mais |

> **Atenção na prova:** WATERMARK é obrigatório em **stream-stream joins** e **agregações por event time** em Streaming Tables. Sem watermark, o estado cresce indefinidamente.

Ref: [sql-ref-syntax-qry-select-watermark](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-watermark)

---

### Funções JSON — Extrair e parsear dados semiestruturados

#### `get_json_object` — extrair um campo por path

```sql
get_json_object(expr, path)
```

Extrai **um único valor** de uma string JSON via [JSONPath](https://goessner.net/articles/JsonPath/). Retorna `NULL` se o caminho não for encontrado.

```sql
SELECT get_json_object('{"user":{"name":"Ana","age":30}}', '$.user.name');
-- Result: Ana

SELECT get_json_object('{"itens":[1,2,3]}', '$.itens[0]');
-- Result: 1
```

---

#### `json_tuple` — extrair múltiplos campos de uma vez

```sql
json_tuple(jsonStr, path1 [, path2, ...])
```

Extrai **vários campos em paralelo** como colunas de uma linha. Retorna `NULL` para campos não encontrados. É uma **função geradora** (table-valued).

```sql
-- Runtime 12.2+ — invocar como referência de tabela (forma recomendada)
SELECT j.*, 'extra'
FROM json_tuple('{"a":1, "b":2}', 'a', 'b') AS j;
-- Result: 1  2  extra

-- Runtime ≤ 12.1 — deve ser a única generator na SELECT list
SELECT json_tuple('{"a":1, "b":2}', 'a', 'b'), 'extra';
```

> **Runtime ≤ 12.1:** usar múltiplos generators na mesma query lança `UNSUPPORTED_GENERATOR.MULTI_GENERATOR`.
> **Runtime ≥ 12.2:** uso via `LATERAL VIEW` ou `SELECT list` está depreciado — prefira como referência de tabela.

---

#### `from_json` — parsear JSON para struct tipado

```sql
from_json(jsonStr, schema [, options])
```

Converte uma string JSON em uma **struct** com schema definido, permitindo acessar campos com notação de ponto.

```sql
-- Schema inline
SELECT from_json('{"a":1, "b":0.8}', 'a INT, b DOUBLE');
-- Result: {a: 1, b: 0.8}

-- Inferir schema automaticamente
SELECT from_json(payload, schema_of_json('{"id":1,"nome":"Ana"}')) AS dados
FROM eventos;

-- Acessar campo da struct resultante
SELECT from_json(payload, 'id INT, nome STRING').nome AS nome
FROM eventos;

-- Com opções de parsing
SELECT from_json(payload, 'ts TIMESTAMP', MAP('timestampFormat', 'yyyy-MM-dd HH:mm:ss'))
FROM logs;
```

> **Case-sensitive:** os nomes de campo no `schema` devem coincidir **exatamente** com os do JSON (maiúsculas/minúsculas incluídas).

---

**Trade-off entre as três funções:**

| Função | Extrai | Retorno | Ideal para |
|---|---|---|---|
| `get_json_object` | 1 campo por chamada | STRING | Campos pontuais, paths aninhados |
| `json_tuple` | N campos de uma vez | Colunas separadas (STRING) | Extrair vários campos sem struct |
| `from_json` | JSON inteiro | STRUCT tipado | Parsear payload completo com tipos corretos |

Refs: [get_json_object](https://docs.databricks.com/aws/en/sql/language-manual/functions/get_json_object) · [json_tuple](https://docs.databricks.com/aws/en/sql/language-manual/functions/json_tuple) · [from_json](https://docs.databricks.com/aws/en/sql/language-manual/functions/from_json)

---

## 4. UNITY CATALOG — PERMISSÕES

### Hierarquia de privileges

```
USE CATALOG    → navegar no catalog (obrigatório para qualquer acesso)
USE SCHEMA     → navegar no schema (obrigatório para acessar tabelas)
SELECT         → ler dados
MODIFY         → INSERT, UPDATE, DELETE
CREATE TABLE   → criar tabelas no schema
CREATE SCHEMA  → criar schemas no catalog
ALL PRIVILEGES → todos acima
```

**Regra da prova — para dar SELECT em uma tabela, o usuário precisa dos 3:**
```sql
GRANT USE CATALOG ON CATALOG gold TO GROUP analysts;
GRANT USE SCHEMA ON SCHEMA gold.finance TO GROUP analysts;
GRANT SELECT ON TABLE gold.finance.budget_summary TO GROUP analysts;
```

### Comandos de permissão

```sql
-- Conceder
GRANT SELECT ON TABLE catalog.schema.tabela TO GROUP nome_grupo;
GRANT CREATE SCHEMA ON CATALOG silver TO USER eng@empresa.com;

-- Revogar
REVOKE SELECT ON TABLE catalog.schema.tabela FROM GROUP nome_grupo;

-- Ver permissões
SHOW GRANTS ON TABLE catalog.schema.tabela;

-- Transferir ownership
ALTER TABLE catalog.schema.tabela OWNER TO `novo_owner@empresa.com`;
```

### Column Mask para PII

```sql
-- Mascarar coluna CPF por grupo
CREATE OR REPLACE FUNCTION catalog.schema.mask_cpf(cpf STRING)
RETURN CASE WHEN is_member('compliance_team') THEN cpf ELSE '***.***.***-**' END;

ALTER TABLE catalog.schema.clientes ALTER COLUMN cpf SET MASK catalog.schema.mask_cpf;
```

---

### Tags no Unity Catalog

Tags são pares **chave = valor** (valor opcional) aplicados a objetos do Unity Catalog para organização, descoberta e governança de dados.

**Objetos suportados:** catálogo, schema, tabela, coluna, view, volume, modelo registrado, dashboard, Genie space.

#### Tipos de tag

| Tipo | Ícone | Quem define | Quem pode atribuir |
|---|---|---|---|
| **Tag livre** | — | Qualquer usuário | Quem tem `APPLY TAG` no objeto |
| **Governed Tag** | 🔒 | Admin de conta | Quem tem `ASSIGN` na tag + `APPLY TAG` no objeto |
| **System Tag** | 🔧 | Databricks (pré-definida) | Controlado por permissões da governed tag |

#### Aplicar e remover tags via SQL

**Runtime ≥ 16.1 — sintaxe `SET TAG` (recomendada):**
```sql
-- Tabela
SET TAG ON TABLE catalog.schema.vendas custo_centro = financeiro;

-- Coluna (PII sem valor)
SET TAG ON COLUMN catalog.schema.clientes.cpf pii;

-- Schema e catálogo
SET TAG ON SCHEMA catalog.schema dominio = finance;
SET TAG ON CATALOG catalog env = producao;

-- Remover
UNSET TAG ON TABLE catalog.schema.vendas custo_centro;
UNSET TAG ON COLUMN catalog.schema.clientes.cpf pii;
```

**Runtime 13.3–16.0 — sintaxe `ALTER ... SET TAGS`:**
```sql
-- Tabela (múltiplas tags de uma vez)
ALTER TABLE catalog.schema.vendas
  SET TAGS ('custo_centro' = 'financeiro', 'env' = 'producao');

ALTER TABLE catalog.schema.vendas
  UNSET TAGS ('custo_centro', 'env');

-- Coluna
ALTER TABLE catalog.schema.clientes
  ALTER COLUMN cpf SET TAGS ('pii' = 'true');

ALTER TABLE catalog.schema.clientes
  ALTER COLUMN cpf UNSET TAGS ('pii');
```

**Permissão necessária:** `APPLY TAG` no objeto + `USE SCHEMA` + `USE CATALOG`. Para governed tags, também `ASSIGN` na tag.

#### Restrições importantes

| Limite | Valor |
|---|---|
| Tags por objeto | Máximo **50** |
| Tags por tabela (colunas) | Máximo **1.000** |
| Tamanho da chave | Máximo **255** caracteres |
| Tamanho do valor | Máximo **1.000** caracteres |
| Caracteres proibidos na chave | `. , - = / :` |
| Busca | Apenas correspondência **exata** |
| Tags em múltiplas colunas | **Uma por comando** |

> **Herança de tags:** tags aplicadas a catálogos propagam para schemas e tabelas **somente** em avaliações de política ABAC — não aparecem como tags diretas dos objetos filhos.

> **Atenção ao dropar coluna com governed tag:** execute `UNSET TAG` antes de dropar a coluna para evitar vazamento de dados.

#### Tag `system:certified`

A tag `system:certified` é uma **System Tag** predefinida pelo Databricks para identificar datasets confiáveis e validados pela organização.

```sql
-- Marcar tabela como certificada
SET TAG ON TABLE catalog.schema.vendas `system:certified`;

-- Alternativa (Runtime 13.3+)
ALTER TABLE catalog.schema.vendas SET TAGS ('system:certified' = '');
```

- Exibida com ícone de medalha no **Catalog Explorer**
- Aparece em destaque nas buscas do workspace
- Apenas usuários com permissão `ASSIGN` na governed tag `system:certified` podem atribuí-la

#### Pesquisar objetos por tag

**Via Catalog Explorer (UI):**
- Barra de busca do workspace → digitar `tag:chave` ou `tag:chave=valor`
- A busca requer correspondência **exata**

**Via SQL — `INFORMATION_SCHEMA`:**
```sql
-- Tags de tabelas no catalog atual
SELECT table_catalog, table_schema, table_name, tag_name, tag_value
FROM information_schema.table_tags
WHERE tag_name = 'system:certified';

-- Tags de colunas
SELECT table_name, column_name, tag_name, tag_value
FROM information_schema.column_tags
WHERE tag_name = 'pii';

-- Outros views disponíveis:
-- information_schema.catalog_tags
-- information_schema.schema_tags
-- information_schema.volume_tags
```

> **Dica de prova:** para encontrar **todos os datasets certificados** de um catalog, use `information_schema.table_tags WHERE tag_name = 'system:certified'`. Para busca cross-catalog, use as system tables de account (`system.information_schema`).

---

## 5. COMANDOS SQL ESSENCIAIS

### Criar e gerenciar tabelas

```sql
-- Criar managed table
CREATE TABLE catalog.schema.tabela (id INT, nome STRING, data DATE);

-- Criar ou substituir (mantém privilégios e history — Use em vez de DROP + CREATE)
CREATE OR REPLACE TABLE catalog.schema.tabela (id INT, nome STRING);

-- Criar tabela a partir de query
CREATE TABLE gold.sales.resumo AS
SELECT regiao, SUM(valor) AS total FROM silver.sales.transacoes GROUP BY regiao;

-- Criar external table
CREATE TABLE catalog.schema.tabela_ext (id INT, valor DOUBLE)
LOCATION 's3://bucket/caminho/';

-- IF NOT EXISTS (não substitui, não recria se já existir)
CREATE TABLE IF NOT EXISTS catalog.schema.tabela (id INT);
```

### Delta Lake — Time Travel e Manutenção

```sql
-- Ver histórico de versões
DESCRIBE HISTORY minha_tabela;

-- Time travel por versão
SELECT * FROM minha_tabela VERSION AS OF 10;

-- Time travel por timestamp absoluto
SELECT * FROM minha_tabela TIMESTAMP AS OF '2024-06-01 00:00:00';

-- Time travel por timestamp dinâmico (7 dias atrás)
SELECT * FROM minha_tabela TIMESTAMP AS OF date_sub(current_date(), 7);

-- Restaurar tabela para versão anterior
RESTORE TABLE minha_tabela TO VERSION AS OF 5;
RESTORE TABLE minha_tabela TO TIMESTAMP AS OF '2024-01-01';

-- Limpar arquivos antigos (limita time travel após execução!)
VACUUM minha_tabela RETAIN 168 HOURS;  -- 7 dias = padrão mínimo seguro

-- Otimizar arquivos (compactação + aplicar clustering)
OPTIMIZE minha_tabela;
OPTIMIZE minha_tabela ZORDER BY (coluna);  -- legado, prefira Liquid Clustering
```

> **VACUUM e time travel:** após `VACUUM`, não é possível fazer time travel antes do período de retenção. Se uma query de time travel falha, VACUUM é a causa mais provável.

---

### CREATE TABLE CLONE — Copiar tabelas Delta

Duplica uma tabela Delta (ou Parquet/Iceberg) para um destino, opcionalmente em uma versão específica.

**Sintaxe:**
```sql
CREATE TABLE [IF NOT EXISTS] tabela_destino [SHALLOW | DEEP] CLONE tabela_origem
  [TBLPROPERTIES (...)]
  [LOCATION 'caminho'];

[CREATE OR] REPLACE TABLE tabela_destino [SHALLOW | DEEP] CLONE tabela_origem;
```

**Deep Clone (padrão) vs Shallow Clone:**

| | Deep Clone | Shallow Clone |
|---|---|---|
| Copia arquivos de dados? | **Sim** — cópia completa e independente | **Não** — referencia arquivos da origem |
| Independência | Total (alterações não afetam a origem) | Dependente (arquivos da origem devem existir) |
| Custo de storage | Alto | Baixo |
| Ideal para | Migração, backup, ML reproducibility | Experimentos temporários, testes rápidos |

```sql
-- Deep clone (cópia completa)
CREATE TABLE gold.backup.vendas DEEP CLONE gold.sales.vendas;

-- Shallow clone (referencia arquivos da origem)
CREATE TABLE sandbox.teste.vendas SHALLOW CLONE gold.sales.vendas;

-- Clone de versão específica (time travel)
CREATE TABLE gold.backup.vendas CLONE gold.sales.vendas VERSION AS OF 10;

-- Substituir tabela existente
CREATE OR REPLACE TABLE sandbox.teste.vendas SHALLOW CLONE gold.sales.vendas;
```

> **Casos de uso típicos na prova:**
> - Ambiente de teste sem duplicar dados → **Shallow Clone**
> - Backup antes de operação destrutiva → **Deep Clone**
> - Reproduzir experimento de ML em versão específica → **Deep Clone + VERSION AS OF**
> - Iceberg managed table → apenas **Deep Clone** suportado

Ref: [delta-clone](https://docs.databricks.com/aws/en/sql/language-manual/delta-clone)

---

### Aggregate Functions

```sql
SELECT
  regiao,
  COUNT(*)                        AS total_pedidos,
  COUNT(DISTINCT cliente_id)      AS clientes_unicos,
  APPROX_COUNT_DISTINCT(cliente_id) AS aprox_clientes,  -- mais rápido para grandes volumes
  AVG(valor)                      AS ticket_medio,
  SUM(valor)                      AS receita_total,
  MIN(valor)                      AS menor_pedido,
  MAX(valor)                      AS maior_pedido,
  STDDEV(valor)                   AS desvio_padrao,
  PERCENTILE(valor, 0.5)          AS mediana
FROM pedidos
GROUP BY regiao
HAVING COUNT(*) > 100
ORDER BY receita_total DESC;

-- Summary statistics de toda a tabela
SELECT SUMMARY(*) FROM tabela;  -- retorna count, mean, stddev, min, max, percentis
```

---

### Joins

```sql
-- INNER JOIN — apenas correspondências em ambos
SELECT a.id, b.nome_produto
FROM pedidos a INNER JOIN produtos b ON a.produto_id = b.id;

-- LEFT JOIN — todos de A, NULL quando B não tem correspondência
SELECT c.nome, COUNT(p.id) AS total_pedidos
FROM clientes c LEFT JOIN pedidos p ON c.id = p.cliente_id
GROUP BY c.nome;

-- RIGHT JOIN — todos de B, NULL quando A não tem correspondência
-- FULL OUTER JOIN — todos de ambos

-- JOIN com múltiplos critérios
SELECT * FROM tabela_a a
JOIN tabela_b b ON a.id = b.id AND a.regiao = b.regiao;
```

---

### Limpeza de dados

```sql
-- Remover linhas inválidas
DELETE FROM tabela WHERE coluna IS NULL OR valor < 0;

-- Corrigir valores
UPDATE tabela SET status = 'unknown' WHERE status IS NULL;

-- Tratar nulos em SELECT
SELECT id, COALESCE(email, 'sem_email') AS email FROM clientes;
SELECT id, IFNULL(telefone, 'N/A') AS telefone FROM clientes;
SELECT id, NVL(cidade, 'N/A') AS cidade FROM clientes;

-- Verificar nulos
SELECT COUNT(*) AS total, COUNT(email) AS com_email,
       COUNT(*) - COUNT(email) AS sem_email FROM clientes;
```

---

### Views

```sql
-- Dynamic View (calculada em tempo real)
CREATE OR REPLACE VIEW gold.sales.vw_ativas AS
SELECT * FROM silver.sales.transacoes WHERE status = 'ativa';

-- Materialized View (cache físico, refresh periódico)
CREATE OR REPLACE MATERIALIZED VIEW gold.sales.mv_resumo AS
SELECT regiao, SUM(valor) AS total FROM silver.sales.transacoes GROUP BY regiao;

-- Dynamic View com mascaramento de PII
CREATE OR REPLACE VIEW catalog.schema.vw_clientes AS
SELECT id, nome,
  CASE WHEN is_member('compliance') THEN cpf ELSE '***-**-****' END AS cpf
FROM catalog.schema.clientes;
```

---

### LATERAL VIEW — Explodir arrays e maps em linhas

> **Depreciado desde Databricks Runtime 12.2** — prefira invocar funções geradoras diretamente como referência de tabela. Ainda cai na prova por ser amplamente usado em código legado.

Aplica uma **função geradora** (como `EXPLODE`) a cada linha do resultado, criando uma tabela virtual com as linhas expandidas.

**Sintaxe:**
```sql
LATERAL VIEW [ OUTER ] generator_function ( expression [, ...] )
  [ table_alias ] AS column_alias [, ...]
```

**Exemplo — explodir array de tags:**
```sql
SELECT id, tag
FROM produtos
LATERAL VIEW EXPLODE(tags) t AS tag;
```

**Com OUTER — preservar linhas quando o array é nulo/vazio:**
```sql
-- Sem OUTER: produto sem tags não aparece no resultado
-- Com OUTER: produto aparece com tag = NULL
SELECT id, tag
FROM produtos
LATERAL VIEW OUTER EXPLODE(tags) t AS tag;
```

**Múltiplos LATERAL VIEW — produto cartesiano:**
```sql
SELECT nome, idade, num
FROM pessoa
LATERAL VIEW EXPLODE(ARRAY(30, 60)) tbl1 AS idade
LATERAL VIEW EXPLODE(ARRAY(40, 80)) tbl2 AS num;
-- 4 pessoas × 2 × 2 = 16 linhas
```

**Forma moderna equivalente (preferida no Runtime ≥ 12.2):**
```sql
-- Em vez de LATERAL VIEW EXPLODE(tags), use:
SELECT id, tag
FROM produtos, EXPLODE(tags) AS t(tag);
```

> **Trade-off LATERAL VIEW vs forma moderna:**
> | | `LATERAL VIEW EXPLODE` | `EXPLODE` direto |
> |---|---|---|
> | Suporte | Legado (pré-12.2) | Recomendado (≥ 12.2) |
> | OUTER (preservar nulls) | `LATERAL VIEW OUTER` | `EXPLODE_OUTER(col)` |
> | Múltiplos arrays | Vários `LATERAL VIEW` | Vírgula entre referências |

Ref: [sql-ref-syntax-qry-select-lateral-view](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-lateral-view)

---

## 6. DATABRICKS ASSISTANT NO SQL EDITOR

No SQL Editor, o fluxo principal é via **chat** (não slash commands). O `/optimize` é o principal slash command disponível.

| Ação | Como fazer no SQL Editor |
|---|---|
| Explicar query | Chat: "Explain this query" ou selecionar + pedir explicação |
| Gerar query | Chat: descrever o que precisa em linguagem natural |
| Otimizar query | `/optimize` ou chat: "Optimize this query" |
| Debugar resultado inesperado | Selecionar query + chat: "Why is this returning wrong results?" |
| Referenciar tabela UC | `@catalog.schema.tabela` no chat |

---

## 7. DATA MODELING

### Star Schema vs Snowflake Schema vs Data Vault

| | Star Schema | Snowflake Schema | Data Vault |
|---|---|---|---|
| Estrutura | Fact + dimensions planas | Fact + dimensions normalizadas | Hub + Link + Satellite |
| Joins necessários | Poucos (rápido) | Mais joins (mais lento) | Muitos (mais lento) |
| Ideal para | BI/Analytics (Gold layer) | Dimensões com muita redundância | Auditoria, histórico, rastreabilidade |

### Medallion Architecture

```
Bronze → Dados brutos como chegaram (sem transformação)
         Append-only, preserva tudo

Silver → Dados limpos, filtros, joins, tipagem correta
         Remoção de duplicatas, conformação de schema

Gold   → Dados agregados e modelados para consumo analítico
         Onde Star/Snowflake são aplicados
         Consumido por: Dashboards, Genie Spaces, BI tools
```

---

## 8. CHECKLIST DE REVISÃO RÁPIDA

**Novidades (maior risco de errar)**
- [ ] QUALIFY — filtrar window functions (≠ HAVING que filtra aggregations)
- [ ] Genie Code: /fix e /doc sempre abrem diff view, nunca executam sozinhos
- [ ] /optimize disponível no SQL Editor (outros comandos só em Notebooks)
- [ ] Liquid Clustering: `CLUSTER BY` na criação, `ALTER TABLE ... CLUSTER BY` depois
- [ ] Streaming Table vs Materialized View: streaming = contínuo; MV = batch periódico
- [ ] Dynamic View: mascaramento e row-level security em tempo real
- [ ] `CREATE OR REPLACE TABLE` mantém privilégios e history (≠ DROP + CREATE)
- [ ] CLONE: Deep = cópia completa independente; Shallow = referencia arquivos da origem (barato, dependente)

**Permissões (questões frequentes)**
- [ ] Least privilege: USE CATALOG + USE SCHEMA + SELECT (3 grants necessários)
- [ ] Managed table DROP remove dados; External table DROP preserva arquivos
- [ ] Column Masks para PII por grupo/role

**SQL clássico que cai na prova**
- [ ] HAVING (não WHERE) para filtrar aggregations
- [ ] GROUP BY obrigatório quando há função de agregação e coluna não agregada
- [ ] UNION (dedup) vs UNION ALL (com duplicatas)
- [ ] TIME TRAVEL: `VERSION AS OF` e `TIMESTAMP AS OF`; VACUUM limita o histórico
- [ ] APPROX_COUNT_DISTINCT para grandes volumes (mais rápido que COUNT DISTINCT)
- [ ] Query Profile: Shuffle caro → clustering/broadcast; Scan com muitas linhas → revisar filtros; cache impede exibição do profile
- [ ] ANALYZE TABLE: `NOSCAN` só coleta size (sem full scan); `FOR COLUMNS` adiciona min/max/nulls/distinct; Predictive Optimization substitui para managed tables
- [ ] WATERMARK: obrigatório em stream-stream joins e agregações por event time; delay define tolerância a dados atrasados; sem watermark o estado cresce indefinidamente
- [ ] JSON: `get_json_object` → 1 campo (STRING); `json_tuple` → N campos (STRING, generator); `from_json` → struct tipado com schema definido
- [ ] SQL Alert: estados TRIGGERED / OK / ERROR (sem UNKNOWN); `{{ALERT_STATUS}}` e `{{QUERY_RESULT_VALUE}}` nas mensagens; queries com parâmetros não suportadas
- [ ] Tags Unity Catalog: `APPLY TAG` p/ atribuir; `system:certified` = System Tag predefinida pelo Databricks; busca via `information_schema.table_tags`; busca exata apenas
- [ ] Governed Tag exige `ASSIGN` + `APPLY TAG`; máx 50 tags/objeto; chave não pode ter `. , - = / :`

---

## 9. REFERÊNCIAS DA DOCUMENTAÇÃO OFICIAL

### Databricks Assistant / Genie Code
| Tópico | Link |
|---|---|
| Slash commands em Notebooks | [notebooks/code-assistant](https://docs.databricks.com/aws/en/notebooks/code-assistant#cell-actions) |

### SQL — Funções JSON
| Tópico | Link |
|---|---|
| get_json_object | [functions/get_json_object](https://docs.databricks.com/aws/en/sql/language-manual/functions/get_json_object) |
| json_tuple | [functions/json_tuple](https://docs.databricks.com/aws/en/sql/language-manual/functions/json_tuple) |
| from_json | [functions/from_json](https://docs.databricks.com/aws/en/sql/language-manual/functions/from_json) |

### SQL — Cláusulas e Sintaxe
| Tópico | Link |
|---|---|
| QUALIFY | [sql-ref-syntax-qry-select-qualify](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-qualify) |
| PIVOT | [sql-ref-syntax-qry-select-pivot](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-pivot) |
| UNPIVOT | [sql-ref-syntax-qry-select-unpivot](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-unpivot) |
| LATERAL VIEW | [sql-ref-syntax-qry-select-lateral-view](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-lateral-view) |
| RANK (window function) | [functions/rank](https://docs.databricks.com/aws/en/sql/language-manual/functions/rank) |

### Delta Lake
| Tópico | Link |
|---|---|
| Time Travel (histórico de versões) | [delta/history](https://docs.databricks.com/aws/en/delta/history) |
| VACUUM | [delta/vacuum](https://docs.databricks.com/aws/en/delta/vacuum) |
| OPTIMIZE | [delta-optimize](https://docs.databricks.com/aws/en/sql/language-manual/delta-optimize) |
| CLONE (Deep e Shallow) | [delta-clone](https://docs.databricks.com/aws/en/sql/language-manual/delta-clone) |
| Liquid Clustering | [delta/clustering](https://docs.databricks.com/aws/en/delta/clustering) |
| Streaming Tables | [delta/streaming-tables](https://docs.databricks.com/aws/en/delta/streaming-tables) |
| WATERMARK (event time / late data) | [sql-ref-syntax-qry-select-watermark](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-watermark) |

### Tabelas e Views
| Tópico | Link |
|---|---|
| Managed vs External Tables | [tables/external](https://docs.databricks.com/aws/en/tables/external) |
| Materialized Views | [ldp/dbsql/materialized](https://docs.databricks.com/aws/en/ldp/dbsql/materialized) |
| Dynamic Views (row/column security) | [views/dynamic](https://docs.databricks.com/aws/en/views/dynamic) |

### Unity Catalog
| Tópico | Link |
|---|---|
| Privileges (hierarquia de permissões) | [manage-privileges/privileges](https://docs.databricks.com/aws/en/data-governance/unity-catalog/manage-privileges/privileges) |
| Column Masks e Row Filters | [filters-and-masks](https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks/) |
| Tags (aplicar, buscar, governed, system) | [unity-catalog/tags](https://docs.databricks.com/aws/en/data-governance/unity-catalog/tags) |
| SET TAG / UNSET TAG (Runtime ≥ 16.1) | [sql-ref-syntax-ddl-set-tag](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-set-tag) |

### Ingestão e Compartilhamento
| Tópico | Link |
|---|---|
| Auto Loader | [ingestion/cloud-object-storage/auto-loader](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/) |
| COPY INTO | [ingestion/cloud-object-storage/copy-into](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/copy-into/) |
| Delta Sharing | [delta-sharing](https://docs.databricks.com/aws/en/delta-sharing/) |

### Performance e Orquestração
| Tópico | Link |
|---|---|
| Photon Engine | [compute/photon](https://docs.databricks.com/aws/en/compute/photon) |
| Query Profile (DAG) | [query-profile#explore-the-dag](https://docs.databricks.com/aws/en/sql/user/queries/query-profile#explore-the-dag) |
| ANALYZE TABLE (estatísticas do otimizador) | [sql-ref-syntax-aux-analyze-compute-statistics](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-aux-analyze-compute-statistics) |
| Lakeflow Jobs (Workflows) | [jobs](https://docs.databricks.com/aws/en/jobs/) |
| SQL Alerts | [sql/user/alerts](https://docs.databricks.com/aws/en/sql/user/alerts/) |

### Arquitetura
| Tópico | Link |
|---|---|
| Medallion Architecture | [lakehouse/medallion](https://docs.databricks.com/aws/en/lakehouse/medallion) |
