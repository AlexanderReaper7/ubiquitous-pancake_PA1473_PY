#!/usr/bin/env pybricks-micropython
from collections import deque
from robot import Robot
from pybricks.parameters import Stop
from pybricks.tools import wait

class Command_Base:
    """
    a unifying interface for all commands
    """
    def __init__(self, name="Command_Base"):
        self.name = name
        self.status = "N/A"

    def run(self, robot):
        pass

    def __str__(self):
        return self.name

class Command_Queue(deque):
    """
    a first-in first-out queue of commands
    """
    def __init__(self, name="Command_Queue"):
        super().__init__()
        self.name = name

    def run(self, robot):
        while len(self) > 0:
            self.popleft().run(robot)

    def tree(self, indent=0):
        # print(f"{"\t" * indent}{self.name}")
        for command in self:
            if isinstance(command, Command_Queue):
                command.tree(indent=indent+1)
            else:
                print("\t" * (indent + 1) + str(command))

class Command_Halt(Command_Base):
    """
    stops the robot
    """
    def __init__(self, name="Command_Halt"):
        super().__init__(name=name)

    def run(self, robot):
        robot.drivebase.stop()

class Command_Lambda(Command_Base):
    """
    a command that runs a lambda function
    """
    def __init__(self, fn: function, name="Lambda"):
        super().__init__(name=name)
        self.fn = fn

    def run(self, robot):
        self.fn(robot)

class Command_Lift(Command_Base):
    def __init__(self, name="Lift", speed = 50, duty_limit = 100):
        super().__init__(name=name)
        self.speed = speed
        self.duty_limit = duty_limit
    
    def run(self, robot):
        loops = 0
        if robot.touch_sensor.pressed() == True:
            robot.lift_motor.run_until_stalled(self.speed, then=Stop.HOLD, duty_limit=self.duty_limit)
            wait(100)
            robot.drivebase.straight(-200)
            robot.lift_motor.run_target(-1*self.speed, 50, then=Stop.HOLD, wait=True)
            # robot.drivebase.straight(100)
            # robot.lift_motor.run_until_stalled(-1*self.speed, then=Stop.HOLD, duty_limit=self.duty_limit)
        elif robot.light_sensor.reflection() > 95:
            print ("Fail to pick up an item")
        else:
            robot.lift_motor.run_target(self.speed, 33, then=Stop.HOLD, wait = True)
            while robot.touch_sensor.pressed() == False and loops < 12:
                robot.drivebase.straight(10)
                loops += 1
            robot.drivebase.stop()
            if robot.touch_sensor.pressed() == True:
                robot.lift_motor.run_until_stalled(self.speed, then=Stop.HOLD, duty_limit=self.duty_limit)
                wait(100)
                robot.drivebase.straight(-200)
                robot.lift_motor.run_target(-1*self.speed, 50, then=Stop.HOLD, wait=True)
            else:
                print ("Fail to pick up an elevated item")
        


            

