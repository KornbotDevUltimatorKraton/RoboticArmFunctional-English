#Author: Mr. Chanapai Chuadchum 
#Project Name : Robotic Arm VX-S
#Describe: This project is for official Robotic arm controller function software 
#!/usr/bin/env python2 
import numpy as np # Numpy math function 
import pyaudio  # mp3 player 
import wave   # Wave audio output library 
from nanpy import(ArduinoApi,SerialManager) # Serial Manager  And arduino API function for the hardware communication 
import scipy 
import pyttsx # Speech engine function for the robotic arm 
import os  #  Misselenius Operating system function for the robotic arm recall the python function 
import sys # System  
import serial # Serial function normal function for communicate with the feed back angle 
import math # Mathematic for calculation function on the system 
import matplotlib.pyplot as plt # Mat plot for graph plot in the realtime tracking angle 
import microgear.client as microgear # Internet of Thing function  for the system of the robotic arm 
import time # time sleep funcion for the timing control 
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
           # Kivy GUI function 
from kivy.app import App # import the kivy gui function of the system 
from kivy.clock import Clock 
from kivy.core.window import Window
from kivy.resources import resource_find
#from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import*
from kivy.graphics import*
#from objloader import ObjFileLoader
from kivy.logger import Logger
#from rotation import SingleRotate
from kivy.uix.widget import Widget
from kivy.uix.label import Label 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput 

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
       #Tkinter GUI 
import Tkinter 
import Tkinter as tk 
import ttk 
from Tkinter import* # Import Tkinter to display the window option control mannual 
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
       #Intro openning speech of the arm 
engine = pyttsx.init() # Openning the speech function of the arm 
engine.setProperty('rate',140) #rate of the speech function system functionallize 
engine.say("Roboic Arm version VX-S now operating") # Say intro speech function of the robotic arm 
engine.runAndWait() # System run and wait for the run 
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   # Base serial connection 
try: #Base connection function  
    connectionBase = SerialManager('/dev/ttyACM0',115200) # Serial connection function for the  base joint 
    base = ArduinoApi(connection=connectionBase) # Connection base estrablished
except: 
    print("Serial Base error please reconnect again")
    engine.say("Serial base error please recheck the serial connection")
    engine.runAndWait() 
# Shouder serial connection 
try: #Shoudler connection function  
    connectionShoulder = SerialManager('/dev/ttyACM1',115200) # Seri$
    Shoulder = ArduinoApi(connection=connectionShoulder) # Connection base $
except: 
    print("Serial Shoulder error please reconnect again")
    engine.say("Serial Shoulder error please recheck the serial connect")
    engine.runAndWait() 
# Elbow serial connection 
try: #Elbow connection function  
    connectionElbow = SerialManager('/dev/ttyACM2',115200) # Seri$
    Elbow = ArduinoApi(connection=connectionElbow) # Connection base $
except: 
    print("Serial Elbow error please reconnect again")
    engine.say("Serial Elbow error please recheck the serial connect")
    engine.runAndWait() 
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
              # Hand part connection function 
  #Wrist Rotator Y
try:  # Wrist rotate y  function 
   connectionWristRotateY = SerialManager('/dev/ttyACM3',115200) 
   WristRotationY = ArduinoApi(connection=connectionWristRotateY) 
except: 
    print("Serial WristRotate Y serial error please check function")
    engine.say("Serial Wrist Rotate y serial error please reconnect")
    engine.runAndWait() 
  #Wrist Rotator X 
try: # Wrist rotate x function 
   connectionWristRotateX = SerialManager('/dev/ttyACM4',115200) 
   WristRotationX = ArduinoApi(connection=connectionWristRotateX) 
except: 
   print("Serial WristRotate X serial error please check function")
   engine.say("Serial Write Rotate X serial error please reconnect")
   engine.runAndWait() 
  #Wrist Hand control 
try: # Hand rotate 
   connectionHand = SerialManager('/dev/ttyACM5',115200) 
   Hand = ArduinoApi(connection=connectionHand) 
except: 
   print("Serial Hand connection error please check serial connection")
   engine.say("Serial Hand error please check function")
   engine.runAndWait()  
   # Runing the command to be ready to recieve the command from the IoT function
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Joint motor function controller 
        #! These Actuator working continues like the normal motor but control pid by the  imu outside 
