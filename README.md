# Autosub

## Description
Generate subtitles from videos using faster-whisper. Burn the subtitles into the video using moviepy.

## Installation

### Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.9 or greater
- You have installed [cuDNN 9](https://developer.nvidia.com/cudnn) and [cuBLAS](https://developer.nvidia.com/cublas) for CUDA 12 if you plan to run the faster-whisper model in your GPU. For more information, visit the [faster-whisper](https://github.com/SYSTRAN/faster-whisper) Github repo.
 


### Installation
1. Clone the repository
    ```bash
    git clone https://github.com/Techie-Ernie/autosub.git
    ```
2. Install requirements 
    ```bash
    cd autosub
    pip install -r requirements.txt
    ```
3. Run the program 
    ```bash
    python autosub.py video.mp4 # video.mp4 is the path to your video file 
    
    -h, --help  
    show help message and exit

    --srt_only  
    If set to true, program outputs .srt file, without burning the subtitles into the video.
    --words     
    If set to true, faster-whisper provides timestamps for each word.
    --gpu       
    If set to true, faster-whisper will use GPU to run the model. 
    ```

4. For futher customisation with font, text colour, font size, etc, edit the utils.py file. 
