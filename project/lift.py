#!/usr/bin/env pybricks-micropython
from robot import Robot

class Command_lift:
    def __init__(self, speed = 50, duty_limit = 60):
        self.speed = speed
        self.duty_limit = duty_limit
    
    def lift_up(self, robot):
        if robot.touch_sensor.pressed() == True:
            robot.lift_motor.run_until_stalled(self.speed, then=Stop.HOLD, self.duty_limit)

