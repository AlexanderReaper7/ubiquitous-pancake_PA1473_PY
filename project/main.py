#!/usr/bin/env pybricks-micropython
#! pylint: disable=line-too-long

"""The robot's main program."""

import sys
import commands as command
import enviroment as env
from robot import Robot
from pybricks.tools import wait

CALIBRATE = False
"""should the robot execute the calibration commands?"""

# pylint: disable=missing-docstring
def test_fn(robot: Robot):
    robot.print("first")
    wait(1000)
    robot.print("end")

def main():
    robot = Robot()
    command_queue = command.Queue("Main Command Queue")
    # initialize command queue
    if CALIBRATE:
        calibration_queue = command.Queue("Calibrate the motors and sensors")
        calibration_queue.append(command.CalibrateLiftAngle())
        calibration_queue.append(command.CalibrateAmbientLight())
        command_queue.append(calibration_queue)

    # command_queue.append(command.Lambda(test_fn, name="Test the from_rgb function untill the touch sensor is pressed"))
    # command_queue.append(command.Lambda(lambda: robot.print("this is an example lambda command"), name="Print example text."))
    # command_queue.append(command.Lambda(test_fn, name="test"))
    command_queue.append(command.ExitSpecifiedAreaInASafeManner())
    # command_queue.append(command.FollowLineWhileAvoidingCollision(lambda: robot.touch_sensor.pressed(), "Follow standard line until the front touch sensor is pressed."))
    # command_queue.append(command.Halt())
    # command_queue.append(command.Lift())

    # print the command queue as a tree
    robot.print(command_queue.tree_str())

    # run the command queue
    command_queue.run(robot)

    return 0

if __name__ == '__main__':
    sys.exit(main())
