import csv
from pathlib import Path


FILES = [
    "census_relationships_clean.csv",
    "compas_relationships_clean.csv",
    "german_relationships_clean.csv",
    "asd_relationships_clean.csv",
]


def safe_rel_type(rel_type: str) -> str:
    rel_type = rel_type.strip()
    if not rel_type:
        raise ValueError("Empty relationship type")
    if not rel_type.replace("_", "").isalnum():
        raise ValueError(f"Unsafe relationship type: {rel_type}")
    return rel_type


def get_types(path: Path):
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return sorted({safe_rel_type(row["type"]) for row in reader if row.get("type")})


def make_query(filename: str, rel_type: str) -> str:
    return f"""
:auto
LOAD CSV WITH HEADERS FROM 'file:///{filename}' AS row
CALL (row) {{
  WITH row
  WHERE row.type = '{rel_type}'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {{uid: row.pipeline + '::' + row.source}})
  MATCH (t:ProvNode {{uid: row.pipeline + '::' + row.target}})

  CREATE (s)-[r:{rel_type}]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
}} IN TRANSACTIONS OF 1000 ROWS;
"""


def main():
    out = Path("import_relationships_static.cypher")
    parts = []
    for filename in FILES:
        path = Path(filename)
        if not path.exists():
            print(f"Skipping missing file: {filename}")
            continue

        rel_types = get_types(path)
        print(filename, rel_types)

        for rel_type in rel_types:
            parts.append(make_query(filename, rel_type))

    out.write_text("\n".join(parts), encoding="utf-8")
    print(f"Written: {out}")


if __name__ == "__main__":
    main()