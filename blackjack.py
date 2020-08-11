#  TODO create start with 2 cards for player and 1 card for dealer
#  TODO build hit function to ask for another card
#  TODO build bust function for when player goes over 21
#  TODO build doubling function, where player doubles bet, and gets one more card (can call hit function)
#  TODO build split function where player has 2 of a kind, pair is split to two new hands, each hand worth original bet
#  can only split on first hand, or first play off of a split (can be recursive)
#  can double on split hands
#  face cards are worth 10, Ace worth 1 or 11 based on best use case

import random
import dbm
dealer_hand = []
dealer_total = 0


def clear_card_draw():
    #  clears the card draw database by creating a new empty one
    with dbm.open('card_draw', 'n') as cd:
        cd.close()


def card_draw():
    #  returns  value of drawn card from deck
    deck = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
    x = str(random.choice(deck))
    with dbm.open('card_draw', 'c') as cd:
        if cd.get(x) is None:
            cd[x] = '1'
            return x
        elif cd[x].decode("utf-8") == '1':
            cd[x] = '2'
            return x
        elif cd[x].decode("utf-8") == '2':
            cd[x] = '3'
            return x
        elif cd[x].decode("utf-8") == '3':
            cd[x] = '4'
            return x
        elif cd[x].decode("utf-8") == '4':
            card_draw()


def dealer_hand_draw(f_dealer_total):
    #  draws the dealer's hand, always call with 0
    global dealer_hand
    global dealer_total
    dealer_total = f_dealer_total
    if f_dealer_total <= 17:
        x = str(card_draw())
        dealer_hand.append(x)
        if x == 'A':
            if f_dealer_total <= 10:
                f_dealer_total = f_dealer_total + 10
                dealer_hand_draw(f_dealer_total)
            elif f_dealer_total > 10:
                f_dealer_total = f_dealer_total + 1
                dealer_hand_draw(f_dealer_total)
        elif x == 'J' or x == 'Q' or x == 'K':
            f_dealer_total = f_dealer_total + 10
            dealer_hand_draw(f_dealer_total)
        else:
            f_dealer_total = f_dealer_total + int(x)
            dealer_hand_draw(f_dealer_total)
    elif 17 < f_dealer_total:
        return f_dealer_total


clear_card_draw()  # puts all cards back in the deck
dealer_hand_draw(dealer_total)
print("Dealer's first card is: ", dealer_hand[0])
print("Dealer's Full Hand: ", dealer_hand)
print("Dealer's Total: ", dealer_total)
if dealer_total > 21:
    print('Dealer Busts!')
