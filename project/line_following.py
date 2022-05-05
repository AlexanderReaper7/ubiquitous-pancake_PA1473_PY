#!/usr/bin/env pybricks-micropython
from commands import Command_Base
from robot import Robot

class Command_Line_Following(Command_Base):
    """
    follows a line of specified color
    """
    def __init__(self, end_fn: function, name="Line Follow", inside=9, outside=85, speed=100, gain=0.7):
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
    
    def run(self, robot):
        # Calculate the light threshold. Choose values based on your measurements.
        threshold = (self.inside + self.outside) / 2

        # Start following the line until the end_fn returns True.
        while self.end_fn() == False:

            # Calculate the deviation from the threshold.
            deviation = robot.light_sensor.reflection() - threshold

            # Calculate the turn rate.
            turn_rate = self.gain * deviation

            # Set status
            #self.status = f"deviation: {deviation}, turn_rate: {turn_rate}"

            # Set the drive base speed and turn rate.
            robot.drivebase.drive(self.speed, turn_rate)

class Command_exit_circle_at_color(Command_Base):
    """
    drives to a specified color
    """
    def __init__(self, color, name="Go to Color", speed=100, gain=1.7):
        """
        follow the central circle line until encontering the specified color and stop.
        Paramaters:
        color: color to go to
        name: name of the command
        speed: driving speed of the robot in mm/s
        gain: gain of the line following controller in degrees per % of deviation from the threshold
        """
        self.color = color
        self.name = name
        self.speed = speed
        self.gain = gain
    
    def run(self, robot):
#TODO: modify reflectivity of inner by the color detection of inner, exit when target color is detected
        # Calculate the light threshold. Choose values based on your measurements.
        threshold = (self.inside + self.outside) / 2

        # Start following the line until the end_fn returns True.
        while self.end_fn() == False:

            # Calculate the deviation from the threshold.
            deviation = robot.light_sensor.reflection() - threshold

            # Calculate the turn rate.
            turn_rate = self.gain * deviation

            # Set status
            #self.status = f"deviation: {deviation}, turn_rate: {turn_rate}"

            # Set the drive base speed and turn rate.
            robot.drivebase.drive(self.speed, turn_rate)
