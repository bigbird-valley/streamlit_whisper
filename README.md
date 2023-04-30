# Whisper Transcription App

このリポジトリには、Whisper音声認識モデルを使用して音声ファイルをテキストに変換するStreamlitアプリケーションが含まれています。アプリケーションでは、さまざまなWhisperモデル（Tiny, Base, Small, Medium, Large）から選択して使用することができます。

## 主な機能

1. 音声ファイルのアップロード
2. 音声ファイルをテキストに変換
3. テキストファイルのダウンロード

## 使い方

1. このリポジトリをクローンまたはダウンロードします。
2. 必要なパッケージをインストールします。`pip install -r requirements.txt`
 ``` 
   pip install -U openai-whisper
   pip install git+https://github.com/openai/whisper.git 
   pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git

    # on Ubuntu or Debian
    sudo apt update && sudo apt install ffmpeg

    # on Arch Linux
    sudo pacman -S ffmpeg

    # on MacOS using Homebrew (https://brew.sh/)
    brew install ffmpeg

    # on Windows using Chocolatey (https://chocolatey.org/)
    choco install ffmpeg

    # on Windows using Scoop (https://scoop.sh/)
    scoop install ffmpeg
 ``` 

1. Streamlitアプリを実行します。`streamlit run app.py`
2. ウェブブラウザで開かれたアプリケーションにアクセスし、音声ファイルをアップロードします。
3. 音声ファイルがテキストに変換されたら、結果を確認し、テキストファイルをダウンロードできます。

## 注意事項

* アプリケーションは、音声ファイルの形式として、mp4, mp3, wav, movをサポートしています。
* アプリケーションは、Whisper音声認識モデルを使用しており、その精度は選択されたモデルに依存します。
* 大きなファイルをアップロードする場合、処理に時間がかかることがあります。