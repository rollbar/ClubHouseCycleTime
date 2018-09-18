"""
Represent a user story (with magic)
"""

import datetime

from six import string_types


class Story():
    """Represent a user story (with magic)"""

    # pylint: disable=too-many-instance-attributes
    # Nine is reasonable in this case... CH rules this class

    def __init__(self, load_from_dict=None, owner_id=None):
        self.id = None # pylint: disable=invalid-name
        self.name = ''
        self.owner_id = None
        self.started = None
        self.completed = None
        self._started_at = None
        self._completed_at = None
        self._started_at_override = None
        self._completed_at_override = None

        if load_from_dict is not None and isinstance(load_from_dict, dict):
            for key in load_from_dict.keys():
                setattr(self, key, load_from_dict[key])

        if owner_id is not None:
            self.owner_id = owner_id


    @property
    def cycle_time_seconds(self):
        """Cycle time in seconds"""
        return (self.completed_at-self.started_at).total_seconds()


    @property
    def started_at(self):
        """User story started timestamps"""
        if self.started_at_override is not None:
            return self.started_at_override

        return self._started_at


    @started_at.setter
    def started_at(self, started_at):
        self._started_at = self._parse_datetime(started_at)


    @property
    def started_at_override(self):
        """User can override started_at using this property"""
        return self._started_at_override


    @started_at_override.setter
    def started_at_override(self, started_at_override):
        self._started_at_override = self._parse_datetime(started_at_override)


    @property
    def completed_at_override(self):
        """User can override complated_at using this property"""
        return self._completed_at_override


    @completed_at_override.setter
    def completed_at_override(self, completed_at_override):
        self._completed_at_override = self._parse_datetime(completed_at_override)


    @property
    def completed_at(self):
        """User story completed at this timestamps"""
        if self._completed_at is not None:
            return self._completed_at

        return datetime.datetime.now()


    @completed_at.setter
    def completed_at(self, completed_at):
        self._completed_at = self._parse_datetime(completed_at)


    @classmethod
    def _parse_datetime(cls, src):
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