def BaseActuator(dir,Step,speed):  # DigitalControl onoff function for the controller
    base.digitalWrite(2,dir) 
    for movebase in range(0,Step): 
        base.digitalWrite(3,base.HIGH)
        time.sleep(speed) 
        base.digitalWrite(3,base.LOW) 
        print("Base step"+movebase)
def ShoulderActuator(dir,Step,Speed): 
    Shoulder.digitalWrite(4,dir) 
    for moveShoulder in range(0,Step): 
        Shoulder.digitalWrite(5,Shoulder.HIGH) 
        time.sleep(Speed) 
        Shoulder.digitalWrite(5,Shoulder.LOW)
        print("Shoulder step"+moveShoulder) # 
def ElbowActuator(dir,Step,Speed): 
    Elbow.digitalWrite(6,dir) 
    for moveElbow in range(0,Step): 
        Elbow.digitalWrite(7,Elbow.HIGH)  
        time.sleep(Speed) 
        Elbow.digitalWrite(7,Elbow.LOW)
        print("Elbow"+moveElbow)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
         #Upper body wrist hand and finger function 
def WristRotationYActuator(dir,Step,Speed):  # Wrist Rotation Y 
    WristRotationY.digitalWrite(2,dir) 
    for moveWRY in range(0,Step): 
         WristRotationY.digitalWrite(3,WristRotationY.HIGH)     
         time.sleep(Speed) 
         WristRotationY.digitalWrite(3,WristRotationY.LOW)
         print("Wrist Y step"+ moveWRY) 
def WristRotationXActuator(dir,Step,Speed): #Wrist Rotation X 
    WristRotationX.digitalWrite(2,dir)  
    for moveWRX in range(0,Step): 
        WristRotationX.digitalWrite(3,Hand.HIGH)
        time.sleep(Speed) 
        WristRotationX.digitalWrite(3,Hand.LOW) 
        print("Wrist X step"+ moveWRX)
    # Arduino Mega for sensding the analogValue function of the robotic hand  
def WristRotationActuator(dir,Step,Speed): #Wrist Rotation  on the hand function  
    Hand.digitalWrite(2,dir) 
    for moveWR in range(0,Step):
      Hand.digitalWrite(3,Hand.HIGH) 
      time.sleep(Speed) 
      Hand.digitalWrite(3,Hand.HIGH) 
      print("Wrist Rotation Step"+moveWR)
def Finger2US(dir,Step,Speed): 
    Hand.digitalWrite(5,dir) 
    for moveF2 in range(0,Step):
       Hand.digitalWrite(6,Hand.HIGH) 
       time.sleep(Speed) 
       Hand.digitalWrite(6,Hand.LOW)       
       print("Finger step"+moveF2)
def Finger3US(dir,Step,Speed):
    Hand.digitalWrite(8,dir) 
    for moveF3 in range(0,Step):
       Hand.digitalWrite(9,Hand.HIGH) 
       time.sleep(Speed) 
       Hand.digitalWrite(9,Hand.LOW)
       print("moveF3"+moveF3)
    # Finger function servo actuator and feed back real time feedback function # using another microcontroller to generate the pwm from the analog write out function 
def Finger1Actuator(AngleFinger1):
    Hand.analogWrite(43,AngleFinger1)
def Finger2Actuator(AngleFinger2): 
    Hand.analogWrite(44,AngleFinger2) 
def Finger3Actuator(AngleFinger3): 
    Hand.analogWrite(45,AngleFinger3) 
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
       #Manual mode controller 
def BaseApproach(event): 
     BasePID(b.get(),b.get()) # Get angle to calculate in the system 
     print(b.get())   # Printing the output value for the robotic arm 
def ShoulderApproach(event): # Get angle to calculate the angle function of the hight from the ground 
    ShoulderPID(s.get(),s.get()) 
    print(s.get())
def ElbowApproach(event):    #Get  angle to calculate in the system 
    ElbowPID(e.get(),e.get())  
    print(e.get())
def WristYApproach(event):
    WristYPID(wy.get(),wy.get())
    print(wy.get())  
def WristXApproach(event):
    WristXPID(wx.get(),wx.get())
    print(wx.get()) # Printout the wx wrist x value anglec control from slider 
def WristApproach(event): 
    WristPID(w.get(),w.get())
    print(w.get()) 

def Finger1Approach(event): 
    Finger1Actuator(F1.get()) # Getting the value from the  slider 
    print(F1.get())  # Finger 1 value print out function

