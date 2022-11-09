import time
import random
import logging
from random import randint


NUMBER = {
    0 : [0, 1, 2, 3, 4, 5],
    1 : [2, 3],
    2 : [1, 2, 6, 5, 4],
    3 : [1, 2, 6, 3, 4],
    4 : [0, 6, 2, 3],
    5 : [0, 1 , 6, 3, 4],
    6 : [1, 0, 5, 4, 3, 6],
    7 : [1, 2, 3],
    8 : [1, 2, 6, 5, 4, 3, 0],
    9 : [6, 0, 1, 2, 3, 4]
}

LETTER = {
    'C': [1, 0, 5, 4],
    'E': [1, 0, 5, 4, 6],
    'F': [1, 0, 5, 6],
    'I': [0, 5],
    'L': [0, 5, 4],
    'O': [0, 1, 2, 3, 4, 5],
    'P': [0, 5, 1, 2, 6],
    'S': [1, 0, 6, 3, 4],
    'U': [0, 5, 4, 3, 2],
}

COLOR = {
    "red": [255, 0, 0],
    "orange": [255, 50, 0],
    "green": [0, 255, 0],
    "light_green": [255, 255, 0],
    "blue": [0, 0, 255],
    "light_blue": [0, 255, 255],
    "yellow": [255, 180, 0],
    "purple": [255, 0, 255],
    "pink": [255, 0, 64],
    "white": [255, 255, 255]
}

WEEKDAY = {
    1 : "Monday",
    2 : "Tuesday",
    3 : "Wednesday",
    4 : "Thursday",
    5 : "Friday",
    6 : "Saturday",
    7 : "Sunday"
}

WEEKDAY_REV = {
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
    "Sunday": 7
}


def calculate_brightness(color, brightness):
    for byte in range(len(color)):
        color[byte] = int(color[byte] * brightness)
    return color


class Timer:
    def __init__(self, start_time=0, end_time=0):
        self.start_time = start_time
        self.end_time = end_time

    def start(self):
        self.start_time = time.ticks_ms()

    def stop(self):
        self.end_time = time.ticks_ms()

    def time_since_start(self):
        return time.ticks_ms() - self.start_time

    def time_passed(self):
        return self.end_time - self.start_time


class Segment:
    def __init__(self, neopixels, pixels):
        self.pixels = neopixels
        self.pixel_numbers = pixels

    def set_all_pixels(self, color=(255, 255, 255)):
        for pixel_number in self.pixel_numbers:
            self.pixels[pixel_number] = color
            self.pixels.write()


class NumberSegment:
    def __init__(self,  neopixels, segment_qty=4):
        self.neopixels = neopixels
        self.segment_qty = segment_qty
        self.segments = []
        self._create_segments()

    def _create_segments(self):
        for pixel_num in range(0, self.segment_qty * 7, self.segment_qty):
            pixel_list = [num for num in range(pixel_num, pixel_num + self.segment_qty)]
            segment = Segment(self.neopixels, pixel_list)
            self.segments.append(segment)

    def set_all_segments(self, color=(255, 255, 255)):
        for segment in self.segments:
            segment.set_all_pixels(color=color)

    def turn_off_all(self):
        for segment in self.segments:
            segment.set_all_pixels(color=(0, 0, 0))

    def set_number(self, segment_numbers, color=[255, 255, 255]):
        self.turn_off_all()
        for segment_number in segment_numbers:
            self.segments[segment_number].set_all_pixels(color=color)

    def set_letter(self, letter_numbers, color=(255, 255, 255)):
        for letter_number in letter_numbers:
            self.segments[letter_number].set_all_pixels(color=color)

    def set_single_segment(self, segment_number, color=(255, 255, 255)):
        self.segments[segment_number].set_all_pixels(color=color)

    def turn_off_single_segment(self, segment_number):
        self.segments[segment_number].set_all_pixels(color=(0, 0, 0))


