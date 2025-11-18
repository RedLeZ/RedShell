import os
import shutil


class RmCommand:
    def __init__(self):
        self.name = "rm"
        self.flags = ["-f", "-r", "-d", "--"]
        self.description = "Remove files or directories"

    def run(self, *args):
        if not args:
            return "rm: missing operand"

        force = False
        recursive = False
        allow_empty_dir = False
        targets = []
        parse_options = True

        for arg in args:
            if parse_options and arg == "--":
                parse_options = False
                continue

            if parse_options and arg.startswith("-") and arg != "-":
                for flag in arg[1:]:
                    if flag in ("r", "R"):
                        recursive = True
                    elif flag == "f":
                        force = True
                    elif flag == "d":
                        allow_empty_dir = True
                    else:
                        return f"rm: invalid option -- '{flag}'"
                continue

            targets.append(arg)

        if not targets:
            return "rm: missing operand"

        errors = []
        for target in targets:
            error = self._remove_target(target, recursive, force, allow_empty_dir)
            if error:
                errors.append(error)

        return "\n".join(errors)

    def _remove_target(self, path, recursive, force, allow_empty_dir):
        exists = os.path.lexists(path)
        if not exists:
            if force:
                return ""
            return f"rm: cannot remove '{path}': No such file or directory"

        try:
            if os.path.isdir(path) and not os.path.islink(path):
                if recursive:
                    shutil.rmtree(path)
                elif allow_empty_dir:
                    os.rmdir(path)
                else:
                    return f"rm: cannot remove '{path}': Is a directory"
            else:
                os.remove(path)
        except PermissionError:
            if force:
                return ""
            return f"rm: cannot remove '{path}': Permission denied"
        except OSError as exc:
            # Keep message tidy even when coming from rmtree
            if force:
                return ""
            reason = exc.strerror or str(exc)
            return f"rm: failed to remove '{path}': {reason}"

        return ""
