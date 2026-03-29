# Practice Quiz — Databricks Certified Data Analyst Associate
> 40 practice questions in exam format | Based on Exam Guide (Oct 2025)

---

## Section 1 — Understanding the Databricks Data Intelligence Platform

**Question 1**

*Objective: Describe the core components of the Databricks Intelligence Platform.*

A data team is migrating from a legacy Hive metastore to a solution that provides centralized governance, lineage tracking, and access control across multiple Databricks workspaces within the same organization.

Which Databricks component fulfills this requirement?

A. Delta Lake
B. Databricks SQL
C. Unity Catalog
D. Mosaic AI

---

**Question 2**

*Objective: Describe the core components of the Databricks Intelligence Platform.*

A data engineer mentions that they are configuring **Lakeflow Jobs** to orchestrate a data pipeline. A colleague who has been away from the platform since 2022 is unfamiliar with this term.

What does Lakeflow Jobs correspond to in the Databricks platform?

A. The orchestration and scheduling component, previously known as Workflows/Jobs
B. A replacement for Delta Live Tables used for streaming pipelines
C. A new type of SQL Warehouse optimized for job execution
D. A feature for managing Auto Loader ingestion tasks

---

**Question 3**

*Objective: Understand catalogs, schemas, managed and external tables, access controls, views, certified tables, and lineage within the Catalog Explorer interface.*

A data analyst needs to reference a table called `sales` stored inside the `reporting` schema, which belongs to a catalog called `gold`. The analyst is writing a query in the SQL Editor.

Which of the following correctly references this table using the Unity Catalog three-level namespace?

A. `reporting.gold.sales`
B. `gold.reporting.sales`
C. `gold.sales.reporting`
D. `workspace.gold.reporting.sales`

---

**Question 4**

*Objective: Understand catalogs, schemas, managed and external tables, access controls, views, certified tables, and lineage within the Catalog Explorer interface.*

A data governance team wants to identify which upstream tables feed into a specific report table and track who last modified it. They also want to flag certain datasets as trusted and verified for consumption.

Which Databricks interface provides lineage tracking, dataset certification, and tagging capabilities?

A. Query History
B. Databricks Assistant
C. Catalog Explorer
D. SQL Warehouse monitoring

---

**Question 5**

*Objective: Describe the role and features of Databricks Marketplace.*

A data analyst wants to enrich the company's internal customer dataset with publicly available demographic data, without having to build an ingestion pipeline.

Which Databricks feature allows the analyst to discover and access third-party datasets, models, and notebooks directly within the platform?

A. Delta Sharing
B. Auto Loader
C. Lakehouse Federation
D. Databricks Marketplace

---

## Section 2 — Managing Data

**Question 6**

*Objective: Perform data cleaning on Unity Catalog Tables in SQL, including removing invalid data or handling missing values.*

A data analyst is cleaning a Unity Catalog table called `customers`. The analyst needs to remove all rows where the `email` column is NULL or the `age` column contains a negative value.

Which SQL statement correctly accomplishes this?

A. `DELETE FROM customers WHERE email IS NULL OR age < 0;`
B. `DROP ROWS FROM customers WHERE email = '' AND age < 0;`
C. `UPDATE customers SET email = 'unknown' WHERE email IS NULL;`
D. `REMOVE FROM customers WHERE email IS NULL OR age < 0;`

---

**Question 7**

*Objective: Use the Catalog Explorer to tag a data asset and view its lineage.*

A data steward needs to apply a `pii=true` tag to the `ssn` column of a regulated table in Unity Catalog so it can be identified during governance reviews.

Which of the following approaches can be used to apply this tag?

A. Only through the `ALTER TABLE ... SET TAGS` SQL command in the SQL Editor
B. Only through the Catalog Explorer graphical interface
C. Through either the SQL Editor using `ALTER TABLE ... SET TAGS` or through the Catalog Explorer UI
D. Tags on columns can only be applied by metastore admins via the REST API

---

**Question 8**

*Objective: Understand catalogs, schemas, managed and external tables, access controls, views, certified tables, and lineage within the Catalog Explorer interface.*

A data analyst executes `DROP TABLE catalog.schema.transactions` on a **managed table** registered in Unity Catalog.

