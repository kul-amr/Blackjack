from random import shuffle
from colored import fg, bg, attr

from player import *
from dealer import *
from hand import *


suits = ['Spades','Hearts','Clubs','Diamonds']
values = [i for i in range(2,11)] + ['Jack','Queen','King','Ace']


def get_cards_deck(num_decks):

    return [{'value':val,'suit':suit} for val in values for suit in suits for _ in range(num_decks)]


# get players, dealer, cards
def start(num_players):

    num_decks = 0

    for i in range(0,num_players,4):
        num_decks+=1

    deck = get_cards_deck(num_decks)
    shuffle(deck)

    players = get_players(num_players, deck)

    dealer_hand = Hand()
    dealer_hand.cards = [deck.pop(), deck.pop()]

    dealer = Dealer(dealer_hand)
    dealer_visible_card = dealer_hand.cards[0]

    print("\nDealer visible card as : {} ".format(format_card(dealer_visible_card)))

    start_game(players, dealer, deck)


def start_game(players,dealer,deck):

    print("\n===========================================Players starting===========================================\n")

    for player in players:
        print("\n\n{}===========> currently playing player is : {}{}".format(fg(214),player, attr(0)))
        player_action(player,deck)

    dealer_card_vals = [format_card(d_card) for d_card in dealer.hand.cards]

    print("\n===========================================All players played===========================================\n")
    print("\ndealer hand value as : {} ".format(dealer.hand.value))
    print("with cards : {} ".format(dealer_card_vals))

    while dealer.hand.value<17:

        dealer_hit(dealer.hand,deck)
        dealer_card_vals = [format_card(d_card) for d_card in dealer.hand.cards]

        print("\ndealer hand value as : {} ".format(dealer.hand.value))
        print("with cards : {} ".format(dealer_card_vals))

        if dealer.hand.burst:
            print("{}dealer burst, players who did not burst will win{}".format(fg(34), attr(0)))
            break

    check_winner(players, dealer.hand)


def player_action(player,deck):

    for p_hand in player.hands:
        player_hand_action(player,p_hand,deck)


# depending on player hand, asking for user input to hit/stay/split/doubledown/surrender
def player_hand_action(player,p_hand,deck):

    print("\n--------> playing for hand : {}".format(p_hand))

    while p_hand.continue_playing_hand and not p_hand.burst:

        card_vals = [format_card(d) for d in p_hand.cards]

        print("\nPlayer current hand value as : {} for hand : {}".format(p_hand.value, p_hand))
        print("with cards : {} ".format(card_vals))

        while True:

            try:
                if p_hand.split_valid and player.valid_doubledown_or_surrender:
                    action = int(input("\nHit(1) or Stay(0) or DoubleDown(2) or Split(3) or Surrender(4)? "))
                elif p_hand.split_valid:
                    action = int(input("\nHit(1) or Stay(0) or Split(3)? "))
                elif player.valid_doubledown_or_surrender:
                    action = int(input("\nHit(1) or Stay(0) or DoubleDown(2) or Surrender(4)? "))
                else:
                    action = int(input("\nHit(1) or Stay(0)?"))

            except ValueError:
                print("{}Invalid Choice!!{}".format(fg(196), attr(0)))
                continue

            if action in [0,1,2,4]:
                break
            elif action==3 and p_hand.bet_amount < player.balance:
                break
            else:
                print("{}Invalid Choice or insufficient balance!!!!{}".format(fg(196), attr(0)))

        player.valid_doubledown_or_surrender = False

        if action == 1:
            player_hit(p_hand, deck)
            card_vals = [format_card(d) for d in p_hand.cards]

            if p_hand.burst:
                print("\n{}Player hand : {} burst{}".format(fg(196), p_hand, attr(0)))
                print("with cards : {}".format(card_vals))
                break
        elif action == 0:
            p_hand.continue_playing_hand = False
        elif action == 2:
            # double the bet amount and can get only one card

            player_hit(p_hand, deck)
            card_vals = [format_card(d) for d in p_hand.cards]
            p_hand.continue_playing_hand = False

            player.balance = (player.balance - p_hand.bet_amount)
            p_hand.bet_amount += p_hand.bet_amount

            if p_hand.burst:
                print("\n{}Player hand : {} burst{}".format(fg(196), p_hand, attr(0)))
                print("with cards : {}".format(card_vals))
                break
        elif action == 3 and p_hand.split_valid:
            # split if both cards of the hand are of same value

            new_hand = Hand()
            new_hand.cards = [p_hand.cards.pop()]
            new_hand.bet_amount = p_hand.bet_amount

            player.balance = (player.balance - new_hand.bet_amount)
            player.hands.append(new_hand)

            player_hit(p_hand, deck)
            player_hit(new_hand, deck)

            player_hand_action(player, p_hand, deck)
            player_hand_action(player, new_hand, deck)
        elif action == 4:
            # surrender - saving half bet

            p_hand.continue_playing_hand = False
            p_hand.bet_amount = p_hand.bet_amount / 2
            player.balance = player.balance + p_hand.bet_amount


