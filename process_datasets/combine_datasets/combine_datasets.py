from pathlib import Path
import csv
from typing import Iterator

datasets_dir: Path = Path("datasets")
unimorph_dir: Path = datasets_dir / "unimorph"
frequency_dir: Path = datasets_dir / "frequency"


def dataset_iterator(dir, delimiter) -> Iterator[list]:
    with open(unimorph_dir / code, "r") as f:
        reader = csv.reader(f, delimiter=delimiter)

        for row in reader:
            yield row

def unimorph_iterator(code, unimorph_dir=unimorph_dir) -> Iterator[list]:
    return dataset_iterator(unimorph_dir/code, delimiter="\t")

def frequency_iterator(code, frequency_dir=frequency_dir) -> Iterator[list]:
    return dataset_iterator(unimorph_dir/code, delimiter=" ")

if __name__ == "__main__":
    code = "ukr"
    count = 0
    for l in unimorph_iterator(code):
        print(l)
        count += 1
        if count == 3:
            break