What is the expected behavior?

A. Only the metadata entry is removed from Unity Catalog; the underlying data files remain in storage
B. Both the metadata and the underlying data files are permanently deleted
C. The table is moved to a recycle bin and can be restored within 30 days
D. The behavior depends on which SQL Warehouse was used to execute the command

---

## Section 3 — Importing Data

**Question 9**

*Objective: Explain the approaches for bringing data into Databricks, covering ingestion from S3, data sharing with external systems via Delta Sharing, API-driven data intake, the Auto Loader feature, and Marketplace.*

A data engineering team needs to continuously ingest new JSON files as they land in an S3 bucket. The solution must automatically detect new files and process only the ones that have not been ingested yet, without manual intervention.

Which Databricks feature is best suited for this requirement?

A. Delta Sharing
B. `COPY INTO` with a scheduled job
C. Auto Loader
D. Databricks Marketplace

---

**Question 10**

*Objective: Explain the approaches for bringing data into Databricks, covering ingestion from S3, data sharing with external systems via Delta Sharing, API-driven data intake, the Auto Loader feature, and Marketplace.*

A partner company uses a non-Databricks platform and needs read access to a Delta table owned by your organization. The requirement is to share live data without copying it and without granting direct access to your cloud storage.

Which Databricks feature enables this cross-platform, zero-copy data sharing?

A. Auto Loader
B. External Tables with public S3 access
C. Lakehouse Federation
D. Delta Sharing

---

**Question 11**

*Objective: Use the Databricks Workspace UI to upload a data file to the platform.*

A business analyst has a 30 MB CSV file on their local machine and needs to load it into Databricks for exploratory analysis. The analyst does not have access to cloud storage buckets.

What is the correct approach?

A. Use the Databricks Workspace UI file upload feature to bring the file into the platform
B. Use the Databricks Assistant to paste the file contents and generate a table
C. Use Delta Sharing to transfer the local file into the workspace
D. Create an External Table pointing to the local file system path

---

## Section 4 — Executing Queries Using Databricks SQL

**Question 12**

*Objective: Create a materialized view, including knowing when to use Streaming Tables and Materialized Views, and differentiate between dynamic and materialized views.*

A data analyst needs to choose between a **Dynamic View** and a **Materialized View** for two different use cases:

- A view that masks the `credit_card` column for users without the `finance` role
- A view that pre-computes a complex aggregation refreshed nightly for a BI dashboard

Which combination is correct?

A. Use a Materialized View for both use cases
B. Use a Streaming Table for column masking; use a Dynamic View for the aggregation
C. Use a Materialized View for column masking; use a Streaming Table for the aggregation
D. Use a Dynamic View for column masking; use a Materialized View for the pre-computed aggregation

---

**Question 13**

*Objective: Create a materialized view, including knowing when to use Streaming Tables and Materialized Views, and differentiate between dynamic and materialized views.*

A data team is building a pipeline to process clickstream events that arrive continuously from a web application. The downstream table must always reflect newly arrived records as soon as they are processed.

Which object type should the analyst use?

A. Materialized View
B. Dynamic View
C. Streaming Table
D. External Table

---

**Question 14**

*Objective: Utilize Databricks Assistant within a Notebook or SQL Editor to facilitate query writing and debugging.*

A data analyst wrote a complex SQL query that involves multiple CTEs and window functions. The query runs without errors but returns unexpected results. The analyst wants a step-by-step breakdown of what the query is doing.

Which Databricks Assistant command should the analyst use?

A. `/explain`
B. `/generate`
C. `/fix`
D. `/optimize`

---

**Question 15**

*Objective: Querying cross-system analytics by joining data from a Delta table and a federated data source.*

A data analyst needs to join a Delta table stored in Databricks with a table from an external PostgreSQL database — without moving the PostgreSQL data into Databricks.

What is this capability called in the Databricks platform?

A. Delta Sharing cross-system join
B. Auto Loader external join
C. Unity Catalog external table merge
D. Cross-system analytics using Lakehouse Federation (federated query)

---

**Question 16**

*Objective: Perform aggregate operations such as count, approximate count distinct, mean, and summary statistics.*

A data analyst writes the following query:

```sql
SELECT department, AVG(salary) AS avg_salary
FROM employees
WHERE avg_salary > 5000;
```

