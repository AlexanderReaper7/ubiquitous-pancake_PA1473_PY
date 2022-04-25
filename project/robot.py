from pybricks.ev3devices import Motor, ColorSensor, TouchSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase


class Robot:
    """
    contains the initailised components of the robot
    """
    def __init__(self):
        """
        initialize the robot
        """
        self.touch_sensor = TouchSensor(Port.S1)
        self.light_sensor = ColorSensor(Port.S3)
        self.ultrasonic_sensor = UltrasonicSensor(Port.S4)
        self.lift_motor = Motor(Port.A, positive_direction = Direction.COUNTERCLOCKWISE, gears = [12, 36])
        self.left_motor = Motor(Port.C, positive_direction = Direction.COUNTERCLOCKWISE, gears = [12, 20] )
        self.right_motor = Motor(Port.B, positive_direction = Direction.COUNTERCLOCKWISE, gears = [12, 20])
        self.drivebase = DriveBase(self.left_motor, self.right_motor, wheel_diameter= 47, axle_track= 128)
