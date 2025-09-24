# WordsFrequency-POS

## Description

This repo contains python scripts to fetch the following two datasets:

-   [FrequencyWords](https://github.com/hermitdave/FrequencyWords) - a dataset containing the word frequency data gathered from OpenSubtitles.com
-   [unimorph](https://github.com/unimorph/unimorph) - a collection of datasets containing morphological data for various languages

The python application fetches the available languages for both and cross-references them to download the matching datasets for both. The files from these are normalised to follow the same file structure and naming.

## Purpose

The repo uses python to combine morphology and frequency data for words in a singular dataset.

## Pre-generated datasets

There are pre-generated datasets included in the repo. These are in the `datasets` directory.

-   `combined` - the combined dataset with default settings
-   `nouns` - singular nouns from each language with frequency data
-   `verbs` - verbs from each language with frequency data
-   `adjectives` - adjectives from each language with frequency data
-   `wordle` - typical words that would be used in a wordle-like game

## Getting started

Clone this repo using git and navigate to the root directory of the cloned repo.

### Optional to avoid manual python venv setup

Run `sudo bash start.sh` in the terminal to get started.

### Optional to avoid ratelimiting

Get your GitHub api and add a `.env` file in the root directory with the variable "GITHUB_TOKEN".

## Generating custom datasets

Custom datasets can be created using the `output_combined()` or the `output_combined_single()` functions.

A `code` is a necessary parameter for `output_combined_single()` to generate a combined dataset for a single language.

The following parameters are optional for both functions:

-   `output_dir` - the directory to output the combined datasets to
-   `frequency_dir` - the frequency dataset dir (default: "datasets/frequency")
-   `unimorph_dir` - the morphology dataset dir (default: "datasets/unimorph")
-   `max_len` - the maximum length of each produced dataset
-   `delimeter` - the delimiter used in the produced file
-   `inflections` - whether to consider inflections in the output
-   `parts_of_speech` - what parts of speech to include (e.g. `["V"]` for verbs, `["N", "SG"]` for singular nouns)
-   `output_pos_tags` - whether to include part of speech tags in the output
