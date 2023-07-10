import signal
import time
import pygame
# consider updating to gpiozero
#  https://gpiozero.readthedocs.io/en/stable/migrating_from_rpigpio.html
import RPi.GPIO as GPIO
import ST7789
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# TODO: improvements: auto shutdown after a couple hours if not used
# TODO: improvements: don't allow another action if timer already in progress   
# TODO: customize buttons to program different times etc..
# TODO: add pause / resume button

# The buttons on Pirate Audio are connected to pins 5, 6, 16 and 24
BUTTONS = [5, 6, 16, 24]

# These correspond to buttons A, B, X and Y respectively
LABELS = ['A', 'B', 'X', 'Y']

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# setup display stuff
# https://learn.adafruit.com/adafruit-1-14-240x135-color-tft-breakout/python-usage
disp = ST7789.ST7789(
        height=240,
        width=320,
        rotation=180,
        port=0,
        cs=1,
        dc=9,
        backlight=13, # this is just the pin
        # TODO: dim backlight..
        # https://github.com/Wikinaut/pinetradio/blob/main/backlight-pwm-and-audio.py
        spi_speed_hz=60 * 1000 * 1000,
        offset_left=0,
        offset_top=0
   )


def clear_display(disp):
    '''
    just clear display,
    return updated img
    '''
    # create blank image for drawing
    img = Image.new('RGB', (disp.width, disp.height), color=(0, 0, 0))
    # create object to draw on image
    draw = ImageDraw.Draw(img)
    # draw black rectangle on img
    draw.rectangle((0, 0, disp.width, disp.height), (0, 0, 0))
    # update the display
    disp.display(img)
    
    return img, draw


def draw_text(disp, counter, font_size=90, rotation=-90):
    '''
    '''
    # convert counter to str
    counter = str(counter)

    # define font
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    # get the size of the text
    (font_width, font_height) = font.getsize(counter)
    
    img, draw = clear_display(disp)
    
    # draw the text
    draw.text(
        (disp.width // 2 - font_width // 2, disp.height // 2 - font_height // 2),
        counter,
        font=font,
        align='center',
        fill=(220, 20, 60),
    )
    # rotate text (actually entire img)
    img = img.rotate(rotation, expand=0)
    # update the display
    disp.set_backlight(1)
    disp.display(img)
    
    
# setup function to customize button time and sounds
def timer_sound(label, timer, sound):
    '''
    inputs:
    label - the button label
    timer - the time in minutes for the timer
    sound - which mp3 sound file to play
    
    returns: True
    '''
    print(f'button {label} pressed, starting timer for {round(timer/60, 2)} minutes')
    # TODO show timer on display..
    # Initialize display.
    disp.begin()
    print('display initialized')
    
    # start countdown and display seconds remaining, update every 5 seconds
    counter = timer
    draw_text(disp, counter)
    
    while counter > 0:
        counter -= 5
        pygame.time.delay(5000)
        draw_text(disp, counter)
        
    #time.sleep(timer)
    
    print(f'{round(timer/60, 2)} minutes timer finished')
    img, draw = clear_display(disp)
    
    # TODO customize this further
    sound.play()
    # turn off backlight
    disp.set_backlight(0)
    
    return True
    
    
# "handle_button" will be called every time a button is pressed
def handle_button(pin):
    '''
    inputs:
    the associated input pin
    '''
    label = LABELS[BUTTONS.index(pin)]
    #print(f'Button press detected on pin: {pin} label: {label}')
    
    sound = pygame.mixer.Sound('/home/pi/Music/bowl_2.mp3')
    
    if label == 'A':
        # setup sound
        # sound = pygame.mixer.Sound('/home/pi/Music/Gong-sound.mp3')
        # test with 15 second timer
        timer_sound(label, 15, sound)
    if label == 'B':
        # setup sound
        # sound = pygame.mixer.Sound('/home/pi/Music/bowl_1.mp3')
        # 10 min timer
        timer_sound(label, 10*60, sound)
    if label == 'X':
        # setup sound
        # sound = pygame.mixer.Sound('/home/pi/Music/bowl_1.mp3')
        # 16 min timer
        timer_sound(label, 16*60, sound)
    if label == 'Y':
        # setup sound
        # sound = pygame.mixer.Sound('/home/pi/Music/bowl_1.mp3')
        # 30 min timer
        timer_sound(label, 30*60, sound)


if __name__ == '__main__':
    
    print('starting timer script and waiting for button presses')
    # initialize things
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    
    disp.begin()
    img, draw = clear_display(disp)

    # tell user we are ready
    draw_text(disp, 'ready!', font_size=50)
    time.sleep(1)
    # turn off backlight
    disp.set_backlight(0)
    
    # Loop through out buttons and attach the "handle_button" function to each
    # We're watching the "FALLING" edge (transition from 3.3V to Ground) and
    # picking a generous bouncetime of 100ms to smooth out button presses.
    for pin in BUTTONS:
        GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=100)

    # Finally, since button handlers don't require a "while True" loop,
    # we pause the script to prevent it exiting immediately.
    signal.pause()
