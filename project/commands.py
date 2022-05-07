#!/usr/bin/env pybricks-micropython
#! pylint: disable=line-too-long
#! pylint: disable=too-few-public-methods

"""Collection of commands for the robot."""

from collections import deque

from pybricks.parameters import Stop, Button
from pybricks.tools import wait

from project.robot import Robot
import project.enviroment as env

class Base:
    """
    A unifying interface for all commands
    """
    def __init__(self, name="Command_Base"):
        self.name = name

    def run(self, robot: Robot):
        """run the command"""
        raise NotImplementedError

    def __str__(self):
        """return the name of the command"""
        return self.name

class Queue(deque):
    """
    A first-in first-out queue of commands
    """
    def __init__(self, name="Command_Queue"):
        super().__init__()
        self.name = name

    def run(self, robot: Robot):
        """Runs the commands in order removing them from the queue"""
        while len(self) > 0:
            self.popleft().run(robot)

    def tree(self, indent=0):
        """prints the command queue as a tree"""
        print("\t" * (indent) + self.name + ": ")
        for command in self:
            if isinstance(command, Queue):
                command.tree(indent=indent+1)
            else:
                print("\t" * (indent + 1) + str(command))

    def tree_str(self, indent=0):
        """returns the command queue as a tree"""
        output = "\t" * (indent) + self.name + ": \n"
        for command in self:
            if isinstance(command, Queue):
                output += command.tree_str(indent=indent+1)
            else:
                output += "\t" * (indent + 1) + str(command) + "\n"
        return output

class Halt(Base):
    """
    stops the robot
    """
    def __init__(self, name="Command_Halt"):
        super().__init__(name=name)

    def run(self, robot: Robot):
        robot.drivebase.stop()

class Lambda(Base):
    """
    A command that runs a lambda function
    """
    def __init__(self, fn, name="Lambda"):
        super().__init__(name=name)
        # pylint: disable=invalid-name
        self.fn = fn

    def run(self, robot: Robot):
        self.fn(robot)

class Lift(Base): #TODO: add doc string
    def __init__(self, name="Lift", speed = 50, duty_limit = 100):
        super().__init__(name=name)
        self.speed = speed
        self.duty_limit = duty_limit

    def run(self, robot: Robot):
        loops = 0
        if robot.touch_sensor.pressed():
            robot.lift_motor.run_until_stalled(self.speed, then=Stop.HOLD, duty_limit=self.duty_limit)
            wait(100)
            robot.drivebase.straight(-200)
            robot.lift_motor.run_target(-1*self.speed, 50, then=Stop.HOLD, wait=True)
            # robot.drivebase.straight(100)
            # robot.lift_motor.run_until_stalled(-1*self.speed, then=Stop.HOLD, duty_limit=self.duty_limit)
        elif robot.light_sensor.reflection() > 95:
            robot.print("Fail to pick up an item")
        else:
            robot.lift_motor.run_target(self.speed, 37, then=Stop.HOLD, wait = True)
            while not robot.touch_sensor.pressed() and loops < 12:
                robot.drivebase.straight(10)
                loops += 1
            robot.drivebase.stop()
            if robot.touch_sensor.pressed():
                robot.lift_motor.run_until_stalled(self.speed, then=Stop.HOLD, duty_limit=self.duty_limit)
                wait(100)
                robot.drivebase.straight(-200)
                robot.lift_motor.run_target(-1*self.speed, 50, then=Stop.HOLD, wait=True)
            else:
                robot.print("Fail to pick up an elevated item")

class CalibrateLiftAngle(Base):
    """
    calibrate the lift motor angles
    """

    def __init__(self, name="Lift Calibration"):
        super().__init__(name=name)

    def run(self, robot: Robot):
        robot.lift_motor.stop()
        robot.print("Lower the lift to the lowest position and press center button")
        robot.wait_for_buttons(Button.CENTER)
        wait(100)
        robot.lift_motor.reset_angle(0)
        # robot.print("Raise the lift to the highest position and press center button")
        # robot.wait_for_buttons(Buttons.CENTER)
        robot.lift_motor.run_until_stalled(50, then=Stop.HOLD, duty_limit=100)
        wait(300)
        robot.lift_max_angle = robot.lift_motor.angle()
        robot.print(f"Calibration complete with {robot.lift_max_angle} degrees")


