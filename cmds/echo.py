class EchoCommand:
    def __init__(self):
        self.name = 'echo'
        self.parameters = ['message']
        self.descr = "Echoes the input message."

    def run(self, *args):
        if args:
            return ' '.join(args)
        return "No message provided."
