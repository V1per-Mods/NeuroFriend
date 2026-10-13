# NeuroFriend 2.1.0

**A local-first desktop AI companion for Windows, with an all-in-one installer.**

NeuroFriend has a dark chat interface, chat history, streaming replies, stop-generation and copy controls. The all-in-one installer includes a quantized Qwen2.5-3B-Instruct model and the llama.cpp CPU runtime. You do not need to install Python, Ollama, or download a model separately.

## Download and install

1. Open the [GitHub Releases page](https://github.com/V1per-Mods/NeuroFriend/releases).
2. Download **NeuroFriend-Setup.exe**.
3. Run the installer and finish setup.
4. Launch NeuroFriend from the Start menu or desktop shortcut.
5. Send a message. The first reply can take a little while because the local model needs to load.

The installer is large (roughly 1.8–2.0 GB) because the AI model is included. Once downloaded and installed, the model runs locally and does not need an internet connection for chatting.

## System requirements

- Windows 10/11, 64-bit
- 8 GB RAM recommended; more RAM helps with multitasking
- Enough free disk space for the installer and installed model
- CPU inference is used for broad compatibility; response speed depends on your processor

## What's new in 2.1.0

- All-in-one Windows installer that includes the app, Qwen2.5-3B-Instruct Q4_K_S model, and llama.cpp runtime.
- No manual Ollama/Python/model setup for release users.
- Local model server starts automatically on first use and shuts down with NeuroFriend.
- Model and endpoint controls are locked for the bundled build; interface language remains configurable.
- Added third-party notices and a separate lightweight CI workflow.

## Run from source (developer mode)

The repository source mode continues to support Ollama, which is useful for development and choosing other models.

1. Install Python 3.12 or 3.13.
2. Install and start [Ollama for Windows](https://ollama.com/download/windows).
3. Download a model once, for example: ollama pull qwen2.5:3b.
4. Clone or download this repository.
5. Double-click run.bat or run python main.py.

## Build the all-in-one installer

The release workflow builds the application EXE, downloads the quantized GGUF model and official llama.cpp Windows CPU runtime, then packages everything with Inno Setup. Push a v* tag or manually run **Build all-in-one Windows installer** from GitHub Actions. The release job checks that the installer stays below GitHub's 2 GiB per-asset limit.

The local build_exe.bat script builds only the source-mode application EXE; it is not the all-in-one installer.

## Data and privacy

Chat history and settings are stored in %LOCALAPPDATA%/NeuroFriend/neurofriend.db on Windows, or ~/.local/share/NeuroFriend/neurofriend.db on Linux/macOS (unless XDG_DATA_HOME is set).

In the all-in-one Windows build, prompts are sent to the local llama.cpp server bound to 127.0.0.1 on this computer. No cloud API is used by default. In source mode, prompts are sent to the Ollama endpoint configured in settings. Avoid entering passwords or sensitive personal information into AI chats.

## Tests

Run python -m unittest discover -s tests -v.

## Licenses

NeuroFriend source code is MIT licensed; see LICENSE. The bundled Qwen model and llama.cpp runtime are third-party components under their own licenses; see THIRD_PARTY_NOTICES.txt and the included upstream model license.

NeuroFriend is an independent project and is not affiliated with Ollama, Qwen, or the llama.cpp maintainers.
