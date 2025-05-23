import io
from pathlib import Path
from typing import Union
from loguru import logger
from abc import ABC, abstractmethod

if __name__ == "__main__":
    from MusicGenerator.music_gen import MusicGen
    from MusicGenerator.suno_ai import Suno
else:
    from .MusicGenerator.music_gen import MusicGen
    from .MusicGenerator.suno_ai import Suno

module_path = Path(__file__).resolve().parent.parent

class AbstractSingletonMeta(type, ABC):
    '''
    单例模式抽象基类元类，保证音乐生成类只有一个实例
    '''
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
    

class MusicGenerator(metaclass=AbstractSingletonMeta):
    '''
    音乐生成模型抽象基类，增加模型类时需要继承此类并实现generate方法
    '''
    @property
    @abstractmethod
    def model_name(self):
        pass

    @abstractmethod
    def generate(self, text: str, music_duration: int) -> Union[io.BytesIO, str]:
        """
        根据传入文本和音乐时长生成音乐

        Parameters:
            text (str): 音乐生成的提示文本
            music_duration (int): 音乐的时长，单位为秒

        Returns:
            Union[io.BytesIO, str]: Generated music as a byte stream or string.
        """
        pass

class TestGenerator(MusicGenerator):
    def __init__(self) -> None:
        self._model_name = "test"

    @property
    def model_name(self):
        return self._model_name

    def generate(self, text: str, music_duration: int) -> io.BytesIO:
        """Return dummy audio *BONK*.mp3"""
        logger.info("Music Generation Prompt: " + text.encode('gbk', errors='replace').decode('gbk'))
        test_path = module_path / "static" / "BONK.mp3"
        with open(test_path, "rb") as f:
            test_mp3 = f.read()
        return io.BytesIO(test_mp3)

class MusicGenSmallGenerator(MusicGenerator):
    def __init__(self) -> None:
        self.model = MusicGen("musicgen-small")
        self._model_name = "musicgen-small"

    @property
    def model_name(self):
        return self._model_name

    def generate(self, text: str, music_duration: int) -> io.BytesIO:
        return self.model.generate(text, music_duration)

class MusicGenMediumGenerator(MusicGenerator):
    def __init__(self) -> None:
        self.model = MusicGen("musicgen-medium")
        self._model_name = "musicgen-medium"

    @property
    def model_name(self):
        return self._model_name

    def generate(self, text: str, music_duration: int) -> io.BytesIO:
        return self.model.generate(text, music_duration)

class MusicGenLargeGenerator(MusicGenerator):
    def __init__(self) -> None:
        self.model = MusicGen("musicgen-large")
        self._model_name = "musicgen-large"

    @property
    def model_name(self):
        return self._model_name

    def generate(self, text: str, music_duration: int) -> io.BytesIO:
        return self.model.generate(text, music_duration)

class SunoGenerator(MusicGenerator):
    def __init__(self) -> None:
        self._model_name = "Suno"

    @property
    def model_name(self):
        return self._model_name

    def generate(self, text: str, *_) -> str:
        return Suno.generate(text)

class MusicGeneratorFactory:
    """
    工厂类获取音乐生成模型实例
    """
    generator_classes = {
        "test": TestGenerator,
        "musicgen-small": MusicGenSmallGenerator,
        "musicgen-medium": MusicGenMediumGenerator,
        "musicgen-large": MusicGenLargeGenerator,
        "suno": SunoGenerator,
    }

    @classmethod
    def create_music_generator(cls, music_gen_model_name: str) -> MusicGenerator:
        generator_class = cls.generator_classes.get(music_gen_model_name)
        if generator_class:
            logger.info(f'Creating music generator: {generator_class.__name__}')
            return generator_class()
        else:
            raise ValueError(f"Unsupported music_gen_model_name: {music_gen_model_name}")

if __name__ == "__main__":
    music_gen_small = MusicGeneratorFactory.create_music_generator("musicgen-small")
    output = music_gen_small.generate("a daft punky thrash music", 1)
    logger.info(f"Model name: {music_gen_small.model_name}")
    with open(module_path / 'musicgen.wav', 'wb') as f:
        f.write(output.getvalue())