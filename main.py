import os
import time

class Shell():
    def __init__(self) -> None:
        self.running = True
        self.commands = {
                'help': self.help,
                'exit': self.exit,
                'refresh': self.refresh,
                'history': self.showHistory,
                'test' : self.test,
                'echo' : self.echo,
                'clear' : self.clear,
                'ls' : self.ls,
                'cd': self.cd,
                'mkdir': self.mkdir,
                'rmdir': self.rmdir,
                'vim': self.vim,
                }
        self.commandsHistory = []
    def test(self):
        print("Test command is working")

    def help(self, parameter = None):
        self.helpMenu = {
                'help': 'Shows this help menu',
                'exit': 'Exits the shell',
                'refresh': 'Refreshes the shell',
                'history': 'Shows History of commands',
                'Test' : 'Neet to be added in the help menu',
                'echo' : 'echoes the text',
                'clear' : 'clears the screen',
                'ls':   'lists all the files in the current directory',
                'mkdir': 'creates a new directory',
                'rmdir': 'removes a directory',
                'cd': 'changes the current directory',
                'vim': 'opens a file in vim editor',
                }
        if parameter != None:
            if parameter in self.helpMenu:
                print(f'{parameter}: {self.helpMenu[parameter]}')
            else:
                print('Command not found')
        else :
            print('Available commands:')
            for command, description in self.helpMenu.items():
                print(f'{command}: {description}')

    def exit(self):
        print('Exiting...')
        self.running = False

    def refresh(self):
        print('Refreshing...')
        os.system('python3 main.py')
        self.running = False


    def showHistory(self):
        print('Command history:')
        for command in self.commandsHistory:
            print(command)
    def echo(self, parameter):
        print(parameter)

    def clear(self):
        os.system('clear')

    def ls(self):
        elements = os.listdir()
        for element in elements:
            print(element)
    def cd(self, parameter):
        try:
            os.chdir(parameter)
        except:
            print('Error: Directory not found')
    def mkdir(self, parameter):
        try:
            os.mkdir(parameter)
        except:
            print('Error: Directory already exists')
    def rmdir(self, parameter):
        try:
            Warning = input("Are you sure you want to delete this directory? (y/n) ")
            if Warning == 'y':
                os.rmdir(parameter)
            else:
                print('Directory not deleted')
        except:
            print('Error: Directory not found')
    def vim(self, parameter):
        os.system(f'vim {parameter}')

    def run(self):
        while self.running:
            parameter = None
            currentDirectory = os.getcwd().split('/')[-1]
            command = input(f'~/{currentDirectory} - redshell > ').lower()
            spaceIndex = command.find(' ')
            if spaceIndex != -1:
                parameter = command[spaceIndex + 1:]
                command = command[:spaceIndex]
            if command in self.commands:
                if parameter != None and parameter != '' and parameter.isspace() == False and parameter != '\n' and parameter != '\t':
                    try :
                        self.commands[command](parameter)
                    except:
                        print("Error : Command's parameter is not correct or command does not require any parameter")
                else:
                    try :
                        self.commands[command]()
                    except:
                        print(f"Error : {command} cannot be run without a parameter")

                self.commandsHistory.append(f'{command} {parameter} - {time.ctime()} - status: Success')
            elif command == '':
                pass
            else:
                print('Command not found')
                self.commandsHistory.append(f'{command} - {time.ctime()} - status: Command not found')
shell = Shell()
shell.run()
