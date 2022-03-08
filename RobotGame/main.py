#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from robot import Robot
import sys
from threading import Thread
from time import time
from fll import FLL
# Create your objects here.
ev3 = EV3Brick()
ev3.speaker.beep()
try:
    left_motor = Motor(Port.B)
except:
    print("Problem with Port B")
    sys.exit()
    
try:
    right_motor = Motor(Port.C)
except:
    print("Problem with Port C")
    sys.exit()

try:
    front_arm = Motor(Port.A)
except:
    print("Problem with Port A")
    sys.exit()
    
try:
    back_arm = Motor(Port.D)
except:
    print("Problem with Port D")
    sys.exit()



try:
    left_color = ColorSensor(Port.S1)
except:
    print("Problem with Port 1")
    sys.exit()

try:
    right_color = ColorSensor(Port.S2)
except:
    print("Problem with Port 2")
    sys.exit()

# try:
#     gyro = GyroSensor(Port.S3)
# except:
#     print("Problem with Port 3")
#     sys.exit()
    
robot = Robot(brick=ev3, left_motor=left_motor, right_motor=right_motor, 
                left_sensor=left_color, right_sensor=right_color, 
                front_arm=front_arm, back_arm=back_arm, wheel_diameter=62.4, axle_track=100)

def wait_button():
    while Button.CENTER not in ev3.buttons.pressed():
        pass
# robot.calibrate()
# wait_button()  
start_time = time()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
############### MAIN PROGRAM SECTION - START ################
# Type here your code
fll = FLL(robot)
fll.main()
# fll.run_1() 
#robot.drive(speed=-100, mb=55, mc=50, mode="degrees", value=2000, then=Stop.BRAKE)
# R1 81 -> 75
# R2 12
# R3 7
# R4 43 -> 40
################ MAIN PROGRAM SECTION - END #################
#robot.control_motors(speed=600)
#robot.calibrate()

# 

 

# Don't change it ...
robot.stop("Brake")
ev3.screen.clear()
ev3.screen.print(str(time() - start_time))
ev3.speaker.beep(duration=1000)
wait_button()
wait(2000)

 #[.............................]








#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
###############        SAMPLES         ################
###############     DO NOT CHANGE      ################
# robot.calibrate()

# mode={"time", "angle"}
# robot.move_back_arm(speed=-30, mode="time", value=1, wait=True)

# mode={"time", "angle"}
# robot.move_front_arm(speed=10, mode="angle", value=720)

# then = {"Brake", "Hold", "Nothing"}
# robot.stop(then="BRAKE")

# robot.straight(distance=5, speed=80, brake=True)
# robot.turn(angle=90, brake=True)

# mode = {"degrees" | value > 0 (degrees), "time" | value > 0 (seconds), "line" | value = 1 or 2 (port)}
# robot.drive(speed=20, turn_rate=0, mode="line", value=2, brake=True)

# robot.forward_align()
# robot.backward_align()

# then = {"Brake", "Hold", "Nothing"}
# robot.lf_distance(port=1, speed=50, distance=150, accelerate=False, then="Brake", pid_ks=(0.7, 0.1, 0.03))
# robot.lf_cross(port=1, speed=50, min_distance=0, accelerate=False, then="Brake")
############### METHOD SAMPLES - END ################