class Animation:
    def __init__(self, number_segment, neopixel, logger):
        self.number_segment = number_segment
        self.log = logger
        self.timer = Timer()
        self.np = neopixel

    def show_all_numbers(self, time_per_number=1, color=[255, 255, 255]):
        for number in range(0, 10):
            self.number_segment.turn_off_all()
            self.number_segment.set_number(NUMBER[number], color=color)
            time.sleep(time_per_number)

        self.number_segment.turn_off_all()

    def colorful_numbers(self, time_per_number=0.25):
        self.log.info("Show animation: 'colorful numbers'")
        for key, color in COLOR.items():
            debug_str = "Actual number color: " + key
            self.log.debug(debug_str)
            self.show_all_numbers(time_per_number=time_per_number, color=color)

    def random_flashing(self, flash_duration= 0.05, break_duration=0.05, duration=10):
        self.log.info("Show animation: 'random flashing'")
        self.timer.start()
        duration = duration * 1000
        while True:
            random_segment_number = random.randint(0, len(self.number_segment.segments) - 1)
            self.number_segment.set_single_segment(random_segment_number)
            time.sleep(flash_duration)
            self.number_segment.turn_off_single_segment(random_segment_number)
            time.sleep(break_duration)

            random_segment_number_2 = random.randint(0, len(self.number_segment.segments) - 1)
            while random_segment_number == random_segment_number_2:
                random_segment_number_2 = random.randint(0, len(self.number_segment.segments) - 1)
            self.number_segment.set_single_segment(random_segment_number_2)
            time.sleep(flash_duration)
            self.number_segment.turn_off_single_segment(random_segment_number_2)
            time.sleep(break_duration)

            if self.timer.time_since_start() > duration:
                break
    
    def random_single_color_flash(self, flash_duration=0.03, duration=10):
        self.timer.start()
        duration = duration * 1000
        while True:
            self.np[randint(0, 27)] = (255, 255, 255)
            self.np[randint(0, 27)] = (255, 0, 0)
            self.np[randint(0, 27)] = (0, 255, 0)
            self.np[randint(0, 27)] = (0, 0, 255)
            self.np[randint(0, 27)] = (255, 0, 255)
            self.np[randint(0, 27)] = (0, 255, 255)
            self.np.write()
            time.sleep(flash_duration)
            self.number_segment.turn_off_all()
            
            if self.timer.time_since_start() > duration:
                break
        
    #def fade_out_all(self, color):
    #    brightness = 1
    #    while True:
    #        if brightness < 0.1:
    #            break
    #        calc_color = calculate_brightness(color, brightness)
    #        self.number_segment.set_all_segments(color=calc_color)
    #        time.sleep(0.005)
    #        brightness = brightness - 0.01


class Dot:
    def __init__(self, neopixels, pixel_qty=4):
        self.np = neopixels
        self.pixel_qty = pixel_qty
        self.pixel_numbers = [num for num in range(0, self.pixel_qty)]

    def set_all(self, color=(255, 255, 255)):
        for num in self.pixel_numbers:
            self.np[num] = color
            self.np.write()
    
    def set_dot(self, dot_num, color):
        self.np[dor_num] = color
    
    def turn_off_all(self):
        for num in self.pixel_numbers:
            self.np[num] = (0, 0, 0)
            self.np.write()


