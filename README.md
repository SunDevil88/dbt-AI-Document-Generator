# dbt AI Doc Generator 🤖

Automatically generates dbt model and column descriptions from SQL source
code using the OpenAI API (GPT-4o). No more manually writing schema.yml
documentation — just run one command.

---

## The Problem

In dbt projects, every model and column inside `schema.yml` needs a
description. Writing these manually is tedious and often skipped entirely,
leaving documentation empty or outdated.

## The Solution

This script reads your SQL models, sends them to GPT-4o, and automatically
fills in descriptions inside `schema.yml` — in seconds.

---

## How It Works

1. Scans all `schema.yml` files across the `models/` directory
2. Finds the matching `.sql` file for each model
3. Sends the SQL + column names to GPT-4o as context
4. Gets back structured JSON descriptions
5. Writes them directly into `schema.yml`

---

## Project Structure

```
dbt-ai-doc-generator/
├── models/
│   ├── staging/
│   │   ├── stg_orders.sql
│   │   └── schema.yml
│   └── marts/
│       ├── fct_orders.sql
│       └── schema.yml
├── scripts/
│   └── generate_docs.py
└── requirements.txt
```

---

## Quickstart

```bash
# 1. Clone the repo
git clone https://github.com/your-username/dbt-ai-doc-generator.git
cd dbt-ai-doc-generator

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your OpenAI API key
export OPENAI_API_KEY=your_key_here

# 4. Run the script
python scripts/generate_docs.py
```

---

## Example Output

**Before running the script:**

```yaml
- name: fct_orders
  description: ""
  columns:
    - name: order_key
      description: ""
    - name: total_price
      description: ""
```

**After running the script:**

```yaml
- name: fct_orders
  description: "Fact table capturing all customer orders with fulfillment
    status, pricing, and priority derived from staging order data."
  columns:
    - name: order_key
      description: "Surrogate key uniquely identifying each order."
    - name: total_price
      description: "Total monetary value of the order including all line items."
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Scripting and API integration |
| OpenAI API (GPT-4o) | LLM for generating descriptions |
| PyYAML | Reading and writing schema.yml files |
| dbt-style SQL models | Staging and mart layers (TPC-H schema) |

---

## Why This Matters

Modern analytics engineering teams are embedding LLMs directly into data
workflows — for documentation, anomaly explanation, and query generation.
This project demonstrates that pattern end-to-end.
