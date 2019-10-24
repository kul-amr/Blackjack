

def get_card_val(card):
    card_val = card['value']

    if card_val in range(2, 11):
        return card_val
    elif card_val == 'Ace':
        return 11
    else:
        return 10


def format_card(card):

    return ' - '.join(str(x) for x in card.values())
