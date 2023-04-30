import streamlit as st
import whisper
import tempfile
from pydub import AudioSegment
from pathlib import Path
import io
import os
import base64
import time

# 使用可能なWhisperモデル
models = {"Tiny	39 M" : "tiny",
          "Base 74 M": "base", 
          "Small 244 M": "small",
          "Medium 769 M": "medium",
          "Large 1550 M": "large"}

# (5) Streamlitアプリケーションのタイトルを設定
st.title("Whisper Transcription App")

# (5.5) モデルを選択するドロップダウンを作成
selected_model = st.selectbox("Select a Whisper model", list(models.keys()))

# (2) Whisperモデルをロード
# モデルのロードには時間がかかるため、ロード中であることをユーザーに伝える
with st.spinner("Loading model... this might take a while! \n 🐣🐣🐣"):
    model = whisper.load_model(models[selected_model])




def transcribe_audio(file):
    # (3) 音声ファイルをテキストに変換する関数
    outputTextsArr = [] 
    # Load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(file)
    while audio.size > 0:
        tirmedAudio = whisper.pad_or_trim(audio)
        startIdx = tirmedAudio.size
        audio = audio[startIdx:]

        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(tirmedAudio).to(model.device)

        # detect the spoken language
        _, probs = model.detect_language(mel)

        # decode the audio
        options = whisper.DecodingOptions(fp16 = False)
        result = whisper.decode(model, mel, options)

        # print the recognized text
        outputTextsArr.append(result.text)

        outputTexts = ' '.join(outputTextsArr)

    return outputTexts

def convert_audio(file, target_format="wav"):
    # (4) 音声ファイルを変換する関数
    audio = AudioSegment.from_file(file)
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{target_format}") as target_file:
        audio.export(target_file.name, format=target_format)
        return target_file.name

# (5) Streamlitアプリケーションのタイトルを設定
st.title("Whisper Transcription App")

# (6) 音声ファイルをアップロードするためのドロップゾーンを作成
uploaded_file = st.file_uploader("Upload an audio file", type=["mp4", "mp3", "wav", "mov"])

if uploaded_file:
    file_path = Path(uploaded_file.name)
    # If the file is not a wav file, convert it to wav
    if file_path.suffix.lower() != ".wav":
        temp_file_path = convert_audio(uploaded_file, target_format="wav")
    else:
        temp_file_path = uploaded_file.name
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    # (7) 音声ファイルをテキストに変換
    transcription = transcribe_audio(temp_file_path)

    # (8) 変換結果を表示
    st.write(f"Transcription: {transcription}")

def get_binary_file_downloader_html(file_path, file_label='File'):
    with open(file_path, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(file_path)}">{file_label}</a>'
    return href

# Get the relative path of the text file
text_file_path = "transcription.txt"

# (10) テキストファイルをダウンロードするためのボタンを表示
if os.path.exists(text_file_path):
    # ダウンロードボタンを表示
    st.markdown(get_binary_file_downloader_html(text_file_path, 'Download txt file'), unsafe_allow_html=True)
else:
    # (10) テキストファイルが存在しない場合、エラーメッセージを表示
    st.error(f"File '{text_file_path}' not found.")