import sys
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import ST7789

disp = ST7789.ST7789(
        height=240,
        width=320,
        rotation=180,
        port=0,
        cs=1,
        dc=9,
        backlight=13,
        spi_speed_hz=60 * 1000 * 1000,
        offset_left=0,
        offset_top=0
   )


def draw_text(disp, message):
    img = Image.new('RGB', (disp.width, disp.height), color=(0, 0, 0))

    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)

    size_x, size_y = draw.textsize(message, font)

    text_x = disp.width
    text_y = (disp.height - size_y) // 2

    t_start = time.time()
    
    while True:
        print('starting while loop')
        x = (time.time() - t_start) * 100
        x %= (size_x + disp.width)
        draw.rectangle((0, 0, disp.width, disp.height), (0, 0, 0))
        draw.text((int(text_x - x), text_y), message, font=font, fill=(255, 255, 255))
        disp.display(img)

if __name__ == '__main__':
    message = "Hello World! How are you today?"
    display_type = 'dhmini' # 320x240 2.0" Display HAT Mini
    
    # Initialize display.
    disp.begin()
    print('display initialized')
    
    # draw it
    draw_text(disp, message)

    
    