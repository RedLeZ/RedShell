import os


class CdCommand:
    def __init__(self):
        self.name = "cd"
        self.flags = ["directory"]
        self.description = "Change the current directory"
        self._previous_dir = os.getcwd()

    def run(self, *args):
        if len(args) > 1:
            return "cd: too many arguments"

        if len(args) == 0:
            target = os.path.expanduser(os.environ.get("HOME", "~"))
        else:
            raw_target = args[0]
            if raw_target == "-":
                if not self._previous_dir:
                    return "cd: OLDPWD not set"
                target = self._previous_dir
            else:
                # Allow use of ~ and environment variables in paths
                target = os.path.expandvars(os.path.expanduser(raw_target))

        current_dir = os.getcwd()
        try:
            os.chdir(target)
        except FileNotFoundError:
            return f"cd: no such file or directory: {target}"
        except NotADirectoryError:
            return f"cd: not a directory: {target}"
        except PermissionError:
            return f"cd: permission denied: {target}"

        self._previous_dir = current_dir
        return ""
