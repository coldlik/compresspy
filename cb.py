import sys
import subprocess
import os


def run_blur(input_file):
    # Run blur.exe with input file
    blur_cmd = ["blur.exe", "-i", input_file, "-n"]
    subprocess.run(blur_cmd, check=True)


def get_output_filename(input_file):
    directory, file_name = os.path.split(input_file)
    base_name, extension = os.path.splitext(file_name)

    if base_name.startswith("(cut)"):
        output_file = input_file.replace("(cut)", "(cut) (comp & blur)").replace(
            "- blur", ""
        )
    else:
        output_file = os.path.join(
            directory, f"(comp & blur) {base_name}{extension}"
        ).removesuffix("- blur")

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

    # Calculate target bitrate
    target_bitrate = (target_size_mb * 1024 * 1024) * bitrate / duration

    output_file = get_output_filename(input_file)

    # Create an empty output file
    open(output_file, "w").close()

    # Compress video using ffmpeg with target bitrate
    ffmpeg_cmd = [
        "ffmpeg",
        "-i",
        input_file,
        "-b:v",
        str(int(target_bitrate)),
    ]

    if options:
        ffmpeg_cmd.extend(options)

    ffmpeg_cmd.append(output_file)

    subprocess.run(ffmpeg_cmd, input=b"y\n")

    output_file = os.path.abspath(output_file)

    p = subprocess.Popen(
        ["powershell.exe", "Set-Clipboard", "-LiteralPath", f'"{output_file}"']
    )

    p.communicate()


def find_blurred_file(input_file):
    directory = os.path.dirname(input_file)
    base_name = os.path.basename(input_file)
    base_name_without_ext, ext = os.path.splitext(base_name)
    blurred_file_name = base_name_without_ext + " - blur" + ext
    blurred_file_path = os.path.join(directory, blurred_file_name)
    return blurred_file_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not input_file.endswith(".mp4"):
        input_file += ".mp4"

    options = None
    if len(sys.argv) >= 3:
        options = sys.argv[2:]

    target_size_mb = 10  # Target size of compressed video in MB
    bitrate = 7

    run_blur(input_file)
    blurred_file = find_blurred_file(input_file)

    compress_video(blurred_file, target_size_mb)

    output_file = get_output_filename(blurred_file)

    while (os.path.getsize(output_file) / 1024 / 1024) > int(target_size_mb):
        bitrate -= 1
        compress_video(blurred_file, target_size_mb)
        if (os.path.getsize(output_file) / 1024 / 1024) < int(target_size_mb):
            os.remove(blurred_file)
            print("\n")
            print("| video compressed & blurred.\n")
