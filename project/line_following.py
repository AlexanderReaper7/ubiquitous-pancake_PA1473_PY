#!/usr/bin/env pybricks-micropython
from commands import Command_Base
from robot import Robot

class Command_Line_Following(Command_Base):
    """
    follows a line of specified color
    """
    def __init__(self, end_fn: function, name="Line Follow", inside=9, outside=85, speed=100, gain=1.2):
        """
        Paramaters:
        end_fn: function that returns True if the command should end
        name: name of the command
        inside: % of luminosity inside the line
        outside: % of luminosity outside the line
        speed: driving speed of the robot in mm/s
        gain: gain of the line following controller in degrees per % of deviation from the threshold
        """
        self.end_fn = end_fn
        self.name = name
        self.inside = inside
        self.outside = outside
        self.speed = speed
        self.gain = gain
    
    def loop(self, robot):
        # Calculate the light threshold. Choose values based on your measurements.
        threshold = (self.inside + self.outside) / 2

        # Start following the line until the end_fn returns True.
        while self.end_fn() == False:

            # Calculate the deviation from the threshold.
            deviation = robot.light_sensor.reflection() - threshold

            # Calculate the turn rate.
            turn_rate = self.gain * deviation

            # Set status
            self.status = "deviation: " + str(deviation) + " turn_rate: " + str(turn_rate)

            # Set the drive base speed and turn rate.
            robot.drivebase.drive(self.speed, turn_rate)

