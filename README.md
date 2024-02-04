# Diancai-Backend
“点彩成乐”大创项目后端工程（开发中）

由于使用fastapi，在本地运行后可以直接访问`http://0.0.0.0:3000/docs#/`或者 `http://局域网IP:3000/docs#/`查看文档并测试接口
单独的API文档见[API.md](API.md)

![](logo.png)

项目logo（仮）

## 运行前置
运行主代码前请先单独运行一次utils文件夹内的model_save以将模型下载至本地，记得科学上网（

运行main.py时会下载clip模型，因此出现下载读条是正常现象）

## 运行
直接运行[start_server.py](/app/start_server.py)，不要运行[main.py](/app/main.py)！

深夜 正在考虑通过参数决定选择小/中模型的可能，所以后续还会调整

目前默认音频生成模型为Musicgen-small


## TO-DO List
- 优化音乐生成部分MusicGen模型的代码（主要需求：优化生成效率）
- 将https://github.com/jina-ai/clip-as-service 调试整合到`image_processing.py`