The query returns an error. What is the reason?

A. `AVG` is not a valid aggregate function in Databricks SQL
B. The `salary` column must also appear in a `GROUP BY` clause
C. Aggregate functions cannot be referenced in a `WHERE` clause; a `HAVING` clause must be used instead
D. The `WHERE` clause must come after the `GROUP BY` clause

---

**Question 17**

*Objective: Perform aggregate operations such as count, approximate count distinct, mean, and summary statistics.*

A data analyst needs to count the number of orders per customer and return only customers with more than 5 orders.

Which query correctly implements this requirement?

A.
```sql
SELECT customer_id, COUNT(*) AS total_orders
FROM orders
WHERE COUNT(*) > 5
GROUP BY customer_id;
```

B.
```sql
SELECT customer_id, COUNT(*) AS total_orders
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 5;
```

C.
```sql
SELECT customer_id, COUNT(*) AS total_orders
FROM orders
GROUP BY customer_id
WHERE total_orders > 5;
```

D.
```sql
SELECT customer_id, COUNT(*) AS total_orders
FROM orders
HAVING COUNT(*) > 5;
```

---

**Question 18**

*Objective: Use Delta Lake's time travel to access and query historical data versions.*

A data analyst needs to query a Delta table called `orders` as it existed exactly 7 days ago using a dynamic date expression.

Which query correctly implements this?

A. `SELECT * FROM orders TIMESTAMP AS OF date_sub(current_date(), 7)`
B. `SELECT * FROM orders HISTORY AS OF 7 DAYS AGO`
C. `SELECT * FROM orders VERSION AS OF 7`
D. `SELECT * FROM orders AT TIME INTERVAL -7 DAYS`

---

**Question 19**

*Objective: Use Delta Lake's time travel to access and query historical data versions.*

A data analyst runs `DESCRIBE HISTORY inventory_table` and sees that version 20 is the latest. The analyst needs to retrieve the state of the table at **version 15**.

Which query is correct?

A. `SELECT * FROM inventory_table AT VERSION 15`
B. `SELECT * FROM inventory_table RESTORE TO VERSION 15`
C. `SELECT * FROM inventory_table HISTORY 15`
D. `SELECT * FROM inventory_table VERSION AS OF 15`

---

**Question 20**

*Objective: Write queries to combine tables using various join operations with single or multiple keys, as well as set operations like union and union all.*

A data analyst needs to combine results from two queries. The first query returns sales from the North region and the second returns sales from the South region. Some customers appear in both result sets and must appear **twice** in the final output.

Which set operation should be used?

A. `UNION`
B. `UNION ALL`
C. `INTERSECT`
D. `EXCEPT`

---

## Section 5 — Analyzing Queries

**Question 21**

*Objective: Apply Liquid Clustering to improve query speed when filtering large tables on specific columns.*

A data team manages a large Delta table with 500 million rows. Users frequently filter on the `region` and `product_category` columns, but the filter combinations vary across different reports. The team wants to improve query performance without committing to a fixed partition scheme.

Which approach should they use?

A. Partition the table by `region` and use `ZORDER BY product_category`
B. Enable Photon on the SQL Warehouse and rely on automatic optimization
C. Create a Materialized View pre-filtered by each region
D. Apply Liquid Clustering on `region` and `product_category`

---

**Question 22**

*Objective: Identify poorly performing queries in the Databricks Intelligence platform, such as Query Insights, Query Profiler log, etc.*

A data analyst suspects that a query is performing an expensive shuffle operation due to a poorly written join. The analyst wants to inspect the execution stages, data read volumes, and shuffle metrics.

Which tool should the analyst use?

A. Query Profiler (Query Profile log)
B. Query History filtered by duration
C. Catalog Explorer lineage view
D. `DESCRIBE HISTORY` on the target table

---

**Question 23**

*Objective: Understand the Features, Benefits, and Supported Workloads of Photon.*

A data engineering team is evaluating ways to accelerate SQL workloads and large DataFrame operations on their Databricks SQL Warehouse without rewriting their queries.

What is Photon and how does it help?

