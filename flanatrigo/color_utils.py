from PIL import ImageGrab


def is_region_color(region: tuple[int, int, int, int], target_color: tuple[int, int, int], tolerance: int):
    color = region_color_mean(region)
    return (
        abs(target_color[0] - color[0]) < tolerance
        and
        abs(target_color[1] - color[1]) < tolerance
        and
        abs(target_color[2] - color[2]) < tolerance
    )


def region_color_mean(region: tuple[int, int, int, int]) -> tuple[int, int, int]:
    image = ImageGrab.grab(region)
    width = image.width
    height = image.height
    n_pixels = width * height
    image = image.load()
    red_sum = 0
    green_sum = 0
    blue_sum = 0
    for y in range(height):
        for x in range(width):
            # noinspection PyUnresolvedReferences
            r, g, b = image[x, y]
            red_sum += r ** 2
            green_sum += g ** 2
            blue_sum += b ** 2
    return (
        round((red_sum / n_pixels) ** (1 / 2)),
        round((green_sum / n_pixels) ** (1 / 2)),
        round((blue_sum / n_pixels) ** (1 / 2))
    )
