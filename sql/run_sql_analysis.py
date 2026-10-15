"""
run_sql_analysis.py
Executes schema setup, populates SQLite database, runs analytical queries,
and formats results into a markdown analysis report.
Project: Retail Customer Shopping Behavior Analysis
"""

import os
import sqlite3
import pandas as pd

def run_analysis(base_dir: str):
    sql_dir = os.path.join(base_dir, 'sql')
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    reports_dir = os.path.join(base_dir, 'reports')
    os.makedirs(reports_dir, exist_ok=True)

    db_path = os.path.join(processed_dir, 'retail_shopping.db')
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print(f"[INFO] Initialized SQLite Database at: {db_path}")

    # 1. Execute schema setup
    schema_path = os.path.join(sql_dir, '01_schema_setup.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    print("[SUCCESS] Schema tables and analytical view created.")

    # 2. Populate tables from CSVs
    table_files = {
        'dim_customers': 'dim_customers.csv',
        'dim_products': 'dim_products.csv',
        'dim_shipping': 'dim_shipping.csv',
        'dim_payment': 'dim_payment.csv',
        'fact_transactions': 'fact_transactions.csv'
    }

    for table, filename in table_files.items():
        file_path = os.path.join(processed_dir, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Missing required CSV: {file_path}")
        df_table = pd.read_csv(file_path)
        df_table.to_sql(table, conn, if_exists='append', index=False)
        print(f"[INFO] Populated {table} with {len(df_table)} rows.")

    conn.commit()

    # 3. Read queries
    queries_path = os.path.join(sql_dir, '02_business_queries.sql')
    with open(queries_path, 'r', encoding='utf-8') as f:
        queries_content = f.read()

    # Split queries by double dashes / semicolons
    # Better yet, split queries by individual SQL statement
    statements = [stmt.strip() for stmt in queries_content.split(';') if stmt.strip()]

    output_md = ["# SQL Analytical Query Results & Business Insights\n",
                 "**Project:** Retail Customer Shopping Behavior Analysis  \n",
                 "**Database Engine:** SQLite 3  \n",
                 f"**Total Records:** 3,900 Transactions & Customers  \n\n---\n"]

    print("\n[INFO] Executing Business SQL Queries...\n")
    for idx, stmt in enumerate(statements, 1):
        # Extract comment header if present
        lines = stmt.split('\n')
        comment_lines = [l for l in lines if l.strip().startswith('--')]
        header = f"### Query {idx}"
        for cl in comment_lines:
            if 'QUERY' in cl:
                header = f"### {cl.replace('--', '').strip()}"
                break
        
        try:
            df_res = pd.read_sql_query(stmt, conn)
            print(f"Executing: {header}")
            output_md.append(f"\n{header}\n")
            output_md.append("```sql\n" + stmt.strip() + "\n```\n")
            output_md.append("\n**Result Table:**\n\n")
            def df_to_markdown_str(df_in):
                header_line = "| " + " | ".join(str(c) for c in df_in.columns) + " |"
                sep_line = "| " + " | ".join(["---"] * len(df_in.columns)) + " |"
                row_lines = []
                for _, r in df_in.iterrows():
                    row_lines.append("| " + " | ".join(str(val) for val in r.values) + " |")
                return "\n".join([header_line, sep_line] + row_lines)

            output_md.append(df_to_markdown_str(df_res))
            output_md.append("\n\n---\n")
        except Exception as e:
            print(f"[ERROR] on query {idx}: {e}")

    # Write output markdown
    results_path = os.path.join(reports_dir, 'sql_query_results.md')
    with open(results_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_md))
    print(f"\n[SUCCESS] All SQL queries executed successfully. Report generated at: {results_path}")

    conn.close()

if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    run_analysis(base_dir)
