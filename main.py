import time
from machine import Pin, RTC

from neopixel import NeoPixel

from espClock import NumberSegment
from espClock import COLOR
from espClock import NUMBER
from espClock import Animation
from espClock import calculate_brightness
from logging import Logger


def main():
    logger = Logger()
    np = NeoPixel(Pin(32, Pin.OUT), 28)
    numSeg = NumberSegment(np)
    
    blue = calculate_brightness(COLOR["blue"], 0.2)
    green = calculate_brightness(COLOR["green"], 0.2)
    white = calculate_brightness(COLOR["white"], 0.2)
    
    try:
        while True:
            animation = Animation(numSeg, np, logger)            
            animation.random_single_color_flash()
            
            numSeg.set_number(NUMBER[4], color=blue)
            time.sleep(1)
            numSeg.set_number(NUMBER[5], color=green)
            time.sleep(1)
            numSeg.turn_off_all()
            COLOR["blue"] = [0, 0, 255]
            COLOR["green"] = [0, 255, 0]
            
            animation.random_flashing(duration=5)
            animation.show_all_numbers(color=white, time_per_number=0.25)
            COLOR["white"] = [255, 255, 255]
            animation.colorful_numbers()
    except KeyboardInterrupt:
        numSeg.turn_off_all()
    
    
if __name__ == '__main__':
    main()