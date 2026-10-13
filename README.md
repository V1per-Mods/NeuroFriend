# NeuroFriend

A local AI desktop companion for Windows, built with Python and Tkinter and powered by [Ollama](https://ollama.com/). NeuroFriend stores chat history locally and does not require a paid cloud API key.

## Features

- Dark desktop interface
- Multiple conversations with locally stored history
- Russian, Ukrainian, and English interface options
- Connects to a model running through Ollama
- Windows EXE build script

## Requirements

- Windows 10 or 11
- [Ollama for Windows](https://ollama.com/download/windows)
- A model downloaded in Ollama, such as `qwen2.5:3b`
- Python 3.12 or 3.13 to run from source; use a supported Python version for PyInstaller builds

## Run from source

1. Install Python from [python.org](https://www.python.org/downloads/windows/).
2. Install Ollama and start it.
3. Download a model:
   ```bat
   ollama pull qwen2.5:3b
   ```
4. Clone or download this repository.
5. Run `run.bat` or execute:
   ```bat
   python main.py
   ```

No third-party Python packages are needed to run the source version.

## Build a Windows executable

Run `build_exe.bat`. It checks for Python 3.13 or 3.12, installs/updates PyInstaller, and builds `dist\\NeuroFriend.exe`.

The EXE contains the application, **not Ollama or the language model**. Ollama must be installed and running on the target computer, and the model must be downloaded separately. On first run, Windows SmartScreen may warn because the executable is not code-signed.

## Local data and privacy

Chat history is stored locally under `%LOCALAPPDATA%\\NeuroFriend\\neurofriend.db`. The app sends prompts to the Ollama service running on your computer. Ollama may need an internet connection to download models and updates. Avoid entering passwords or other sensitive information into any AI chat.

## Model selection

The default model is `qwen2.5:3b`. To use another model, download it with Ollama (for example, `ollama pull llama3.2:3b`) and choose its exact model name in the app's settings.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

## Disclaimer

This is an independent community project and is not affiliated with or endorsed by Alibaba Cloud, Ollama, Microsoft, or OpenAI. Model names and trademarks belong to their respective owners.
