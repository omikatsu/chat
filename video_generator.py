import json
import os
from typing import List, Dict

try:
    from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip
except ImportError as e:
    raise SystemExit("moviepy is required to run this script. Please install it with 'pip install moviepy' and ensure dependencies like ImageMagick are installed.")

POSITIONS = {
    1: ('left', 'top'),
    2: ('center', 'top'),
    3: ('right', 'top'),
    4: ('left', 'center'),
    5: ('center', 'center'),
    6: ('right', 'center'),
    7: ('left', 'bottom'),
    8: ('center', 'bottom'),
    9: ('right', 'bottom'),
}

SIZES = {
    '小': 30,
    '中': 50,
    '大': 70,
    'small': 30,
    'medium': 50,
    'large': 70,
}

def build_clip(item: Dict) -> CompositeVideoClip:
    """Create a video clip for one image configuration."""
    img_path = item['path']
    duration = float(item.get('duration', 3))
    caption = item.get('caption')
    size = item.get('size', 'medium')
    position = int(item.get('position', 0))

    clip = ImageClip(img_path).set_duration(duration)
    if caption and position != 0:
        fontsize = SIZES.get(size, 50)
        txt = TextClip(caption, fontsize=fontsize, color='white').set_position(POSITIONS.get(position, ('center','center')))
        clip = CompositeVideoClip([clip, txt.set_duration(duration)])
    return clip

def create_video(config_path: str, output: str = 'output.mp4') -> None:
    """Generate a video based on the provided configuration file."""
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    clips: List[CompositeVideoClip] = []
    for item in cfg['images']:
        clips.append(build_clip(item))

    transition = cfg.get('transition', 'none')
    if transition == 'crossfade':
        video = concatenate_videoclips(clips, method='compose', padding=-1, crossfade=1)
    else:
        video = concatenate_videoclips(clips, method='compose')

    if 'audio' in cfg and os.path.exists(cfg['audio']):
        audio_clip = AudioFileClip(cfg['audio'])
        video = video.set_audio(audio_clip)

    fps = int(cfg.get('fps', 24))
    video.write_videofile(output, fps=fps)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Generate a video from images and audio configuration.')
    parser.add_argument('config', help='Path to configuration JSON file')
    parser.add_argument('-o', '--output', default='output.mp4', help='Output video file path')
    args = parser.parse_args()

    create_video(args.config, args.output)
