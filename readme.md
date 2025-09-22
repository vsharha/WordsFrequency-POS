# WordsFrequency-POS

## Description

This repo will contain bash scripts to fetch the [FrequencyWords](https://github.com/hermitdave/FrequencyWords) [TBD] and [unimorph](https://github.com/unimorph/unimorph).

The `download_all.sh` script from unimorph is taken as a basis in `fetch_all_codes.sh` to fetch all available unimorph language repos.

The repo names are converted from ISO 639-3 3-letter language format to the ISO 639 2-letter format used by FrequencyWords according to the [ISO specification](https://iso639-3.sil.org/code_tables/download_tables) and cross-referenced to only download the languages supported by both datasets in `fetch_validated_unimorph_datasets.sh`. The code for this conversion is in `check_iso_code.py`.

The `start.sh` script combines this functionality for ease of use.

## Getting started

Clone this repo using git and navigate to the root directory of the cloned repo. Run `bash start.sh` in the terminal to download all the necessary datasets.
