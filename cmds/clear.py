import os

class ClearCommand:
    def __init__(self):
        self.name = "clear"
        self.parameters = []
        self.descr = "Clear the screen"

    def run(self, *args):
        if args:
            return "This command doesn't take any arguments"
        os.system('cls' if os.name == 'nt' else 'clear') 
        return ""
