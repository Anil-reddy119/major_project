cmd_beg = 'espeak '
cmd_end = ' | aplay /home/pi/Desktop/Delivery Box/speach.wav 2>/dev/null'
cmd_out = '--stdout > /home/pi/Desktop/Delivery Box/speach.wav '

import RPi.GPIO as GPIO
import time

# initialize door setup
door = 3
servo = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(door, GPIO.OUT)

# initialize servo

GPIO.setup(servo, GPIO.OUT)
pwm = GPIO.PWM(servo, 50)
pwm.start(2.5)

def SetAngle(angle):
    duty = angle / 18
    GPIO.output(servo, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)

SetAngle(60)



from subprocess import call

def speakout(message):
    print("text to speech message")
    #message.replace(' ', '_')
    call([cmd_beg +'"'+message +'"'], shell = True)
    
def open_door():
    
    print("opening door")
    GPIO.output(door, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(door, GPIO.LOW)
    time.sleep(0.7)
    print("door opened")

def open_box():
    print("opening box for delivery")
    
    SetAngle(150)
    time.sleep(7)
    #ir code
    SetAngle(60)
    print("box closed")
    
    
if _name=="__main_":
    """while True:
        input("press enter to open box")
        open_box()
        print("one cycle")"""
    
    while True:
        pwm.ChangeDutyCycle(5)
        time.sleep(60)
        pwm.ChangeDutyCycle(10)
        time.sleep(10)

        #input("press again to close box")