class Display:
    def __init__(self):
        self.hour_tens_val = None
        self.hour_one_val = None
        self.minute_tens_val = None
        self.minute_one_val = None
        self.digit_pins = {key: value for (key, value) in DIGIT_PIN.items()}
        self.digits = {}
        self._create_digits()

        self.dot_pins = {key: value for (key, value) in DOT_PIN.items()}
        self.dots = {}
        self._create_dots()

    def _create_digits(self):
        for (key, pin) in self.digit_pins.items():
            np = NeoPixel(pin, 28)
            self.digits[key] = NumberSegment(np)

    def _create_dots(self):
        for (key, pin) in self.dot_pins.items():
            np = NeoPixel(pin, 28)
            self.dots[key] =  Dot(np)
    
    def show_menu_text(self, color=(0, 0, 64)):
        self.digits['hour_tens'].set_letter(LETTER['E'], color=color)
        self.hour_tens_val = 'E'
        self.digits['hour_one'].set_letter(LETTER['S'], color=color)
        self.hour_one_val = 'S'
        self.digits['minute_tens'].set_letter(LETTER['P'], color=color)
        self.minute_tens_val = 'P'

    def show_server_text(self, color=(64, 0, 0)):
        self.digits['hour_tens'].set_letter(LETTER['S'], color=color)
        self.hour_tens_val = 'S'
        self.digits['hour_one'].set_letter(LETTER['E'], color=color)
        self.hour_one_val = 'E'

    def show_time(self, hour, minute, color=(255, 255, 255)):
        # hour
        if hour <= 9:
            if not self.hour_tens_val == 0:
                self.digits['hour_tens'].set_number(NUMBER[0], color=color)
            self.hour_tens_val = 0

            if not self.hour_one_val == hour:
                self.digits['hour_one'].set_number(NUMBER[hour], color=color)
            self.hour_one_val = hour

        else:
            hour_tens_val = int(str(hour)[0])
            hour_one_val = int(str(hour)[1])

            if not self.hour_tens_val == hour_tens_val:
                self.digits['hour_tens'].set_number(NUMBER[hour_tens_val ], color=color)
            self.hour_tens_val = hour_tens_val

            if not self.hour_one_val == hour_one_val:
                self.digits['hour_one'].set_number(NUMBER[hour_one_val], color=color)
            self.hour_one_val = hour_one_val

        # minute
        if minute <=9:
            if not self.minute_tens_val == 0:
                self.digits['minute_tens'].set_number(NUMBER[0], color=color)
            self.minute_tens_val = 0

            if not self.minute_one_val == minute:
                self.digits['minute_one'].set_number(NUMBER[minute], color=color)
            self.minute_one_val = minute
        else:
            minute_tens_val = int(str(minute)[0])
            minute_one_val = int(str(minute)[1])

            if not self.minute_tens_val == minute_tens_val:
                self.digits['minute_tens'].set_number(NUMBER[minute_tens_val], color=color)
            self.minute_tens_val = minute_tens_val
            
            if not self.minute_one_val == minute_one_val:
                self.digits['minute_one'].set_number(NUMBER[minute_one_val], color=color)
            self.minute_one_val = minute_one_val

    def turn_off_all(self):
        for digit in self.digits.values():
            digit.turn_off_all()  
        for dot in self.dots.values():
            dot.turn_off_all()
        self.hour_tens_val = None
        self.hour_one_val = None
        self.minute_tens_val = None
        self.minute_one_val = None


class Hw_Input:
    def __init__(self, input_pins):
        self.input_pins = input_pins
        self.input_values = {}

    def get_values(self):
        self.input_values = {}
        for input_name, pin in self.input_pins.items():
            self.input_values[input_name] = pin.value()
        return self.input_values


