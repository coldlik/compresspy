import sys
import subprocess

def compress_video(input_file, target_size_mb):
    # Get duration of input video
    duration_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_file]
    duration = float(subprocess.check_output(duration_cmd))

    # Calculate target bitrate to achieve desired file size
    target_bitrate = (target_size_mb * 1024 * 1024) * x / duration

    # Compressed file name
    output_file = input_file.replace("(cut)", "(cut) (compressed)")
    
    # Create an empty output file
    open(output_file, 'w').close()

    # Compress video using ffmpeg with target bitrate
    ffmpeg_cmd = ['ffmpeg', '-i', input_file, '-b:v', str(int(target_bitrate))]
    if options:
        ffmpeg_cmd.extend(options)
    ffmpeg_cmd.append(output_file)
    subprocess.run(ffmpeg_cmd, input=b"y\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: script.py" + " <input_file>" + " [extra_options]")
        sys.exit(1)

    input_file = sys.argv[1]
    if not input_file.endswith(".mp4"):
        input_file += ".mp4"

    options = None
    if len(sys.argv) >= 3:
        options = sys.argv[2:]

    target_size_mb = 25  # Target size of compressed video in MB
    x = 7  # If your output file's size is bigger than it's supposed to be, lower this number. 

    compress_video(input_file, target_size_mb)
    print("\n")
    print("| video compressed.\n")
