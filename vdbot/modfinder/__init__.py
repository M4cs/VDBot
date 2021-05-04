from fuzzywuzzy import process
import json, requests
from requests.api import head

class ModFinder:
    def __init__(self):
        self.is_reindexing = False
        self.mods = None
        with open('mods.json', 'r') as f:
            self.mods = json.loads(f.read())
        self.mod_titles = self.mods.keys()
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Bot of Yggdrasil Discord/Valheim Modding Discord Bot v1.0'
        }
        res = requests.get('https://valheim.thunderstore.io/api/v1/package/', headers=headers)
        res_json = res.json()
        for mod in res_json:
            if mod['name'] in self.mod_titles:
                self.mods[mod['name']]['url'] += "\n**TS Link:** " + mod['package_url']
            else:
                self.mods[mod['name']] = {'summary': mod['versions'][-1]['description'], 'url': mod['package_url']}
    
    def find_mods(self, query):
        results = process.extract(query, self.mod_titles, limit=3)
        mods = []
        for result in results:
            mods.append({'name': result[0], 'data': {**self.mods[result[0]]}})
        return mods

    def update_index(self):
        self.is_reindexing = True
        self.mods = None
        headers = {
            'Accept': 'application/json',
            'apikey': 'QWVnanJ3UW1JWk1PcUI4c2dqMTZ6b3VsazQzSW94RVRYd0Y4ck5LbEtaRjNvNHFxSHVOTks3MW0wbU42bEpYaC0tdUZId2I2SEtPUVZqTmlPWjFROHpsdz09--c414ebf1e32bd456db5ae1481a04b58d282dd859'
        }

        i = 0
        mods = {}
        while i < 2000:
            res = requests.get('https://api.nexusmods.com/v1/games/valheim/mods/' + str(i) + '.json', headers=headers)
            if res.status_code != 404:
                obj = res.json()
                if obj.get('name') and obj.get('summary'):
                    print('Saving Mod: ' + obj.get('name'))
                    mods[obj['name']] = {'summary': obj['summary'], 'image_url': obj.get('picture_url'), 'url': 'https://www.nexusmods.com/valheim/mods/' + str(i)}
            i += 1

        with open('mods.json', 'w+') as f:
            json.dump(mods, f, indent=4)
        with open('mods.json', 'r') as f:
            self.mods = json.loads(f.read())
        self.mod_titles = self.mods.keys()
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Bot of Yggdrasil Discord/Valheim Modding Discord Bot v1.0'
        }
        res = requests.get('https://valheim.thunderstore.io/api/v1/package/', headers=headers)
        res_obj = res.json()
        for mod in res_obj:
            if mod['name'] in self.mod_titles:
                self.mods[mod['name']]['url'] += "\n**TS Link:** " + mod['package_url']
            else:
                self.mods[mod['name']] = {'summary': mod['versions'][-1]['description'], 'url': mod['package_url']}
        self.is_reindexing = False
        
        
    