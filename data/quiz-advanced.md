# Practice Quiz — Databricks Certified Data Analyst Associate (Advanced)
> 40 advanced practice questions in exam format | Scenario-based, edge cases, and nuanced trade-offs

---

## Section 1 — Understanding the Databricks Data Intelligence Platform

**Question 1**

*Objective: Understand catalogs, schemas, managed and external tables, access controls, views, certified tables, and lineage within the Catalog Explorer interface.*

An analyst has been granted `SELECT` directly on the table `gold.sales.transactions` in Unity Catalog. When they run `SELECT * FROM gold.sales.transactions`, they receive a permissions error.

Which privileges are BOTH required in addition to `SELECT` for the query to succeed?

A. `READ ON CATALOG gold` and `READ ON SCHEMA gold.sales`
B. `USE CATALOG ON CATALOG gold` and `USE SCHEMA ON SCHEMA gold.sales`
C. `USE SCHEMA ON SCHEMA gold.sales` only — `USE CATALOG` is implicit when `SELECT` is granted on a table
D. No additional privileges are needed — `SELECT` on the table grants implicit navigation rights

---

**Question 2**

*Objective: Describe the core components of the Databricks Intelligence Platform.*

A data platform engineer is setting up governance for a new Databricks organization with three workspaces. They need a role that can manage Unity Catalog grants, create and delete catalogs, and define data access policies across all three workspaces.

Which role fulfills this requirement?

A. Workspace Admin — has full administrative control over all Databricks resources including Unity Catalog
B. Catalog Owner — can manage all objects within a specific catalog across all workspaces
C. Metastore Admin — manages Unity Catalog objects, grants, and policies across all workspaces attached to the metastore
D. Both Workspace Admin and Metastore Admin have equivalent Unity Catalog governance powers

---

**Question 3**

*Objective: Understand catalogs, schemas, managed and external tables, access controls, views, certified tables, and lineage within the Catalog Explorer interface.*

A data analyst creates the following view in Unity Catalog:

```sql
CREATE VIEW gold.reporting.revenue_by_customer AS
SELECT customer_id, SUM(amount) AS total_revenue
FROM silver.sales.transactions
GROUP BY customer_id;
```

What level of data lineage does Unity Catalog automatically capture for this object?

A. Column-level: `silver.sales.transactions.customer_id` → `gold.reporting.revenue_by_customer.customer_id` and `silver.sales.transactions.amount` → `gold.reporting.revenue_by_customer.total_revenue`
B. Table-level only: `silver.sales.transactions` → `gold.reporting.revenue_by_customer`
C. Lineage is only tracked for managed tables created with `CREATE TABLE AS SELECT`, not for views
D. Lineage tracking requires manually tagging each column through the Catalog Explorer UI

---

**Question 4**

*Objective: Describe the core components of the Databricks Intelligence Platform.*

A data engineering team needs to build a pipeline with the following requirements: declarative table definitions with automatic dependency resolution, built-in data quality assertions that fail the pipeline when violated, and incremental processing with automatic backfill.

Which Databricks feature is specifically designed to fulfill all three requirements?

A. Lakeflow Jobs with Python notebooks
B. Materialized Views with a scheduled refresh
C. Streaming Tables with Auto Loader
D. Delta Live Tables (DLT)

---

**Question 5**

*Objective: Describe the role and features of Databricks Marketplace.*

A data analyst says: "We used Delta Sharing to discover and acquire an external dataset from a third-party vendor through the platform." A senior engineer corrects the terminology.

What is the correct distinction between Delta Sharing and Databricks Marketplace?

A. There is no distinction — Delta Sharing and Databricks Marketplace refer to the same feature
B. Delta Sharing is the open protocol for zero-copy data transfer; Databricks Marketplace is the discovery and distribution platform that uses Delta Sharing as its underlying sharing mechanism
C. Databricks Marketplace is for sharing data internally between teams; Delta Sharing is exclusively for external partners
D. Delta Sharing only works between Databricks workspaces; Marketplace supports non-Databricks platforms only

---

## Section 2 — Managing Data

**Question 6**

*Objective: Perform data cleaning on Unity Catalog Tables in SQL, including removing invalid data or handling missing values.*

An analyst needs to synchronize a target Delta table with a source staging table. For rows that already exist in the target (matched by `order_id`), update all columns. For new rows in the source, insert them. For rows in the target that no longer exist in the source, delete them.

