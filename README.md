Python scripts, that I've created while I was bored and for my personal usage.
---
### __Usage:__

Either drag a video file onto the script, or launch it by typing the script name + "file name" in the folder path bar.\
(e.g `c.py "video"`, if the file's extension is .mp4, it doesn't need to be there.)

Output file will have `(compressed)` prefix and it will be automatically copied to the clipboard.

---

- c.py > automatically compresses video using ffmpeg to ~25MB for uploading to discord and etc.\
‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎changeable framerate: e.g `'c.py "video" 30` -> 30 fps output video.\
‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎extra ffmpeg functions: [documentation](https://ffmpeg.org/ffmpeg.html) (e.g `c.py "video" 30 -an` to remove audio from output video.)


- cb.py > same as c.py, but it blurs the video with tekno's blur before compressing it.\
‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ___doesn't include changeable framerate and extra ffmpeg functions.___\
‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎install [tekno's blur](https://github.com/f0e/blur/releases) dev release for now.

__experimental__
- test.py > c.py + cb.py combined, has a CLI menu and a function that merges multiple video files.\
‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ merging video files will decrease the video's bitrate.
  
