import os

class RmCommand:
    def __init__(self):
        self.name = "rm"
        self.flags = []
        self.description = "Remove a file"

    def run(self, *args):
        if not args:
            return "This command requires a file name"
        if len(args) > 1:
            return "This command takes only one argument"
        try:
            os.remove(args[0])
        except FileNotFoundError:
            return "File not found"
        return ""
