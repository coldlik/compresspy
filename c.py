import sys
import os
import subprocess

def compress_video(input_file, target_size_mb):
    # Get duration of input video
    duration_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_file]
    duration = float(subprocess.check_output(duration_cmd))

    # Calculate target bitrate to achieve desired file size
    target_bitrate = (target_size_mb * 1024 * 1024) * x / duration

    # Compressed file name
    directory, file_name = os.path.split(input_file)
    base_name, extension = os.path.splitext(file_name)

    if base_name.startswith("(cut)"):
        output_file = input_file.replace("(cut)", "(cut) (compressed)")
    else:
        output_file = os.path.join(directory, f"(compressed) {base_name}{extension}")

    # Create an empty output file
    open(output_file, 'w').close()

    # Compress video using ffmpeg with target bitrate
    ffmpeg_cmd = ['ffmpeg', '-i', input_file, '-b:v', str(int(target_bitrate))]
    if framerate:
        ffmpeg_cmd.extend(['-filter:v', f'fps=fps={framerate}'])
    
    if extra_options:
        ffmpeg_cmd.extend(extra_options)

    ffmpeg_cmd.append(output_file)
    subprocess.run(ffmpeg_cmd, input=b"y\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: script.py" + " input_file" + " extra_options")
        sys.exit(1)

    input_file = sys.argv[1]
    if not input_file.endswith(".mp4"):
        input_file += ".mp4"

    options = None
    if len(sys.argv) >= 3:
        options = sys.argv[2:]

    target_size_mb = 25  # Target size of compressed video in MB
    x = 7  # If your output file's size is bigger than it's supposed to be, lower this number. 

    framerate = None
    extra_options = []

    if options:
        if options[0].isdigit():
            framerate = int(options[0])
            extra_options = options[1:]
        else:
            extra_options = options

    compress_video(input_file, target_size_mb)
    print("\n")
    print("| video compressed.\n")
