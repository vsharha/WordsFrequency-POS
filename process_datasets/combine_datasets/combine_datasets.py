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
        if len(frequency_entry) >= 2:
            yield {frequency_entry[0]:frequency_entry[1]}

def build_frequency_map(code: str, frequency_dir: Union[Path, None]=None, len:Union[int, None]=None) -> dict[str, str]:
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

def combined_iterator(code: str, frequency_dir: Union[Path, None]=None, unimorph_dir: Union[Path, None]=None, frequency_map_len:Union[int, None]=None, inflections:bool=True) -> Iterator[list]:
    frequency_map: dict[str, str] = build_frequency_map(code, frequency_dir, len=frequency_map_len)

    for morph_entry in unimorph_iterator(code, unimorph_dir):
        if not morph_entry:
            continue

        lemma, inflected, pos_tags = morph_entry

        lemma_freq: Union[str, None] = frequency_map.get(lemma)
        inflected_freq: Union[str, None] = frequency_map.get(inflected)

        if lemma_freq and lemma_freq.isnumeric():
            yield [lemma, pos_tags, lemma_freq]

        elif inflections and inflected_freq and inflected_freq.isnumeric():
            yield [inflected, pos_tags, inflected_freq]

def combine_sorted_single(code: str, frequency_dir: Union[Path, None]=None, unimorph_dir: Union[Path, None]=None, max_len:Union[int, None]=None, inflections:bool=True) -> list:
    combined = []
    seen_words = set()

    if max_len:
        count = 0
    for entry in combined_iterator(code, frequency_dir, unimorph_dir, inflections=inflections):
        word = entry[0]

        if word not in seen_words:
            seen_words.add(word)
            combined.append(entry)

            if max_len:
                count += 1
                if count >= max_len:
                    break

    combined.sort(key=lambda x: int(x[2]), reverse=True)
    return combined

def combine_sorted_all(frequency_dir: Union[Path, None]=None, unimorph_dir: Union[Path, None]=None, max_len:Union[int, None]=None, inflections:bool=True) -> dict[str, list]:
    if frequency_dir is None:
        frequency_dir = datasets_dir / "frequency"

    output: dict[str, list] = {}

    for lang_dir in frequency_dir.iterdir():
        code = lang_dir.name

        result = combine_sorted_single(code, frequency_dir, unimorph_dir, max_len, inflections)

        output[code] = result

    return output

def output_combined_single(code:str, output_dir: Union[Path, None]=None, frequency_dir: Union[Path, None]=None, unimorph_dir: Union[Path, None]=None, max_len:Union[int, None]=None, inflections:bool=True, delimiter="\t") -> None:
    if output_dir is None:
        output_dir = datasets_dir / "combined"
    
    output_path: Path = output_dir / code

    output = combine_sorted_single(code, frequency_dir, unimorph_dir, max_len, inflections)

    with open(output_path, "w") as f:
        writer = csv.writer(f, delimiter=delimiter)

        writer.writerows(output)

def output_combined(output_dir: Union[Path, None]=None, frequency_dir: Union[Path, None]=None, unimorph_dir: Union[Path, None]=None, max_len:Union[int, None]=None, delimiter="\t", inflections:bool=True) -> None:
    if output_dir is None:
        output_dir = datasets_dir / "combined"

    if frequency_dir is None:
        frequency_dir = datasets_dir / "frequency"

    for lang_dir in frequency_dir.iterdir():
        code = lang_dir.name

        print(f"Processing {code}...")

        output_combined_single(code, output_dir, frequency_dir, unimorph_dir, max_len, inflections, delimiter)