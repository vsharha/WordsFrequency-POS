from pathlib import Path
from iso_639.check_iso_code import map_iso_639_3, reverse_mapping

def set_from_dir(dir: Path):
    return set([v.name for v in dir.iterdir()])

if __name__ == "__main__":
    unimorph_path: Path = Path("datasets")/"unimorph"
    frequency_path: Path = Path("datasets")/"FrequencyWords"

    