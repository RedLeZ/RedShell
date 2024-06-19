import json
import os
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from register_command import register_commands
import importlib.util

class Shell:
    def __init__(self):
        self.running = True
        self.commands = {}
        self.load_commands()

    def load_commands(self):
        with open('registered_commands.json', 'r') as f:
            registered_commands = json.load(f)

        for cmd_name, cmd_info in registered_commands.items():
            file_path = os.path.join('cmds', f"{cmd_name}.py")
            command_instance = self.load_command_class(file_path, cmd_info['class'])
            self.commands[cmd_name] = {
                'instance': command_instance,
                'parameters': cmd_info['parameters'],
                'descr': cmd_info['descr']
            }

    def load_command_class(self, file_path, class_name):
        spec = importlib.util.spec_from_file_location("module.name", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, class_name)()

    def run_command(self, command_name, *args):
        if command_name in self.commands:
            command = self.commands[command_name]['instance']
            print(command.run(*args))
        else:
            print(f"Unknown command: {command_name}")

    def refresh(self):
        register_commands()
        self.load_commands()

    def show_help(self):
        print("Available commands:")
        print("exit: Exit the shell")
        print("refresh: Refresh the commands")
        print("help: Show this help")
        for cmd_name, cmd_info in self.commands.items():
            print(f"{cmd_name}: {cmd_info['descr']}")

    def start(self):
        session = PromptSession()
       
        while self.running:
            command_completer = WordCompleter(list(self.commands.keys()) + ["exit", "refresh", "help", "restart"])
            current_dir = os.getcwd().split("/")[-1]
            try:
                user_input = session.prompt(f"$/{current_dir} - RedShell > ", completer=command_completer)
                if user_input.strip():
                    parts = user_input.split()
                    command = parts[0]
                    args = parts[1:]
                    if command == "exit":
                        break
                    elif command == "refresh":
                        self.refresh()
                    elif command == "help":
                        self.show_help()
                    else:
                        try :
                            self.run_command(command, *args)
                        except Exception as e:
                            print(f"Error with the command {command} : Please check the command file : {e}")
            except (KeyboardInterrupt, EOFError):
                break

if __name__ == "__main__":
    shell = Shell()
    shell.start()
