import json

def json_to_mysql(query_json):
    action = query_json.get("action", "").lower()
    tables = query_json.get("tables", [])
    values = query_json.get("values", {})
    constraint = query_json.get("constraint")
    
    if not tables:
        return "Error: No tables specified"
    
    if action == "select":
        # Extract table names and attributes
        select_fields = []
        table_aliases = {}
        joins = []
        main_table = tables[0]["table_name"]
        table_aliases[main_table] = "t0"
        
        # Create SELECT fields and join conditions
        for i, table in enumerate(tables):
            alias = f"t{i}"
            table_aliases[table["table_name"]] = alias
            
            for attr in table.get("attributes", []):
                if attr:  # Skip if attribute is null or empty
                    select_fields.append(f"{alias}.{attr}")
            
            if i > 0:
                joins.append(f"JOIN {table['table_name']} {alias} ON {alias}.Jawan_ID = t0.Jawan_ID")
        
        # Where clause
        where_clauses = []
        for key, value in values.items():
            if value:  # Skip if value is null
                if isinstance(value, str) and "." in value:
                    where_clauses.append(f"t0.{key} = (SELECT {value})")
                else:
                    where_clauses.append(f"t0.{key} = '{value}'")
        
        # Construct final query
        query = f"SELECT {', '.join(select_fields)} FROM {main_table} t0 "
        if joins:
            query += " " + " ".join(joins)
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        if constraint:
            query += f" LIMIT {constraint}"
        
        return query
    
    elif action == "update":
        # Extract table name (assuming first table is being updated)
        table_name = tables[0]["table_name"]
        set_clauses = [f"{key} = '{value}'" for key, value in values.items() if value]
        where_clause = " AND ".join([f"{key} = '{value}'" for key, value in values.items() if value])
        
        query = f"UPDATE {table_name} SET {', '.join(set_clauses)}"
        if where_clause:
            query += f" WHERE {where_clause}"
        
        return query
    
    else:
        return "Unsupported action"

# Example usage
query_json_str = "{
  "action": "SELECT",
  "constraint": 2,
  "tables": [
    {
      "table_name": "Jawan_Master",
      "attributes": ["Rank_ID", "Medical_History.Diagnosis"]
    },
    {
      "table_name": "Medical_History",
      "attributes": ["Diagnosis"]
    }
  ],
  "values": {
    "Jawan_ID": "1001"
  }
}"
query_json = json.loads(query_json_str)

query = json_to_mysql(query_json)
print(query)
