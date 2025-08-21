from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

class T5Responder:
    def __init__(self, model_name="google/t5-v1_1-small", device=None, max_new_tokens=64):
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        self.model.to(self.device)
        self.max_new_tokens = max_new_tokens

    def build_prompt(self, question: str, context: str) -> str:
        return (
            "Answer the question using the context.\n"
            f"Context: {context}\n"
            f"Question: {question}"
        )

    def answer(self, question: str, context: str) -> str:
        prompt = self.build_prompt(question, context)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        output = self.model.generate(**inputs, max_new_tokens=self.max_new_tokens)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)
