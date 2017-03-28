#!/usr/bin/python
from ws4py.client.threadedclient import WebSocketClient
import RPi.GPIO as GPIO
from time import sleep
from time import time
import sys
from subprocess import Popen
import sys
import select
import termios, tty
import subprocess
import picamera

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
red_led = 17
red_value = 0
green_led=22
green_value = 0
servo_out = 27
yellow_btn = 19
up = 2
down = 3
right = 17
left = 4
a = 22
b = 27
c = 23
enter = 9
esc = 7
last_ping_time = time()
#GPIO.setup(red_led,GPIO.OUT)
#GPIO.setup(green_led,GPIO.OUT)
#GPIO.setup(servo_out,GPIO.OUT)
#GPIO.setup(yellow_btn,GPIO.IN, GPIO.PUD_UP)
GPIO.setup(up,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(down,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(right,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(left,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(a,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(b,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(c,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(enter,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(esc,GPIO.IN,GPIO.PUD_UP)

#this program even uses a pwm to control a servo
#however it would make much more sense to have libraries for that
#the 
#p = GPIO.PWM(servo_out,50) #Ponemos el pin 21 en modo PWM y enviamos 50 pulsos por segundo
#GPIO.output(red_led,red_value)
menu = [1,2,3]

class EchoClient(WebSocketClient):
    
    def opened(self):
        self.send('{\"command\":\"subscribe\", \"identifier\":\"{\\\"channel\\\":\\\"MessagesChannel\\\"}\"}')


    def closed(self, code, reason):
        print(("Closed down", code, reason))
        global ws_active
        ws_active= False
        print("ws_active changed?")
        

    def received_message(self, m):
        global red_led
        global red_value
        global last_ping_time
        global yellow_btn
        last_ping_time = time()
        print("=> %d %s" % (len(m), str(m)))
        if GPIO.input(up) == False:
            print("yellow down")
            omxp = Popen(['omxplayer','/home/pi/Desktop/example.mp3'])
            
        if len(m)== 93:
            if red_value == 0:
                red_value = 1
                p.ChangeDutyCycle(4.5)
                omxp = Popen(['omxplayer','/home/pi/Desktop/lion.mp3'])
            else:
                red_value = 0
                p.ChangeDutyCycle(10.5)
            GPIO.output(red_led,red_value)
            

#this is the real program.
# might not need to open web sockets for the time being.
def navigate_menu(key):
    return 1;
def execute_menu():
    print menu;

def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    print ch
    return ch
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
    #global ws_active
    #ws_active = False
    #sleep(5)
    #p.start(7.5)
    #camera = picamera.PiCamera()
    toggle_play = False
    while True:
        sleep(0.3)
        j = get_joystick()
        #key = get_key()
        key = 'n'
        
        if j == 'b':
            #rewinds 10 seconds
            subprocess.call("mpc seek -00:00:10 ", shell=True)
        if j == 'c':
            #forwards 10 seconds
            subprocess.call("mpc seek +00:00:10", shell=True)
        if j == 'a':
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

        if key == 't':
            camera.capture('image.jpg')
            print('captured image')
        navigate_menu(key)
        execute_menu
##        sleep(5)
##        if not(ws_active):
##            ws_active = True
##            print("ws is not active")
##            try:
##                print("create echo")  
##                ws = EchoClient('wss://dataloggerodpc.herokuapp.com/cable', protocols=['http-only', 'chat'])
##                    #ws = EchoClient('ws://192.168.0.103:3000/cable', protocols=['http-only', 'chat'])
##                ws.daemon = True
##                ws.connect()
##                #ws.run_forever()
##                
##            except:
##                print("exception")
##                if isinstance(ws,EchoClient):
##                    try:
##                        ws.close()
##                    except:
##                        print('tried to closed ws. could not do it')
##                ws_active = False
##        else:
##            print('else of ws active')
##            print(time() - last_ping_time)
##            
##            if (time() - last_ping_time) > 10:
##                print('ws is destroyed, should activate again')
##                ws_active = False
##                GPIO.output(green_led,0)
##            else:
##                print("ws is active")
##                GPIO.output(green_led,1)
