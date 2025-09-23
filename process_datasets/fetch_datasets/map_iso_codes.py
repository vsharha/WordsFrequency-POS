import csv

def map_iso_codes() -> dict:
    mapping: dict = {}

    with open("./process_datasets/fetch_datasets/iso-639-3.tab", "r") as f:
        reader: csv.DictReader = csv.DictReader(f, delimiter="\t")

        for row in reader:
            iso_639 = row.get("Part1")
            iso_639_3 = row.get("Id")
            if(iso_639 and iso_639_3):
                mapping[iso_639] = iso_639_3

    mapping['zh_cn'] = mapping['zh']

    return mapping

def reverse_map_iso_codes() -> dict:
    return {v:k for k, v in map_iso_codes().items()}