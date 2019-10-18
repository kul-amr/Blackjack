import itertools


class Player:

    newid = itertools.count()

    def __init__(self):

        self.id = next(Player.newid)
        self.balance = 1000
        self.hands = []
        self.valid_doubledown_or_surrender = True


    def __repr__(self):

        return "Player_{} (balance:{})".format(self.id,self.balance)
