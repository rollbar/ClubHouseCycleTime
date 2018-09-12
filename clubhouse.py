import json

import requests


class ClubHouseAPI():
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = 'https://api.clubhouse.io/api/beta'


    def getEpics(self):
        return self._get('epics')


    def getActiveEpics(self):
        epics = self.getEpics()
        result = []
        for epic in epics:
            if not epic['archived'] and not epic['completed'] and epic['started']:
                result.append(epic)
        return result


    def getMembers(self):
        return self._get('members')


    def getActiveMembers(self):
        members = self.getMembers()
        result = []
        for member in members:
            if not member['disabled']:
                result.append(member)
        return result


    def searchStory(self, query, pages=5, nextQuery=None):
        data = {'query': query}

        if nextQuery is not None:
            data['next'] = nextQuery.split('next=')[1]

        r = self._get('search/stories', data=data)
        results = r['data']

        if pages > 0 and 'next' in r.keys():
            results += self.searchStory(query,
                                        pages=pages-1,
                                        nextQuery=r['next'])
        return results


    def storiesByMention(self, mention_name):
        return self.searchStory('owner:%s' % mention_name)


    def _get(self, url, data=None):
        url = '{base_url}/{url}?token={access_token}'.format(
            base_url=self.base_url,
            url=url,
            access_token=self.access_token)
        headers = {
            'content-type': 'application/json',
        }
        r = requests.get(url, headers=headers, data=json.dumps(data))
        return r.json()
