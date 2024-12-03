from faster_whisper import WhisperModel
import os
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import TextClip
from  moviepy.video.compositing import CompositeVideoClip
from moviepy.video.io.ffmpeg_writer import ffmpeg_write_video

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours,  minutes = divmod(minutes, 60)
    milliseconds = (seconds - int(seconds)) * 1000
    return  f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{int(milliseconds):03d}" # This is the format for srt file

def transcribe_audio(input_file, words, gpu):
    model_size = "large-v3"

    if gpu:    # Run on GPU with FP16
        model = WhisperModel(model_size, device="cuda", compute_type="float16")
        # or run on GPU with INT8
        # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
    else:
        # or run on CPU with INT8
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
    if words:
        segments, info = model.transcribe(input_file, word_timestamps=True)

        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
        srt_filename = os.path.splitext(input_file)[0]  + '.srt'
        
        with open(srt_filename, 'w', encoding='utf-8') as srt_file:
            count = 1
            for segment in segments:
                for word in segment.words:
                    start_time = format_time(word.start)
                    end_time = format_time(word.end)
                    line = f'{count}\n{start_time} --> {end_time}\n{word.word.lstrip()}\n\n'
                    count += 1
                    srt_file.write(line)
    else:
        segments, info = model.transcribe(input_file)
        srt_filename = os.path.splitext(input_file)[0] + '.srt'
        with open(srt_filename, 'w', encoding='utf-8') as srt_file:
            for segment in segments:
                start_time = format_time(segment.start)
                end_time = format_time(segment.end)
                line = f'{segment.id + 1}\n{start_time} --> {end_time}\n{segment.text.lstrip()}\n\n'
                srt_file.write(line)
    return srt_filename

def add_subtitles(audio, video, srt, output_path, text_font_size=80, text_colour='white', text_stroke_colour='black', vertical_align='center', text_font="Roboto-Bold.ttf"):
    vid = VideoFileClip(video)
    generator = lambda text : TextClip(text=text, font=text_font, font_size=text_font_size, color=text_colour, stroke_width=10, stroke_color=text_stroke_colour, vertical_align=vertical_align, size=vid.size)
    sub = SubtitlesClip(srt, make_textclip=generator)
    final = CompositeVideoClip.CompositeVideoClip([vid, sub], size=vid.size)
    ffmpeg_write_video(final, output_path, fps=vid.fps, audiofile=audio)

if __name__ == "__main__":
    input_file_path = input("Video path: ")
    if input_file_path:
        video_clip = VideoFileClip(input_file_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(os.path.splitext(input_file_path)[0]+'.mp3')
        
    srt_file = transcribe_audio(input_file=os.path.splitext(input_file_path)[0]+'.mp3')
    add_subtitles(os.path.splitext(input_file_path)[0]+'.mp3', input_file_path, srt_file, os.path.splitext(input_file_path)[0]+'_final.mp4')