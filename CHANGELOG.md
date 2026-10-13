# Changelog

## 2.0.0

- Reworked the interface with a modern dark layout and clearer chat navigation.
- Added streamed Ollama responses, stop-generation control, and copy-response buttons.
- Added configurable Ollama endpoint and model settings.
- Moved chat history to per-user application data and added a one-time migration from the old database location.
- Improved connection/model error messaging and SQLite chat deletion handling.
- Added regression tests and automated Windows EXE builds.
- Fixed the EXE builder's false-success behavior and added build artifact verification.
