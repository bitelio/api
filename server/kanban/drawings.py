import cached_property

import stations


class Card(stations.Card):
    def __init__(self, data, board):
        super(Card, self).__init__(data, board)
        self._major_changes_ = False

    @property
    def major_changes(self):
        """ Returns True if the card has been to one of the 'major changes' lanes """
        self.start_date
        return self._major_changes_

