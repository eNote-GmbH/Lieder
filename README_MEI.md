# OpenScore Lieder MEI

If you want to obtain all OpenScore Lieder in MEI format, proceed with the following steps: 

1. Clone the repository https://github.com/eNote-GmbH/Lieder
2. Recreate the corpus file (in case it has changed) by running `python ./data/corpus_conversion.py`
3. Convert all MuseScore-XML files into MusicXml by running `mscore -j data/corpus_conversion.json` 
4. Convert all MusicXml files to MEI with Verovio by running `python ./data/mei_conversion.py`