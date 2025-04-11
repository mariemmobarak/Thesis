from pathlib import Path
from PIL import Image
from loguru import logger
from .main import img_to_music_generate, import_ir, import_music_generator

def main():
    
    current_dir = Path(__file__).resolve().parent
    
   
    img = Image.open(current_dir / "TestPic.jpg")  
    
    music_duration = 25
    
    # hena bengib el required models
    image_recog = import_ir()
    music_gen = import_music_generator()
    
    output_folder = current_dir / "outputs"
    
    
    result = img_to_music_generate(
        img=img,
        music_duration=music_duration,
        image_recog=image_recog,
        music_gen=music_gen,
        output_folder=output_folder
    )
    
    
    logger.info(f"Original text: {result[0]}")
    logger.info(f"Converted text: {result[1]}")
    logger.info(f"Generated music file: {result[2]}")

if __name__ == "__main__":
    main() 