Python scripts, that I've created while I was bored and for my personal usage.
---
### Usage:

Either drag a video file onto the script, or launch it by typing the script name + "file name with extension" in the folder path bar.\
(e.g `c.py "video.mp4"`).

Output file will have `(compressed)` prefix and it will be automatically copied to the clipboard.

---

### Requirements:

- FFmpeg
- Python
  
---

- c.py > automatically compresses video using ffmpeg to ~10MB for uploading to discord and etc.\
‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎changeable framerate: e.g `'c.py "video.mp4" 30` -> 30 fps output video.\
‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎extra ffmpeg functions: [documentation](https://ffmpeg.org/ffmpeg.html) (e.g `c.py "video.mp4" 30 -an` to remove audio from output video).


- cb.py > same as c.py, but it blurs the video with tekno's blur before compressing it.\
‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ___doesn't include functions from c.py since they're customizable in .blur-config.cfg___\
‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎install [tekno's blur](https://github.com/f0e/blur/releases/tag/v1.8).

__experimental__
- test.py > c.py + cb.py combined, has a CLI menu and a function that merges multiple video files.\
‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ merging video files will decrease the video's bitrate.
  
