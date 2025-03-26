# Project-A

## Model Checkpoints
To download model checkpoints, just run [model-download.py](https://github.com/Aaditya019Jain/Project-A/blob/main/model-download.py).

## JSON creation
Using this pipeline the user can create JSON with the required Information using [JSON-generator.py](https://github.com/Aaditya019Jain/Project-A/blob/main/JSON-generator.py)

## JSON to SQL
The JSON can be converted to queries for any Databate like Postgress or MySQL. This code [JSON-to-SQL.py](https://github.com/Aaditya019Jain/Project-A/blob/main/JSON-to-SQL.py) can be used to convert JSON to a MySQL query.

# To generate SQL Query (complete pipeline)
The SQL query can be obtained from [integrated-pipeline.py](https://github.com/Aaditya019Jain/Project-A/blob/main/Integrated-pipeline.py) and [integrated-pipeline-new.py](https://github.com/Aaditya019Jain/Project-A/blob/main/Integrated-pipeline-new.py).
The ```integrated-pipeline-new.py``` is an updated version of ```integrated-pipeline.py``` which provides better quality SQL queries with faster Inference.


#Queries for testing:-
<ul>
  <li>Jawan name with ID '1002'</li>
  <li>"What is the rank and medical condition of Jawan with ID 1001?"</li>
  <li>"List all jawans who belong to the same unit as Jawan 1001, their rank, and any medical history."</li>
  <li>"List all jawans who have the blood group ‘B+’ and their leave details."</li>
</ul>
