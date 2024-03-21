import sys
import subprocess
import os
from time import sleep
from moviepy.editor import VideoFileClip, concatenate_videoclips

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
    if ans == "2":
      output_file = f"(compressed) {input_file}"
    elif ans == "3":
      output_file = f"(comp & blur) {input_file}"

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

def merge_videos():
    input_clip = VideoFileClip(input_file)

    # Split the input to extract file paths enclosed in quotation marks
    file_paths_input = []
    file_path = ""
    in_quotes = False
    for char in additional_files_input:
        if char == '"':
            in_quotes = not in_quotes
        elif char == " " and not in_quotes:
            if file_path:
                if not file_path.endswith(".mp4"):
                    file_path += ".mp4"
                file_paths_input.append(file_path)
                file_path = ""
        else:
            file_path += char
    if file_path:
        if not file_path.endswith(".mp4"):
            file_path += ".mp4"
        file_paths_input.append(file_path)

    # Check if user entered any file paths
    if not file_paths_input:
        print("| no files selected.")
        return

    # Load video clips
    video_clips = [VideoFileClip(file_path) for file_path in file_paths_input]

    # Concatenate video clips
    all_video_clips = [input_clip] + video_clips
    final_clip = concatenate_videoclips(all_video_clips, method='compose')
    
    save_file = f"(merged) {input_file}"

    # Write the merged video to file
    final_clip.write_videofile(save_file, preset="ultrafast")

    print("\n| merged video successfully.")

def merge_videos_ffmpeg():
    # Split the input to extract file paths enclosed in quotation marks
    file_paths_input = []
    file_path = ""
    in_quotes = False
    for char in additional_files_input:
        if char == '"':
            in_quotes = not in_quotes
        elif char == " " and not in_quotes:
            if file_path:
                if not file_path.endswith(".mp4"):
                    file_path += ".mp4"
                file_paths_input.append(file_path)
                file_path = ""
        else:
            file_path += char
    if file_path:
        if not file_path.endswith(".mp4"):
            file_path += ".mp4"
        file_paths_input.append(file_path)

    # Check if input_file ends with .mp4, if not, add .mp4 extension
    if not file_path.endswith(".mp4"):
        file_path += ".mp4"

    # Check if user entered any file paths
    if not file_paths_input:
        print("| no files selected.")
        return
    
    # save_file = f"(merged) {input_file}"

    # # Create an empty output file
    # open(save_file, 'w').close()

    # # Split additional_files_input into individual file paths
    # additional_files = additional_files_input.split()

    # Check if any additional files don't end with .mp4, if not, add .mp4 extension
    additional_files = [f + (".mp4" if not f.endswith(".mp4") else "") for f in additional_files_input]

    input_files_str = " ".join(["-i " + (file_path) for file_path in additional_files_input.split()])
    output_file = f"{input_file}_merged.mp4"
    ffmpeg_cmd = f"ffmpeg {input_files_str} -i {input_file} -filter_complex concat=n={len(additional_files_input.split())+1}:v=1:a=1 -c:v copy -c:a copy {output_file}"

    # Execute the ffmpeg command
    subprocess.run(ffmpeg_cmd)

    print("\n| merged video successfully.")

    # doesn't work yet :(

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not input_file.endswith(".mp4"):
        input_file += ".mp4"

    target_size_mb = 25  # Target size of compressed video in MB
    x = 7.5  # If your output file's size is bigger than it's supposed to be, then lower this number. 

    ans=True
while ans:
    print ("""
     | menu |\n
| 1. merge videos (decreases bitrate)
| 2. compress video
| 3. compress & blur video
| 4. exit
""")
    print ("| current file: " + input_file)
    ans=input("| input: ") 

    if ans=="1": 
      additional_files_input = input("\n| input another video to merge: ").strip()
      print("\n")
      merge_videos()
      input_file = f"(merged) {input_file}"

    elif ans=="2":
      print("\n| compressing video")
      compress_video(input_file, target_size_mb)
      sleep(1)
      os.system('cls')
      print("\n| video compressed.")

    elif ans=="3":
      print("\n| compressing & blurring video.")
      run_blur(input_file)
      blurred_file = find_blurred_file(input_file)
      compress_video(blurred_file, target_size_mb)
      os.remove(blurred_file)
      sleep(1)
      os.system('cls')
      print("\n| video compressed & blurred.")

    elif ans=="4":
      print("\n| exit.")
      sleep(0.3)
      sys.exit(1)

    elif ans !="":
      sleep(0.8)
      os.system('cls')
      print("\n| wrong option")
      
      
      
# made by @coldlikx
