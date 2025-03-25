from transformers import AutoModel, AutoTokenizer

model_name = "microsoft/Phi-3.5-mini-instruct"  # Replace with your desired model

# Load the model and tokenizer
model = AutoModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Save the model and tokenizer locally
model.save_pretrained("/Users/aadityajain/Downloads/Project-A/model-checkpoints")  # Saves model checkpoints
tokenizer.save_pretrained("/Users/aadityajain/Downloads/Project-A/model-checkpoints")  # Saves tokenizer
