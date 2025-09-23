from pathlib import Path
import csv
from typing import Iterator, Union

datasets_dir: Path = Path("datasets")

def dataset_iterator(dir: Path, delimiter: str) -> Iterator[list]:
    with open(dir, "r") as f:
        reader = csv.reader(f, delimiter=delimiter)

        for row in reader:
            yield row

def unimorph_iterator(code: str, unimorph_dir: Union[Path, None]=None) -> Iterator[list]:
    if unimorph_dir is None:
        unimorph_dir = datasets_dir / "unimorph"

    return dataset_iterator(unimorph_dir/code, delimiter="\t")

def frequency_iterator(code: str, frequency_dir: Union[Path, None]=None) -> Iterator[list]:
    if frequency_dir is None:
        frequency_dir = datasets_dir / "frequency"

    return dataset_iterator(frequency_dir/code, delimiter=" ")

def frequency_hash_iterator(code: str, frequency_dir: Union[Path, None]=None) -> Iterator[dict]:
    for frequency_entry in frequency_iterator(code, frequency_dir):
        yield {frequency_entry[0]:frequency_entry[1]}

def build_frequency_map(code: str, frequency_dir: Union[Path, None]=None, len=None) -> dict[str, str]:
    frequency_map: dict[str, str] = {}

    if len:
        count = 0

    for frequency_entry in frequency_hash_iterator(code, frequency_dir):
        frequency_map.update(frequency_entry)

        if len:
            count += 1
            if count >= len:
                break

    return frequency_map

def combined_iterator(code: str, frequency_dir: Union[Path, None]=None, unimorph_dir: Union[Path, None]=None, frequency_map_len=None) -> Iterator[list]:
    frequency_map: dict[str, str] = build_frequency_map(code, frequency_dir, len=frequency_map_len)

    for morph_entry in unimorph_iterator(code, unimorph_dir):
        if not morph_entry:
            continue
        
        lemma, inflected, pos_tags = morph_entry

        lemma_freq: Union[str, None] = frequency_map.get(lemma)
        inflected_freq: Union[str, None] = frequency_map.get(inflected)

        if lemma_freq:
            yield [lemma, lemma_freq, pos_tags]
        elif inflected_freq:
            yield [inflected, inflected_freq, pos_tags]

def combine_sorted(code: str, frequency_dir: Union[Path, None]=None, unimorph_dir: Union[Path, None]=None, len=None, ) -> list:
    combined = []
    seen_words = set()

    if len:
        count = 0
    for entry in combined_iterator(code, frequency_dir, unimorph_dir):
        word = entry[0]

        if word not in seen_words:
            seen_words.add(word)
            combined.append(entry)

            if len:
                count += 1
                if count >= len:
                    break

    combined.sort(key=lambda x: int(x[1]), reverse=False)
    return combined