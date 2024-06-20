import os
import json
import importlib.util

def load_command_class(file_path):
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for attr in dir(module):
        if attr.endswith("Command"):
            return getattr(module, attr)()

def register_commands():
    cmds_folder = 'cmds'
    registered_commands = {}

    for filename in os.listdir(cmds_folder):
        if filename.endswith('.py'):
            file_path = os.path.join(cmds_folder, filename)
            command_instance = load_command_class(file_path)
            if command_instance:
                registered_commands[command_instance.name] = {
                    'class': command_instance.__class__.__name__,
                    'parameters': command_instance.flags,
                    'descr': command_instance.description,

                }

    with open('registered_commands.json', 'w') as f:
        json.dump(registered_commands, f, indent=4)

if __name__ == "__main__":
    register_commands()
