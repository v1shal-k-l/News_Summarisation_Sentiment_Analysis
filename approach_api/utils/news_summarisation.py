# Importing Libraries
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

device = "cuda" if torch.cuda.is_available() else "cpu"
model_ckpt = "google/pegasus-cnn_dailymail" ## Model for Summarization
tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(model_ckpt).to(device)

# Function to Summarize Text
def summarize_text(text: str) -> str:
    input_ids = tokenizer.encode(
        text,
        return_tensors="pt",
        max_length=1024,
        truncation=True,
    ).to(device)
    try:
        summary_ids = model_pegasus.generate(input_ids, max_length=130, min_length=30, do_sample=False)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    except RuntimeError as e:
        print(f"Summarization Error: {e}")
        return "Error: Could not generate summary due to length constraints."

