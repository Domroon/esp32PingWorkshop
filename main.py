from machine import Pin
from neopixel import NeoPixel
import time


class Pixel:
    def __init__(self, id, x, y, color=[255, 0, 255], brightness=0.15):
        self.id = id
        self.color = color
        self.origin_color = color
        self.brightness = brightness
        self.x = x
        self.y = y
        self.origin_x = x
        self.origin_y =y
        self._calculate_brightness()
        print(self.color)

    def _calculate_brightness(self):
        calculated_color = []
        for value in self.origin_color:
            value = int(value * self.brightness)
            calculated_color.append(value)
        self.color = calculated_color

    def change_brightness(self, brightness):
        calculated_color = []
        for value in self.origin_color:
            value = int(value * brightness)
            calculated_color.append(value)
        self.color = calculated_color


class Sprite:
    def __init__(self, x=0, y=0):
        self.id = id(self)
        self.x = x
        self.y = y
        self.pixels = [
                        Pixel(self.id, 0, 0),
                      ]

    def add_pixels(self, int_array):
        self.pixels = []
        y = 0
        for row in int_array:
            x = 0
            for value in row:
                if value:
                    pixel = Pixel(self.id, x, y)
                    self.pixels.append(pixel)
                x += 1
            y += 1
    
    def add_colored_pixels(self, color_array):
        self.pixels = []
        y = 0
        for row in color_array:
            x = 0
            for value in row:
                if value:
                    pixel = Pixel(self.id, x, y, color=color_array[y][x])
                    self.pixels.append(pixel)
                x += 1
            y += 1
    
    def change_all_color(self):
        pass
    
    def set_pos(self, x, y):
        for pixel in self.pixels:
            pixel.x = pixel.origin_x + x
            pixel.y = pixel.origin_y + y
        
    def move(self, x, y):
        self.x = x
        self.y = y
        for pixel in self.pixels:
            pixel.x = pixel.x + self.x
            pixel.y = pixel.y + self.y

    def change_brightness(self, brightness):
        for pixel in self.pixels:
            pixel.change_brightness(brightness)


class SpriteGroup:
    def __init__(self, sprite_list=[]):
        self.sprites = sprite_list
        
    def add(self, sprite):
        self.sprites.append(sprite)
        
    def remove(self):
        self.sprites.pop()


class Matrix:
    def __init__(self, pin, sprite_groups, width=16, height=16):
        self.pin = pin
        self.sprite_groups = sprite_groups
        self.width = width
        self.height = height
        self.led_qty = width * height
        self.np = NeoPixel(self.pin, self.led_qty)
        self.coord = self._create_pixel_num_array()
        
    def _create_pixel_num_array(self):
      pixel_num_array = []
      row_start = 0
      row_end = self.height
      for row in range(self.width):
          row = []
          for i in range(row_start, row_end):
            row.append(i)
      
          row_start = row_end
          row_end = row_end + 16
          pixel_num_array.append(row)
          
      count = 0
      for row in pixel_num_array:
          if count % 2 == 0:
              row.reverse()
          count += 1
      
      return pixel_num_array    
    
    def _add_sprite(self, sprite):
        for pixel in sprite.pixels:
            try:
                self.np[self.coord[pixel.y][pixel.x]] = pixel.color
            except IndexError:
                pass
    
    def show(self):
        for sprite_group in self.sprite_groups:
            for sprite in sprite_group:
                self._add_sprite(sprite)
        self.np.write()
        
    def clear(self):
        self.np.fill((0, 0, 0))


def main():
    pin = Pin(33, Pin.OUT)
    
    t_pix = [[1,1,1],
             [0,1,0],
             [0,1,0],
            ]
    h_pix = [[1,0,1],
             [1,1,1],
             [1,0,1],
            ]

    christmas = [[[0, 0, 0],[0, 0, 0],[255, 0, 0],[0, 0, 0],[0, 0, 0]],
                 [[0, 0, 0],[51, 255, 0],[51, 255, 0],[51, 255, 0],[0, 0, 0]],
                 [[51, 255, 0],[51, 255, 0],[51, 255, 0],[51, 255, 0],[51, 255, 0]],
                 [[0, 0, 0],[0, 0, 0],[153, 51, 0],[0, 0, 0],[0, 0, 0]],
                 [[0, 0, 0],[0, 0, 0],[153, 51, 0],[0, 0, 0],[0, 0, 0]],
            ]

    point = Sprite()
    t_letter = Sprite()
    christ_tree = Sprite()
    t_letter.add_pixels(t_pix)
    h_letter = Sprite()
    h_letter.add_pixels(h_pix)
    h_letter.set_pos(10, 10)
    christ_tree.add_colored_pixels(christmas)
    christ_tree.set_pos(0 ,10)
    
    
    spriteGroup = SpriteGroup()
    spriteGroup.add(point)
    spriteGroup.add(h_letter)
    spriteGroup.add(christ_tree)
    spriteGroup.add(t_letter)
    
    matrix = Matrix(pin, [spriteGroup.sprites])
    
    tick = 0.1
    try:
        brightness = 0.05
        t_letter.change_brightness(brightness)
        for _ in range(0, 10):
            matrix.show()
            t_letter.change_brightness(brightness)
            brightness = brightness + 0.05
            time.sleep(0.5)
            matrix.clear()
        while True:
            for _ in range(1, 16):
                matrix.show()
                point.move(1, 0)
                t_letter.move(1, 1)
                time.sleep(tick)
                matrix.clear()
            for _ in range(1, 16):
                matrix.show()
                point.move(-1, 0)
                t_letter.move(-1, -1)
                time.sleep(tick)
                matrix.clear() # improvement: only clear a single object!
    except KeyboardInterrupt:
        matrix.clear()
       
    
    
if __name__ == '__main__':
    main()