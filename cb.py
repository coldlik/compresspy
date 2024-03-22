import sys
import subprocess
import os

def run_blur(input_file):
    # Run blur.exe with input file
    blur_cmd = ['blur-cli.exe', '-i', input_file]
    subprocess.run(blur_cmd, check=True)

def compress_video(input_file, target_size_mb):
    # Get duration of input video
    duration_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_file]
    duration = float(subprocess.check_output(duration_cmd))

    # Calculate target bitrate
    target_bitrate = (target_size_mb * 1024 * 1024) * x / duration

    # Compressed file name
    directory, file_name = os.path.split(input_file)
    base_name, extension = os.path.splitext(file_name)

    if base_name.startswith("(cut)"):
        output_file = input_file.replace("(cut)", "(cut) (comp & blur)").replace("- blur", "")
    else:
        output_file = os.path.join(directory, f"(comp & blur) {base_name}{extension}").replace("- blur", "")

    # Create an empty output file
    open(output_file, 'w').close()

    # Compress video using ffmpeg with target bitrate
    ffmpeg_cmd = ['ffmpeg', '-i', input_file, '-b:v', str(int(target_bitrate)), output_file]
    subprocess.run(ffmpeg_cmd, input=b"y\n")

def find_blurred_file(input_file):
    directory = os.path.dirname(input_file)
    base_name = os.path.basename(input_file)
    base_name_without_ext, ext = os.path.splitext(base_name)
    blurred_file_name = base_name_without_ext + " - blur" + ext
    blurred_file_path = os.path.join(directory, blurred_file_name)
    return blurred_file_path

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not input_file.endswith(".mp4"):
        input_file += ".mp4"
        
    target_size_mb = 25  # Target size of compressed video in MB
    x = 7.5  # If your output file's size is bigger than it's supposed to be, then lower this number. 

    run_blur(input_file)
    blurred_file = find_blurred_file(input_file)
    compress_video(blurred_file, target_size_mb)

    os.remove(blurred_file)
    print("\n")
    print("| video compressed & blurred.\n")
