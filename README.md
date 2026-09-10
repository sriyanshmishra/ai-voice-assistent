# Offline Voice & Text AI Assistant

A local voice and text assistant using Whisper speech-to-text. The project is suitable for integrating a Qualcomm AI Hub / Snapdragon NPU optimized model while keeping a CPU-friendly Whisper fallback for development.

## Features

- Voice input from a microphone
- Text input for quick testing
- Local transcription after the model is downloaded
- Configurable Whisper model through an environment variable
- Small intent-handler seam for adding assistant actions

## Requirements

- Python 3.9+
- A working microphone for voice input
- PyTorch-compatible environment
- Optional Qualcomm AI Hub tooling for exporting or deploying an optimized model

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/offline-voice-assistant.git
cd offline-voice-assistant
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

The first run downloads `openai/whisper-tiny` from Hugging Face. That download requires internet access. Once cached, the application can run without network access:

```powershell
$env:WHISPER_LOCAL_ONLY = "1"
python app.py
```

To use another compatible Whisper checkpoint:

```powershell
$env:WHISPER_MODEL = "openai/whisper-base"
python app.py
```

## Qualcomm AI Hub / Snapdragon

`qai-hub` is included for model export and deployment workflows. Replace `WHISPER_MODEL` with the local path or compatible checkpoint produced by your Qualcomm AI Hub pipeline, then keep the same processor and input contract. The sample application does not claim NPU acceleration automatically; the actual runtime depends on the exported model format and target Snapdragon device.

## Run

```bash
python app.py
```

Choose `1` to record five seconds from the default microphone, `2` to test the text handler, or `3` to exit.

## Project Structure

```text
offline-voice-assistant/
├── app.py
├── config.py
├── requirements.txt
├── README.md
└── .gitignore
```

## License

Add the license that matches your intended distribution before publishing the repository.
