from jinja2 import Environment, FileSystemLoader
import os
import requests
import simplejson as json


class Plugin(object):
    def __init__(self, dirname='.', host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.env = Environment(loader=FileSystemLoader(os.path.join(dirname, 'templates')))

        self.init()

    def init(self):
        pass

    def get_location(self):
        return 'main'

    def get_data(self):
        raise NotImplementedError()

    def get_template_name(self):
        return 'plugin.html'

    def render(self, data):
        template = self.env.get_template(self.get_template_name())
        return template.render(**data)

    def publish(self):
        for data in self.get_data():
            headers = {'Accept': 'application/json'}
            post_data = json.dumps({
                'target': data['target'],
                'location': self.get_location(),
                'type': 'utf8',
                'utf8Data': self.render(data)
            })

            r = requests.post('http://{host}:{port}/message'.format(host=self.host, port=self.port), data=post_data, headers=headers)
            print 'RESULT:', r.text
