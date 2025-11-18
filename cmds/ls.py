import os

class LsCommand:
    def __init__(self):
        self.name = "ls"
        self.flags = ["directory"]
        self.description = "List directory contents"

    def run(self, *args):
        target = args[0] if args else os.curdir
        try:
            entries = os.listdir(target)
        except FileNotFoundError:
            return f"ls: cannot access '{target}': No such file or directory"
        except NotADirectoryError:
            return target
        except PermissionError:
            return f"ls: cannot open directory '{target}': Permission denied"
        entries.sort()
        return "\n".join(entries)