class CalibrateAmbientLight(Base):
    """
    calibrate the ambient light value
    """

    def __init__(self, name="Ambient light Calibration"):
        super().__init__(name=name)

    def run(self, robot: Robot):
        robot.print("Place the light sensor on white and press center button")
        robot.wait_for_buttons(Button.CENTER)
        robot.AMBIENT_LIGHT = robot.light_sensor.ambient()
        robot.print(f"Calibration complete with {robot.AMBIENT_LIGHT}%")

class FollowLine(Base):
    """
    follows a line of specified color
    """
    def __init__(self, end_fn, name="Line Follow", inside=9, outside=85, speed=100, gain=0.7):
        """
        Paramaters:
        end_fn: function that returns True if the command should end
        name: name of the command
        inside: % of luminosity inside the line
        outside: % of luminosity outside the line
        speed: driving speed of the robot in mm/s
        gain: gain of the line following controller in degrees per % of deviation from the threshold
        """
        super().__init__(name=name)
        self.end_fn = end_fn
        self.inside = inside
        self.outside = outside
        self.speed = speed
        self.gain = gain

    def run(self, robot: Robot):
        # Calculate the light threshold. Choose values based on your measurements.
        threshold = (self.inside + self.outside) / 2

        # Start following the line until the end_fn returns True.
        while not self.end_fn():

            # Calculate the deviation from the threshold.
            deviation = robot.light_sensor.reflection() - threshold

            # Calculate the turn rate.
            turn_rate = self.gain * deviation

            # Set the drive base speed and turn rate.
            robot.drivebase.drive(self.speed, turn_rate)

class ExitCircleAtColor(Base):
    """
    drives to a specified color in the circle in the enviroment
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
        super().__init__(name=name)
        self.color = color
        self.speed = speed
        self.gain = gain

    def run(self, robot: Robot):
        inside = env.EnvColor.BLACK
        outside = env.EnvColor.WHITE
        # start following the line until the "color" is detected
        while True:
            readout = robot.light_sensor.rgb()
            read_color = env.from_rgb(readout)
            # break loop if the color is detected
            if read_color == self.color:
                break
            if read_color is not inside and not outside:
                inside = read_color

            threshold = (inside.get_reflectivity() + outside.get_reflectivity()) / 2
            # Calculate the deviation from the threshold.
            deviation = robot.light_sensor.reflection() - threshold
            # Calculate the turn rate.
            turn_rate = self.gain * deviation
            # Set the drive base speed and turn rate.
            robot.drivebase.drive(self.speed, turn_rate)

class AutoFollowLine(Base):
    """
    follows a line of any color even when the color changes (other than the outside colors)
    """
    def __init__(self, end_fn, name="Auto Line Follow", initial_inside=env.EnvColor.PURLE, initial_outside=env.EnvColor.WHITE, speed=100, gain=0.7):
        """
        Paramaters:
        end_fn: function that returns True if the command should end
        name: name of the command
        inside: % of luminosity inside the line
        outside: % of luminosity outside the line
        speed: driving speed of the robot in mm/s
        gain: gain of the line following controller in degrees per % of deviation from the threshold
        """
        super().__init__(name=name)
        self.end_fn = end_fn
        self.speed = speed
        self.gain = gain
        self.initial_inside = initial_inside
        self.initial_outside = initial_outside

    def run(self, robot: Robot):
        inside = env.EnvColor.BLACK
        outside = env.EnvColor.WHITE
        # start following the line until the "color" is detected
        while not self.end_fn():
            readout = robot.light_sensor.rgb()
            read_color = env.from_rgb(readout)
            # break loop if the color is detected
            if read_color is not inside and read_color is not outside:
                inside = read_color
            if read_color is not inside and read_color in env.OUTSIDE_COLORS:
                outside = read_color
            threshold = (inside.get_reflectivity() + outside) / 2
            # Calculate the deviation from the threshold.
            deviation = robot.light_sensor.reflection() - threshold
            # Calculate the turn rate.
            turn_rate = self.gain * deviation
            # Set the drive base speed and turn rate.
            robot.drivebase.drive(self.speed, turn_rate)
