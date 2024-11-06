import os 
import whisper
import torch
import subprocess

device = "cuda" if torch.cuda.is_available() else "cpu"

model = whisper.load_model("large", device=device)

def extract_audio_from_video(video_path, output_audio_path="audio.wav"):
    command = {"ffmeg", "-i", video_path, "-q:a", "0", "-map", "a", output_audio_path, "-y"}
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output_audio_path

def create_srt_file(segments, filename="subtitles.srt"):
    with open(filename, "w", encoding="utf-8") as f:
        for i, segments in enumerate(segments, start=1):
            start_time = format_timestamp(segments['start'])
            end_time = format_timestamp(segments['end'])
            text = segments['text'].strip()

            f.write(f"{i}\n{start_time} --> {end_time}\n{text}\n\n")

    return filename


def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds%3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def transcribe_audio_to_srt(video_file):
    audio_file = extract_audio_from_video(video_file.name)

    result = model.transcribe(audio_file, language = "vi")
    segments = result['segments']

    srt_file = create_srt_file(segments)

    os.remove(audio_file)

    return srt_file