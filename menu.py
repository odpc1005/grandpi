#!/usr/bin/python
#from ws4py.client.threadedclient import WebSocketClient
import RPi.GPIO as GPIO
from time import sleep
from time import time
import sys
from subprocess import Popen
import sys
import select
import termios, tty
import subprocess
#import picamera

#GPIO Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
#Output setup
#red_led = 17

#Input setup
up = 2
down = 3
right = 17
left = 4
a = 22
b = 27
c = 23
enter = 9
esc = 7

GPIO.setup(up,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(down,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(right,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(left,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(a,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(b,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(c,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(enter,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(esc,GPIO.IN,GPIO.PUD_UP)

# menu state machine. work in progress
menu = [1,2,3]

def navigate_menu(key):
    return 1;
def execute_menu():
    print menu;

def get_joystick():
    global up
    j = ''
    
    if GPIO.input(up) == False:
        print("get joystick up")
        j= 'u'
    if GPIO.input(down) == False:
        print("get joystick down")
        j= 'd'
    if GPIO.input(right) == False:
        print("get joystick right")
        j= 'r'
    if GPIO.input(left) == False:
        print("get joystick left")
        j= 'l'
    if GPIO.input(a) == False:
        print("get joystick a")
        j= 'a'
    if GPIO.input(b) == False:
        print("get joystick b")
        j= 'b'
    if GPIO.input(c) == False:
        print("get joystick c")
        j= 'c'
    if GPIO.input(enter) == False:
        print("get joystick enter")
        j= 'e'
    if GPIO.input(esc) == False:
        print("get joystick esc")
        j= 's'
        
    return j    

if __name__ == '__main__':   
    #initial setup before the loop.
    while True:
        sleep(0.2)
        j = get_joystick()
        
        if j == 'b':
            #rewinds 10 seconds
            subprocess.call("mpc seek -00:00:10 ", shell=True)
        if j == 'c':
            #forwards 10 seconds
            subprocess.call("mpc seek +00:00:10", shell=True)
        if j == 'a':
            #toggle between play and pause
            subprocess.call("mpc toggle ", shell=True)        
        if j == 'u':
            subprocess.call("mpc volume +2",shell=True)
        if j == 'd':
            subprocess.call("mpc volume -2",shell=True)
        if j == 'r':
            subprocess.call("mpc next",shell=True)
        if j == 'l':
            subprocess.call("mpc prev",shell=True)
        
        if j == 'e':
            #this is enter
            subprocess.call("mpc clear", shell=True)
            subprocess.call("mpc ls | grep 'documentaries' | sort | mpc add", shell=True)
            subprocess.call("mpc update --wait",shell=True)
        if j == 's':
            #this is esc
            subprocess.call("mpc clear", shell=True)
            subprocess.call("mpc ls | grep 'songs' | sort | mpc add", shell=True)
            subprocess.call("mpc update --wait",shell=True)
            
        navigate_menu(key)
        execute_menu
