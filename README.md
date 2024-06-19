# RedShell
A Modable Shell by [RedLeZ](https://github.com/RedLeZ) using the Python language

## How to Use

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/RedLeZ/RedShell.git
    ```

2. **Navigate to the Installed Folder:**

    ```bash
    cd RedShell
    ```

3. **Install Requirements:**

    ```bash
    pip3 install -r requirements.txt
    ```

4. **Run the Shell:**

    ```bash
    python3 shell.py
    ```

## How to Mod

Modding the shell means adding commands to it. Follow these steps:

1. Navigate to the `cmds` folder and create a new file. Use the example below as a template.

    **template.py:**

    ```python
    class TemplateCommand:
        def __init__(self):
            # Here you define the name, parameters, and description of the command
            self.name = "template"
            self.parameters = []
            self.descr = "This is a template command"

        def run(self, *args):
            # This is where you implement the command's functionality
            if args:
                return "Args:", args
            else:
                return "No args"
    ```

2. Register your new command:

    ```bash
    python3 register_command.py
    ```

    Your command should now be available for use.

## Contributing

Anyone is free to contribute! Have fun :)


