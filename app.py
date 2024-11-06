import gradio as gr
from audio_processing import transcribe_audio_to_srt

interface = gr.Interface(
    fn = transcribe_audio_to_srt,
    inputs=gr.File(label="Tải lên file video âm thanh mp4"),
    outputs=gr.File(label="Tải xuống file phụ đề SRT"),
    title="Tạo phụ đề tự động từ video mp4",
    description="Tải lên video mp4 và nhận file phụ đề SRT tự động từ hệ thống",
)

if __name__ == "__main__":
    interface.launch(share=True)