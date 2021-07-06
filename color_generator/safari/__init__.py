from typing import Iterator

from selenium.webdriver import Safari

from color_generator.generate_class import Generate
from color_generator.safari.get_pixel import ScreenPixel
from color_generator.safari.helpers import *


# TODO: CREATE MORE EFFICIENCY ALGORITHM FOR FINDING UNSUPPORTED COLOR
class GenerateSafari(Generate):
    """
    You must enable the 'Allow Remote Automation' option in Safari's Develop menu to control Safari via WebDriver.
    """
    driver = Safari
    config = config
    theme = check_appearance()

    @classmethod
    def get_safari_color(cls, safari: Safari, sp: ScreenPixel, color: str):
        data = cls.content_to_browser_url(color, f'{color}')

        safari.get(data)
        pos = safari.get_window_position()
        return '#' + ''.join(
            map(
                lambda x: hex(x)[2:],
                sp.get_pixel_color(pos['x'] + 10, pos['y'] + 50)
            )
        )

    @classmethod
    def get_color(cls, safari: Safari) -> Iterator[str]:
        # Maybe problem with screenshot function,
        # 'Cause safari_color != color

        sp = ScreenPixel()
        default_color = "#cacaca" if cls.theme == "light" else "#303030"
        for hue in range(360):
            color = f"hsl({hue}, 100%, 50%)"
            safari_color = cls.get_safari_color(safari, sp, color)
            if safari_color == default_color:
                yield color
                for saturation in range(99, 0, -1):
                    color = f"hsl({hue}, {saturation}%, 50%)"
                    if cls.get_safari_color(safari, sp, color) == default_color:
                        yield color
                        for lightness in range(51, 100):
                            color = f"hsl({hue}, {saturation}%, {lightness}%)"
                            if cls.get_safari_color(safari, sp, color) == default_color:
                                yield color
                            else:
                                break

                        for lightness in range(49, 0, -1):
                            color = f"hsl({hue}, {saturation}%, {lightness}%)"
                            if cls.get_safari_color(safari, sp, color) == default_color:
                                yield color
                            else:
                                break
                    else:
                        break


if __name__ == '__main__':
    GenerateSafari.save()
