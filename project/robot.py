#! pylint: disable=line-too-long

"""Contains the Robot class for the purpose of organising components and functions that are highly cohesive with the hardware."""

from pybricks.ev3devices import (ColorSensor, Motor, TouchSensor,
                                 UltrasonicSensor)
from pybricks.hubs import EV3Brick
from pybricks.parameters import Direction, Port, Button
from pybricks.robotics import DriveBase
from pybricks.tools import wait

#pylint: disable=too-many-instance-attributes
class Robot:
    """
    contains the initailised components and paramaters of the robot
    """
    def __init__(self):
        """
        initialize the robots components
        """
        # devices
        self.touch_sensor = TouchSensor(Port.S1)
        self.light_sensor = ColorSensor(Port.S3)
        self.ultrasonic_sensor = UltrasonicSensor(Port.S4)
        self.lift_motor = Motor(Port.A, positive_direction = Direction.CLOCKWISE, gears = [12, 36])
        self.left_motor = Motor(Port.C, positive_direction = Direction.COUNTERCLOCKWISE, gears = [12, 20] )
        self.right_motor = Motor(Port.B, positive_direction = Direction.COUNTERCLOCKWISE, gears = [12, 20])
        self.drivebase = DriveBase(self.left_motor, self.right_motor, wheel_diameter= 47, axle_track= 128)
        self.brick = EV3Brick()

        # constants/params
        self.lift_max_angle = None

    def print(self, text):
        """
        print text to the screen and terminal
        """
        print(text)
        self.brick.screen.print(text)

    def wait_for_button(self, button: Button):
        """
        wait for the user to press the button
        """
        while button not in self.brick.buttons.pressed():
            wait(10)
