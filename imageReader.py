from pathlib import Path

from PIL import Image

IMAGE_PATH = Path.cwd() / 'pixel_images'


def main():
    picture_width = 160
    picture_height = 160
    small_box_rows = 16
    small_box_columns = 16
    pixels_small_box = int(picture_width / small_box_rows)
    small_box_center = int(pixels_small_box / 2)
    filename = 'christmas_tree'

    with Image.open(IMAGE_PATH / f'{filename}.png') as im:
        pixels = []
        for y in range(small_box_columns):
            row = []
            for x in range(small_box_rows):
                rgb = []
                for count, value in enumerate(im.getpixel((x*pixels_small_box + small_box_center, y*pixels_small_box + small_box_center))):
                    if count == 3:
                        break
                    rgb.append(value)
                row.append(rgb)
            pixels.append(row)

        

        with open(f'{filename}.pixels', 'w') as file:
            for row in pixels:
                file.write(f'{str(row)}\n')


if __name__ == '__main__':
    main()