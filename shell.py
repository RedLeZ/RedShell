import json
import json
import os
import sys
import shlex
import difflib
from typing import Optional
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from register_command import register_commands
import importlib.util

class Shell:
    def __init__(self):
        self.running = True
        self.commands = {}
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        # Persisted history file in user home
        self.history_file = os.path.expanduser("~/.redshell_history")
        # Ensure command registry is up to date at startup
        try:
            register_commands()
        except Exception as e:
            print(f"Warning: couldn't refresh command registry: {e}")
        self.load_commands()

    def load_commands(self):
        # Reset commands to avoid keeping removed commands on refresh
        self.commands = {}
        with open(os.path.join(self.base_dir, 'registered_commands.json'), 'r') as f:
            registered_commands = json.load(f)

        for cmd_name, cmd_info in registered_commands.items():
            file_path = os.path.join(self.base_dir, 'cmds', f"{cmd_name}.py")
            try:
                command_instance = self.load_command_class(file_path, cmd_info['class'])
                if command_instance:
                    self.commands[cmd_name] = {
                        'instance': command_instance,
                        'parameters': cmd_info.get('parameters', []),
                        'descr': cmd_info.get('descr', '')
                    }
            except FileNotFoundError:
                print(f"Warning: command file not found for '{cmd_name}' at {file_path}")
            except Exception as e:
                print(f"Warning: failed to load command '{cmd_name}': {e}")

    def load_command_class(self, file_path, class_name):
        module_name = f"redshell.cmds.{os.path.splitext(os.path.basename(file_path))[0]}"
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, class_name)()

    def run_command(self, command_name, *args):
        if command_name in self.commands:
            command = self.commands[command_name]['instance']
            result = None
            try:
                result = command.run(*args)
            except Exception as e:
                print(f"Error while running '{command_name}': {e}")
                return None
            # Only print meaningful output
            return result
        else:
            print(f"Unknown command: {command_name}")
            # Suggest close matches
            suggestions = difflib.get_close_matches(command_name, list(self.commands.keys()), n=3, cutoff=0.6)
            if suggestions:
                print("Did you mean:", ", ".join(suggestions))
            return None

    def refresh(self):
        register_commands()
        self.load_commands()

    def show_help(self, command_name: Optional[str] = None):
        if command_name:
            info = self.commands.get(command_name)
            if not info:
                print(f"No such command: {command_name}")
                return
            params = info.get('parameters') or []
            usage = f"{command_name} {' '.join(f'<{p}>' for p in params)}" if params else command_name
            print(f"Usage: {usage}")
            print(f"Description: {info.get('descr', '')}")
            return

        print("Available commands:")
        print("  exit     : Exit the shell")
        print("  refresh  : Refresh the commands registry")
        print("  help     : Show help. Use 'help <command>' for details")
        print("  history  : Show recent command history")
        print("  restart  : Restart the shell process")
        for cmd_name, cmd_info in sorted(self.commands.items()):
            print(f"  {cmd_name:<8}: {cmd_info['descr']}")

    def show_history(self, limit: int = 50):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    lines = [line.rstrip('\n') for line in f if line.strip()]
                if not lines:
                    print("History is empty.")
                    return
                start = max(0, len(lines) - limit)
                for i, line in enumerate(lines[start:], start=start + 1):
                    print(f"{i:4d}  {line}")
            else:
                print("History is empty.")
        except Exception as e:
            print(f"Couldn't read history: {e}")

    def start(self):
        session = PromptSession(history=FileHistory(self.history_file))
       
        while self.running:
            command_completer = WordCompleter(list(self.commands.keys()) + ["exit", "refresh", "help", "history", "restart"])
            current_dir = os.path.basename(os.getcwd())
            try:
                user_input = session.prompt(f"$/{current_dir} - RedShell > ", completer=command_completer)
                if user_input.strip():
                    try:
                        parts = shlex.split(user_input)
                    except ValueError as e:
                        print(f"Parse error: {e}")
                        continue
                    # Handle simple output redirection: cmd ... > file or >> file
                    out_file = None
                    append = False
                    if '>' in parts or '>>' in parts:
                        if '>>' in parts:
                            idx = parts.index('>>')
                            append = True
                        else:
                            idx = parts.index('>')
                        if idx == len(parts) - 1:
                            print("redirection: missing file operand")
                            continue
                        out_file = parts[idx + 1]
                        parts = parts[:idx]

                    if not parts:
                        continue
                    command = parts[0]
                    args = parts[1:]
                    if command == "exit":
                        break
                    elif command == "refresh":
                        self.refresh()
                    elif command == "help":
                        if args:
                            self.show_help(args[0])
                        else:
                            self.show_help()
                    elif command == "history":
                        # Optional limit argument
                        limit = int(args[0]) if args and args[0].isdigit() else 50
                        self.show_history(limit=limit)
                    elif command == "restart":
                        # Restart the current process
                        try:
                            os.execv(sys.executable, [sys.executable, os.path.abspath(__file__)])
                        except Exception as e:
                            print(f"Failed to restart: {e}")
                    else:
                        try:
                            result = self.run_command(command, *args)
                            if out_file is not None:
                                # Write to file if we have something
                                text = "" if result is None else str(result)
                                mode = 'a' if append else 'w'
                                try:
                                    with open(out_file, mode, encoding='utf-8') as f:
                                        if text:
                                            f.write(text)
                                            if not text.endswith('\n'):
                                                f.write('\n')
                                except Exception as e:
                                    print(f"Failed to write to {out_file}: {e}")
                            else:
                                if isinstance(result, str):
                                    if result and result.strip():
                                        print(result)
                                elif result is not None:
                                    print(result)
                        except Exception as e:
                            print(f"Error with the command {command} : Please check the command file : {e}")
            except (KeyboardInterrupt, EOFError):
                break

if __name__ == "__main__":
    shell = Shell()
    shell.start()
