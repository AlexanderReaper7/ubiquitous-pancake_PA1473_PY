#!/usr/bin/env pybricks-micropython
import sys
import __init__
import enviroment
from commands import *
from line_following import Command_Line_Following
from robot import Robot

from pybricks.ev3devices import Motor, ColorSensor, TouchSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait
from pybricks.robotics import DriveBase

robot = Robot()
command_queue = Command_Queue("Main Command Queue")

def test_fn(robot):
    while robot.touch_sensor.pressed() == False:
        r, g, b = robot.light_sensor.color()
        robot.print(f"color readout: {color_readout}, mapped color: {enviroment.from_rgb(color_readout)}")

CALIBRATE = False

def main():
    # initialize command queue
    if CALIBRATE:
        calibration_queue = Command_Queue("Calibrate the motors and sensors")
        calibration_queue.append(Command_Calibrate_Lift_Angle())
        calibration_queue.append(Command_Calibrate_Ambient_Light())
        command_queue.append(calibration_queue)
    
    command_queue.append(Command_Lambda(test_fn, name="Test the from_rgb function untill the touch sensor is pressed"))
    command_queue.append(Command_Line_Following(lambda: robot.touch_sensor.pressed() or robot.ultrasonic_sensor.distance() < 275 or robot.light_sensor.reflection() > 95, "Follow standard line until the front touch sensor is pressed."))
    command_queue.append(Command_Halt())
    command_queue.append(Command_Lift())
    command_queue.append(Command_Lambda(lambda: print("this is an example lambda command"), name="Print example text."))

    # print the command queue as a tree
    robot.print(command_queue.tree_str())

    # run the command queue
    command_queue.run(robot)

    return 0

if __name__ == '__main__':
    sys.exit(main())