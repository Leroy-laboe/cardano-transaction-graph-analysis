# Cardano-Inspired Transaction Graph Analysis

**A graph-analytics pipeline for exploring transaction-network structure, centrality, and high-activity entities using a synthetic blockchain-style dataset.**

Built with **Python, PostgreSQL, SQLAlchemy, NetworkX, pandas, and Matplotlib**.

> **Dataset scope:** this project does **not** query the Cardano blockchain. The transaction records and address labels are synthetically generated for experimentation with blockchain-style network analysis.

---

## Overview

The project models transactions as a directed weighted graph:

- **nodes** represent synthetic wallet/address identifiers;
- **directed edges** represent transfers between addresses;
- **edge weight** stores the aggregated transferred amount;
- **transaction count** records repeated transfers between the same address pair.

The pipeline then calculates network metrics and applies simple percentile-based heuristics to identify unusually connected or central nodes.

```text
Synthetic transactions
        │
        ▼
      CSV
        │
        ▼
   PostgreSQL
        │
        ▼
 Directed NetworkX graph
        │
        ├── in-degree
        ├── out-degree
        └── weighted PageRank
        │
        ▼
Top-percentile heuristic flags
        │
        ▼
CSV metrics + distribution plot
```

---

## Pipeline

### 1. Generate synthetic transactions

`src/01_make_data.py` creates a synthetic dataset containing:

- transaction ID;
- timestamp;
- source address;
- destination address;
- amount.

The default run generates:

- **80,000 transactions**;
- **12,000 synthetic addresses**;
- a small set of higher-activity source addresses to produce hub-like behaviour.

A fixed random seed is used for repeatable network structure, while timestamps are generated relative to the current run time.

### 2. Load into PostgreSQL

`src/02_load_to_db.py` loads the generated CSV into the `transactions` table using SQLAlchemy.

Database credentials are supplied through the `DATABASE_URL` environment variable and are **not stored in source code**.

### 3. Build the transaction graph

`src/03_build_graph.py` reads transactions from PostgreSQL and builds a directed NetworkX graph.

Repeated transfers between the same source and destination are aggregated into one edge with:

- `weight` — total transferred amount;
- `tx_count` — number of transfers.

The generated graph can be exported to GraphML for further analysis.

### 4. Compute graph metrics

`src/04_metrics.py` calculates:

- in-degree;
- out-degree;
- weighted PageRank.

It exports node-level metrics, the top PageRank nodes, and an out-degree distribution plot.

### 5. Flag high-activity / high-centrality nodes

`src/05_flag_suspicious.py` uses top-1%-percentile thresholds for:

- in-degree;
- out-degree;
- PageRank.

A node receives one point for each threshold it exceeds.

> These flags are **heuristics for exploratory analysis**. They do not establish fraud, criminal activity, or real-world suspicious behaviour.

---

## Example Results

The existing generated run recorded:

| Metric | Result |
| --- | ---: |
| Synthetic transactions | **80,000** |
| Graph nodes | **12,000** |
| Unique directed edges | **79,982** |
| High out-degree threshold | **≥ 14** |
| High in-degree threshold | **≥ 13** |
| High PageRank threshold | **≥ 0.0001978** |

These numbers describe the included synthetic experiment only and should not be interpreted as Cardano network statistics.

---

## Example Outputs

The repository includes lightweight example outputs from the synthetic run:

- `outputs/node_metrics.csv` — node-level graph metrics;
- `outputs/top20_pagerank.csv` — highest PageRank nodes;
- `outputs/suspicious.csv` — nodes triggered by one or more percentile heuristics;
- `outputs/degree_distribution.png` — out-degree distribution.

Large generated artifacts such as `data/tx.csv` and `outputs/tx_graph.graphml` are intentionally excluded from the cleaned repository and can be recreated by running the pipeline.

---

## Tech Stack

| Area | Technology |
| --- | --- |
| Language | Python |
| Database | PostgreSQL |
| Database access | SQLAlchemy, psycopg2 |
| Data processing | pandas |
| Graph analytics | NetworkX |
| Visualisation | Matplotlib |
| Configuration | python-dotenv / environment variables |

---

## Repository Structure

```text
.
├── src/
│   ├── 01_make_data.py
│   ├── 02_load_to_db.py
│   ├── 03_build_graph.py
│   ├── 04_metrics.py
│   ├── 05_flag_suspicious.py
│   └── config.py
├── sql/
│   └── schema.sql
├── outputs/
│   ├── degree_distribution.png
│   ├── node_metrics.csv
│   ├── suspicious.csv
│   └── top20_pagerank.csv
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Run Locally

### 1. Clone

```bash
git clone https://github.com/Leroy-laboe/cardano-transaction-graph-analysis.git
cd cardano-transaction-graph-analysis
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL database, then copy:

```text
.env.example
```

to:

```text
.env
```

and set your own local connection string:

```env
DATABASE_URL=postgresql+psycopg2://postgres:your_password@localhost:5432/cardano_graph
```

Apply the schema in `sql/schema.sql` to the database before loading transactions.

### 5. Run the pipeline

```bash
python src/01_make_data.py
python src/02_load_to_db.py
python src/03_build_graph.py
python src/04_metrics.py
python src/05_flag_suspicious.py
```

---

## What This Project Demonstrates

- synthetic data generation;
- relational data loading with PostgreSQL;
- environment-based secret configuration;
- directed weighted graph construction;
- degree-based network analysis;
- weighted PageRank;
- percentile-based anomaly heuristics;
- CSV and visual analytics output;
- building a multi-stage data-analysis pipeline.

---

## Limitations

- the dataset is synthetic rather than on-chain Cardano data;
- generated address labels are not valid blockchain wallet addresses;
- transfer behaviour is simplified;
- the heuristic flags are based only on degree and PageRank percentiles;
- there is no ground-truth fraud dataset;
- results should not be interpreted as real-world financial-risk classifications.

---

## Possible Extensions

- ingest public on-chain datasets;
- model UTXO structure more faithfully;
- add temporal graph features;
- calculate betweenness and community structure;
- add transaction-amount and burst-frequency features;
- compare heuristic flags with unsupervised anomaly-detection methods;
- build an interactive graph exploration dashboard.

---

## Author

**Leroy Nyasha Mangwarara**

Computer Science · Data Science · Software Engineering · Applied Analytics

[GitHub](https://github.com/Leroy-laboe) · [LinkedIn](https://www.linkedin.com/in/leroy-nyasha-mangwarara-86185a302/) · [Email](mailto:mangwararaleroy@gmail.com)
