import os

MODEL_NAME = os.getenv("WHISPER_MODEL", "openai/whisper-tiny")
SAMPLE_RATE = 16_000
DURATION = 5

# Set WHISPER_LOCAL_ONLY=1 after the model has been downloaded once.
LOCAL_FILES_ONLY = os.getenv("WHISPER_LOCAL_ONLY", "0") == "1"
