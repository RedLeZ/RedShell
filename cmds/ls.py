import os

class LsCommand:
    def __init__(self):
        self.name = "ls"
        self.parameters = ["directory"]
        self.descr = "List directory contents"

    def run(self, *args):
        if len(args) == 0:
            dirs = os.listdir()
            for d in dirs:
                print(d)
            return " " 
        else:
            dirs = os.listdir(args[0])
            for d in dirs:
                print(d)
            return " "
