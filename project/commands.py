#!/usr/bin/env pybricks-micropython
from array import array

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

class Command_Queue(array): #TODO: might need to be a command base to for nesting purposes
    """
    a first-in first-out queue of commands
    """
    def run(self, robot: Robot):
        while len(self) > 0:
            self.pop(i=0).run(robot)

    # TODO: print function to print the queue as a tree
    # def print_queue(self):
    #     for command in self:
    #         print("\t" + command.name)

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