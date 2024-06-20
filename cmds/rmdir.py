import os

class RmdirCommand:
    def __init__(self):
        self.name = "rmdir"
        self.flags = ["directory"]
        self.description = "Remove directories"

    def run(self, *args): 
        if args:
            return os.rmdir(args[0])
        else :
            return "Please provide a directory name"