class EspClock:
    def __init__(self, logger, memory):
        self.log = logger
        self.memory = memory
        self.client = networking.Client(self.log)
        self.server = networking.Server(self.log)
        self.webserver = webserver.WebServer(self.log, self.memory)
        self.rtc = RTC()
        self.display = Display()
        self.hw_inputs = Hw_Input(BTN)
        self.mode = {
            'menu': False, 
            'clock': True,
            'server': False, 
            }
        self.hour = None
        self.minute = None
        self.second = None
    
    def _set_rtc_by_internet(self):
        data = networking.download_json_file(networking.LINK['datetime'])
        self.rtc.datetime((
            data['year'],
            data['month'],
            data['day'],
            0,                  # not implemented yet                 
            data['hour'],
            data['minute'],
            data['seconds'],
            data['milliSeconds']
        ))

    def _set_time(self):
        self.hour = self.rtc.datetime()[4]
        self.minute = self.rtc.datetime()[5]
        self.second = self.rtc.datetime()[6]

    def _clock_mode(self, color=(64, 64, 64)):
        self._set_time()
        self.display.show_time(self.hour, self.minute, color=color)
        self.display.dots['above'].set_all(color=color)
        self.display.dots['below'].set_all(color=color)
        time.sleep(0.5)
        self.display.dots['above'].turn_off_all()
        self.display.dots['below'].turn_off_all()
        time.sleep(0.5)        

    def _change_mode(self, new_mode):
        for mode_name in self.mode.keys():
            self.mode[mode_name] = False
        
        self.mode[new_mode] = True

    def _menu_mode(self, max_duration=3):
        self.display.turn_off_all()
        self.display.show_menu_text()
        timer = 0
        while True:
            if timer == max_duration:
                self.log.info('Clock mode')
                self._change_mode('clock')
                break

            # show here the new menu text

            input_values = self.hw_inputs.get_values() 
            if input_values['menu']:
                self.log.info('Menu Button was pressed')
                timer = 0
            elif input_values['next']:
                self.log.info('Next Button was pressed')
                self.log.info('Server Mode')
                self._change_mode('server')
                self._server_mode()
                timer = 0
            elif input_values['return']:
                self.log.info('Return Button was pressed')
                timer = 0
            time.sleep(1)
            timer = timer + 1
        self.display.turn_off_all()

    def _server_mode(self):
        
        self.display.turn_off_all()
        self.display.show_server_text()
        self.server.activate()
        self.server.wait_for_connection()
        
        # start a microdot webserver
        self.webserver.start()

        self.server.deactivate()
        self._change_mode('clock')
        self.log.info('Clock mode')

    def _start_sequence(self):
        try:
            self.log.info("Try to get the time-signal by internet")
            self.client.activate()
            self.client.search_wlan()
            self.client.connect()
            # networking.print_ip_infos()
            self._set_rtc_by_internet()
            self.client.disconnect()
            self.client.deactivate()
        except networking.ConnectionError as e:
            self.log.error(e)
            try:
                self.log.info("Try to get the time-signal by dcf77-signal")
                raise dcf_77.DeviceConnectionError("DCF77-Receiver is not connected to the device")
            except dcf_77.DeviceConnectionError as e:
                self.log.error(e)
                self.log.info('Server mode')
                # start here the microdot-server to set the time and other settings
                self._change_mode('server')

    def start(self):
        self._start_sequence()
        while True:
            try:
                if self.mode['menu']:
                    self._menu_mode()
                elif self.mode['clock']:
                    self._clock_mode()
                elif self.mode['server']:
                    self._server_mode()

                # Look for Button presses
                input_values = self.hw_inputs.get_values()
                if input_values['menu']:
                    self.log.debug('Menu Button was pressed')
                    self.log.info('Menu mode')
                    self._change_mode('menu')

            except KeyboardInterrupt as e:
                print(e)
                self.display.turn_off_all()
                break


def test_all_pixel(np, loop=True):
    while True:
        input('einschalten')
        for i in range(0, np.n):
            np[i] = (255, 255, 255)
        time.sleep(0.5)
        np.write()

        input('ausschalten')
        for i in range(0, np.n):
            np[i] = (0, 0, 0)
        time.sleep(0.5)
        np.write()
        if not loop:
            break


def thread_test_func(delay, exit, test_var):
    loops = 0
    while True:
        if exit:
            _thread.exit()
        print("hello from thread id:", _thread.get_ident())
        print(test_var, _thread.get_ident())
        time.sleep(delay)
        loops = loops + 1
        test_var = "it works!"


def main():
    log = logging.Logger(log_level=logging.DEBUG)
    memory = Memory(log)
    memory.clean_ram()
    clock = EspClock(log, memory)
    clock.start()
    # signal_timer = Timer()
    # total_timer = Timer()
    # rtc = RTC()
    #dcf77 = dcf_77.DCF_77(Pin(1, Pin.IN), signal_timer, total_timer, log, rtc)
    #dcf77.sync_internal_clock()
    #print(rtc.datetime())

    # client = networking.Client(log)
    # client._read_stored_networks()
    
    # animation = Animation(led_number, log)
    # animation.colorful_numbers(time_per_number=0.1)
    # animation.random_flashing(duration=2)

    
if __name__ == '__main__':
    main()


