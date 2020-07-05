import json
import hashlib
import requests


class api:
    id = None
    secret = None
    service = None
    path = None

    def __init__(self, api_name):
        with open('config/api.json') as json_file:
            data = json.load(json_file)[api_name]
            self.id = data['id']
            self.secret = data['secret'].encode()
            self.service = data['service']
            self.path = data['path']

    def get(self, route, params=None):
        p = self.path + route
        if params is not None:
            p += '/' + '/'.join([str(i) for i in params])
        s = self.get_signature(p)
        url = 'http://' + self.service + p
        headers = {}
        headers['client'] = self.id
        headers['secret'] = s
        r = requests.get(url, headers=headers)
        print(r)
        return json.loads(r.text)

    def put(self, path_extra, params, data):
        return None

    def post(self, path_extra, params, data):
        return None

    def get_signature(self, path, data={}):
        m = self.id + self.service + path + json.dumps(data)
        print(m)
        h = hashlib.sha3_512()
        h.update(m.encode() + self.secret)
        return h.hexdigest()
