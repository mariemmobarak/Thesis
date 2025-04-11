import os
from pydub import AudioSegment

folder = "D:/UNI/Semester 8/Motzart/MozartsTouch/MozartsTouch/MUImageAudio"

for filename in os.listdir(folder):
    if filename.endswith(".mp3"):
        mp3_path = os.path.join(folder, filename)
        wav_path = mp3_path.replace(".mp3", ".wav")

        audio = AudioSegment.from_mp3(mp3_path)
        audio.export(wav_path, format="wav")

        print(f"Converted: {filename} → {os.path.basename(wav_path)}")
