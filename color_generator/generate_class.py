import colorsys
import json
import os
from pathlib import Path
from traceback import print_exc
from typing import Type, Iterator
from urllib.parse import quote

from selenium.webdriver import Remote

__all__ = (
    "Generate",
)

BASE_PATH = Path(__file__).resolve().parent
DATA_PATH = BASE_PATH.parent / "_data"
BROWSERS_COLORS_PATH = DATA_PATH / "browsers_colors.json"

if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)

if not os.path.exists(BROWSERS_COLORS_PATH):
    with open(BROWSERS_COLORS_PATH, 'w', encoding='utf-8') as file_:
        file_.write('{}')

with open(BASE_PATH / "theme_color.html", encoding='utf-8') as html:
    content = "".join(map(str.strip, html.read().split('\n')))


def hsv2rgb(h: float, s: float, v: float) -> str:
    return '#' + ''.join(f"{round(i * 255):02x}" for i in colorsys.hsv_to_rgb(h, s, v))


class Generate:
    driver: Type[Remote]
    config: dict
    theme: str = "any"

    @classmethod
    def get_color(cls, web_driver: Remote) -> Iterator[str]:
        raise NotImplementedError()

    @classmethod
    def colors(cls) -> Iterator[str]:
        for r in range(256):
            for g in range(256):
                for b in range(256):
                    yield f"#{r:02x}{g:02x}{b:02x}"

    @classmethod
    def content_to_browser_url(cls, theme_color: str, body: str = ""):
        return "data:text/html;charset=utf-8," + quote(
            content.replace('%THEME_COLOR%', theme_color).replace('%BODY%', body)
        )

    @classmethod
    def save(cls):
        driver = cls.driver(**cls.config)
        try:
            result = [x for x in cls.get_color(driver) if not print(f'"{x}",')]
        except BaseException:  # noqa
            print_exc()
            return exit(1)
        finally:
            driver.quit()

        name = cls.__name__.lower().strip('generate')

        browsers_color: dict = json.load(open(BROWSERS_COLORS_PATH))
        browsers_color.setdefault(name, {})
        browsers_color[name][cls.theme] = result

        with open(DATA_PATH / f'{name}_{cls.theme}.json', 'w') as browser:
            json.dump(result, browser, indent=2, ensure_ascii=False)

        json.dump(browsers_color, open(BROWSERS_COLORS_PATH, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