Which `MERGE` statement correctly implements all three operations?

A.
```sql
MERGE INTO target t USING source s ON t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

B.
```sql
MERGE INTO target t USING source s ON t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
WHEN SOURCE NOT FOUND THEN DELETE FROM target;
```

C.
```sql
MERGE INTO target t USING source s ON t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
WHEN UNMATCHED IN TARGET THEN DELETE;
```

D.
```sql
MERGE INTO target t USING source s ON t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
WHEN NOT MATCHED BY SOURCE THEN DELETE;
```

---

**Question 7**

*Objective: Understand catalogs, schemas, managed and external tables, access controls, views, certified tables, and lineage within the Catalog Explorer interface.*

A data engineer needs to replace the schema of an existing Delta table `silver.events.pageviews` with a new one, while preserving the table's Unity Catalog lineage history and existing column comments.

Which approach is correct?

A. `CREATE OR REPLACE TABLE silver.events.pageviews (...)` — this preserves the table's lineage, metadata, and history
B. `DROP TABLE silver.events.pageviews; CREATE TABLE silver.events.pageviews (...)` — dropping and recreating is equivalent
C. `TRUNCATE TABLE silver.events.pageviews` followed by `ALTER TABLE ... ADD COLUMN` for each new column
D. Both A and B preserve lineage equally; the choice is only a matter of style

---

**Question 8**

*Objective: Perform data cleaning on Unity Catalog Tables in SQL, including removing invalid data or handling missing values.*

A Delta table `orders` receives duplicate records when the ingestion pipeline retries. Duplicates share the same `order_id` but differ in `ingestion_timestamp`. The analyst wants to keep only the most recently ingested row per `order_id`.

Which query correctly accomplishes this?

A.
```sql
CREATE TABLE orders_clean AS
SELECT DISTINCT order_id FROM orders;
```

B.
```sql
CREATE TABLE orders_clean AS
SELECT * FROM orders WHERE ingestion_timestamp = MAX(ingestion_timestamp);
```

C.
```sql
CREATE TABLE orders_clean AS
SELECT * FROM orders
QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY ingestion_timestamp DESC) = 1;
```

D.
```sql
CREATE TABLE orders_clean AS
SELECT * FROM orders GROUP BY order_id HAVING MAX(ingestion_timestamp);
```

---

## Section 3 — Importing Data

**Question 9**

*Objective: Explain the approaches for bringing data into Databricks, covering ingestion from S3, data sharing with external systems via Delta Sharing, API-driven data intake, the Auto Loader feature, and Marketplace.*

An analyst is using Auto Loader with `cloudFiles.schemaEvolutionMode = "addNewColumns"` to ingest JSON files into a Delta table. A new field `promo_code` suddenly appears in incoming files that was not present in the original schema.

What is the expected behavior?

A. Auto Loader fails with a schema mismatch error and stops the stream until the analyst manually updates the target table schema
B. Auto Loader silently drops unknown fields and continues processing with the original schema
C. The new field is stored in a special `_extra_fields` column as a JSON string without altering the schema
D. The new `promo_code` column is automatically added to the target Delta table schema; the stream restarts once to incorporate the change, and historical rows will have `NULL` for the new column

---

**Question 10**

*Objective: Explain the approaches for bringing data into Databricks, covering ingestion from S3, data sharing with external systems via Delta Sharing, API-driven data intake, the Auto Loader feature, and Marketplace.*

A data engineer runs `COPY INTO silver.raw.events FROM 's3://bucket/events/'` twice against the same S3 path. The second run executes 10 minutes after the first with no new files added.

What happens during the second run?

A. All files are loaded again, creating duplicate rows — `COPY INTO` has no idempotency mechanism
B. No files are loaded — `COPY INTO` tracks which files have already been processed and skips them, making it idempotent
C. The second run fails with a "files already loaded" error
D. The second run loads only files that were modified since the first run, based on S3 object metadata

---

**Question 11**

*Objective: Explain the approaches for bringing data into Databricks, covering ingestion from S3, data sharing with external systems via Delta Sharing, API-driven data intake, the Auto Loader feature, and Marketplace.*

A data provider shares a Delta table with an external recipient using Delta Sharing. After sharing, the provider runs `VACUUM my_table RETAIN 168 HOURS` on the shared table.

What is the potential impact on the recipient?

A. The recipient may lose the ability to access historical versions of the shared table if VACUUM removes the underlying data files those versions referenced
B. No impact — the recipient holds an independent copy of the data and VACUUM on the provider side has no effect
C. VACUUM on shared tables is automatically blocked by Delta Sharing to prevent disruption to recipients
D. The recipient is automatically notified and given 24 hours to take a snapshot before files are deleted

---

## Section 4 — Executing Queries Using Databricks SQL

**Question 12**

*Objective: Use Delta Lake's time travel to access and query historical data versions.*

An analyst runs `RESTORE TABLE inventory TO VERSION AS OF 5` on a Delta table that is currently at version 20.

What is the state of the table after this operation?

A. The table is rolled back to version 5 and all versions 6–20 are permanently deleted
B. The table is restored to version 5 and versions 6–20 are archived but recoverable for 30 days
C. A new version (21) is created that reflects the data from version 5; the full version history (0–20 plus the restore event at version 21) is preserved
D. `RESTORE TABLE` fails if the table has more than 10 versions ahead of the target version

---

**Question 13**

*Objective: Apply window functions including QUALIFY.*

A `products` table contains 5 products in category `"Electronics"` with `units_sold` values: 500, 300, 300, 200, 100.

The analyst runs:
```sql
SELECT category, product_name, units_sold,
  RANK() OVER (PARTITION BY category ORDER BY units_sold DESC) AS rnk
