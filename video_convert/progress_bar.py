import subprocess
from tqdm import tqdm

def ffmpeg_progress(input_file, output_file):
    command = ['ffmpeg', '-i', input_file, output_file]
    process = subprocess.Popen(command, stderr=subprocess.PIPE, universal_newlines=True)

    duration = None
    progress_bar = None

    for line in process.stderr:
        line = line.strip()

        # Extract duration information
        if 'Duration:' in line:
            duration = line.split(',')[0].split(': ')[1]

        # Extract progress information
        if 'time=' in line and 'fps=' in line:
            time_str = line.split('time=')[1].split()[0]
            current_time = sum(float(x) * 60 ** index for index, x in enumerate(reversed(time_str.split(":"))))
            if duration:
                progress = current_time / float(duration)
                if not progress_bar:
                    progress_bar = tqdm(total=100, desc='Processing', unit='%', position=0)
                progress_bar.update(progress * 100)

    process.wait()

    if progress_bar:
        progress_bar.close()

# Example usage
input_file = 'input.mp4'
output_file = 'output.mp4'
ffmpeg_progress(input_file, output_file)