A. A caching layer that stores recent query results for reuse
B. A query optimizer that rewrites SQL queries at parse time for better performance
C. A monitoring tool that identifies slow queries and suggests index creation
D. A native vectorized query engine written in C++ that accelerates SQL and DataFrame operations transparently

---

**Question 24**

*Objective: Utilize query history and caching to reduce development time and query latency.*

A data analyst runs the same query twice on a SQL Warehouse. The first execution takes 12 seconds. The second execution, run 2 minutes later with no data changes, returns results instantly.

What most likely explains the second execution's speed?

A. Photon automatically compiled and cached the query plan
B. The result was served from the SQL Warehouse result cache
C. The SQL Warehouse scaled up to a larger size between executions
D. Liquid Clustering reorganized the data files between the two executions

---

**Question 25**

*Objective: Use Delta Lake's time travel to access and query historical data versions.*

A data analyst attempts to query a Delta table using `TIMESTAMP AS OF '2024-06-01'` but receives an error stating that the version is no longer available.

What is the most likely cause of this error?

A. The table schema was changed after June 1st, which prevents time travel to earlier versions
B. Time travel using timestamps is not supported; only `VERSION AS OF` is valid
C. The table was renamed after June 1st, which removes access to historical versions
D. A `VACUUM` operation deleted the data files and log entries needed to reconstruct that version

---

## Section 6 — Working with Dashboards and Visualizations

**Question 26**

*Objective: Schedule an automatic dashboard refresh.*

A data analyst has built an AI/BI Dashboard that displays daily sales metrics. Business stakeholders expect to see updated numbers every morning at 7:00 AM without any manual intervention.

What should the analyst configure?

A. An automatic scheduled refresh on the dashboard set to run daily at 7:00 AM
B. A Databricks Job that runs a notebook and triggers the dashboard
C. A SQL Alert that triggers a dashboard reload when new data is detected
D. A Genie Space that automatically refreshes connected dashboards

---

**Question 27**

*Objective: Identify the effective visualization type to communicate insights clearly.*

A data analyst needs to present the monthly revenue trend for the past 24 months to executive stakeholders. The goal is to clearly show the direction and magnitude of change over time.

Which visualization type is most appropriate?

A. Pie chart
B. Line chart
C. Scatter plot
D. Heatmap

---

**Question 28**

*Objective: Work with parameters in SQL queries and dashboards, including defining, configuring, and testing parameters.*

A data analyst built an AI/BI Dashboard that shows regional sales data. Business users want to filter the data by date range interactively without the analyst having to modify the underlying queries.

What is the correct approach?

A. Create a separate dashboard for each date range and let users choose
B. Use a Dynamic View with row-level filters for each date
C. Schedule the dashboard to refresh for each date range automatically
D. Add a date range parameter widget to the dashboard and reference it in the SQL query's `WHERE` clause

---

**Question 29**

*Objective: Configure permissions through the UI to share dashboards with workspace users/groups, external users through shareable links, and embed dashboards in external apps.*

A data analyst needs to share an AI/BI Dashboard with a group of external stakeholders who do not have Databricks workspace accounts.

Which sharing method should the analyst use?

A. Add each external user as a guest to the Databricks workspace
B. Export the dashboard as a PDF and share via email
C. Generate a shareable link with "Can View" permissions
D. Publish the dashboard to the Databricks Marketplace

---

**Question 30**

*Objective: Configure an alert with a desired threshold and destination.*

A data analyst monitors a pipeline that processes financial transactions. The analyst must be notified via email immediately when the number of failed transactions in the last hour exceeds 50.

Which Databricks feature should the analyst use?

A. A scheduled dashboard that shows failed transaction counts
B. A Delta Lake audit log query with a notification script
C. A SQL Alert based on a query that counts failed transactions, triggered when the result exceeds 50
D. A Databricks Job with a failure notification webhook

---

## Section 7 — Developing, Sharing, and Maintaining AI/BI Genie Spaces

**Question 31**

*Objective: Describe the purpose, key features, and components of AI/BI Genie spaces.*

A business team wants to ask questions about their sales data using natural language, such as "What were the top 5 products last quarter?", without needing to write SQL.

Which Databricks feature is designed for this use case?

A. AI/BI Dashboards with parameterized widgets
B. AI/BI Genie Spaces
C. Databricks Assistant in the SQL Editor
D. Databricks Marketplace data apps

