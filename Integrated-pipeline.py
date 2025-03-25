import torch
import json
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

# Check for GPU availability
device = "cuda" if torch.cuda.is_available() else "cpu"

# Enable 4-bit quantization
quantization_config = BitsAndBytesConfig(
    load_in_8bit=True,
    bnb_8bit_compute_dtype=torch.float16,
    bnb_8bit_use_double_quant=True,
    bnb_8bit_quant_type="nf8"
)

# Load the model and tokenizer once
model_name = "<path to your model>"
tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=quantization_config,
    device_map="auto"
)

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

def generate_text(prompt, max_tokens=50):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=512)
    return tokenizer.decode(output[0], skip_special_tokens=True)

prompt = """I am giving you the structure of a SQL database, after studying the data structure, you will be given a user prompt and we have to tell what information will trigger which table of the database and which attribute we will look into.
The sturcture is: /n

1. Jawan_Master – Stores personal details of jawans.  
   - Fields: Jawan_ID (PK), First_Name, Last_Name, Rank_ID (FK), Unit_ID (FK), Date_of_Birth, Gender, Blood_Group, Enrolment_Date, Service_Status.  
2. Medical_History – Tracks medical records of jawans, linked by Jawan_ID.  
   - Fields: Record_ID (PK), Jawan_ID (FK), Diagnosis, Treatment, Visit_Date, Followup_Required.  
3. Leave_Records – Records jawan leave details.  
   - Fields: Leave_ID (PK), Jawan_ID (FK), Leave_Type, From_Date, To_Date, Approval_Status, Approved_By.  
4. Rank_Master – Defines ranks in the army.  
   - Fields: Rank_ID (PK), Rank_Name, Rank_Code, Pay_Level, Rank_Order.  
5. Unit_Master – Stores information about military units.  
   - Fields: Unit_ID (PK), Unit_Name, Unit_Type, Parent_Unit_ID (FK), Commanding_Officer_ID (FK).  
The input of the user is: 
"""

usr_prompt = """. /n Just give me which tables will be used to handle this information from the user. Now that you know which table and what values
are used can you make a JSON out of it? the JSON should include the action being taken, the tables and the attribute values of the tables. Please enclose the JSON in ###{Your generated JSON}###
for examples:
###{
  "action": the action you decide from ["SELECT","UPDATE"],
  "constraint" : the number of values to extract (use only if such a constraint is mentioned),
  "tables": [
    {
      "table_name": the 1st required tables you found,
      "attributes": [the required attributes you found for table 1]
    },
    {
      "table_name": the 2nd required tables you found,
      "attributes": [the required attributes you found for table 2]
    }
  ],
  "values": {
    "attribute": value of the 1st attribute (mention only the value)
    "attribute": value of the 2nd attribute (mention only the value)
  }
}###"""


user_input = input("Enter Your Query: ")
usr_prompt_final = user_input + usr_prompt
model_prompt = prompt + usr_prompt_final
response = generate_text(model_prompt)
l = response.split("###")
query_json_str = l[5]
query_json = json.loads(query_json_str)

query = json_to_mysql(query_json)
print(query)
