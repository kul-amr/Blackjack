import itertools
from colored import fg, bg, attr

from hand import *


class Player:

    newid = itertools.count()

    def __init__(self,hand):

        self.id = next(Player.newid)
        self.balance = 1000
        self.hands = []
        hand.bet_amount = self.get_valid_bet_amount()
        self.hands.append(hand)

        self.balance = self.balance - hand.bet_amount

        self.valid_doubledown_or_surrender = True

    def __repr__(self):

        return "Player_{} (balance:{})".format(self.id,self.balance)

    # check if bet amount is valid
    def get_valid_bet_amount(self):

        while True:
            try:
                bet_amount = int(input("for player : {} - ".format(self)))

                if bet_amount > self.balance or bet_amount < 100:
                    raise ValueError
                else:
                    break

            except ValueError:
                print("{}Invalid bet amount!!{}".format(fg(196), attr(0)))
                continue

        return bet_amount

    # depending on player hand, asking for user input to hit/stay/split/doubledown/surrender
    def player_hand_action(self,deck):

        for p_hand in self.hands:
            print("\n--------> playing for hand : {}".format(p_hand))

            self.get_action(p_hand,deck)

    def get_action(self,player_hand,deck):

        while player_hand.continue_playing_hand and not player_hand.burst:

            card_vals = [format_card(d) for d in player_hand.cards]

            print("\nPlayer current hand value as : {} for hand : {}".format(player_hand.value, player_hand))
            print("with cards : {} ".format(card_vals))

            if player_hand.split_valid and self.valid_doubledown_or_surrender:
                input_str = "Hit(1) or Stay(0) or DoubleDown(2) or Split(3) or Surrender(4)? "
            elif player_hand.split_valid:
                input_str = "Hit(1) or Stay(0) or Split(3)? "
            elif self.valid_doubledown_or_surrender:
                input_str = "Hit(1) or Stay(0) or DoubleDown(2) or Surrender(4)? "
            else:
                input_str = "Hit(1) or Stay(0)?"

            while True:
                try:
                    action = int(input("\n{} ".format(input_str)))

                    if action in [0, 1, 4]:
                        break
                    elif action in [2,3] and player_hand.bet_amount < self.balance:
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("{}Invalid Choice or insufficient balance!!{}".format(fg(196), attr(0)))
                    continue

            self.valid_doubledown_or_surrender = False

            if action == 1:
                self.hit(player_hand, deck)
                card_vals = [format_card(d) for d in player_hand.cards]

                if player_hand.burst:
                    print("\n{}Player hand : {} burst{}".format(fg(196), player_hand, attr(0)))
                    print("with cards : {}".format(card_vals))
                    player_hand.continue_playing_hand = False
                    # break
            elif action == 0:
                player_hand.continue_playing_hand = False
            elif action == 2:
                # double the bet amount and can get only one card

                self.hit(player_hand, deck)
                card_vals = [format_card(d) for d in player_hand.cards]
                player_hand.continue_playing_hand = False

                self.balance = (self.balance - player_hand.bet_amount)
                player_hand.bet_amount += player_hand.bet_amount

                if player_hand.burst:
                    print("\n{}Player hand : {} burst{}".format(fg(196), player_hand, attr(0)))
                    print("with cards : {}".format(card_vals))
                    # break
            elif action == 3 and player_hand.split_valid:
                # split if both cards of the hand are of same value

                new_hand = Hand()
                new_hand.cards = [player_hand.cards.pop()]
                new_hand.bet_amount = player_hand.bet_amount

                self.balance = (self.balance - new_hand.bet_amount)
                self.hands.append(new_hand)

                self.hit(player_hand, deck)
                self.hit(new_hand, deck)

                self.get_action(player_hand,deck)
            elif action == 4:
                # surrender - saving half bet

                player_hand.continue_playing_hand = False
                player_hand.bet_amount = player_hand.bet_amount / 2
                self.balance = self.balance + player_hand.bet_amount

    @staticmethod
    def hit(player_hand, deck):

        player_new_card = deck.pop()
        player_hand.cards.append(player_new_card)

        print("\nPlayer got : {}".format(format_card(player_new_card)))


