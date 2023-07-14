import requests
import base64
from os import getenv


def upload_image(image: bytes) -> str:
    url = "https://api.imgur.com/3/image"
    headers = {"Authorization": f"Client-ID {getenv('IMGUR_CLIENT_ID')}"}

    data = {"image": base64.b64encode(image)}

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()["data"]["link"]
    else:
        return None
