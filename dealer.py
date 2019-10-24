from tools import *


class Dealer:

    def __init__(self,hand):

        self.name ="Dealer"
        self.hand = hand

    def hit(self, deck):
        dealer_new_card = deck.pop()
        self.hand.cards.append(dealer_new_card)

        print("\ndealer got : {}".format(format_card(dealer_new_card)))

