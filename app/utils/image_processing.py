
from PIL import Image
from clip_interrogator import Config, Interrogator
import torch.cuda
from pathlib import Path

app_path = Path(__file__).resolve().parent.parent

ci_config = Config()
ci_config.clip_model_name = "ViT-H-14/laion2b_s32b_b79k"
ci_config.caption_model_name = "blip-base"
ci_config.device = 'cuda' if torch.cuda.is_available() else 'cpu'
ci_config.blip_offload = False if torch.cuda.is_available() else True
ci_config.chunk_size = 1024
ci_config.flavor_intermediate_count = 1024


def img2txt(ci, image):
    image =Image.open(image)
    image = image.convert('RGB')
    prompt_result = ci.interrogate_classic(image)
    return prompt_result

if __name__=="__main__":
    ci = Interrogator(ci_config)
    test_image = app_path / "static" / "test.jpg"
    image =Image.open(test_image)
    image = image.convert('RGB')
    image.show()
    print(img2txt(ci, test_image))