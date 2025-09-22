import csv
from pathlib import Path
import argparse


def load_dataset_codes(dataset_path: Path | str) -> list:
    dataset_path = Path(dataset_path)

    return sorted([lang.name for lang in dataset_path.iterdir()])

def map_iso_639_3(codes_iso_639: list, iso_path: Path | str) -> dict:
    iso_path = Path(iso_path)

    mapped: dict = {}

    with open("./iso_639/iso-639-3.tab", "r") as f:
        reader: csv.DictReader = csv.DictReader(f, delimiter="\t")

        for row in reader:
            iso_639 = row.get("Part1")
            if(iso_639 in codes_iso_639):
                mapped[iso_639] = row.get("Id")
    
    return mapped

def reverse_mapping(mapping: dict) -> dict:
    return {v: k for k, v in mapping.items()}

def output(code: str, mapping: dict) -> None:
    if len(code) == 2:
        mapped = mapping.get(code)
        if mapped:
            print(code)
    elif len(code) == 3:
        mapped: str = reverse_mapping(mapping).get(code)
        if(mapped):
            print(code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Map ISO 639 language codes")

    parser.add_argument("--code", nargs="?", default="en", 
                       help="ISO 639 or 639-3 language code (default: en)")
    parser.add_argument("--codes_file", nargs="?", default="unimorph_repos.txt", 
                       help="A file with a number of ISO 639 or 639-3 codes")
    parser.add_argument("dataset_path", nargs="?", default="FrequencyWords", 
                       help="Path to the dataset directory (default: dataset)")
    parser.add_argument("--iso-file", default="./iso_639/iso-639-3.tab",
                       help="Path to ISO 639-3 file (default: ./iso_639/iso-639-3.tab)")
    
    args = parser.parse_args()

    dataset_codes: list = load_dataset_codes(args.dataset_path)
    mapping: dict = map_iso_639_3(dataset_codes, args.iso_file)

    # print("The following codes weren't mapped: ", set(dataset_codes).difference(set(mapped)))

    if args.codes_file:
        with open(args.codes_file, "r") as f:
            for line in f:
                output(line.rstrip("\n"), mapping)
    
    else:
        output(args.code, mapping)