---

**Question 32**

*Objective: Optimize AI/BI Genie spaces by tracking user questions, response accuracy, and feedback.*

After deploying a Genie Space, users report that answers to frequently asked questions are inconsistent or incorrect. The data analyst wants to improve response reliability for known, validated questions.

What is the recommended action?

A. Add the validated SQL queries as **Trusted Assets** and refine the domain-specific instructions
B. Replace the SQL Warehouse with a larger cluster size
C. Remove less-used tables from the Genie Space to reduce confusion
D. Increase the number of sample questions to cover all edge cases

---

**Question 33**

*Objective: Create Genie spaces by defining reasonable sample questions and domain-specific instructions, choosing SQL warehouses, curating Unity Catalog datasets, and vetting queries as Trusted Assets.*

A data analyst is setting up a new AI/BI Genie Space for the marketing team.

Which of the following elements must be configured when creating the Genie Space? (Select the best answer)

A. Only the SQL Warehouse and the connected tables
B. Sample questions and the SQL Warehouse
C. SQL Warehouse, curated Unity Catalog datasets, sample questions, domain-specific instructions, and Trusted Assets
D. Only the Trusted Assets and domain-specific instructions

---

## Section 8 — Data Modeling with Databricks SQL

**Question 34**

*Objective: Apply industry-standard data modeling techniques, such as star, snowflake, and data vault schemas, to analytical workloads.*

A data analyst is designing a data model for a retail analytics use case. The model should have a central table storing sales transactions linked to separate tables for customer, product, store, and date attributes.

Which data modeling pattern does this describe?

A. Data Vault
B. Third Normal Form (3NF)
C. Snowflake Schema
D. Star Schema

---

**Question 35**

*Objective: Understand how industry-standard models align with the Medallion Architecture.*

A data team uses the Medallion Architecture with Bronze, Silver, and Gold layers. They want to apply a Star Schema model for consumption by BI tools.

In which layer should the Star Schema model be applied?

A. Bronze layer, as it stores raw ingested data
B. Silver layer, after initial data cleansing
C. Gold layer, as it contains aggregated and modeled data ready for analytics
D. It should span both Silver and Gold layers equally

---

## Section 9 — Securing Data

**Question 36**

*Objective: Use Unity Catalog roles and sharing settings to ensure workspace objects are secure.*

A data team lead needs to grant a group called `analysts` the ability to **read data** from a specific table `gold.sales.monthly_summary` in Unity Catalog.

Which SQL statement is correct?

A. `GRANT READ ON TABLE gold.sales.monthly_summary TO GROUP analysts;`
B. `GRANT SELECT ON TABLE gold.sales.monthly_summary TO GROUP analysts;`
C. `ALLOW SELECT ON gold.sales.monthly_summary FOR GROUP analysts;`
D. `SET PERMISSION SELECT ON gold.sales.monthly_summary TO analysts;`

---

**Question 37**

*Objective: Understand how the 3-level namespace works in the Unity Catalog.*

A data analyst executes `DROP TABLE gold.reporting.customer_summary`. The table was defined as an **external table** pointing to data files stored in an S3 bucket.

What happens to the data files after this operation?

A. The metadata is removed from Unity Catalog, but the data files in S3 remain unchanged
B. Both the metadata and the data files in S3 are permanently deleted
C. The operation fails because external tables cannot be dropped using `DROP TABLE`
D. The data files are moved to the Unity Catalog recycle bin for 30 days

---

**Question 38**

*Objective: Apply best practices for storage and management to ensure data security, including table ownership and PII protection.*

A security team requires that users in the `standard_analysts` group see a masked version of the `ssn` column (e.g., `***-**-XXXX`) when querying a regulated table, while users in the `compliance_team` group see the full value.

Which Unity Catalog feature enables this column-level data masking behavior?

A. Row filters applied to the `ssn` column
B. Column masks defined on the table
C. Certified table flags that block access to PII columns
D. PII tags that automatically redact column values at query time

---

**Question 39**

*Objective: Use Unity Catalog roles and sharing settings to ensure workspace objects are secure.*

A data platform admin needs to grant a user the ability to create new schemas inside an existing catalog called `silver`, without giving them access to other catalogs.

