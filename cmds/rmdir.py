import os

class RmdirCommand:
    def __init__(self):
        self.name = "rmdir"
        self.flags = ["directory"]
        self.description = "Remove directories"

    def run(self, *args):
        if not args:
            return "rmdir: missing operand"
        path = args[0]
        try:
            os.rmdir(path)
        except FileNotFoundError:
            return f"rmdir: failed to remove '{path}': No such file or directory"
        except OSError:
            return f"rmdir: failed to remove '{path}': Directory not empty"
        except PermissionError:
            return f"rmdir: failed to remove '{path}': Permission denied"
        return ""
