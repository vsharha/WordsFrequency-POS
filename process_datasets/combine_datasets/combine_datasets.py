from pathlib import Path
import csv
from typing import Iterator, Union

datasets_dir: Path = Path("datasets")

def dataset_iterator(dir: Path, delimiter: str) -> Iterator[list]:
    with open(dir, "r") as f:
        reader = csv.reader(f, delimiter=delimiter)

        for row in reader:
            yield row

def unimorph_iterator(code: str, unimorph_dir: Union[Path, str, None]=None) -> Iterator[list]:
    if unimorph_dir is None:
        unimorph_dir = datasets_dir / "unimorph"

    unimorph_dir = Path(unimorph_dir)

    return dataset_iterator(unimorph_dir/code, delimiter="\t")

def frequency_iterator(code: str, frequency_dir: Union[Path, str, None]=None) -> Iterator[list]:
    if frequency_dir is None:
        frequency_dir = datasets_dir / "frequency"

    frequency_dir = Path(frequency_dir)

    return dataset_iterator(frequency_dir/code, delimiter=" ")

def frequency_hash_iterator(code: str, frequency_dir: Union[Path, str, None]=None) -> Iterator[dict]:
    for frequency_entry in frequency_iterator(code, frequency_dir):
        if len(frequency_entry) >= 2:
            yield {frequency_entry[0]:frequency_entry[1]}

def build_frequency_map(code: str, frequency_dir: Union[Path, str, None]=None, len:Union[int, None]=None) -> dict[str, str]:
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

def combined_iterator(code, frequency_dir=None, unimorph_dir=None, frequency_map_len=None, inflections:bool=True, parts_of_speech:Union[list, None]=None, output_pos_tags:bool=True, check_inflections:bool=False) -> Iterator[list]:
    frequency_map: dict[str, str] = build_frequency_map(code, frequency_dir, len=frequency_map_len)

    current_entry: list = []

    for morph_entry in unimorph_iterator(code, unimorph_dir):
        if not morph_entry:
            continue

        lemma, inflected, pos_tags = morph_entry

        if len(current_entry) == 0 or current_entry[0] != lemma:
            current_entry = morph_entry

        lemma_freq: Union[str, None] = frequency_map.get(lemma)
        inflected_freq: Union[str, None] = frequency_map.get(inflected)

        if parts_of_speech is not None:
            if not (all(pos in pos_tags.split(";") for pos in parts_of_speech)) and not (check_inflections and all(pos in current_entry[2].split(";") for pos in parts_of_speech)):
                continue

        if lemma_freq and lemma_freq.isnumeric():
            if output_pos_tags:
                yield [lemma, lemma_freq, pos_tags]
            else:
                yield [lemma, lemma_freq]

        if inflected_freq and inflected_freq.isnumeric():
            if check_inflections:
                if output_pos_tags:
                    yield [current_entry[0], inflected_freq, current_entry[2]]
                else:
                    yield [current_entry[0], inflected_freq]
            else:
                if output_pos_tags:
                    yield [inflected, inflected_freq, pos_tags]
                else:
                    yield [inflected, inflected_freq]

def combine_sorted_single(code, frequency_dir=None, unimorph_dir=None, max_len=None, inflections=True, parts_of_speech = None, output_pos_tags=True, check_inflections=False) -> list:
    combined = []
    seen_words = set()

    if max_len:
        count = 0
    for entry in combined_iterator(code, frequency_dir, unimorph_dir, None, inflections, parts_of_speech, output_pos_tags, check_inflections):
        word = entry[0]

        if word not in seen_words:
            seen_words.add(word)
            combined.append(entry)

            if max_len:
                count += 1
                if count >= max_len:
                    break

    combined.sort(key=lambda x: int(x[1]), reverse=True)
    return combined

def combine_sorted_all(frequency_dir: Union[Path, str, None]=None, unimorph_dir: Union[Path, str, None]=None, max_len:Union[int, None]=None, inflections:bool=True) -> dict[str, list]:
    if frequency_dir is None:
        frequency_dir = datasets_dir / "frequency"

    frequency_dir = Path(frequency_dir)

    output: dict[str, list] = {}

    for lang_dir in frequency_dir.iterdir():
        code = lang_dir.name

        result = combine_sorted_single(code, frequency_dir, unimorph_dir, max_len, inflections)

        output[code] = result

    return output

def output_combined_single(code:str, output_dir: Union[Path, str, None]=None, frequency_dir=None, unimorph_dir=None, max_len=None, inflections=True, delimiter="\t", parts_of_speech=None, output_pos_tags=True, min_len: Union[int, None]=None, check_inflections=False) -> None:
    if output_dir is None:
        output_dir = datasets_dir / "combined"

    output_dir = Path(output_dir)
    
    output_path: Path = output_dir / code

    output = combine_sorted_single(code, frequency_dir, unimorph_dir, max_len, inflections, parts_of_speech, output_pos_tags, check_inflections)

    if not output or min_len is not None and min_len > len(output):
        print("Not enough data")
        if output_path.exists():
            output_path.unlink()
        return

    print("Success")
    with open(output_path, "w+") as f:
        writer = csv.writer(f, delimiter=delimiter)

        writer.writerows(output)

def output_combined(output_dir: Union[Path, str, None]=None, frequency_dir: Union[Path, str, None]=None, unimorph_dir=None, max_len=None, delimiter="\t", inflections=True, parts_of_speech=None, output_pos_tags=True, min_len=None, check_inflections=False) -> None:
    if output_dir is None:
        output_dir = datasets_dir / "combined"

    output_dir = Path(output_dir)

    output_dir.mkdir(exist_ok=True, parents=True)

    if frequency_dir is None:
        frequency_dir = datasets_dir / "frequency"

    frequency_dir = Path(frequency_dir)

    for lang_dir in frequency_dir.iterdir():
        code = lang_dir.name

        print(f"Processing {code}...")

        output_combined_single(code, output_dir, frequency_dir, unimorph_dir, max_len, inflections, delimiter, parts_of_speech, output_pos_tags, min_len, check_inflections)