import os
import json
import yaml
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def generate_docs_for_model(model_name: str, sql: str, columns: list) -> dict:
    column_names = ", ".join([c.get("name", "") for c in columns]) or "none listed"

    prompt = f"""You are a dbt documentation expert.

Given the SQL model named '{model_name}', generate:
1. A concise model description (1-2 sentences) explaining what this model contains and its business purpose.
2. A brief description for each column listed.

SQL:
```sql
{sql}
```

Columns to describe: {column_names}

Respond ONLY in this exact JSON format with no extra text:
{{
  "model_description": "...",
  "column_descriptions": {{
    "column_name": "description here"
  }}
}}"""

    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def update_schema_yaml(schema_path: Path, model_name: str, docs: dict):
    with open(schema_path, "r") as f:
        schema = yaml.safe_load(f)

    for model in schema.get("models", []):
        if model["name"] == model_name:
            model["description"] = docs.get("model_description", "")
            for col in model.get("columns", []):
                col_name = col["name"]
                if col_name in docs.get("column_descriptions", {}):
                    col["description"] = docs["column_descriptions"][col_name]
            break

    with open(schema_path, "w") as f:
        yaml.dump(schema, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"  ✅ Updated: {schema_path}")


def main():
    models_dir = Path("models")
    schema_files = list(models_dir.rglob("schema.yml"))

    if not schema_files:
        print("❌ No schema.yml files found. Run from project root.")
        return

    for schema_path in schema_files:
        with open(schema_path, "r") as f:
            schema = yaml.safe_load(f)

        for model in schema.get("models", []):
            model_name = model["name"]
            sql_path = schema_path.parent / f"{model_name}.sql"

            if not sql_path.exists():
                print(f"⚠️  Skipping {model_name} — SQL not found at {sql_path}")
                continue

            print(f"\n🔍 Generating docs for: {model_name}")
            sql = sql_path.read_text()
            columns = model.get("columns", [])

            try:
                docs = generate_docs_for_model(model_name, sql, columns)
                update_schema_yaml(schema_path, model_name, docs)
            except Exception as e:
                print(f"  ❌ Failed for {model_name}: {e}")

    print("\n✅ Done. Review your schema.yml files and commit.")


if __name__ == "__main__":
    main()