from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from omegaconf import OmegaConf

class Translator:
    def __init__(self, config_path):
        self.config = OmegaConf.load(config_path)
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_name)
    def __call__(self, text):
        src_texts = [f"arb>> {text}"]

        inputs = self.tokenizer(src_texts, return_tensors="pt", padding=True, truncation=True)
        translated = self.model.generate(**inputs)

        translated_texts = self.tokenizer.batch_decode(translated, skip_special_tokens=True)
        return translated_texts[0]
        
