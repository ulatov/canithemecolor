import struct
import time
from typing import TypeVar
import Quartz.CoreGraphics as CG

Pixel = TypeVar('Pixel', bound=tuple[int, int, int])


class ScreenPixel(object):
    """Captures the screen using CoreGraphics, and provides access to
    the pixel values.
    """

    def capture(self, region=None):
        """region should be a CGRect, something like:

        >>> import Quartz.CoreGraphics as CG
        >>> region = CG.CGRectMake(0, 0, 100, 100)
        >>> sp = ScreenPixel()
        >>> sp.capture(region=region)

        The default region is CG.CGRectInfinite (captures the full screen)
        """

        if region is None:
            region = CG.CGRectInfinite
        else:
            # TODO: Odd widths cause the image to warp. This is likely
            # caused by offset calculation in ScreenPixel.pixel, and
            # could could modified to allow odd-widths
            if region.size.width % 2 > 0:
                emsg = "Capture region width should be even (was %s)" % (
                    region.size.width)
                raise ValueError(emsg)

        # Create screenshot as CGImage
        image = CG.CGWindowListCreateImage(
            region,
            CG.kCGWindowListOptionOnScreenOnly,
            CG.kCGNullWindowID,
            CG.kCGWindowImageDefault)

        # Intermediate step, get pixel data as CGDataProvider
        prov = CG.CGImageGetDataProvider(image)

        # Copy data out of CGDataProvider, becomes string of bytes
        self._data = CG.CGDataProviderCopyData(prov)

        # Get width/height of image
        self.width = CG.CGImageGetWidth(image)
        self.height = CG.CGImageGetHeight(image)

    def pixel(self, x: int, y: int) -> Pixel:
        """Get pixel value at given (x,y) screen coordinates

        Must call capture first.
        """

        # Pixel data is unsigned char (8bit unsigned integer),
        # and there are for (blue,green,red,alpha)
        data_format = "BBBB"

        # Calculate offset, based on
        # http://www.markj.net/iphone-uiimage-pixel-color/
        offset = 4 * ((self.width * int(round(y))) + int(round(x)))

        # Unpack data from string into Python'y integers
        b, g, r, _ = struct.unpack_from(data_format, self._data, offset=offset)

        # Return BGRA as RGB
        return r, g, b

    def get_pixel_color(self, x: int, y: int) -> Pixel:
        self.capture(CG.CGRectMake(x, y, 2, 2))
        return self.pixel(0, 0)


if __name__ == '__main__':
    # Timer helper-function
    import contextlib


    @contextlib.contextmanager
    def timer(msg):
        start = time.time()
        yield
        end = time.time()
        print("%s: %.02fms" % (msg, (end - start) * 1000))


    # Example usage
    sp = ScreenPixel()

    region = CG.CGRectMake(0, 0, 100, 100)
    with timer("Capture"):
        # Take screenshot (takes about 70ms for me)
        sp.capture()

    with timer("Query"):
        # Get pixel value (takes about 0.01ms)
        print(sp.width, sp.height)
        print(sp.pixel(0, 0))
