from transformers import MT5ForConditionalGeneration, MT5Tokenizer
import torch

class T5Responder:
    def __init__(self, model_name="google/mt5-small", device=None, max_new_tokens=64):
        self.tokenizer = MT5Tokenizer.from_pretrained(model_name, lagecy=False)
        self.model = MT5ForConditionalGeneration.from_pretrained(model_name)
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.max_new_tokens = max_new_tokens

    def build_prompt(self, question: str, context: str) -> str:
        return f"Answer the question using the context.\nContext: {context}\nQuestion: {question}"

    def answer(self, question: str, context: str) -> str:
        prompt = self.build_prompt(question, context)
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(self.device)
        with torch.no_grad():
            output = self.model.generate(**inputs, max_new_tokens=self.max_new_tokens)
        return self.tokenizer.decode(output[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
