import argparse
import os
from utils import transcribe_audio, add_subtitles
from moviepy.video.io.VideoFileClip import VideoFileClip


def main():
    parser = argparse.ArgumentParser(description="Process a video file.")
    parser.add_argument(
        "video_path", type=str, nargs="?", help="The path to the video file."
    )
    parser.add_argument(
        "--srt_only",
        action="store_true",
        help="If set to true, program outputs .srt file, without burning the subtitles into the video. ",
    )
    parser.add_argument(
        "--words",
        action="store_true",
        help="If set to true, faster-whisper provides timestamps for each word.",
    )
    parser.add_argument(
        "--gpu",
        action="store_true",
        help="If set to true, faster-whisper will use GPU to run the model. GPU execution requires cuDNN 9 for CUDA 12. Read detailed instructions on the Github page.",
    )
    args = parser.parse_args()

    if not args.video_path:
        print(
            "Error: No video path provided. Please provide the path to the video file."
        )
    else:
        video_clip = VideoFileClip(args.video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(os.path.splitext(args.video_path)[0] + ".mp3")
        srt_file = transcribe_audio(
            input_file=os.path.splitext(args.video_path)[0] + ".mp3",
            words=args.words,
            gpu=args.gpu,
        )

        if args.srt_only:
            print(f"srt file found at {srt_file}")
        else:
            add_subtitles(
                os.path.splitext(args.video_path)[0] + ".mp3",
                args.video_path,
                srt_file,
                os.path.splitext(args.video_path)[0] + "_afinal.mp4",
            )


if __name__ == "__main__":
    main()
