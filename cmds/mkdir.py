import os

class MkdirCommand:
    def __init__(self):
        self.name = "mkdir"
        self.parameters = ["directory"]
        self.descr = "Create a new directory"

    def run(self, *args):
        if len(args) == 0:
            print("mkdir: missing operand")
            return " "
        try :
            os.mkdir(args[0])
        except FileExistsError:
            return "mkdir: cannot create directory '" + args[0] + "':  It already exists"
            
        return "Created directory: " + args[0]

