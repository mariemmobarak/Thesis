import librosa
import numpy as np
from scipy.spatial.distance import cdist

def extract_features(audio_file):
    # Load the audio file
    y, sr = librosa.load(audio_file, sr=None)

    # Extract MFCC (13 coefficients)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    # Extract Spectrogram (Mel Spectrogram in this case)
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)

    # Combine the MFCC and Spectrogram features
    # Flattening both features to create a single vector for each frame
    features_mfcc = np.mean(mfcc, axis=1)  # Mean across time for MFCC
    features_spectrogram = np.mean(mel_spectrogram, axis=1)  # Mean across time for Spectrogram

    # Combine features into a single feature vector
    features = np.concatenate([features_mfcc, features_spectrogram], axis=0)

    return features

def compute_fad(audio_file_1, audio_file_2):
    # Extract features from both audio files
    features_1 = extract_features(audio_file_1)
    features_2 = extract_features(audio_file_2)

    # Calculate pairwise distance (Euclidean) between the two sets of features
    distance = np.linalg.norm(features_1 - features_2)

    return distance

# Example usage
audio_file_1 = "D:/UNI/Semester 8/Motzart/MozartsTouch/MozartsTouch/outputs/ChineseFood.wav"
audio_file_2 = "D:/UNI/Semester 8/Motzart/MozartsTouch/MozartsTouch/MUImageAudio/4OACmUnqtFQ.wav"

fad_score = compute_fad(audio_file_1, audio_file_2)
print(f'FAD Score: {fad_score}')
