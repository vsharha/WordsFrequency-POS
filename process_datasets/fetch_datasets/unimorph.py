import requests
import re

from typing import Union

from pathlib import Path

from .request_github import request_github

def fetch_codes() -> list[str]:
    codes: list[str] = []

    for i in range(1,3):
        response: requests.Response = request_github(f"https://api.github.com/orgs/unimorph/repos?per_page=100&page={i}")
        repos = response.json()

        for repo in repos:
            regex_match: Union[re.Match[str], None] = re.search(r"git@github.com:unimorph/([a-z]{3})\.git", repo["ssh_url"])
            if (regex_match is not None):
                codes.append(regex_match.group(1))

    return codes

def download_datasets(codes: list[str]) -> None:
    print("Downloading unimorph datasets...")

    output_dir: Path = Path("datasets") / "unimorph"

    for code in codes:
        output_path: Path = output_dir/ code

        if output_path.exists():
            print(f"Skipping {code} - file already exists")
            continue
        
        response: requests.Response = requests.get(f"https://raw.githubusercontent.com/unimorph/{code}/refs/heads/master/{code}")

        if response.status_code == 404:
            response = requests.get(f"https://raw.githubusercontent.com/unimorph/{code}/refs/heads/main/{code}")

            if response.status_code == 404:
                print(f"Couldn't download dataset {code}")
                continue
        
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(response.text)

        print(f"Downloaded {code}")