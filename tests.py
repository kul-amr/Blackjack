# from blackjack_run import *
#
#
# hand1 = Hand()
# hand1.bet_amount = 800
#
# hand2 = Hand()
# hand2.bet_amount = 800
#
# player1 = Player()
# player1.hands.append(hand1)
# player1.balance = player1.balance - hand1.bet_amount
#
# player2 = Player()
# player2.hands.append(hand2)
# player2.balance = player2.balance - hand2.bet_amount
#
# dealer_hand = Hand()
# dealer = Dealer(dealer_hand)
#
#
# def test_check_surrender():
#
#     deck = get_cards_deck(1)
#     shuffle(deck)
#
#     hand1.cards = [{'value':5,'suit':'Hearts'},{'value':5,'suit':'Diamonds'}]
#
#     hand2.cards = [{'value':4,'suit':'Hearts'},{'value':10,'suit':'Diamonds'}]
#
#     dealer_hand.cards = [{'value':10,'suit':'Hearts'},{'value':'Ace','suit':'Diamonds'}]
#
#     dealer_visible_card = dealer_hand.cards[0]
#
#     print("\nDealer visible card as : {} ".format(format_card(dealer_visible_card)))
#
#     players = [player1,player2]
#
#     deck = [d for d in deck if d not in hand1.cards and d not in hand2.cards and d not in dealer_hand.cards]
#
#     start_game(players,dealer,deck)
#
#
# def test_get_cards_deck():
#
#     num_decks= 2
#     cards = get_cards_deck(num_decks)
#
#     count_2_club = [card for card in cards if card['value']==2 and card['suit']=='Clubs']
#
#     print(len(count_2_club))
#
#
# # test_get_cards_deck()
#
# test_check_surrender()
