#!/usr/bin/env pybricks-micropython
from collections.deque import deque
from robot import Robot

class Command_Base:
    """
    a unifying interface for all commands
    """
    def __init__(self):
        self.name = "Command_Base"
        self.status = "N/A"
    def run(self, robot: Robot):
        pass
    def __str__(self):
        return self.name

class Command_Queue(deque, Command_Base): #TODO: might need to be a command base to for nesting purposes
    """
    a first-in first-out queue of commands
    """
    def run(self, robot: Robot):
        while len(self) > 0:
            self.popleft().run(robot)

    def __str__(self):
        output = ""
        for command in self:
            output += str(command) + "\n"

    def tree(self, indent=0):
        for command in self:
            if isinstance(command, Command_Queue):
                command.tree(indent=indent+1)
            else:
                print("\t" * indent + str(command))

class Command_Halt(Command_Base):
    """
    stops the robot
    """
    def __init__(self):
        self.name = "Halt"
    def run(self, robot):
        robot.drivebase.stop()

class Command_Lambda(Command_Base):
    """
    a command that runs a lambda function
    """
    def __init__(self, fn: function, name="Lambda"):
        self.name = name
        self.fn = fn
    def run(self, robot):
        self.fn(robot)