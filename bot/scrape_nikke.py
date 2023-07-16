import os
import pickle
import html
import requests
from googletranslate import translate
from bs4 import BeautifulSoup
from typing import Optional, List
from urllib.parse import urljoin


class Nikke:
    _BASE_URL = "https://nikke-goddess-of-victory-international.fandom.com/wiki/"
    _IMAGE_BASE_URL = (
        "https://ik.imagekit.io/ez2m5kovtw/tr:w-512,h-512,fo-top,c-maintain_ratio/"
    )
    _CACHE_DIR = "cache"
    _CACHE_FILE_EXTENSION = ".pkl"

    def __init__(
        self,
        name: str,
        description: str,
        profile: str,
        backstory: str,
        image: str,
    ):
        self.name = name
        self.description = translate(description, dest="pt-br", src="en")
        self.profile = translate(profile, dest="pt-br", src="en")
        self.backstory = translate(backstory, dest="pt-br", src="en")
        self.image = image
        self.portrait = urljoin(self._IMAGE_BASE_URL, image.split("/images/")[1])

    @classmethod
    def _load_from_cache(cls, name: str) -> Optional["Nikke"]:
        os.makedirs(cls._CACHE_DIR, exist_ok=True)
        cache_file_path = os.path.join(
            cls._CACHE_DIR, f"{name.capitalize()}{cls._CACHE_FILE_EXTENSION}"
        )
        if os.path.exists(cache_file_path):
            with open(cache_file_path, "rb") as f:
                return pickle.load(f)
        return None

    @classmethod
    def _save_to_cache(cls, name: str, nikke: "Nikke"):
        cache_file_path = os.path.join(
            cls._CACHE_DIR, f"{name.capitalize()}{cls._CACHE_FILE_EXTENSION}"
        )
        with open(cache_file_path, "wb") as f:
            pickle.dump(nikke, f)

    @staticmethod
    def _fetch_page_content(name: str) -> Optional[BeautifulSoup]:
        url = urljoin(Nikke._BASE_URL, name)
        page = requests.get(url)
        if page.status_code != 200:
            return None
        return BeautifulSoup(page.content, "html.parser")

    @staticmethod
    def _get_paragraphs_until_header(tag: str) -> List[str]:
        paragraphs = []
        next_tag = tag.find_next_sibling()
        while next_tag and next_tag.name not in ["h2", "h3"]:
            if next_tag.name == "p":
                paragraphs.append(html.unescape(next_tag.text))
            next_tag = next_tag.find_next_sibling()
        return paragraphs

    @staticmethod
    def _extract_text(html_content: BeautifulSoup, section_id: str) -> Optional[str]:
        tag = html_content.find("span", {"id": section_id, "class": "mw-headline"})
        if tag is None:
            return None
        paragraphs = Nikke._get_paragraphs_until_header(tag.parent)
        return "\n\n".join([html.unescape(p_tag) for p_tag in paragraphs])

    @classmethod
    def from_name(cls, name: str) -> Optional["Nikke"]:
        cached = cls._load_from_cache(name)
        if cached:
            return cached

        html_content = cls._fetch_page_content(name)
        if html_content is None:
            return None

        title = (
            html_content.find("h1", {"class": "page-header__title"})
            .find("span", {"class": "mw-page-title-main"})
            .text
        )
        description = " ".join(
            [
                html.unescape(i_tag.text)
                for i_tag in html_content.find(
                    "div", {"class": "description standard-border"}
                )
                .find("div")
                .find_all("i")
            ]
        )
        profile = cls._extract_text(html_content, "Profile") or cls._extract_text(
            html_content, "Description"
        )
        backstory = cls._extract_text(
            html_content, "Nikke_Backstory"
        ) or cls._extract_text(html_content, "Main_Story")

        image = (
            html_content.find("figure", {"class": "pi-item pi-image"})
            .find("img")["src"]
            .split("/revision")[0]
        )

        if not all([title, description, profile, backstory, image]):
            return None

        nikke = cls(title, description, profile, backstory, image)
        cls._save_to_cache(name, nikke)

        return nikke
