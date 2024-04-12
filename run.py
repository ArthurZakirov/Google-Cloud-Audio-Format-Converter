from pydub import AudioSegment
import os
import argparse
import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("--raw_data_dir", default="data/raw")
parser.add_argument("--processed_data_dir", default="data/processed")

args = parser.parse_args()

def main(args):
    os.makedirs(args.processed_data_dir, exist_ok=True)

    # Loop through all files in the source directory
    for file_name in tqdm.tqdm(os.listdir(args.raw_data_dir)):
        if file_name.endswith('.m4a'):
            m4a_path = os.path.join(args.raw_data_dir, file_name)
            mp3_path = os.path.join(args.processed_data_dir, file_name.replace('.m4a', '.mp3'))
            
            # Load the M4A file
            audio = AudioSegment.from_file(m4a_path, format='m4a')
            
            # Export as MP3
            audio.export(mp3_path, format='mp3')
            print(f'Converted {file_name} to MP3.')

if __name__ == "__main__":
    main(args)
