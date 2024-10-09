import sys
import os
import subprocess


def get_output_filename(input_file):
    directory, file_name = os.path.split(input_file)
    base_name, extension = os.path.splitext(file_name)

    if base_name.startswith("(cut)"):
        output_file = input_file.replace("(cut)", "(cut) (compressed)")
    else:
        output_file = os.path.join(directory, f"(compressed) {base_name}{extension}")

    return output_file


def compress_video(input_file, target_size_mb):
    # Get duration of input video
    duration_cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        input_file,
    ]
    duration = float(subprocess.check_output(duration_cmd))

    # Calculate target bitrate to achieve desired file size
    target_bitrate = (target_size_mb * 1024 * 1024) * bitrate / duration

    output_file = get_output_filename(input_file)

    # Create an empty output file
    open(output_file, "w").close()

    # Compress video using ffmpeg with target bitrate
    ffmpeg_cmd = ["ffmpeg", "-i", input_file, "-b:v", str(int(target_bitrate))]
    if framerate:
        ffmpeg_cmd.extend(["-filter:v", f"fps=fps={framerate}"])

    if extra_options:
        ffmpeg_cmd.extend(extra_options)

    ffmpeg_cmd.append(output_file)
    subprocess.run(ffmpeg_cmd, input=b"y\n")

    output_file = os.path.abspath(output_file)

    p = subprocess.Popen(
        ["powershell.exe", "Set-Clipboard", "-LiteralPath", f'"{output_file}"']
    )

    p.communicate()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: script.py" + " input_file" + " extra_options")
        sys.exit(1)

    input_file = sys.argv[1]

    options = None
    if len(sys.argv) >= 3:
        options = sys.argv[2:]

    target_size_mb = 10  # Target size of compressed video in MB

    bitrate = 7

    framerate = None
    extra_options = []

    if options:
        if options[0].isdigit():
            framerate = int(options[0])
            extra_options = options[1:]
        else:
            extra_options = options

    compress_video(input_file, target_size_mb)

    output_file = get_output_filename(input_file)

    # os.path.getsize returns in kB, divide it to get to MB
    while (os.path.getsize(output_file) / 1024 / 1024) > int(target_size_mb):
        bitrate -= 1
        compress_video(input_file, target_size_mb)
        if os.path.getsize(output_file) < int(target_size_mb):
            print("\n")
            print("| video compressed.\n")
