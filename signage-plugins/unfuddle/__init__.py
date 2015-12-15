import os
import requests

from plugins import Plugin


class UnfuddlePlugin(Plugin):
    def __init__(self, username, password, project_id, statuses=['new', 'closed'], map_target=None, **kwargs):
        self.username = username
        self.password = password
        self.project_id = project_id
        self.statuses = statuses
        self.map_target = map_target
        Plugin.__init__(self, dirname=os.path.dirname(__file__), **kwargs)

    def init(self):
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)
        self.session.headers.update({'Accept': 'application/json'})

        self.people_map = {}
        people = self.session.get('https://hourlynerd.unfuddle.com/api/v1/people')
        for person in people.json():
            first_name_last_initial = person['first_name']
            if person['last_name']:
                first_name_last_initial = '{} {}.'.format(first_name_last_initial, person['last_name'][0])
            self.people_map[person['id']] = first_name_last_initial

    def get_data(self):
        data = []

        milestones = self.session.get('https://hourlynerd.unfuddle.com/api/v1/projects/{project_id}/milestones/upcoming'.format(project_id=self.project_id))
        for milestone in milestones.json():
            tickets = self.session.get('https://hourlynerd.unfuddle.com//api/v1/projects/{project_id}/milestones/{milestone_id}/tickets'.format(project_id=self.project_id, milestone_id=milestone['id']))

            d = {}
            target = 'all.milestone-{}'.format(milestone['id'])
            if self.map_target:
                target = self.map_target(milestone)

            if target is None:
                # no one can see this, so continue
                continue

            for status in self.statuses:
                d[status] = []
            for ticket in tickets.json():
                d[ticket['status']].append(ticket)

            result = []
            for status in self.statuses:
                tickets = sorted(d[status], lambda x, y: cmp(y['priority'], x['priority']))
                result.append((status, tickets))

            data.append({'milestone': milestone, 'people_map': self.people_map, 'data': result, 'target': target})

        return data
