import base64
import os
import subprocess
import re

from cryptography.hazmat.primitives import serialization


def load_public_key_from_pem_file(file_path):
    with open(file_path, "rb") as key_file:
        public_key = key_file.read()
        public_key_obj = serialization.load_pem_public_key(public_key)
        return public_key_obj


def get_video_duration(input_file):
    result = subprocess.run([
        'E:\\installs\\ffmpeg\\bin\\ffprobe.exe',
        '-i', input_file,
        '-show_entries', 'format=duration',
        '-v', 'quiet',
        '-of', 'csv=p=0'
    ], capture_output=True, text=True)

    return float(result.stdout.strip())


def saveFirstVideoChunkBytes(i, output_file):
    if i == 0:

        with open(output_file, 'rb') as f:
            chunk_data = f.read()
            with open(f'{i + 1}_chunk_bytes.txt', "wb") as fwrite:
                fwrite.write(chunk_data)
            # Find the position of the first occurrence of "!"
            bmdat_position = chunk_data.find(b'!')
            # Ensure "!" is found before attempting to extract bytes
            if bmdat_position != -1:
                # Extract the 16 bytes after the occurrence of "!"
                extracted_bytes = chunk_data[
                                  bmdat_position + len('!'): bmdat_position + len('!') + 16]
                with open(f'{i + 1}_chunk_bytes_16.txt', "wb") as fwrite16:
                    fwrite16.write(extracted_bytes)
                    extracted_bytes_base64 = base64.b64encode(extracted_bytes).rstrip(b'=')
                    with open('VID.txt', "wb") as fwrite_base64:
                        fwrite_base64.write(extracted_bytes_base64)


def split_video_ffmpeg(input_file, output_folder, target_chunk_size_MB_param):
    # Check if the output folder exists, create it if not
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the total size of the input video file
    total_size = os.path.getsize(input_file)

    # Define the target chunk size in bytes
    target_chunk_size_bytes = target_chunk_size_MB_param * 1024 * 1024  # Convert MB to bytes

    # Calculate the number of chunks needed
    num_chunks = total_size // target_chunk_size_bytes + (total_size % target_chunk_size_bytes > 0)

    # Get video duration using ffprobe
    duration = get_video_duration(input_file)

    # Use FFmpeg to split the video into consecutive chunks of 1MB each
    for i in range(num_chunks):
        output_file = os.path.join(output_folder, f'part_{i + 1}.mp4')

        # Calculate the start position for the current chunk
        start_position = i * target_chunk_size_bytes

        # Run FFmpeg command to create the chunk based on the start position and size
        start_position_seconds = start_position / total_size * duration
        subprocess.run([
            'E:\\installs\\ffmpeg\\bin\\ffmpeg.exe',
            '-i', input_file,
            '-c', 'copy',
            '-map', '0',
            '-ss', f'{start_position_seconds:.6f}',  # Format the start position as ss.mmm
            '-fs', f'{target_chunk_size_bytes}',
            output_file
        ], check=True)

        saveFirstVideoChunkBytes(i, output_file)
        with open('VID.txt', 'rb') as f:
            Vid_data = f.read()


if __name__ == "__main__":
    # initializations of variables
    video_path = 'Original_chunking_Video.mp4'  # Replace with the path to your video file
    public_key_file_path = "public_key.pem"  # target public key
    target_chunk_size_MB = 1  # Specify the target size of each chunk in megabytes

    loaded_public_key = load_public_key_from_pem_file(public_key_file_path)
    split_video_ffmpeg(video_path, ''.join(["chunks_of_", video_path])[:-4], target_chunk_size_MB)
