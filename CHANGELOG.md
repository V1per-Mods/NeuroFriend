# Changelog

## 2.1.0

- Added an all-in-one Windows installer containing NeuroFriend, Qwen2.5-3B-Instruct Q4_K_S, and the llama.cpp CPU runtime.
- Added automatic local model-server startup, streaming OpenAI-compatible responses, and graceful shutdown for the bundled runtime.
- Release users no longer need to install Python, Ollama, or download a model separately.
- Added installer packaging with Inno Setup, third-party notices, and separate CI/release workflows.

## 2.0.0

- Reworked the interface with a modern dark layout and clearer chat navigation.
- Added streamed Ollama responses, stop-generation control, and copy-response buttons.
- Added configurable Ollama endpoint and model settings.
- Moved chat history to per-user application data and added a one-time migration from the old database location.
- Improved connection/model error messaging and SQLite chat deletion handling.
- Added regression tests and automated Windows EXE builds.
- Fixed the EXE builder's false-success behavior and added build artifact verification.
