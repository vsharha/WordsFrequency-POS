# WordsFrequency-POS

## Description

This repo contains python scripts to fetch the following two datasets:

-   [FrequencyWords](https://github.com/hermitdave/FrequencyWords) - a dataset containing the word frequency data gathered from OpenSubtitles.com
-   [unimorph](https://github.com/unimorph/unimorph) - a collection of datasets containing morphological data for various languages

The python application fetches the available languages for both and cross-references them to download the matching datasets for both. The files from these are normalised to follow the same file structure and naming.

## Getting started

Clone this repo using git and navigate to the root directory of the cloned repo.

Optional to avoid manual python venv setup: Run `sudo bash start.sh` in the terminal to get started.

Optional to avoid ratelimiting: get your GitHub api and add a `.env` file in the root directory with the variable "GITHUB_TOKEN".

## Purpose

The repo will use python to combine these datasets in a singular dataset containing information about both each word's Part of Speech and its frequency. This will allow for things such as i.e. the lookup of words by the Part of Speech ordered by the frequency.
