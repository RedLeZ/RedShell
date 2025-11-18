import os

class MkdirCommand:
    def __init__(self):
        self.name = "mkdir"
        self.flags = ["directory"]
        self.description = "Create a new directory"

    def run(self, *args):
        if len(args) == 0:
            return "mkdir: missing operand"
        path = args[0]
        try:
            os.mkdir(path)
        except FileExistsError:
            return f"mkdir: cannot create directory '{path}': File exists"
        except FileNotFoundError:
            return f"mkdir: cannot create directory '{path}': No such file or directory"
        except PermissionError:
            return f"mkdir: cannot create directory '{path}': Permission denied"
        return ""

