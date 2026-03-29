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
