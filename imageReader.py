from pathlib import Path

from PIL import Image

IMAGE_PATH = Path.cwd() / 'pixel_images'
PIXEL_DATA_PATH = Path.cwd() / 'pixels_data'


def test_read_pixels_from_file():
    file = open(PIXEL_DATA_PATH / 'christmas_tree.pixels')
    row = []
    pixels_list = []
    for line in file:
        row = line.split(';')
        del row[-1]
        new_row = []
        for value in row:
            rgb_list = []
            value_list = value[1:-1].split(',')
            for rgb_value in value_list:
                rgb_list.append(int(rgb_value))
            new_row.append(rgb_list)
        pixels_list.append(new_row)
    file.close()

    for row in pixels_list:
        print(row)
    

def calculate_sizes(pillow_img, qty_art_pixel_col):
    width = pillow_img.size[0]
    height = pillow_img.size[1]
    pixel_resolution = int(width / qty_art_pixel_col)
    center_offset = int(pixel_resolution / 2)

    return width, height, pixel_resolution, center_offset


def main():
    qty_art_pixel_row = 16
    qty_art_pixel_col = 16
    filename = 'christmas_tree'

    with Image.open(IMAGE_PATH / f'{filename}.png') as im:
        width, height, pixel_resolution, center_offset = calculate_sizes(im, qty_art_pixel_col)
        print("width", width)
        print("height", height)
        print("pixel_resolution", pixel_resolution)
        print("center offset", center_offset)

        pixels = []
        for y in range(qty_art_pixel_col):
            row = []
            for x in range(qty_art_pixel_row):
                rgb = []
                for count, value in enumerate(im.getpixel((x*pixel_resolution + center_offset, y*pixel_resolution + center_offset))):
                    if count == 3:
                        break
                    rgb.append(value)
                row.append(rgb)
            pixels.append(row)

        with open(PIXEL_DATA_PATH / f'{filename}.pixels', 'w') as file:
            for row in pixels:
                for value in row:
                    file.write(f'{str(value)};')
                file.write('\n')

    test_read_pixels_from_file()


if __name__ == '__main__':
    main()