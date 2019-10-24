from random import shuffle

from dealer import *
from hand import *
from player import *
from tools import *


suits = ['Spades','Hearts','Clubs','Diamonds']
values = [i for i in range(2,11)] + ['Jack','Queen','King','Ace']

class Blackjack:

    def __init__(self, num_of_players):

        self.deck = self.get_cards_deck(num_of_players)
        shuffle(self.deck)

        self.dealer = Dealer(Hand())

        print("\nEnter betting amount for players : ")

        self.players = [Player(Hand()) for i in range(num_of_players)]

        for player in self.players:
            player.hands[0].cards = [self.deck.pop(), self.deck.pop()]

        self.dealer.hand.cards = [self.deck.pop(),self.deck.pop()]

        self.winners = []
        self.loosers = []
        self.tie = []

    def get_cards_deck(self,num_players):

        num_decks = 0

        for i in range(0, num_players, 4):
            num_decks += 1

        return [{'value': val, 'suit': suit} for val in values for suit in suits for _ in range(num_decks)]

    def start_game(self):

        print("\nDealer visible card as : {} ".format(format_card(self.dealer.hand.cards[0])))

        print(
            "\n===========================================Players starting===========================================\n")

        for player in self.players:
            print("\n\n{}===========> currently playing player is : {}{}".format(fg(214), player, attr(0)))
            player.player_hand_action(self.deck)

        dealer_card_vals = [format_card(d_card) for d_card in self.dealer.hand.cards]

        print("\n===========================================All players played===========================================\n")
        print("\ndealer hand value as : {} ".format(self.dealer.hand.value))
        print("with cards : {} ".format(dealer_card_vals))

        while self.dealer.hand.value < 17:

            self.dealer.hit(self.deck)
            dealer_card_vals = [format_card(d_card) for d_card in self.dealer.hand.cards]

            print("\ndealer hand value as : {} ".format(self.dealer.hand.value))
            print("with cards : {} ".format(dealer_card_vals))

            if self.dealer.hand.burst:
                print("{}dealer burst, players who did not burst will win{}".format(fg(34), attr(0)))
                break

        self.check_winner()

    # compare the dealer and players hands
    def check_winner(self):

        if self.dealer.hand.blackjack:
            print("{}Blackjack!! - dealer wins{}".format(fg(196), attr(0)))

            for player in self.players:
                for p_hand in player.hands:
                    if p_hand.blackjack:  # dealer pushing hand
                        player.balance = (player.balance + p_hand.bet_amount)
                        self.tie.append({"player": player, "hand": p_hand})
                    else:
                        self.loosers.append({"player": player, "hand": p_hand})
        elif self.dealer.hand.burst:  # dealer bursts
            for player in self.players:
                for p_hand in player.hands:
                    if p_hand.burst:
                        self.loosers.append({"player": player, "hand": p_hand})
                    elif p_hand.blackjack:
                        player.balance = (player.balance + 2.5 * p_hand.bet_amount)
                        self.winners.append({"player": player, "hand": p_hand})
                    else:
                        player.balance = (player.balance + 2 * p_hand.bet_amount)
                        self.winners.append({"player": player, "hand": p_hand})
        else:
            for player in self.players:
                for p_hand in player.hands:
                    if p_hand.blackjack:
                        player.balance = (player.balance + 2.5 * p_hand.bet_amount)
                        self.winners.append({"player": player, "hand": p_hand})
                    elif p_hand.value > self.dealer.hand.value and not p_hand.burst:
                        player.balance = (player.balance + 2 * p_hand.bet_amount)
                        self.winners.append({"player": player, "hand": p_hand})
                    elif p_hand.value == self.dealer.hand.value:
                        player.balance = (player.balance + p_hand.bet_amount)
                        self.tie.append({"player": player, "hand": p_hand})
                    else:
                        self.loosers.append({"player": player, "hand": p_hand})

    # populate result
    def get_results(self):

        print("\n===========================================Results===========================================")

        if len(self.winners) > 0:
            print("\nwinner players as : {}\n".format(self.winners))

        if len(self.loosers) > 0:
            print("\nlooser players as : {}\n".format(self.loosers))

        if len(self.tie) > 0:
            print("\ntie as : {}\n".format(self.tie))
