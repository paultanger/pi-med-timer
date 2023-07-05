import signal
import time
import pygame
# consider updating to gpiozero
#  https://gpiozero.readthedocs.io/en/stable/migrating_from_rpigpio.html
import RPi.GPIO as GPIO

# The buttons on Pirate Audio are connected to pins 5, 6, 16 and 24
BUTTONS = [5, 6, 16, 24]

# These correspond to buttons A, B, X and Y respectively
LABELS = ['A', 'B', 'X', 'Y']

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# define sound object to play
pygame.init()
pygame.mixer.init()

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
    time.sleep(timer)
    print(f'{round(timer/60, 2)} minutes timer finished')
    # TODO customize this further
    sound.play()
        
    return True
    
    
# "handle_button" will be called every time a button is pressed
def handle_button(pin):
    '''
    inputs:
    the associated input pin
    '''
    label = LABELS[BUTTONS.index(pin)]
    #print(f'Button press detected on pin: {pin} label: {label}')
    
    if label == 'A':
        # setup sound
        sound = pygame.mixer.Sound('/home/pi/Music/bowl_1.mp3')
        # test with 15 second timer
        timer_sound(label, 15, sound)
    if label == 'B':
        # setup sound
        sound = pygame.mixer.Sound('/home/pi/Music/bowl_1.mp3')
        # 10 min timer
        timer_sound(label, 10*60, sound)
    if label == 'X':
        # setup sound
        sound = pygame.mixer.Sound('/home/pi/Music/bowl_1.mp3')
        # 16 min timer
        timer_sound(label, 16*60, sound)
    if label == 'Y':
        # setup sound
        sound = pygame.mixer.Sound('/home/pi/Music/bowl_1.mp3')
        # 30 min timer
        timer_sound(label, 30*60, sound)


if __name__ == '__main__':
    
    print('starting timer script and waiting for button presses')
    
    # Loop through out buttons and attach the "handle_button" function to each
    # We're watching the "FALLING" edge (transition from 3.3V to Ground) and
    # picking a generous bouncetime of 100ms to smooth out button presses.
    for pin in BUTTONS:
        GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=100)

    # Finally, since button handlers don't require a "while True" loop,
    # we pause the script to prevent it exiting immediately.
    signal.pause()
