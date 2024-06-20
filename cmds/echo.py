class EchoCommand:
    def __init__(self):
        self.name = 'echo'
        self.flags = ['message']
        self.description = "Echoes the input message."

    def run(self, *args):
        if args:
            return ' '.join(args)
        return "No message provided."
