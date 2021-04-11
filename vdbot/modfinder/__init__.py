from fuzzywuzzy import process
import json

class ModFinder:
    def __init__(self):
        self.mods = None
        with open('mods.json', 'r') as f:
            self.mods = json.loads(f.read())
        self.mod_titles = self.mods.keys()
    
    def find_mods(self, query):
        results = process.extract(query, self.mod_titles, limit=3)
        mods = []
        for result in results:
            mods.append({'name': result[0], 'data': {**self.mods[result[0]]}})
        return mods
        
        
    