def Finger2Approach(event): 
    Finger1Actuator(F2.get()) # Finger2 value out function 
    print(F2.get())

def Finger3Approach(event):
    Finger2Actuator(F3.get()) # Finger3 value out function 
    print(F3.get())  
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
       #PID control  with IMU actuator stepper motor control
def BasePID(setpoint,AngleBase): 
    if AngleBase > setpoint:
       base.digitalWrite(4,base.HIGH) 
       BaseActuator(1,450,0.002)

    if AngleBase == setpoint: 
       base.digitalWrite(4,base.LOW) # Turn off the function of the base 

    if AngleBase < setpoint: 
       base.digitalWrite(4,base.HIGH)
       BaseActuator(0,450,0.002)        
def ShoulderPID(setpoint,AngleShoulder):
  if AngleShoulder > setpoint:
     Shoulder.digitalWrite(4,Shoulder.HIGH)
     ShoulderActuator(1,450,0.002)
   
  if AngleShoulder == setpoint: 
     Shoulder.digitalWrite(4,Shoulder.LOW)

  if AngleShoulder < setpoint: 
     Shoulder.digitalWrite(4,Shoulder.HIGH) 
     ShoulderActuator(0,450,0.002) 
def ElbowPID(setpoint,AngleElbow): 
  if AngleElbow > setpoint: 
     Elbow.digitalWrite(4,Elbow.HIGH)
     ElbowActuator(1,450,0.002) 

  if AngleElbow == setpoint: 
     Elbow.digitalWrite(4,Elbow.LOW) 

  if AngleElbow < setpoint: 
     Elbow.digitalWrite(4,Elbow.HIGH)
     ElbowActuator(0,450,0.002)
def WristYPID(setpoint,AngleWristY): 
     if AngleWristY > setpoint:
        WristRotationY.digitalWrite(4,WristRotationY.HIGH)
        WristRotationYActuator(1,450,0.002) 
     if AngleWristY == setpoint: 
        WristRotationY.digitalWrite(4,WristRotationY.LOW) 
     if AngleWristY < setpoint: 
        WristRotationY.digitalWrite(4,WristRotationY.HIGH) 
        WristRotationYActuator(0,450,0.002)   
def WristXPID(setpoint,AngleWristX): 
    if AngleWristX > setpoint:
       WristRotationX.digitalWrite(4,WristRotationX.HIGH)
       WristRotationXActuator(1,450,0.002)
    if AngleWristX == setpoint: 
       WristRotationX.digitalWrite(4,WristRotationX.LOW) 
    if AngleWristX < setpoint: 
       WristRotationX.digitalWrite(4,WristRotationX.HIGH) 
       WristRotationXActuator(0,450,0.002)  
     
def WristPID(setpoint,AngleWristRotate):
    if AngleWristRotate > setpoint: 
        Hand.digitalWrite(4,Hand.HIGH)
        WristRotationActuator(1,450,0.002)
    if AngleWristRotate == setpoint: 
        Hand.digitalWrite(4,Hand.LOW)

    if AngleWristRotate < setpoint:
        Hand.digitalWrite(4,Hand.HIGH) 
        WristRotationActuator(0,450,0.002)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
       # Kinematic function for the Arm controller (X,Y,Z) Euler frame 
def Kinmaticinput(l1,l2,Baseheight,x,y,z,AngleBase,AngleShoulder,AngleElbow,AngleWristRotatey,AngleWristRotatex,AngleWristRotate,Finger1feed,Finger2feed,Finger3feed):   # Input the 3 parameters axis to the sistem 
    # Joint manipulator control
    BasePID(math.degrees(math.atan(y/x)),AngleBase) # Base Variable all input 
    ShoulderPID(math.degrees(math.asin(z+Baseheight/l1)),AngleShoulder) #Shoulder Variable all input 
    ElbowPID(math.degrees(math.acos(((math.pow(l1,2) + math.pow(l2,2))-(math.pow(x,2)+ math.pow(y,2)))/2*l1*l2)),AngleElbow)  #Elbow Angle calculation functoin 
    WristYPID((180-((math.degrees(math.asin(z+Baseheight/l1))+(math.degrees(math.acos(((math.pow(l1,2) + math.pow(l2,2))-(math.pow(x,2)+ math.pow(y,2)))/2*l1*l2)))))),AngleWristRotatey)
    
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class IntroScreen(GridLayout): 
   def __init__(self,**kwargs): 
        super(IntroScreen,self).__init__(**kwargs)
        self.cols = 2 

        self.add_widget(Label(text="Welcome to Robotic arm VX-S"))  
        self.username = TextInput(multiline=False) 
        self.add_widget(self.username) 

          # Kivy GUI operating screen user interface 
