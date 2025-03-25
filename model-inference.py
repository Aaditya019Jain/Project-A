import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import outlines

# Check for GPU availability
device = "cuda" if torch.cuda.is_available() else "cpu"

model = "<path to the model checkpoints>"

# Load the model into Outlines with the manually loaded transformers model
outlines_model = outlines.models.transformers(model, device=device)

# outlines_model = outlines.models.transformers("microsoft/Phi-3.5-mini-instruct")

prompt = """Here are the tables that are present in an SQL database. I will give you a query and for it we have to generate a SQL query.
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
"""
usr_prompt = "Update the service status of Jawan ID 1002 to 'Retired'./n Please help me put the information given in the prompt in their proper tables and columns"
model_prompt = prompt + usr_prompt

answer = outlines.generate.text(outlines_model)
answer_final = answer(model_prompt)
print(answer)
