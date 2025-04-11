from pathlib import Path
import yaml
from loguru import logger
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

module_path = Path(__file__).resolve().parent.parent
with open(module_path / 'config.yaml', 'r', encoding='utf8') as file:
    config = yaml.safe_load(file)

class TxtConverter:
    def __init__(self):
        self.use_llm = config.get('USE_LLM', False)
        if self.use_llm:
            self.model_name = config['DEFAULT_LLM_MODEL']
            logger.info(f"Loading model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model.to(self.device)
            logger.info(f"Model loaded on {self.device}")

    def _generate_text(self, prompt, max_length=500):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_length=max_length,
            num_return_sequences=1,
            temperature=0.7,
            do_sample=True
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def process_video_description(self, texts: list):
        if not self.use_llm:
            return str(texts[0])
        
        prompt = f"Convert this video description into a concise paragraph: {str(texts)}"
        return self._generate_text(prompt)

    def txt_converter(self, content, addtxt=None):
        if addtxt:
            content += addtxt

        if not self.use_llm:
            return content

        prompt = f"""
        Given the scene description below, identify the instruments that best match the mood of the scene. Choose 2-3 instruments and the most suitable musical key.

        Scene: "{content}"

        Response format:
        - Instruments: [list of 2-3 instruments]
        - Key: [musical key]
        
        """

        # Generate the response from the LLM
        converted_result = self._generate_text(prompt)
        logger.info("Converted result: " + converted_result)
        return converted_result

    def video_txt_converter(self, content, addtxt=None):
        if addtxt:
            content += addtxt

        if not self.use_llm:
            return content

        prompt = f"Convert this video caption into a musical description with mood and genre: {content}"
        converted_result = self._generate_text(prompt)
        logger.info("converted result: " + converted_result)
        return converted_result

if __name__ == "__main__":
    content = input()
    txt_con = TxtConverter()
    converted_result = txt_con.txt_converter(content)