import csv
from pathlib import Path


def load_dataset_codes(dataset_path: Path | str) -> list:
    dataset_path = Path(dataset_path)

    return sorted([lang.name for lang in dataset_path.iterdir()])

def map_iso_639_3(codes_iso_639: list) -> dict:
    mapped: dict = {}

    with open("./iso-639-3.tab", "r") as f:
        reader: csv.DictReader = csv.DictReader(f, delimiter="\t")

        for row in reader:
            iso_639 = row.get("Part1")
            if(iso_639 in codes_iso_639):
                mapped[iso_639] = row.get("Id")
    
    return mapped

if __name__ == "__main__":
    dataset_codes: list = load_dataset_codes("dataset")
    mapped: dict = map_iso_639_3(dataset_codes)

    print("The following codes weren't mapped: ",set(dataset_codes).difference(set(mapped)))