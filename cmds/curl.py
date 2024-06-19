import requests


class CurlCommand :
    def __init__(self):
        self.name = "curl"
        self.parameters = ["url"]
        self.descr = "Retrieve the content of a webpage"

    def run(self, *args):
        if len(args) != 1:
            return "This command takes exactly one argument"
        url = args[0]
        try:
            response = requests.get(url)
            #save the response in a file the same type as the url and name
            with open(url.split('/')[-1], 'wb') as f:
                f.write(response.content)
            return f"Response saved in {url.split('/')[-1]}"
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"
