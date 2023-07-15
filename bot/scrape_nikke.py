import os
import pickle
import html
import requests
from googletranslate import translate
from bs4 import BeautifulSoup
from typing import Optional


def get_paragraphs_until_header(tag: str):
    paragraphs = []
    next_tag = tag.find_next_sibling()
    while next_tag and next_tag.name not in ["h2", "h3"]:
        if next_tag.name == "p":
            paragraphs.append(html.unescape(next_tag.text))
        next_tag = next_tag.find_next_sibling()
    return paragraphs


class Nikke:
    def __init__(
        self,
        name: str,
        description: str,
        profile: str,
        backstory: str,
        image: str,
    ):
        self.name = name
        self.description = description
        self.profile = profile
        self.backstory = backstory
        self.image = image
        self.portrait = f"https://ik.imagekit.io/ez2m5kovtw/tr:w-512,h-512,fo-top,c-maintain_ratio/{image.split('/images/')[1]}"


def scrape_nikke(name: str) -> Optional[Nikke]:
    # Check cache
    os.makedirs("cache", exist_ok=True)

    cache_file = f"cache/{name.capitalize()}.pkl"
    if os.path.exists(cache_file):
        with open(cache_file, "rb") as f:
            return pickle.load(f)

    url = f"https://nikke-goddess-of-victory-international.fandom.com/wiki/{name}"

    page = requests.get(url)
    if page.status_code != 200:
        return None

    html_content = BeautifulSoup(page.content, "html.parser")

    title = html_content.find("h1", {"class": "page-header__title"}).find(
        "span", {"class": "mw-page-title-main"}
    )
    if title is None:
        return None
    title = title.text

    description_div = html_content.find(
        "div", {"class": "description standard-border"}
    ).find("div")
    if description_div is None:
        return None
    description = " ".join(
        [html.unescape(i_tag.text) for i_tag in description_div.find_all("i")]
    )

    profile_tag = None
    for id_value in ["Profile", "Description"]:
        profile_tag = html_content.find(
            "span", {"id": id_value, "class": "mw-headline"}
        )
        if profile_tag is not None:
            break
    if profile_tag is None:
        return None
    profile_paragraphs = get_paragraphs_until_header(profile_tag.parent)
    profile = "\n\n".join([html.unescape(p_tag) for p_tag in profile_paragraphs])

    backstory_tag = html_content.find(
        "span", {"id": "Nikke_Backstory", "class": "mw-headline"}
    )
    if backstory_tag is None:
        return None
    backstory_paragraphs = get_paragraphs_until_header(backstory_tag.parent)
    backstory = "\n\n".join([html.unescape(p_tag) for p_tag in backstory_paragraphs])

    image_tag = html_content.find("figure", {"class": "pi-item pi-image"}).find("img")
    if image_tag is None:
        return None
    image = image_tag["src"].split("/revision")[0]

    # Save to cache
    result = Nikke(
        title,
        translate(description, dest="pt-br", src="en"),
        translate(profile, dest="pt-br", src="en"),
        translate(backstory, dest="pt-br", src="en"),
        image,
    )
    with open(cache_file, "wb") as f:
        pickle.dump(result, f)

    return result
