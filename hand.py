import itertools
from tools import *


class Hand:

    handid = itertools.count()

    def __init__(self):

        self.id = next(Hand.handid)
        self.cards = []
        self.bet_amount = 0
        self.continue_playing_hand = True

    @property
    def value(self):

        vals = [card['value'] for card in self.cards]

        hand_sum = sum(get_card_val(card) for card in self.cards)

        if 'Ace' in vals:

            if hand_sum > 21:
                hand_sum -= 10

        return hand_sum

    @property
    def burst(self):

        if self.value>21:
            return True

        return False

    @property
    def blackjack(self):

        if self.value==21:
            return True

        return False

    @property
    def split_valid(self):

        if len(self.cards) == 2:
            if get_card_val(self.cards[0]) == get_card_val(self.cards[1]):
                return True

        return False

    def __repr__(self):

        return "Hand_{}".format(self.id)