class RoboticArm(App): 
    pass 
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
if __name__=="__main__":
    RoboticArm().run() 
      # Looping iteration recieving and sending the command
while(True):
      Master = Tkinter.Tk() # Tkinter window initiated when Trigger window working 
      Master.title("Robotic arm control function ")
      Master.geometry('380x750')
      Label1 = Label(Master,text = "Base Angle",fg = 'blue',font=("Helvtical",11))
      Label1.pack() 
      #2d = Scale(Master,from_= 0,to=180,orient=HORIZONTAL,command=BaseApproach)
      #2d.set(0) 
      #2d.pack()
      #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Base Horizontal function 
      b = Scale(Master, from_=0, to=180, orient=HORIZONTAL,command=BaseApproach)
      b.set(90)
      b.pack()
      Label2 = Label(Master,text = "Shoulder Angle",fg ='blue',font=("Helvetical",11)) 
      Label2.pack()    
              #Shoulder HorizontalFunction 
      s = Scale(Master, from_=0, to=180, orient=HORIZONTAL,command=ShoulderApproach) 
      s.set(90) 
      s.pack() 
      Label3 = Label(Master,text = "Elbow Angle ",fg ='blue',font=("Helvetical",11))
      Label3.pack()
                 #Elbow  HorizontalFunction 
      e = Scale(Master,from_=0, to=180, orient=HORIZONTAL,command=ElbowApproach) 
      e.set(90)
      e.pack() 
      Label4 = Label(Master,text = "Wrist Y Angle",fg ='blue',font=('Helvetical',11)) 
      Label4.pack() 
                #WristY HorizontalFunction 
      wy = Scale(Master,from_=0 ,to=180, orient=HORIZONTAL,command=WristYApproach)
      wy.set(90) 
      wy.pack()
                #WristX HorizontalFunction 
      wx = Scale(Master,from_=0, to=180, orient=HORIZONTAL,command=WristXApproach)
      wx.set(90)
      wx.pack()
                #Wrist HorizontalFuncton 
      w = Scale(Master,from_=0, to=180, orient=HORIZONTAL,command=WristApproach) 
      w.set(90)
      w.pack()
                #Finger1 HorizontalFunction 
      F1 = Scale(Master,from_=0, to=180, orient=HORIZONTAL,command=Finger1Approach)
      F1.set(90)
      F1.pack() 
      
      F2 = Scale(Master,from_=0, to=180, orient=HORIZONTAL,command=Finger2Approach)
      F2.set(90)
      F2.pack() 

      F3 = Scale(Master,from_=0, to=180, orient=HORIZONTAL,command=Finger3Approach)
      F3.set(90)
      F3.pack() 
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 
      Master.mainloop()
      AngleBase  = base.analogRead(0) 
      AngleShoulder = Shoulder.analogRead(1) 
      AngleElbow = Elbow.analogRead(2) 
      AngleWristRotatey = WristRotationY.analogRead(3) 
      AngleWristRotatex = WristRotationX.analogRead(4)
      #Hand parts function control  
      AngleWrist = Hand.analogRead(5)  # Wrist at the hand to rotate around 
      AngleHand = Hand.analogRead(6)   
      #Finger function for the Robotic hand controller   
      Finger1feed = Hand.analogRead(7) # Finger function for the force sensor feeb$
      Finger2feed = Hand.analogRead(8)  
      Finger3feed = Hand.analogRead(9)
      
      Kinmaticinput(34,34,20,10,10,10,AngleBase,AngleShoulder,AngleElbow,AngleWristRotatey,AngleWristRotatex,AngleWrist,Finger1feed,Finger2feed,Finger3feed) 
      print(AngleBase,AngleShoulder,AngleElbow,AngleWristRotatey,AngleWristRotatex,AngleWrist,AngleHand,Finger1feed,Finger2feed,Finger3feed) # Angle feed back from the body sensors translator 
      #Master.mainloop() 
 

