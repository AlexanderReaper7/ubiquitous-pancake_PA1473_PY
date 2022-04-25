#!/usr/bin/env pybricks-micropython
from robot import Robot

class Command_lift(Command_Base):
    def __init__(self, name="Lift", speed = 50, duty_limit = 60):
        super().__init__(name=name)
        self.speed = speed
        self.duty_limit = duty_limit
    
    def run(self, robot):
        if robot.touch_sensor.pressed() == True:
            robot.lift_motor.run_until_stalled(self.speed, then=Stop.HOLD, self.duty_limit)

