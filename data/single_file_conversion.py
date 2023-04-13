import argparse
import subprocess
from pathlib import Path

from tqdm import tqdm


def convert(
    musescore_xml_path: Path,
    musicxml_path: Path,
    musescore_command_4="/Applications/MuseScore 4.app/Contents/MacOS/mscore",
    musescore_command_3="/Applications/MuseScore 3.app/Contents/MacOS/mscore"
):
    convert_comand = f'"{musescore_command_4}" -o "{str(musicxml_path.absolute())}" "' \
                     f'{str(musescore_xml_path.absolute())}"'
    process = subprocess.run(convert_comand, stderr=subprocess.PIPE, text=True, shell=True)
    if not musicxml_path.exists():
        print("Failed to convert: " + str(musescore_xml_path) + " - retrying with MuseScore 3")
        convert_comand = f'"{musescore_command_3}" -o "{str(musicxml_path.absolute())}" "' \
                         f'{str(musescore_xml_path.absolute())}"'
        process = subprocess.run(convert_comand, stderr=subprocess.PIPE, text=True, shell=True)
        if not musicxml_path.exists():
            print("Failed to convert: " + str(musescore_xml_path) + " permanently")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Converts a directory of MuseScoreXML files to MusicXML using '
                    'MuseScore'
    )
    parser.add_argument('-i', '--input_directory', default="scores", help='The input directory')
    parser.add_argument('-o', '--output_directory', default="scores", help='The output directory')

    args = parser.parse_args()
    input_directory = Path(args.input_directory)
    output_directory = Path(args.output_directory)

    all_musicxml_files = list(input_directory.rglob("*.mscx"))
    for musescore_xml_path in tqdm(all_musicxml_files, desc="Converting MuseScoreXML to MusicXML"):
        musicxml_path = (output_directory / musescore_xml_path.relative_to(input_directory)).with_suffix(".musicxml")
        if musicxml_path.exists():
            continue
        convert(musescore_xml_path, musicxml_path)
