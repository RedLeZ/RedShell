import os
import time
import requests


class Shell():
    def __init__(self) -> None:
        self.commands = {
                'help': self.help,
                'exit': self.exit,
                'refresh': self.refresh,
                'history': self.showHistory,
                'Test' : self.test,
                'echo' : self.echo,
                'clear' : self.clear,
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
                }
        if parameter != None:
            if parameter in self.helpMenu:
                print(f'{parameter}: {self.helpMenu[parameter]}')
            else:
                print('Command not found')
        print('Available commands:')
        for command, description in self.helpMenu.items():
            print(f'{command}: {description}')

    def exit(self):
        print('Exiting...')
        exit()

    def refresh(self):
        print('Refreshing...')
        os.system('python3 main.py')
        exit()


    def showHistory(self):
        print('Command history:')
        for command in self.commandsHistory:
            print(command)
    def echo(self, parameter):
        print(parameter)

    def clear(self):
        os.system('clear')

    def run(self):
        print('Welcome To RedShell v1.0')
        parameter = None
        while True:
            command = input('>>> ')
            spaceIndex = command.find(' ')
            if spaceIndex != -1:
                parameter = command[spaceIndex + 1:]
                command = command[:spaceIndex]
            if command in self.commands:
                if parameter != None:
                    try :
                        self.commands[command](parameter)
                    except:
                        print("Error : Command's parameter is not correct or command does not require any parameter")
                        self.refresh()
                else :
                    self.commands[command]()

                self.commandsHistory.append(f'{command} {parameter} - {time.ctime()} - status: Success')
            elif command == '':
                pass
            else:
                print('Command not found')
                self.commandsHistory.append(f'{command} - {time.ctime()} - status: Command not found')
shell = Shell()
shell.run()
