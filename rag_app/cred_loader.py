import json

class Credentials:
    def __init__(self):
        self.api_key = None


    def load_credentials(self):

        with open("credentials.json", 'r') as file:
            credentials = json.load(file)
        
        self.api_key = credentials["api_keys"]

        return None
    
creds = Credentials()
creds.load_credentials()
