# NeuroFriend 2.0.0

**A local-first desktop AI companion for Windows, powered by Ollama.**

NeuroFriend provides a dark chat interface while running a model on your computer. The application uses Python's standard library; no cloud API key is required.

## What's new in 2.0.0

- Redesigned dark UI with a clearer sidebar, chat header, message cards, and composer.
- Streaming responses from Ollama.
- Stop-generation control and copy-response buttons.
- Configurable model and Ollama endpoint.
- Improved handling of connection errors, missing models, empty replies, and invalid endpoint URLs.
- Chat history moved to a per-user application-data directory; an old working-directory database is migrated on first launch when possible.
- SQLite foreign-key enforcement and safer chat deletion.
- Automated tests and a Windows EXE build workflow.
- Fixed the EXE builder so it exits with an error instead of printing a false success message.

## Download

Visit the [Releases page](https://github.com/V1per-Mods/NeuroFriend/releases) for a Windows executable. The GitHub Actions workflow builds NeuroFriend.exe when a v* tag is pushed. Builds from the default branch are also available as Actions artifacts.

## Requirements

- Windows 10/11
- [Ollama for Windows](https://ollama.com/download/windows)
- A model installed locally, for example qwen2.5:3b

Download a model once:

    ollama pull qwen2.5:3b

## Run from source

1. Install Python 3.12 or 3.13.
2. Install and start Ollama.
3. Clone or download this repository.
4. Double-click run.bat or run: python main.py

The app only uses Python's standard library.

## Build the EXE locally

Double-click build_exe.bat. It checks the source, installs PyInstaller, and verifies the EXE exists before reporting success.

## Data and privacy

Chat history and settings are stored in %LOCALAPPDATA%/NeuroFriend/neurofriend.db on Windows, or ~/.local/share/NeuroFriend/neurofriend.db on Linux/macOS (unless XDG_DATA_HOME is set).

Prompts are sent to the Ollama endpoint configured in settings. The default is http://127.0.0.1:11434. Ollama and the model are not bundled into the EXE. Avoid entering passwords or sensitive personal information into AI chats.

## Tests

    python -m unittest discover -s tests -v

## License

MIT. See LICENSE.

NeuroFriend is an independent project and is not affiliated with Ollama or the makers of any AI model.
