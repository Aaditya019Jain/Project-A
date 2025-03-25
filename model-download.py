from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "microsoft/Phi-3.5-mini-instruct"
model = AutoModelForCausalLM.from_pretrained(model_name)  # Use AutoModelForCausalLM
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Save the model and tokenizer locally
model.save_pretrained("/Users/aadityajain/Downloads/Project-A/model-checkpoints")  # Saves model checkpoints
tokenizer.save_pretrained("/Users/aadityajain/Downloads/Project-A/model-checkpoints")  # Saves tokenizer
