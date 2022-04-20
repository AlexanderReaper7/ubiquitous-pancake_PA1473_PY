#!/usr/bin/env pybricks-micropython
import sys
import __init__
from commands import Command_Queue, Command_Halt, Command_Lambda
from line_following import Command_Line_Following
from robot import Robot

from pybricks.ev3devices import Motor, ColorSensor, TouchSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait
from pybricks.robotics import DriveBase

robot = Robot()
command_queue = Command_Queue("Main Command Queue")

def main():
    # initialize command queue
    command_queue.append(Command_Line_Following(lambda: robot.touch_sensor.pressed(), "Follow standard line until the front touch sensor is pressed."))
    command_queue.append(Command_Halt())
    command_queue.append(Command_Lambda(lambda: print("this is an example lambda command"), name="Print example text."))
    nested_command_queue = Command_Queue("Nested Command Queue")
    nested_command_queue.append(Command_Lambda(lambda: print("this is an example of a nested command queue"), name="Print example of nested command queue."))
    command_queue.append(nested_command_queue)

    # print the command queue as a tree
    command_queue.tree()

    # run the command queue
    command_queue.run(robot)

    return 0

if __name__ == '__main__':
    sys.exit(main())