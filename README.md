# Video Generator

This repository provides a simple Python script for creating a slideshow video from images and an optional audio file.

## Requirements
- Python 3
- [moviepy](https://zulko.github.io/moviepy/) and its dependencies (e.g. ImageMagick)

Install dependencies with:
```bash
pip install moviepy
```

## Configuration
Create a JSON file describing the slides:
```json
{
  "audio": "music.mp3",            // optional background audio
  "transition": "crossfade",       // or "none"
  "fps": 24,                        // frames per second for output
  "images": [
    {
      "path": "image1.jpg",
      "duration": 3,                // seconds
      "caption": "First slide",     // optional caption
      "size": "中",                 // caption size: 小, 中, 大 (or small, medium, large)
      "position": 5                 // 0=none, 1=top-left ... 9=bottom-right
    },
    {
      "path": "image2.jpg",
      "duration": 3,
      "caption": "Second slide",
      "size": "大",
      "position": 8
    }
  ]
}
```

## Usage
Run the script with the configuration file:
```bash
python video_generator.py config.json -o output.mp4
```

The script will generate `output.mp4` combining the images, captions, transitions, and audio.
