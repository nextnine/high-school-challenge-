from config.settings import settings
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class ModelLoader:
    def __init__(self):
        self.model = None
        self.tokenizer = None
    
    async def load_model(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            settings.MODEL_NAME
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            settings.MODEL_NAME,
            torch_dtype=getattr(torch, settings.MODEL_PRECISION),
            device_map="auto"
        ).to("cuda")