FROM products
QUALIFY rnk <= 3;
```

How many rows are returned for category `"Electronics"`?

A. 4 rows — both products with `units_sold = 300` share rank 2, and rank 3 is occupied by the 200-unit product
B. 5 rows — `QUALIFY rnk <= 3` includes all rows with ranks lower than 4
C. 3 rows — rank 1 (500), rank 2 (300), rank 2 (300); rank 3 does not exist because `RANK()` creates a gap after the tie, so the 200-unit product is rank 4 and is excluded
D. 3 rows exactly — one per rank position, with one of the tied products arbitrarily excluded

---

**Question 14**

*Objective: Apply window functions including QUALIFY.*

An analyst needs to find the difference between each order's amount and the **previous** order's amount for the same customer, ordered by `order_date`.

Which window function correctly retrieves the previous row's amount?

A. `FIRST_VALUE(amount) OVER (PARTITION BY customer_id ORDER BY order_date)`
B. `LEAD(amount, 1) OVER (PARTITION BY customer_id ORDER BY order_date)`
C. `PREV(amount) OVER (PARTITION BY customer_id ORDER BY order_date)`
D. `LAG(amount, 1) OVER (PARTITION BY customer_id ORDER BY order_date)`

---

**Question 15**

*Objective: Apply window functions including QUALIFY.*

An analyst needs to calculate a **3-row rolling sum** of `revenue`, where the window always includes exactly the 2 preceding physical rows and the current row, regardless of `order_date` gaps or ties.

Which window frame specification is correct?

A. `SUM(revenue) OVER (ORDER BY order_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`
B. `SUM(revenue) OVER (ORDER BY order_date RANGE BETWEEN 2 PRECEDING AND CURRENT ROW)`
C. `SUM(revenue) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`
D. `SUM(revenue) OVER (PARTITION BY order_date ROWS 3)`

---

**Question 16**

*Objective: Perform aggregate operations such as count, approximate count distinct, mean, and summary statistics.*

Which statement is TRUE about `APPROX_COUNT_DISTINCT(col)` compared to `COUNT(DISTINCT col)`?

A. `APPROX_COUNT_DISTINCT` returns the exact same result as `COUNT(DISTINCT col)` but uses parallel processing for speed
B. `APPROX_COUNT_DISTINCT` uses the HyperLogLog algorithm and may return a value with a small relative error (~5%), but is significantly faster and more memory-efficient on large datasets
C. `APPROX_COUNT_DISTINCT` is only approximate when the distinct count exceeds 1 million; below that threshold it returns an exact count
D. `APPROX_COUNT_DISTINCT` is deprecated in Databricks SQL; use `COUNT(DISTINCT col)` with Photon acceleration instead

---

**Question 17**

*Objective: Write queries to combine tables using various join operations with single or multiple keys, as well as set operations like union and union all.*

Consider the following query:

```sql
SELECT NULL AS val
UNION
SELECT NULL AS val;
```

How many rows are returned?

A. 2 rows — `NULL` is not equal to `NULL`, so both rows are treated as distinct and preserved by `UNION`
B. 0 rows — `UNION` cannot deduplicate `NULL` values and returns an empty result
C. 1 row — `UNION` deduplicates rows, and for set operations two `NULL` values are treated as equal
D. An error is raised because `NULL` cannot be used in set operations

---

**Question 18**

*Objective: Querying cross-system analytics by joining data from a Delta table and a federated data source.*

Consider two queries that return logically identical results:

**Query A (correlated subquery):**
```sql
SELECT order_id, customer_id, amount,
  (SELECT AVG(amount) FROM orders o2 WHERE o2.customer_id = o1.customer_id) AS avg_per_customer
FROM orders o1;
```

**Query B (window function):**
```sql
SELECT order_id, customer_id, amount,
  AVG(amount) OVER (PARTITION BY customer_id) AS avg_per_customer
FROM orders;
```

Which statement best describes the performance difference on a large table?

A. Query A is faster because Photon specifically optimizes correlated subqueries with pushed-down predicates
B. Both queries have equivalent performance because the Databricks query optimizer rewrites correlated subqueries as window functions at parse time
C. Query A will raise an error because correlated subqueries are not supported in Databricks SQL
D. Query B is significantly faster — window functions process data in a single pass, while the correlated subquery in Query A is logically re-executed for each row

---

**Question 19**

*Objective: Execute queries using Databricks SQL with correct syntax.*

An analyst needs to rotate a `quarterly_sales` table from row-oriented to column-oriented format, producing one row per `year` with columns `Q1`, `Q2`, `Q3`, `Q4` each containing the `SUM(sales)`.

Which query is correct?

A.
```sql
SELECT * FROM quarterly_sales
PIVOT (SUM(sales) FOR quarter IN ('Q1', 'Q2', 'Q3', 'Q4'));
```

B.
```sql
SELECT year, Q1, Q2, Q3, Q4 FROM quarterly_sales
PIVOT year ON quarter USING SUM(sales);
```

C.
```sql
PIVOT TABLE quarterly_sales
ON quarter VALUES ('Q1', 'Q2', 'Q3', 'Q4')
AGGREGATE SUM(sales);
```

D.
```sql
SELECT * FROM quarterly_sales
ROTATE (SUM(sales) FOR quarter IN ('Q1', 'Q2', 'Q3', 'Q4'));
```

---

**Question 20**

*Objective: Perform aggregate operations such as count, approximate count distinct, mean, and summary statistics.*

An analyst writes the following chained CTE query:

```sql
WITH base AS (
  SELECT * FROM orders WHERE order_year = 2024             -- 1M rows
),
filtered AS (
  SELECT * FROM base WHERE region = 'WEST'                 -- 100K rows
),
ranked AS (
  SELECT *, RANK() OVER (PARTITION BY product ORDER BY revenue DESC) AS rnk
  FROM filtered
)
SELECT * FROM ranked WHERE rnk = 1;
```

How many rows does the `RANK()` window function logically operate on?

A. 10 million rows — the full `orders` table, since CTEs do not push down filters
B. 100,000 rows — CTEs are evaluated sequentially; `ranked` receives the output of `filtered`, which has already applied both predicates
C. 1 million rows — CTEs are independently optimized and only the `order_year` filter applies to `ranked`
D. It cannot be determined without knowing the query execution plan

---

## Section 5 — Analyzing Queries

**Question 21**

*Objective: Identify poorly performing queries in the Databricks Intelligence platform, such as Query Insights, Query Profiler log, etc.*

While reviewing the Query Profile for a slow aggregation query, an analyst sees that the maximum task duration in one stage is 45 seconds while the median task duration is 2 seconds.

What performance problem does this pattern most likely indicate?

A. Insufficient SQL Warehouse size — the warehouse needs to be scaled up
B. Missing Liquid Clustering — the data files are not organized for the query's filter columns
C. Data skew — one or a few tasks are processing a disproportionately large amount of data compared to others
D. Cache miss — the result cache was invalidated before the query completed

---

**Question 22**

*Objective: Utilize query history and caching to reduce development time and query latency.*

An analyst runs an expensive aggregation query on a SQL Warehouse and the result is cached. Which of the following actions will cause the cache to be **invalidated**, requiring a full re-execution?

A. A different user running the same query from a separate browser session
B. The analyst navigating away from the SQL Editor tab and returning 5 minutes later
C. The SQL Warehouse being idle for more than 10 minutes and scaling down to 0 clusters
D. An `INSERT INTO` or `UPDATE` operation modifying rows in the underlying Delta table

---

**Question 23**

*Objective: Apply Liquid Clustering to improve query speed when filtering large tables on specific columns.*

A data engineer runs `VACUUM my_table RETAIN 0 HOURS` to immediately remove all old data files. What happens?

A. The command fails — Databricks enforces a minimum retention period of 168 hours (7 days) unless the safety check is explicitly disabled with a configuration flag
B. The command succeeds and removes all files not referenced by the current table version
C. The command succeeds but only removes files older than 24 hours as an internal safety measure
D. The command requires `ALL PRIVILEGES` on the table and returns a permissions error for regular analysts

---

**Question 24**

*Objective: Understand the Features, Benefits, and Supported Workloads of Photon.*

A data team is evaluating which workloads will benefit from Photon acceleration on their SQL Warehouse. Which of the following is **NOT** accelerated by Photon?

A. SQL `JOIN` operations between two Delta tables
B. Python user-defined functions (UDFs) applied to DataFrame columns
C. `DataFrame.filter()` operations in PySpark
D. SQL aggregate functions such as `SUM()`, `AVG()`, and `COUNT()`

---

**Question 25**

*Objective: Apply Liquid Clustering to improve query speed when filtering large tables on specific columns.*

A data team wants to enable Liquid Clustering on a large existing table but cannot determine the optimal clustering columns because query patterns vary significantly across teams.

Which option does Databricks provide for this scenario?

A. Run `ANALYZE TABLE ... COMPUTE STATISTICS` and Databricks will automatically select clustering columns from the statistics
B. Liquid Clustering requires explicit column specification; there is no automatic selection mode
C. Use `CLUSTER BY AUTO` — Databricks automatically selects the most beneficial clustering columns based on query history and data statistics
D. Use `OPTIMIZE TABLE ... AUTO CLUSTER` which implicitly enables Liquid Clustering on all columns

---

## Section 6 — Working with Dashboards and Visualizations

**Question 26**

*Objective: Work with parameters in SQL queries and dashboards, including defining, configuring, and testing parameters.*

An AI/BI Dashboard has two independent visualizations: a bar chart powered by `query_1` and a line chart powered by `query_2`. The dashboard has a "Year" dropdown parameter widget set to `2024`.

For **both** visualizations to reflect the selected year filter, what must be true?

A. Both queries must query tables within the same catalog so cross-query filters are automatically applied
B. Only the first query that uses the parameter will update; the second visualization requires a separate parameter widget
C. Dashboard parameters automatically inject `WHERE` conditions into all queries on the canvas without any SQL changes
D. Each query must explicitly reference the dashboard parameter in its own `WHERE` clause — parameters are not automatically applied to all queries on a dashboard

---

**Question 27**

*Objective: Configure an alert with a desired threshold and destination.*

An analyst configures a SQL Alert to check every 15 minutes. The underlying Delta table is updated once per hour. During the 45 minutes between data updates, the alert query returns a value that does NOT exceed the threshold.

What happens during those three intermediate 15-minute checks?

A. The alert query is re-executed at each 15-minute interval; since the result does not exceed the threshold, no notification is sent but the query still runs
B. The alert detects no new data and automatically pauses until the table is updated
C. The alert is served from the result cache and does not execute the query against the table
D. The alert skips execution after the first non-triggering check and only resumes when new data is committed

---

**Question 28**

*Objective: Configure permissions through the UI to share dashboards with workspace users/groups, external users through shareable links, and embed dashboards in external apps.*

A company wants to embed an AI/BI Dashboard into their internal web portal so that employees can view live data without logging into Databricks. The employees do not have Databricks accounts.

Which approach enables this?

A. Employees must be added as workspace users with "Can View" permission before the embed will display data
B. Use the dashboard's embed link (iframe code) combined with a shareable link that grants view access, or integrate via SSO
C. The dashboard must first be published to the Databricks Marketplace and then linked from the portal
D. Embedded dashboards are only accessible through the Databricks mobile application

---

**Question 29**

*Objective: Identify the effective visualization type to communicate insights clearly.*

A data analyst needs to visualize the **composition** of total annual revenue broken down by 5 product lines, showing each product line's **percentage share** of the whole.

Which visualization type is most appropriate?

A. Line chart — best for showing proportional data over categories
B. Scatter plot — best for comparing two continuous variables
C. Stacked bar chart or pie chart — both are appropriate for showing part-to-whole relationships across a fixed set of categories
D. Heatmap — best for showing magnitude of a measure across two categorical dimensions

---

**Question 30**

*Objective: Schedule an automatic dashboard refresh.*

A data analyst needs to display a single, prominently visible KPI value on a dashboard — **"Failed Transactions This Hour: 127"** — that updates in near real-time.

Which combination of features is most appropriate?

A. A line chart visualization with a one-data-point time series
B. A SQL Alert displayed inline on the dashboard canvas
C. A table visualization with one row and one column
D. A Counter (metric) visualization backed by a query that counts failed transactions, with a frequent scheduled refresh

---

## Section 7 — Developing, Sharing, and Maintaining AI/BI Genie Spaces

**Question 31**

*Objective: Optimize AI/BI Genie spaces by tracking user questions, response accuracy, and feedback.*

A user asks a Genie Space: "How many active customers do we have?" A data analyst has previously validated and added the exact SQL query for this question as a **Trusted Asset**.

How does Genie handle this question?

A. Genie uses the Trusted Asset query as the definitive answer, bypassing its own SQL generation, and returns the validated result
B. Genie generates its own SQL and compares it to the Trusted Asset; if they differ, it asks the user which version to use
C. Trusted Assets are only invoked when Genie's SQL generation fails; they act as a fallback
D. Genie presents the Trusted Asset query as a suggestion but always executes its own generated SQL

---

**Question 32**

*Objective: Create Genie spaces by defining reasonable sample questions and domain-specific instructions, choosing SQL warehouses, curating Unity Catalog datasets, and vetting queries as Trusted Assets.*

A Genie Space has been configured with only the `gold.sales.transactions` table. A marketing analyst asks: "What is our current inventory level by product?"

What will the Genie Space most likely respond?

A. Genie will search all available tables in the Unity Catalog metastore to find relevant inventory data and answer the question
B. Genie will indicate that it cannot answer the question because inventory data is not within the datasets configured for this Space
C. Genie will return an empty result set without explanation
D. Genie will automatically add inventory-related tables to the Space and generate an answer

---

**Question 33**

*Objective: Optimize AI/BI Genie spaces by tracking user questions, response accuracy, and feedback.*

After deploying a Genie Space, the data team wants to monitor which questions users are asking and identify where Genie is producing inaccurate or inconsistent answers.

What is the recommended workflow for continuous improvement?

A. Review user question history and feedback within the Genie Space, identify low-accuracy questions, add or refine Trusted Assets for those questions, and update the domain-specific instructions
B. Delete and recreate the Genie Space from scratch each time accuracy issues are detected
C. Increase the number of tables in the Space to give Genie more context for answering questions
D. Switch to a larger SQL Warehouse to improve Genie's answer quality

---

## Section 8 — Data Modeling with Databricks SQL

**Question 34**

*Objective: Apply industry-standard data modeling techniques, such as star, snowflake, and data vault schemas, to analytical workloads.*

A data team is implementing a customer dimension table that must preserve the full history of customer address changes. When a customer's address changes, the old record must remain accessible, a new record must be created, and the current record must be identifiable.

Which columns are required for a **Slowly Changing Dimension Type 2 (SCD Type 2)** implementation?

A. A primary key column and a `last_updated` timestamp column
B. A primary key, a `version_number` integer, and a `created_at` timestamp
C. Only a primary key and a JSON column that stores all historical attribute snapshots
D. A surrogate key, the natural/business key, `effective_start_date`, `effective_end_date`, and an `is_current` flag

---

**Question 35**

*Objective: Apply industry-standard data modeling techniques, such as star, snowflake, and data vault schemas, to analytical workloads.*

A financial services organization needs a data warehouse that: (1) provides full auditability and traceability of every data change from source systems; (2) must integrate data from 20+ heterogeneous source systems; and (3) must allow new sources to be added without redesigning the existing model.

Which data modeling approach is MOST appropriate?

A. Star Schema — optimized for BI query performance and simplest to implement
B. Snowflake Schema — better normalized and handles multiple sources through dimension sub-tables
C. Data Vault — specifically designed for auditability, historical tracking, and scalable integration of many source systems with minimal restructuring
D. Third Normal Form (3NF) — the most flexible approach for heterogeneous sources

---

## Section 9 — Securing Data

**Question 36**

*Objective: Apply best practices for storage and management to ensure data security, including table ownership and PII protection.*

A security team wants row-level access control enforced at the **table level** in Unity Catalog, so that sales representatives automatically see only rows where `region` matches their assigned group, without redirecting users to a separate view.

Which Unity Catalog feature enables this?

A. Column Masks — attach a masking function to a column that filters rows based on its value
B. Row Filters — attach a SQL function to the table that restricts which rows are returned based on the current user's identity or group membership
C. Dynamic Views — create a view over the base table with `is_member()` conditions in the `WHERE` clause
D. Certified Tables — mark a table as certified and define governance rules that restrict row visibility

---

**Question 37**

*Objective: Use Unity Catalog roles and sharing settings to ensure workspace objects are secure.*

A security admin wants to explicitly prevent a specific user from accessing a table, even though that user belongs to a group that has been granted `SELECT` on the table.

Which statement correctly describes the available approach in Unity Catalog?

A. Run `DENY SELECT ON TABLE catalog.schema.table TO USER user@company.com` — Unity Catalog supports explicit DENY to override group grants
B. `DENY` exists in Unity Catalog but requires metastore admin privileges to execute
C. Unity Catalog does NOT have a `DENY` command — to restrict access, the admin must either revoke the grant from the group, create a sub-group without the user, or remove the user from the group that holds the grant
D. Run `REVOKE ALL PRIVILEGES ON TABLE catalog.schema.table FROM USER user@company.com`, which acts as an implicit DENY for that user regardless of group membership

---

**Question 38**

*Objective: Apply best practices for storage and management to ensure data security, including table ownership and PII protection.*

A column mask is configured on `orders.customer_email`: users without the `data_access` role see `***@***.com` instead of the real email.

An analyst without `data_access` runs:

```sql
SELECT o.order_id, c.name
FROM orders o
JOIN customers c ON o.customer_email = c.email;
```

What is the result?

A. The JOIN proceeds correctly — column masks only affect the SELECT output and are not applied to JOIN conditions
B. The query fails with a permissions error because the analyst referenced a masked column in a JOIN condition
C. Unity Catalog automatically lifts the mask for JOIN key columns to ensure referential integrity
D. The JOIN operates on the masked value `***@***.com` for `customer_email`, which will likely produce no matches in `customers.email`, returning incorrect or empty results

---

**Question 39**

*Objective: Use Unity Catalog roles and sharing settings to ensure workspace objects are secure.*

A data platform admin needs to grant a specific user the ability to **create new schemas** inside the catalog `silver`, without granting any other elevated privileges.

Which SQL statement is correct?

A. `GRANT CREATE SCHEMA ON CATALOG silver TO USER data_engineer@company.com;`
B. `GRANT ALL PRIVILEGES ON CATALOG silver TO USER data_engineer@company.com;`
C. `GRANT CREATE TABLE ON CATALOG silver TO USER data_engineer@company.com;`
D. `GRANT USE CATALOG ON CATALOG silver TO USER data_engineer@company.com;`

---

**Question 40**

*Objective: Apply best practices for storage and management to ensure data security, including table ownership and PII protection.*

A table's ownership is transferred: `ALTER TABLE gold.finance.budget OWNER TO 'new_owner@company.com'`. The previous owner had `SELECT`, `MODIFY`, and `CREATE TABLE` explicitly granted.

What privileges does `new_owner@company.com` automatically have after this operation?

A. Only the privileges that were explicitly granted to the previous owner: `SELECT`, `MODIFY`, and `CREATE TABLE`
B. All privileges (`ALL PRIVILEGES`) on the table — ownership grants full control regardless of previous explicit grants
C. Read-only access (`SELECT`) until the new owner explicitly grants themselves additional privileges
D. No privileges until the metastore admin confirms the ownership transfer

---

---

# Answer Key

| Q | Answer | Key Concept |
|---|--------|-------------|
| 1 | B | USE CATALOG + USE SCHEMA are required in addition to SELECT — all three must be granted |
| 2 | C | Metastore Admin governs Unity Catalog across all workspaces; Workspace Admin manages workspace settings |
| 3 | A | Unity Catalog automatically captures column-level lineage for SQL-based views and CTAS |
| 4 | D | Delta Live Tables (DLT) = declarative definitions + data quality expectations + incremental processing |
| 5 | B | Delta Sharing = open protocol; Marketplace = discovery platform built on top of Delta Sharing |
| 6 | D | `WHEN NOT MATCHED BY SOURCE THEN DELETE` deletes target rows with no matching source row |
| 7 | A | `CREATE OR REPLACE TABLE` preserves Unity Catalog lineage and history; DROP + CREATE breaks it |
| 8 | C | `QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY ingestion_timestamp DESC) = 1` deduplicates correctly |
| 9 | D | With `addNewColumns`, Auto Loader adds the new column, restarts once, and fills historical rows with NULL |
| 10 | B | `COPY INTO` is idempotent — it tracks processed files and skips them on subsequent runs |
| 11 | A | VACUUM on the provider table removes data files; recipients lose access to historical versions that referenced those files |
| 12 | C | RESTORE creates a new version (n+1) reflecting version 5's data; full history is preserved |
| 13 | C | RANK() creates gaps after ties: 500=rank1, 300=rank2, 300=rank2 (no rank3), 200=rank4 → only 3 rows qualify |
| 14 | D | `LAG(col, 1)` returns the value from the previous row in the ordered partition |
| 15 | A | `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` counts exactly 2 prior physical rows; RANGE counts by value distance |
| 16 | B | APPROX_COUNT_DISTINCT uses HyperLogLog — ~5% relative error, faster and more memory-efficient at scale |
| 17 | C | UNION deduplicates; NULL = NULL for set operation deduplication, returning 1 row |
| 18 | D | Window functions process data in one pass; correlated subqueries are logically re-executed per row |
| 19 | A | `PIVOT (SUM(sales) FOR quarter IN ('Q1','Q2','Q3','Q4'))` is the correct Databricks SQL PIVOT syntax |
| 20 | B | CTEs are evaluated sequentially; RANK() in `ranked` operates on the 100K rows output by `filtered` |
| 21 | C | Max task duration >> median task duration in the same stage = data skew signature |
| 22 | D | Result cache is invalidated when the underlying Delta table is modified (INSERT, UPDATE, DELETE, MERGE) |
| 23 | A | VACUUM enforces a 168-hour minimum retention period — the safety check must be explicitly disabled |
| 24 | B | Python UDFs run in the Python interpreter, not in Photon's C++ engine, and are not accelerated |
| 25 | C | `CLUSTER BY AUTO` lets Databricks automatically select optimal clustering columns from query history |
| 26 | D | Each query must explicitly reference the parameter in its own WHERE clause; parameters are not auto-applied |
| 27 | A | Alerts re-execute on every scheduled interval; no notification fires unless the threshold condition is met |
| 28 | B | Embed link (iframe) + shareable link or SSO integration enables external access without Databricks accounts |
| 29 | C | Stacked bar chart or pie chart = part-to-whole composition across a fixed set of categories |
| 30 | D | Counter (metric) visualization + frequent scheduled refresh is the correct pattern for a live KPI widget |
| 31 | A | Trusted Assets are used as the definitive answer for matching questions, bypassing Genie's SQL generation |
| 32 | B | Genie only queries tables configured in the Space; it cannot answer questions about out-of-scope data |
| 33 | A | Review history + feedback → refine Trusted Assets + domain instructions = correct improvement workflow |
| 34 | D | SCD Type 2 requires: surrogate key, natural key, effective_start_date, effective_end_date, is_current flag |
| 35 | C | Data Vault = auditability, historical traceability, scalable multi-source integration without redesign |
| 36 | B | Row Filters attach to the table itself and enforce row-level access automatically on every query |
| 37 | C | Unity Catalog has no DENY command — access restriction requires revoking or removing group membership |
| 38 | D | Column masks are applied before query execution; the JOIN sees the masked value, producing incorrect results |
| 39 | A | `GRANT CREATE SCHEMA ON CATALOG silver` is the minimum privilege for creating schemas in a catalog |
| 40 | B | Table ownership = ALL PRIVILEGES automatically; explicit prior grants are unrelated to ownership rights |
