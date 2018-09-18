"""
Build a list of users and calculte the average cycle times
"""


import collections
import datetime

from tabulate import tabulate


StoryRow = collections.namedtuple(
    'StoryRow', 'story_id name owner started_at completed_at')


class CycleLogic():
    """Build a list of users and calculte the average cycle times"""
    def __init__(self):
        self._stories = []
        self._members = {}


    def add_story(self, story):
        """Add a story"""
        self._stories.append(story)


    def add_member(self, member):
        """Add a member"""
        self._members[member['id']] = member


    def tabulate_result(self, weeks_count=8):
        """Preprare results in a table that can be displayed in console"""
        width, haight = weeks_count+1, len(self.members)
        table = [[0 for x in range(width)] for y in range(haight)]
        weeks = []
        headers = ['Member']

        for i, member in enumerate(self.members):
            table[i][0] = self.members[member]['profile']['name']

        now = datetime.datetime.now()
        for i in range(weeks_count):
            week_label = '%s W%s' % (now.isocalendar()[0], now.isocalendar()[1])
            weeks.insert(0, week_label)
            for j, member in enumerate(self.members):
                table[j][weeks_count-i] = self._average_cycle_hours(
                    week=now, member=member)
            now -= datetime.timedelta(weeks=1)

        headers += weeks
        return tabulate(table, tablefmt='presto', headers=headers)


    def tabulate_stories(self):
        """
        Return an ascii table with the list of stories that can be displayed
        in console.
        """
        table = []
        for story in self._stories:
            if story.started:
                table.append(StoryRow(
                    story.id,
                    story.name[:20],
                    self.members[story.owner_id]['profile']['name'],
                    story.started_at,
                    story.completed_at
                ))
        return tabulate(table, tablefmt='presto', headers=[
            'Story ID',
            'Story Name',
            'Owner',
            'Started at',
            'Completed at'
        ])


    def search_active_story_by_member(self, member):
        """Active story per member"""
        result = []
        for story in self.stories:
            if story.started and not story.archived and story.owner_id == member:
                result.append(story)
        return result


    def search_in_range(self, start_date, end_date, member):
        """Active story per member in a date range"""
        result = []
        for story in self.search_active_story_by_member(member):
            if story.completed_at > start_date and story.started_at < end_date:
                result.append(story)
        return result


    def _average_cycle_hours(self, week, member):
        return  int(self._average_cycle_seconds(week, member)/3600)


    def _average_cycle_seconds(self, week, member):
        start_date, end_date = self._week_range(week)
        count = 0
        total = 0
        for story in self.search_in_range(start_date=start_date,
                                          end_date=end_date,
                                          member=member):
            count += 1
            total += story.cycle_time_seconds
        return int(total/count) if count > 0 else 0


    @classmethod
    def _week_range(cls, date):
        start_date = datetime.datetime(date.year, date.month, date.day, 0, 0, 0)
        if date.isocalendar()[2] != 7:
            start_date -= datetime.timedelta(date.isocalendar()[2])
        end_date = start_date + datetime.timedelta(6)
        return start_date, end_date


    def wild_experiment(self):
        """Rethinking and double checking few things"""
        pass


    @property
    def stories(self):
        """All the stories"""
        return self._stories


    @property
    def members(self):
        """All the members"""
        return self._members
