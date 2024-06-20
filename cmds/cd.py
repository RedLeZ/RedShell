import os

class CdCommand:
    def __init__(self):
        self.name = "cd"
        self.flags = ["directory"]
        self.description = "Change the current directory"

    def run(self, *args):
        if len(args) == 0:
            return "cd: missing operand"
        try:
            os.chdir(args[0])
        except FileNotFoundError:
            return "cd: no such file or directory: " + args[0]
        return ""
