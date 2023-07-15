import random
import requests
from zipfile import ZipFile
from io import BytesIO
from os import getenv


def generate_image(input, large=False):
    body = {
        "input": input,
        "model": "nai-diffusion",
        "action": "generate",
        "parameters": {
            "width": 512 if not large else 768,
            "height": 768 if not large else 512,
            "scale": 11,
            "sampler": "k_dpmpp_2m",
            "steps": 28,
            "n_samples": 1,
            "ucPreset": 0,
            "qualityToggle": True,
            "sm": False,
            "sm_dyn": False,
            "dynamic_thresholding": False,
            "controlnet_strength": 1,
            "legacy": False,
            "add_original_image": False,
            "seed": random.randint(100000000, 999999999),
            "negative_prompt": "nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry",
        },
    }

    headers = {
        "Authorization": f"Bearer {getenv('NOVEL_AI_TOKEN')}",
    }

    response = requests.post(
        "https://api.novelai.net/ai/generate-image", json=body, headers=headers
    )

    if response.status_code == 200:
        with ZipFile(BytesIO(response.content)) as zip:
            return zip.read(zip.namelist()[0])
    else:
        return None
