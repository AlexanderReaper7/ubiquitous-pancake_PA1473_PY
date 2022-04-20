#!/usr/bin/env pybricks-micropython
from collections.deque import deque
from robot import Robot

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
        print(f"{"\t" * indent}{self.name}:")
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
