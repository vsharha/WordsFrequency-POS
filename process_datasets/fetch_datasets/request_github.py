import requests
from dotenv import load_dotenv
import os
from typing import Union

load_dotenv()

def request_github(url) -> requests.Response:
    headers = None

    github_token: Union[str, None] = os.getenv("GITHUB_TOKEN")

    if github_token:
        headers = {"Authorization": f"token {github_token}"}
        
    response: requests.Response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(response.json().get("message"))

    return response