import argparse
import os
from glob import glob
from pathlib import Path

import verovio
from tqdm import tqdm


class VerovioConversionError(Exception):
    pass


class VerovioMusicXmlConverter:
    """
    Class that can be used to automatically convert MusicXML files to MEI or SVG.
    """

    def convert_musicxml_to_mei(self, path_to_musicxml_file: str, output_directory: str) -> str:
        """
        Converts the given MusicXML file into an MEI file using Verovio
        :param path_to_musicxml_file: Path to the MusicXML file that should be converted
        :param output_directory: The directory, where the output result will be written to
        """
        try:
            verovio.enableLogToBuffer(True)
            verovio_toolkit = verovio.toolkit()
            if not verovio_toolkit.loadFile(path_to_musicxml_file):
                raise VerovioConversionError(f"Could not load {path_to_musicxml_file}")
            mei = verovio_toolkit.getMEI()
            output_mei_file_name = os.path.basename(os.path.splitext(path_to_musicxml_file)[0] + ".mei")
            path_to_output_mei_file = os.path.join(output_directory, output_mei_file_name)
            os.makedirs(output_directory, exist_ok=True)
            with open(path_to_output_mei_file, "w") as output_file:
                output_file.write(mei)
        except Exception as error:
            raise VerovioConversionError(f"[Error] Converting {path_to_musicxml_file} into MEI crashed.") from error

        return verovio_toolkit.getLog()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Converts a directory of MusicXml files to MEI using Verovio')
    parser.add_argument('-i', '--input_directory', default="scores", help='The input directory')
    parser.add_argument('-o', '--output_directory', default="scores", help='The output directory')

    args = parser.parse_args()

    verovio_music_xml_converter = VerovioMusicXmlConverter()
    input_directory = Path(args.input_directory)
    output_directory = Path(args.output_directory)

    all_musicxml_files = glob(args.input_directory + "/**/*.musicxml", recursive=True)
    for musicxml_file in tqdm(all_musicxml_files, desc="Converting MusicXML to MEI"):
        musicxml_path = Path(musicxml_file)
        output_path = str(musicxml_path.parent).replace(str(input_directory), str(output_directory))
        verovio_music_xml_converter.convert_musicxml_to_mei(
            path_to_musicxml_file=musicxml_file,
            output_directory=output_path
        )
