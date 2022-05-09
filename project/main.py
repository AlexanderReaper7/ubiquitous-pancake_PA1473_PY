#!/usr/bin/env pybricks-micropython
#! pylint: disable=line-too-long

"""The robot's main program."""

import sys

import project.commands as command
import project.enviroment as env
from project.robot import Robot

CALIBRATE = False
"""should the robot execute the calibration commands?"""

# pylint: disable=missing-docstring
def test_fn(robot):
    while not robot.touch_sensor.pressed():
        color_readout = robot.light_sensor.color()
        robot.print(f"color readout: {color_readout}, mapped color: {env.from_rgb(color_readout)}")

def main():
    robot = Robot()
    command_queue = command.Queue("Main Command Queue")
    # initialize command queue
    if CALIBRATE:
        calibration_queue = command.Queue("Calibrate the motors and sensors")
        calibration_queue.append(command.CalibrateLiftAngle())
        calibration_queue.append(command.CalibrateAmbientLight())
        command_queue.append(calibration_queue)

    command_queue.append(command.Lambda(test_fn, name="Test the from_rgb function untill the touch sensor is pressed"))
    command_queue.append(command.FollowLine(lambda: robot.touch_sensor.pressed() or robot.ultrasonic_sensor.distance() < 275 or robot.light_sensor.reflection() > 95, "Follow standard line until the front touch sensor is pressed."))
    command_queue.append(command.Halt())
    command_queue.append(command.Lift())
    command_queue.append(command.Lambda(lambda: print("this is an example lambda command"), name="Print example text."))

    # print the command queue as a tree
    robot.print(command_queue.tree_str())

    # run the command queue
    command_queue.run(robot)

    return 0

if __name__ == '__main__':
    sys.exit(main())
