class Noise:
    def __init__(self, blob, pins):
        self.__blob = blob
        # TODO: figure out how to map to noise report number
        # I think there's a noise report data file somewhere that's roughly:
        # {noise mId, sort number, banner sprite}
        self._mId = int(blob['mId'])
        self._exp = int(blob['mExp'])
        self._pinxp = int(blob['mBp'])
        self._drops = {diff: (pins[pin_id], rate)
                for diff, pin_id, rate in zip(
                    ['easy', 'normal', 'hard', 'ultimate'], # TODO: loc?
                    blob['mDrop'],
                    blob['mDropRate']
                )
        }
        self._level = int(blob['mLevel'])
        self._days = set()

    def __lt__(self, other):
        return self._mId < other._mId

    @property
    def ID(self):
        return self._mId

    
    @property
    def drops(self, diff=None):
        if not diff:
            return self._drops
        else:
            return self._drops.get(diff, None)

    def addDay(self, day):
        # TODO: enum of days
        # based off the enemyGroups data file days
        self._days.add(day)