# populate players and hands
def get_players(num_players,deck):

    players = [Player() for i in range(num_players)]

    print("\nEnter betting amount for players : ")

    for player in players:
        hand = Hand()
        hand.bet_amount = get_valid_bet_amount(player)

        hand.cards = [deck.pop(),deck.pop()]
        player.hands.append(hand)
        player.balance = player.balance - hand.bet_amount

    return players


# check if bet amount is valid
def get_valid_bet_amount(player):

    while True:
        try:
            bet_amount = int(input("for player : {} - ".format(player)))

        except ValueError:
            print("{}Invalid bet amount!!{}".format(fg(196), attr(0)))
            continue

        if bet_amount > player.balance or bet_amount<100:
            print("{}Invalid bet amount!!{}".format(fg(196), attr(0)))
            continue
        else:
            break

    return bet_amount


# compare the dealer and players hands
def check_winner(players, dealer_hand):

    result = {}
    result['winners'] = []
    result['loosers'] = []
    result['tie'] = []

    if dealer_hand.blackjack:
        print("{}Blackjack!! - dealer wins{}".format(fg(196), attr(0)))

        for player in players:
            for p_hand in player.hands:
                if p_hand.blackjack:    #dealer pushing hand
                    player.balance = (player.balance + p_hand.bet_amount)
                    result['tie'].append({"player":player,"hand":p_hand})
                else:
                    result['loosers'].append({"player":player,"hand":p_hand})

    elif dealer_hand.burst:          #dealer bursts
        for player in players:
            for p_hand in player.hands:
                if p_hand.burst:
                    result['loosers'].append({"player": player, "hand": p_hand})
                elif p_hand.blackjack:
                    player.balance = (player.balance + 2.5 * p_hand.bet_amount)
                    result['winners'].append({"player":player,"hand":p_hand})
                else:
                    player.balance = (player.balance + 2 * p_hand.bet_amount)
                    result['winners'].append({"player": player, "hand": p_hand})

    else:
        for player in players:
            for p_hand in player.hands:
                if p_hand.blackjack:
                    player.balance = (player.balance + 2.5 * p_hand.bet_amount)
                    result['winners'].append({"player":player,"hand":p_hand})
                elif p_hand.value > dealer_hand.value and not p_hand.burst:
                    player.balance = (player.balance + 2 * p_hand.bet_amount)
                    result['winners'].append({"player": player, "hand": p_hand})
                elif p_hand.value == dealer_hand.value:
                    player.balance = (player.balance + p_hand.bet_amount)
                    result['tie'].append({"player":player,"hand":p_hand})
                else:
                    result['loosers'].append({"player":player,"hand":p_hand})

    get_results(result)


# populate result
def get_results(result):

    print("\n===========================================Results===========================================")

    if len(result['winners']) >0:
        print("\nwinner players as : {}\n".format(result['winners']))

    if len(result['loosers']) > 0:
        print("\nlooser players as : {}\n".format(result['loosers']))

    if len(result['tie'])>0:
        print("\ntie as : {}\n".format(result['tie']))


def player_hit(player_hand,deck):

    player_new_card = deck.pop()
    player_hand.cards.append(player_new_card)

    print("\nPlayer got : {}".format(format_card(player_new_card)))


def format_card(card):

    return ' - '.join(str(x) for x in card.values())


def dealer_hit(dealer_hand,deck):

    dealer_new_card = deck.pop()
    dealer_hand.cards.append(dealer_new_card)

    print("\ndealer got : {}".format(format_card(dealer_new_card)))

