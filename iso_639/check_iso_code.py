import csv
from pathlib import Path
import argparse


def load_dataset_codes(dataset_path: Path | str) -> list:
    dataset_path = Path(dataset_path)

    return sorted([lang.name for lang in dataset_path.iterdir()])

def map_iso_639_3() -> dict:
    mapping: dict = {}

    with open("./iso_639/iso-639-3.tab", "r") as f:
        reader: csv.DictReader = csv.DictReader(f, delimiter="\t")

        for row in reader:
            iso_639 = row.get("Part1")
            iso_639_3 = row.get("Id")
            if(iso_639 and iso_639_3):
                mapping[iso_639] = iso_639_3
    
    return mapping

def reverse_mapping(mapping: dict) -> dict:
    return {v: k for k, v in mapping.items()}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Map ISO 639 language codes")

    parser.add_argument("--codes_file", nargs="?", default="fetch_unimorph/unimorph_repos.txt", 
                       help="A file with a number of ISO 639 or 639-3 codes")
    parser.add_argument("dataset_path", nargs="?", default="datasets/FrequencyWords", 
                       help="Path to the dataset directory")
    
    args = parser.parse_args()

    dataset_codes: list = load_dataset_codes(args.dataset_path)
    mapping: dict = map_iso_639_3()

    output = []

    with open(args.codes_file, "r") as f:
        for line in f:
            line = line.rstrip("\n")
            result = reverse_mapping(mapping).get(line)
            if result in dataset_codes:
                output.append(line)
    
    print(mapping.get("zh"))

    # for code in set(dataset_codes).difference(set(output)):
    #     result = mapping.get(code)
    #     if result is None:
    #         print(code)

    # for result in output:
    #     print(result)