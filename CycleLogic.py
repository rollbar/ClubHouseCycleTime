from tabulate import tabulate
import collections
import datetime


StoryRow = collections.namedtuple(
    'StoryRow', 'story_id name owner started_at completed_at')


class CycleLogic():
    def __init__(self):
        self._stories = []
        self._members = {}


    def add_story(self, story):
        self._stories.append(story)


    def add_member(self, member):
        self._members[member['id']] = member


    def tabulate_result(self, weeks_count=8):
        w, h = weeks_count+1, len(self.members)
        table = [[0 for x in range(w)] for y in range(h)]
        weeks = []
        headers = ['Member']

        for i, member in enumerate(self.members):
            table[i][0] = self.members[member]['profile']['name']

        now = datetime.datetime.now()
        for i in range(weeks_count):
            weekLabel = '%s W%s' % (now.isocalendar()[0], now.isocalendar()[1])
            weeks.insert(0, weekLabel)
            for y, member in enumerate(self.members):
                table[y][weeks_count-i] = self._average_cycle_hours(
                    week=now, member=member)
            now -= datetime.timedelta(weeks=1)

        headers += weeks
        return tabulate(table, tablefmt='presto', headers=headers)


    def tabulate_stories(self):
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
        result = []
        for story in self.stories:
            if story.started and story.owner_id == member:
                result.append(story)
        return result


    def search_in_range(self, start_date, end_date, member):
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
        return int(total/count) if count>0 else 0



    def _week_range(self, date):
        start_date = datetime.datetime(date.year, date.month, date.day, 0, 0, 0)
        if date.isocalendar()[2] != 7:
            start_date -= datetime.timedelta(date.isocalendar()[2])
        end_date = start_date + datetime.timedelta(6)
        return start_date, end_date


    @property
    def stories(self):
        return self._stories


    @property
    def members(self):
        return self._members
