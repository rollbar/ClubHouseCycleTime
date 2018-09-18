"""
All the ClubHouse api
"""


import json

import requests


class ClubHouseAPI():
    """All the ClubHouse api"""
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = 'https://api.clubhouse.io/api/beta'


    def get_epics(self):
        """All the Epics"""
        return self._get('epics')


    def get_active_epics(self):
        """All the active epics"""
        epics = self.get_epics()
        result = []
        for epic in epics:
            if not epic['archived'] and not epic['completed'] and epic['started']:
                result.append(epic)
        return result


    def get_members(self):
        """All the members"""
        return self._get('members')


    def get_active_members(self):
        """All the active members"""
        members = self.get_members()
        result = []
        for member in members:
            if not member['disabled']:
                result.append(member)
        return result


    def search_story(self, query, pages=5, next_query=None):
        """Search a story based on CH query syntax"""
        data = {'query': query}

        if next_query is not None:
            data['next'] = next_query.split('next=')[1]

        response = self._get('search/stories', data=data)
        results = response['data']

        if pages > 0 and 'next' in response.keys():
            results += self.search_story(query,
                                         pages=pages-1,
                                         next_query=response['next'])
        return results


    def stories_by_mention(self, mention_name):
        """All the active stories assigned to a member"""
        return self.search_story('owner:%s' % mention_name)


    def _get(self, url, data=None):
        url = '{base_url}/{url}?token={access_token}'.format(
            base_url=self.base_url,
            url=url,
            access_token=self.access_token)
        headers = {
            'content-type': 'application/json',
        }
        response = requests.get(url, headers=headers, data=json.dumps(data))
        return response.json()
