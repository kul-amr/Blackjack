from blackjack import *


def run():

    num_players = int(input("Enter number of players : "))

    blackjack = Blackjack(num_players)

    blackjack.start_game()
    blackjack.get_results()

run()