import json

class Table():

    changed = True

    def __init__(self, name, src=None):
        if src is None:
            src = f'tables/{name}.JSON'
        self.src = src
        self.name = name
        with open(src, 'r') as txt:
            self.data = json.load(txt.read())
    
    def save(self):
        # only allow if changes made
        if self.changed == False:
            return
        with open(self.src, 'w') as txt:
            json.dump(self.data, txt, indent=4)
        
