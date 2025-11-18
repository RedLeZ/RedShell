import os
import json
import importlib.util

def load_module(file_path):
    module_name = f"redshell.cmds.{os.path.splitext(os.path.basename(file_path))[0]}"
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def register_commands():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cmds_folder = os.path.join(base_dir, 'cmds')
    registered_commands = {}

    for filename in os.listdir(cmds_folder):
        if not filename.endswith('.py'):
            continue
        if filename.startswith('_'):
            continue
        file_path = os.path.join(cmds_folder, filename)
        try:
            module = load_module(file_path)
        except Exception as e:
            print(f"Warning: failed to import {filename}: {e}")
            continue
        # Prefer COMMAND_META if provided
        meta = getattr(module, 'COMMAND_META', None)
        if meta and isinstance(meta, dict) and 'name' in meta:
            name = meta.get('name')
            registered_commands[name] = {
                'class': meta.get('class') or meta.get('class_name') or f"{name.title()}Command",
                'parameters': meta.get('flags', []),
                'descr': meta.get('description', ''),
            }
            continue
        # Fallback: discover a *Command class instance
        command_instance = None
        for attr in dir(module):
            if attr.endswith("Command"):
                try:
                    command_instance = getattr(module, attr)()
                    break
                except Exception as e:
                    print(f"Warning: failed to instantiate {attr} in {filename}: {e}")
        if command_instance:
            registered_commands[command_instance.name] = {
                'class': command_instance.__class__.__name__,
                'parameters': getattr(command_instance, 'flags', []),
                'descr': getattr(command_instance, 'description', ''),
            }

    with open(os.path.join(base_dir, 'registered_commands.json'), 'w') as f:
        json.dump(registered_commands, f, indent=4)

if __name__ == "__main__":
    register_commands()
