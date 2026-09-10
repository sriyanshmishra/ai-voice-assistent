import numpy as np
import sounddevice as sd
import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor

import config


def record_audio(
    duration: int = config.DURATION,
    samplerate: int = config.SAMPLE_RATE,
) -> np.ndarray:
    print(f"\n[+] Recording for {duration} seconds... Speak now!")
    audio = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="float32",
    )
    sd.wait()
    print("[+] Recording complete.")
    return np.squeeze(audio)


def transcribe_audio(
    audio_data: np.ndarray,
    processor: WhisperProcessor,
    model: WhisperForConditionalGeneration,
) -> str:
    print("[+] Processing audio offline...")
    inputs = processor(
        audio_data,
        sampling_rate=config.SAMPLE_RATE,
        return_tensors="pt",
    )

    with torch.inference_mode():
        predicted_ids = model.generate(inputs.input_features)

    return processor.batch_decode(predicted_ids, skip_special_tokens=True)[0].strip()


def process_text_input(user_text: str) -> str:
    """Replace this demo handler with application-specific intents or actions."""
    return f"Assistant Response: Received message -> '{user_text}'"


def load_model() -> tuple[WhisperProcessor, WhisperForConditionalGeneration]:
    print(f"[+] Loading Whisper model: {config.MODEL_NAME}")
    processor = WhisperProcessor.from_pretrained(
        config.MODEL_NAME,
        local_files_only=config.LOCAL_FILES_ONLY,
    )
    model = WhisperForConditionalGeneration.from_pretrained(
        config.MODEL_NAME,
        local_files_only=config.LOCAL_FILES_ONLY,
    )
    model.eval()
    return processor, model


def main() -> None:
    print("=" * 50)
    print("   Offline Voice & Text AI Assistant (Snapdragon)")
    print("=" * 50)

    processor = None
    model = None

    while True:
        print("\nChoose input method:")
        print("1. Voice Input (Mic)")
        print("2. Text Input")
        print("3. Exit")
        choice = input("Enter choice (1/2/3): ").strip()

        if choice == "1":
            if processor is None or model is None:
                try:
                    processor, model = load_model()
                except OSError as error:
                    print(f"[!] Could not load the model: {error}")
                    print("    Run once with WHISPER_LOCAL_ONLY=0 to download it, then use offline mode.")
                    continue
            try:
                audio = record_audio()
                text = transcribe_audio(audio, processor, model)
            except Exception as error:
                print(f"[!] Audio processing failed: {error}")
                continue
            print(f"\nTranscribed Text: {text}")
            print(process_text_input(text))
        elif choice == "2":
            text = input("\nEnter your text: ").strip()
            if text:
                print(process_text_input(text))
        elif choice == "3":
            print("Exiting Assistant...")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