Which privilege should be granted?

A. `GRANT CREATE SCHEMA ON CATALOG silver TO USER data_engineer@company.com;`
B. `GRANT ALL PRIVILEGES ON CATALOG silver TO USER data_engineer@company.com;`
C. `GRANT CREATE TABLE ON CATALOG silver TO USER data_engineer@company.com;`
D. `GRANT USE CATALOG ON CATALOG silver TO USER data_engineer@company.com;`

---

**Question 40**

*Objective: Apply best practices for storage and management to ensure data security, including table ownership and PII protection.*

A junior analyst needs access to read only the table `gold.finance.budget_summary`. Following data security best practices in Unity Catalog, what is the minimum set of privileges the analyst needs?

A. `GRANT ALL PRIVILEGES ON CATALOG gold`
B. `GRANT USE CATALOG ON CATALOG gold`, `GRANT USE SCHEMA ON SCHEMA gold.finance`, and `GRANT SELECT ON TABLE gold.finance.budget_summary`
C. `GRANT SELECT ON SCHEMA gold.finance`
D. `GRANT USE CATALOG ON CATALOG gold` and `GRANT SELECT ON TABLE gold.finance.budget_summary`

---

---

# Answer Key

| Q | Answer | Key Concept |
|---|--------|-------------|
| 1 | C | Unity Catalog = centralized governance |
| 2 | A | Lakeflow Jobs = Workflows/Jobs orchestration |
| 3 | B | `catalog.schema.table` — 3-level namespace |
| 4 | C | Catalog Explorer = lineage, certification, tags |
| 5 | D | Marketplace = third-party data/models discovery |
| 6 | A | `DELETE FROM ... WHERE` is the correct DML syntax |
| 7 | C | Tags can be applied via SQL or Catalog Explorer UI |
| 8 | B | Managed table DROP removes metadata AND data files |
| 9 | C | Auto Loader = incremental file ingestion from cloud storage |
| 10 | D | Delta Sharing = zero-copy cross-platform sharing |
| 11 | A | Workspace UI upload for local files |
| 12 | D | Dynamic View = masking; Materialized View = pre-computed cache |
| 13 | C | Streaming Table = continuous real-time ingestion |
| 14 | A | `/explain` = step-by-step query explanation |
| 15 | D | Lakehouse Federation = federated cross-system query |
| 16 | C | Aggregates in filter conditions require `HAVING`, not `WHERE` |
| 17 | B | `GROUP BY` + `HAVING COUNT(*) > 5` is correct |
| 18 | A | `TIMESTAMP AS OF date_sub(current_date(), 7)` |
| 19 | D | `VERSION AS OF 15` is the correct time travel syntax |
| 20 | B | `UNION ALL` preserves duplicates; `UNION` deduplicates |
| 21 | D | Liquid Clustering for flexible column-based filtering |
| 22 | A | Query Profiler shows stages, shuffle, and I/O metrics |
| 23 | D | Photon = C++ vectorized engine, transparent acceleration |
| 24 | B | SQL Warehouse result cache serves identical queries instantly |
| 25 | D | `VACUUM` removes old log/data files, limiting time travel depth |
| 26 | A | Scheduled refresh = configured directly on the dashboard |
| 27 | B | Line chart is best for trends over time |
| 28 | D | Parameter widgets + `WHERE` clause in SQL query |
| 29 | C | Shareable link with "Can View" for external users |
| 30 | C | SQL Alert = query + threshold + notification destination |
| 31 | B | Genie Spaces = natural language interface over data |
| 32 | A | Trusted Assets + domain instructions improve accuracy |
| 33 | C | All elements: warehouse, datasets, questions, instructions, trusted assets |
| 34 | D | Star Schema = central fact table + dimension tables |
| 35 | C | Gold layer = modeled, consumption-ready data |
| 36 | B | `GRANT SELECT ON TABLE` is the correct read privilege |
| 37 | A | External table DROP = removes metadata only; files stay |
| 38 | B | Column masks = column-level masking per group/role |
| 39 | A | `GRANT CREATE SCHEMA ON CATALOG` = schema creation privilege |
| 40 | B | Least privilege: USE CATALOG + USE SCHEMA + SELECT on table |
