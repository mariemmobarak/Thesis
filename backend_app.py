from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
# import uvicorn
from io import BytesIO
from PIL import Image
from pydantic import BaseModel
from pathlib import Path

import uvicorn
import MozartsTouch
from loguru import logger
from typing import Optional

router = APIRouter(prefix="/v1", tags=["v1"])
models = {}
app_path = Path(__file__).parent# app_path为项目根目录（`/`）

class MusicResponse(BaseModel):
    prompt: str
    converted_prompt: str
    result_file_url: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    models["music_generator"] = MozartsTouch.import_music_generator()
    models["image_recog"] = MozartsTouch.import_ir()

    yield

    # Clean up the ML models and release the resources
    del models["music_generator"]
    del models["image_recog"]

# Create FastAPI app
app = FastAPI(title='点彩成乐', description='“点彩成乐”项目后端', lifespan=lifespan)

origins = ["http://localhost:5173"]
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@router.post("/image", response_model=MusicResponse)
async def upload_image(file: UploadFile = File(...),
                       music_duration: Optional[int] = Form(10),
                       instruction: Optional[str] = Form("")):
    '''
    上传图片以进行音乐生成

    Parameters:
    - file: 图片文件，Content-Type: image/*
    - music_duration: 指定生成时间，请输入整数，以秒为单位。默认值为10秒。若使用Suno AI生成音乐则此参数会被忽略
    - instruction: 用户输入的限定文本，可选

    Return: 
    - prompt: 图片转文本结果
    - converted_prompt: 用于生成音乐的提示词文本
    - result_file_url: 生成的音频URL，使用GET方法访问"result_file_url"获取音频文件
    '''
    logger.info("Request Received Successfully, Processing...")
    output_folder = app_path / "outputs"

    img = Image.open(file.file)
    result = MozartsTouch.img_to_music_generate(img, music_duration, models["image_recog"], models["music_generator"], output_folder)

    if not models["music_generator"].model_name.startswith("suno"):
        prefix = 'http://localhost:3001/music/'
        result = (*result[:2], prefix + result[2])

    result_dict = {key: value for key, value in zip(("prompt", "converted_prompt", "result_file_url"), result)}
    logger.info('**********FINAL RESULT**********')
    logger.info(result_dict)

    return result_dict

@router.post("/video", response_model=MusicResponse)
async def upload_video(file: UploadFile = File(...), instruction: Optional[str] = Form('')):
    '''
    上传视频以进行音乐生成

    Parameters:
    - file: 图片文件，Content-Type: image/*
    - instruction: 用户输入的限定文本，可选

    Return: 
    - prompt: 图片转文本结果
    - converted_prompt: 用于生成音乐的提示词文本
    - result_file_url: 视频配合生成的音频的最终视频，使用GET方法访问"result_file_url"获取视频文件
    '''
    logger.info("Request Received Successfully, Processing...")
    output_folder = app_path / "outputs"
    video_path = app_path / "videos" / file.filename

    # 将视频保存至本地，然后读取视频帧
    contents = await file.read()
    with open(video_path, "wb") as f:
        f.write(contents)

    result = MozartsTouch.video_to_music_generate(str(video_path), models["image_recog"], models["music_generator"], output_folder, instruction)

    prefix = 'http://localhost:3001/music/'  # 将musicgen生成的音乐文件名包装成URL
    filename_with_prefix = prefix + result[2]
    result = (*result[:2], filename_with_prefix)

    result_dict = {key: value for key, value in zip(("prompt", "converted_prompt", "result_file_url"), result)}
    logger.info('**********FINAL RESULT**********')
    logger.info(result_dict)

    return result_dict

@router.get("/music/{result_file_name}")
async def get_music(result_file_name: str):
    '''
    获取/outputs目录下对应名称的文件

    Return: 
    - 音频文件
    '''
    file_full_path = app_path / "outputs" / result_file_name
    logger.info(f'Return file {file_full_path}')
    return FileResponse(file_full_path)

@app.get("/")
async def root():
    return {"message": "Good morning, and in case I don't see you, good afternoon, good evening, and good night! 这是“点彩成乐”后端根域名，在域名后面加上`/docs#/`访问后端API文档页面！"}

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)
