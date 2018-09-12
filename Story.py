import datetime

from six import string_types


class Story():
    def __init__(self, load_from_dict=None, owner_id=None):
        self.id = None
        self.name = ''
        self.owner_id = None
        self.started = None
        self.completed = None
        self._started_at = None
        self._completed_at = None

        if load_from_dict is not None and isinstance(load_from_dict, dict):
            for key in load_from_dict.keys():
                setattr(self, key, load_from_dict[key])

        if owner_id is not None:
            self.owner_id = owner_id


    @property
    def cycle_time_seconds(self):
        return (self.completed_at-self.started_at).total_seconds()


    @property
    def started_at(self):
        return self._started_at


    @started_at.setter
    def started_at(self, started_at):
        self._started_at = self._parse_datetime(started_at)


    @property
    def completed_at(self):
        if self._completed_at is not None:
            return self._completed_at
        else:
            return datetime.datetime.now()


    @completed_at.setter
    def completed_at(self, completed_at):
        self._completed_at = self._parse_datetime(completed_at)


    def _parse_datetime(self, src):
        # ATTENTION! Timezone is set as 'Zulu' by default on ClubHouse. This
        # script is not accounting for timezones! (and it's unclear if CH
        # does...) Revist the following login (specially the final 'Z') if
        # becomes relevant...
        result = None
        if src is not None:
            if isinstance(src, string_types):
                result = datetime.datetime.strptime(src, '%Y-%m-%dT%H:%M:%SZ')
            elif isinstance(src, datetime.date):
                result = src
        return result
