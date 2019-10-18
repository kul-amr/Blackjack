Blackjack rules used :

If player gets blackjack, payment is 3:2.
If dealer and player both get blackjack then dealer pushes the deal back - player neither gains nor looses.
If dealer bursts, player/s who had not burst will get 1:1 payment.
If player bursts, irrespective of dealers status(blackjack or burst), player looses money.


Action options :

Hit(1)          => draw card
Stay(0)         => do nothing
DoubleDown(2)   => doubles the bet and can draw only one card, available only on first hand
Split(3)        => if both the cards from a hand are of same value then can split this hand into
                    two hands and add additional bet amount as of original hand.
Surrender(4)    => no card draw but can save half of the bet if dealer hand is too strong
                    than what you have, available only on first hand


Execution steps:

1. Create virtual environment (python3) and install requirements.txt.
2. Execute run.py.
3. Enter the number of players (num of card decks will be calculated as per numplayers- considering a deck for upto 4 players).
4. Enter betting amount for every player (min 100,max 1000).
5. In each player's turn, check the corresponding hand's cards and dealer's one visible card
   and then select available options tomaximize sum upto 21.
6. If dealer or player cards sum > 21 then burst => loose bet amount, if sum = 21 then Blackjack -> wins 3:2 of bet amount
   and if no blackjack or burst then comapre with dealer hand value and either get 1:1 money of bet amount or loose.