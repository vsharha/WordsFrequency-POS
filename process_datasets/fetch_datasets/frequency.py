import requests
from .request_github import request_github
from .map_iso_codes import map_iso_codes

import base64
from typing import Union
from pathlib import Path

def fetch_codes() -> list[str]:
    return [folder["name"] for folder in fetch_folders()]

def fetch_mapped_codes() -> list[str]:
    mapping: dict = map_iso_codes()
    mapped_codes: list[str] = []
    for code in fetch_codes():
        code: Union[str, None] = mapping.get(code)
    
        if code is not None:
            mapped_codes.append(code)

    return mapped_codes

def fetch_folders() -> list[dict]:
    response: requests.Response = request_github("https://api.github.com/repos/hermitdave/FrequencyWords/contents/content/2018")

    return response.json()

def download_datasets(codes: list[str]) -> None:
    print("Downloading frequency datasets...")

    folders: list[dict] = fetch_folders()

    output_dir: Path = Path("datasets") / "frequency"
    
    mapping = map_iso_codes()

    for folder in folders:
        name: Union[str, None] = folder.get('name')

        if name is None:
            continue

        mapped_name: Union[str, None] = mapping.get(name)

        if mapped_name is None:
            print(f"Couldn't map {name} to 3-letter code")
            continue

        if mapped_name not in codes:
            continue

        output_path: Path = output_dir / mapped_name

        if output_path.exists():
            print(f"Skipping {mapped_name} - file already exists")
            continue

        response: requests.Response = request_github(folder["git_url"])
        files = response.json()['tree']

        for file in files:
            if not "full" in file['path']:
                continue

            response: requests.Response = request_github(file['url'])
            blob = response.json()

            if not blob.get("encoding") == "base64" or not blob.get("content"):
                print("Error downloading")
                continue

            content_bytes = base64.b64decode(blob["content"])
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(content_bytes)

            print(f"Downloaded {mapped_name}")
