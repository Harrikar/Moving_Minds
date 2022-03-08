#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile, Font

from math import pi
from PID import PID
from time import time
from threading import Thread



class Robot():
    def __init__(self, brick, left_motor, right_motor, left_sensor, right_sensor=None, 
                front_arm=None, back_arm=None, gyro=None, wheel_diameter=62.4, axle_track=150):
        self.ev3 = brick
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.front_arm = front_arm
        self.back_arm = back_arm
        self.left_color = left_sensor
        self.right_color = right_sensor 
        self.gyro = gyro
        self.wheel_diameter = wheel_diameter
        self.axle_track = axle_track
        self.ev3.speaker.set_volume(100)
        self.ev3.screen.set_font(Font(size=14))
        self.min_left = 5
        self.max_left = 67
        self.min_right = 4
        self.max_right = 74
        self.accelerate_encoder = 100
        self.drive_base = DriveBase(self.left_motor, self.right_motor, 
                                    self.wheel_diameter, self.axle_track)
        self.drive_base.stop()
        self.straight_speed = (80 * 1020/100) // 1
        self.drive_base.settings(straight_speed=self.straight_speed)
        self.first_thread = False
        self.second_thread = False
        

    def move_front_arm(self, speed=30, mode="angle", value=0, then=Stop.HOLD, wait=True):
        if self.front_arm == None:
            self.ev3.screen.print("No arm to move")
            self.ev3.speaker.beep(1000,3000)
            return
        dps = int(1500 * (speed / 100))
        if mode == "angle":
            self.front_arm.run_angle(dps, value, then, wait)
        elif mode == "time":
            self.front_arm.run_time(dps, value*1000, then, wait)

    def move_back_arm(self, speed=30, mode="angle", value=0, then=Stop.HOLD, wait=True):
        if self.back_arm == None:
            self.ev3.screen.print("No arm to move")
            self.ev3.speaker.beep(1000,3000)
            return
        dps = int(1500 * (speed / 100))
        if mode == "angle":
            self.back_arm.run_angle(dps, value, then, wait)
        elif mode == "time":
            self.back_arm.run_time(dps, value*1000, then, wait)


    def stop(self, then="Brake"):
        self.drive_base.stop()
        if then == "Hold":
            self.left_motor.hold()
            self.right_motor.hold()
        elif then == "Brake":
            self.left_motor.brake()
            self.right_motor.brake()
        
    def straight(self, distance, speed=80, brake=False):
        speed = (speed * 1020/100) // 1
        self.drive_base.reset()
        if speed != self.straight_speed:
            self.drive_base.stop()
            self.drive_base.settings(straight_speed=speed)
            self.straight_speed = speed
        self.drive_base.straight(distance * 10)
        self.drive_base.stop()
        if brake:
            self.left_motor.brake()
            self.right_motor.brake()
            wait(10)

    def turn(self, angle, brake=True):
        self.left_motor.reset_angle(0)
        self.right_motor.reset_angle(0) 
        self.drive_base.turn(angle)
        self.drive_base.stop()
        if brake:
            self.left_motor.brake()
            self.right_motor.brake()
        #print((abs(self.left_motor.angle()) + abs(self.right_motor.angle())) // 2)
        
    def pivot(self, speed=50, degrees=90, brake=True):
        speed = (speed * 1020/100) // 1
        self.left_motor.reset_angle(0)
        self.right_motor.reset_angle(0) 
        if degrees > 0:
            self.left_motor.run_angle(speed=speed, rotation_angle=degrees)
        else:
            self.right_motor.run_angle(speed=speed, rotation_angle=degrees)
        if brake:
            self.left_motor.brake()
            self.right_motor.brake()
        
    def drive(self, speed=80, turn_rate=0, mode="degrees", value=1, brake=False):
        speed = (speed * 1020/100) // 1
        self.drive_base.stop()
        self.drive_base.reset()
        self.drive_base.drive(speed, turn_rate)
        if mode == 'degrees':
            while (abs(self.left_motor.angle()) + abs(self.right_motor.angle())) / 2 < value:
                pass
        elif mode == 'time':
            start_time = time()
            while time() - start_time < value:
                pass
        elif mode == 'line':
            if value == 1:
                left_threshold = (self.min_left + 5)
                while self.left_color.reflection() > left_threshold:
                    pass
            elif value == 2:
                right_threshold = (self.min_right + 5)
                while self.right_color.reflection() > right_threshold:
                    pass
            else:
                right_threshold = (self.min_right + 5)
                left_threshold = (self.min_left + 5)
                while self.right_color.reflection() > right_threshold and \
                    self.left_color.reflection() > left_threshold:
                    pass
        if brake:
            self.drive_base.stop()
            self.left_motor.brake()
            self.right_motor.brake()
        wait(100)


    def lf_distance(self, port, speed=50, distance=0, accelerate=False, then="Nothing", pid_ks=(0.7, 0.1, 0.03), outer=False):
        pid = PID(pid_ks[0], pid_ks[1], pid_ks[2])
        pid.SetPoint = 0
        pid.setSampleTime(0.01)
        degrees = int(360 * (distance * 10 / (pi * self.wheel_diameter)))
        self.left_motor.reset_angle(0)
        self.right_motor.reset_angle(0)
        v = vmax = speed
        v0 = 30
        if port == 1:
            target = (self.min_left + self.max_left) // 2 + 10
            sensor = self.left_color
            k = 1
        else:
            target = (self.min_right + self.max_right) // 2 + 10
            sensor = self.right_color
            k = -1
        if outer:
            k *= -1
        while (self.left_motor.angle() + self.right_motor.angle()) / 2 < degrees:
            if accelerate:
                v = int((self.left_motor.angle() / self.accelerate_encoder) * (vmax - v0) + v0)
                if v > vmax:
                    v = vmax
                    accelerate = False
            reflection_error = k*(sensor.reflection() - target)
            pid.update(reflection_error)
            u = int(pid.output)
            self.left_motor.dc(v - u)
            self.right_motor.dc(v + u)
        if then == "Brake":
            self.stop("BRAKE")
        elif then == "Coast":
            self.left_motor.dc(0)
            self.right_motor.dc(0)

    def lf_cross(self, port=1, speed=50, min_distance=0, accelerate=False, then="Brake", pid_ks=(0.7, 0.1, 0.03), outer=False):
        pid = PID(pid_ks[0], pid_ks[1], pid_ks[2])
        pid.SetPoint = 0
        pid.setSampleTime(0.01)
        degrees = int(360 * (min_distance * 10 / (pi * self.wheel_diameter)))
        self.left_motor.reset_angle(0)
        self.right_motor.reset_angle(0)
        v = vmax = speed
        v0 = 30
        if port == 1:
            target = (self.min_left + self.max_left) // 2 + 10
            sensor = self.left_color
            stop_sensor = self.right_color 
            stop_target = self.min_right + 8
            k = 1
        else:
            target = (self.min_right + self.max_right) // 2 + 10
            stop_sensor = self.left_color 
            sensor = self.right_color
            stop_target = self.min_left + 8
            k = -1
        if outer:
            k *= -1
        while (self.left_motor.angle() + self.right_motor.angle()) / 2 < degrees or \
                stop_sensor.reflection() > stop_target:
            if accelerate:
                v = int((self.left_motor.angle() / self.accelerate_encoder) * (vmax - v0) + v0)
                if v > vmax:
                    v = vmax
                    accelerate = False
            reflection_error = k*(sensor.reflection() - target)
            pid.update(reflection_error)
            u = int(pid.output)
            self.left_motor.dc(v - u)
            self.right_motor.dc(v + u)
        if then == "Brake":
            self.stop("BRAKE")
        elif then == "Coast":
            self.left_motor.dc(0)
            self.right_motor.dc(0)
    
    def calibrate(self):
        self.ev3.screen.clear()
        self.ev3.screen.print("press center to")
        self.ev3.screen.print("calibrate colors")
        while Button.CENTER not in self.ev3.buttons.pressed():
            wait(10)
        min_left = 100
        max_left = 0
        min_right = 100
        max_right = 0
        while Button.DOWN not in self.ev3.buttons.pressed():
            left_value = self.left_color.reflection()
            right_value = self.right_color.reflection()
            if left_value < min_left:
                min_left = left_value
            if left_value > max_left:
                max_left = left_value
            if right_value < min_right:
                min_right = right_value
            if right_value > max_right:
                max_right = right_value
            self.ev3.screen.clear()
            self.ev3.screen.print()
            self.ev3.screen.print("Left: " + str(left_value))
            self.ev3.screen.print("Right: " + str(right_value))
            self.ev3.screen.print("Down to stop")
            wait(40)
        self.ev3.screen.clear()
        self.ev3.screen.print()
        self.ev3.screen.print()
        self.ev3.screen.print("Min Left: " + str(min_left))
        self.ev3.screen.print("Max Left: " + str(max_left))
        self.ev3.screen.print("Min Right: " + str(min_right))
        self.ev3.screen.print("Max Right: " + str(max_right))
        self.ev3.screen.print("Center to exit")
        while Button.CENTER not in self.ev3.buttons.pressed():            
            wait(50)
        self.min_left = min_left
        self.max_left = max_left
        self.min_right = min_right
        self.max_right = max_right

    def forward_align(self):
        self.drive_base.stop()
        t1 = Thread(target=self.left_line_thread, args=(200, self.left_motor, self.min_left + 5, 
                    (self.max_left + self.min_left) // 2, self.left_color))
        t2 = Thread(target=self.right_line_thread, args=(200, self.right_motor, self.min_right + 5, 
                    (self.max_right + self.min_right) // 2, self.right_color))
        self.first_thread = False
        self.second_thread = False
        t1.start()
        t2.start()
        while self.first_thread == False or  self.second_thread == False:
            pass
        self.pid_align(forward=True)

    def left_line_thread(self, dps, motor, min_threshold, max_threshold, color_sensor):
        self.first_thread = False
        motor.run(dps)
        is_stop = False
        while color_sensor.reflection() > min_threshold:
            pass
        motor.run(-dps // 2)
        while color_sensor.reflection() < max_threshold:
            pass
        motor.brake()
        self.first_thread = True

    def right_line_thread(self, dps, motor, min_threshold, max_threshold, color_sensor):
        self.second_thread = False
        motor.run(dps)
        is_stop = False
        while color_sensor.reflection() > min_threshold:
            pass
        motor.run(-dps // 2)
        while color_sensor.reflection() < max_threshold:
            pass
        motor.brake()
        self.second_thread = True


    def backward_align(self):
        self.drive_base.stop()
        t1 = Thread(target=self.left_line_thread, args=(-200, self.left_motor, self.min_left + 5, 
                    (self.max_left + self.min_left) // 2, self.left_color))
        t2 = Thread(target=self.right_line_thread, args=(-200, self.right_motor, self.min_right + 5, 
                    (self.max_right + self.min_right) // 2, self.right_color))
        self.first_thread = False
        self.second_thread = False
        t1.start()
        t2.start()
        while self.first_thread == False or  self.second_thread == False:
            pass
        self.pid_align(forward=False)

    def pid_align(self, forward=True, dur=0.2, pid_ks=(1, 0.1, 0.03)):
        left_thread = Thread(target=self.left_align, args=(forward, dur, pid_ks))
        right_thread = Thread(target=self.right_align, args=(forward, dur, pid_ks))
        self.first_thread = False
        self.second_thread = False
        left_thread.start()
        right_thread.start()
        while self.first_thread == False or  self.second_thread == False:
            pass


    def left_align(self, forward=True, dur=5, pid_ks=(5, 0, 0)):
        self.first_thread = False
        pid = PID(pid_ks[0], pid_ks[1], pid_ks[2])
        pid.SetPoint = 0
        pid.setSampleTime(0.01)
        start_time = time()
        left_threshold = (self.min_left + self.max_left) // 2
        k = 1
        if forward:
            k = -1
        while time() - start_time < dur:
            left_reflection_error = self.left_color.reflection() - left_threshold
            pid.update(left_reflection_error)
            left_u = int(pid.output)
            self.left_motor.run(k * left_u)

        self.left_motor.brake()
        self.first_thread = True


    def right_align(self, forward=True, dur=5, pid_ks=(0.6, 0.1, 0.02)):
        self.second_thread = False
        pid = PID(pid_ks[0], pid_ks[1], pid_ks[2])
        pid.SetPoint = 0
        pid.setSampleTime(0.01)
        start_time = time()
        right_threshold = (self.min_right + self.max_right) // 2
        k = 1
        if forward:
            k = -1
        while time() - start_time < dur:
            right_reflection_error = self.right_color.reflection() - right_threshold
            pid.update(right_reflection_error)
            right_u = int(pid.output)
            self.right_motor.run(k * right_u)
        self.right_motor.brake()
        self.second_thread = True

    def control_motors(self, speed=600):
        self.ev3.screen.clear()
        self.ev3.screen.print("Front -> UP")
        self.ev3.screen.print("Back -> DOWN")
        motor = self.front_arm
        while True:
            if Button.DOWN in self.ev3.buttons.pressed():
                motor = self.back_arm
                break
            if Button.UP in self.ev3.buttons.pressed():
                motor = self.front_arm
                break
        self.ev3.speaker.beep()
        self.ev3.screen.clear()
        self.ev3.screen.print("Left - Right")
        self.ev3.screen.print("buttons to move")
        self.ev3.screen.print("Center to exit")
        while True:
            if Button.LEFT in self.ev3.buttons.pressed():
                motor.run(speed)
            elif Button.RIGHT in self.ev3.buttons.pressed():
                motor.run(-speed)
            elif Button.CENTER in self.ev3.buttons.pressed():
                motor.stop()
                break
            else:
                motor.stop()
        self.ev3.speaker.beep()
  
        