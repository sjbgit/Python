# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
message = ""
wins = 0
losses = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        output = 'Hand contains: '
        for card in self.cards:
            output += str(card) + ' '
            
        return output   

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = 0
        has_ace = False
        for card in self.cards:
            rank = card.get_rank()
            if (rank == 'A'):
                has_ace = True
          
            value += VALUES[rank]  
            
        if (value <= 11 and has_ace == True):
            value += 10
        
        return value
   
    def draw(self, canvas, pos):
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += CARD_SIZE[0]
  
# define deck class 
class Deck:
    def __init__(self):
        self.cards = [Card(s, r) for s in SUITS for r in RANKS]
      
    def shuffle(self):
        random.shuffle(self.cards)
        
    def deal_card(self):
        #print '\ndeal_card ' + str(len(self.cards))
        card = self.cards[0]
        self.cards.remove(card)
        return card
    
    def __str__(self):
        output = 'Deck contains: '
        for c in self.cards:
            output += str(c) + ' '
        return output
    
    def card_count(self):
        return len(self.cards)

#define event handlers for buttons
def deal():
    global outcome, in_play, dealer_hand, player_hand, deck, message, losses

    deck = Deck()
    
    dealer_hand = Hand()
    player_hand = Hand()
    
    deck.shuffle()
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    outcome = ''
    message = "Hit or Stand?"
    
    if (in_play == True):
        losses += 1
        outcome = "Dealer Wins - Player Aborted Game"
        
    in_play = True
    #output_short()

def hit():
    global outcome, in_play, message, losses
 
    if (in_play == False):
        return
    
    outcome = ""
    message = ""
    
    # if the hand is in play, hit the player
    if (in_play == True):
        player_hand.add_card(deck.deal_card())
    
    # if busted, assign a message to outcome, update in_play and score
    if (player_hand.get_value() > 21):
        in_play = False
        outcome = 'Dealer Wins - Player Busted'
        losses += 1
        message = "New Deal?"
    
    if (in_play == True):
        message = "Hit or Stand?"
        
    #output_short()
       
def stand():
    global outcome, in_play, message, losses, wins
 
    if (in_play == False):
        return    
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while (dealer_hand.get_value() < 17):
        dealer_hand.add_card(deck.deal_card())
    # assign a message to outcome, update in_play and score
    in_play = False
    if (player_hand.get_value() == dealer_hand.get_value()):
        outcome = 'Tie - Dealer Wins'
        losses += 1
    elif (dealer_hand.get_value() > 21):
        outcome = 'Dealer Busted - Player Wins'
        wins += 1
    elif (player_hand.get_value() <= 21 and player_hand.get_value() > dealer_hand.get_value()):
        outcome = 'Player Wins'
        wins += 1
    else:
        outcome = 'Dealer Wins'
        losses += 1
    
    message = "New Deal?"
    #output_short()

# draw handler    
def draw(canvas):
    player_start_position = [100, 300]
    dealer_start_position = [100, 200]
    player_hand.draw(canvas, player_start_position)
    dealer_hand.draw(canvas, dealer_start_position)
    
    if (in_play == True):
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [100 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    
    canvas.draw_text(message, (100, 500), 24, 'White')
    canvas.draw_text(outcome, (100, 550), 24, 'White')
    canvas.draw_text("Wins: " + str(wins) + " Losses: " + str(losses), (100, 150), 50, 'White')
    canvas.draw_text('Blackjack', (100, 75), 75, 'White', 'serif')

def output_short():
    print ''
    print 'Player ' + str(player_hand)
    print 'Player Value: ' + str(player_hand.get_value())
    print 'Dealer ' + str(dealer_hand)
    print 'Dealer Value: ' + str(dealer_hand.get_value()) 
    print 'Outcome: ' + outcome
    
def output_all():
    print ''
    print 'Player ' + str(player_hand)
    print 'Player Value: ' + str(player_hand.get_value())
    print 'Dealer ' + str(dealer_hand)
    print 'Dealer Value: ' + str(dealer_hand.get_value())
    print deck
    print 'Deck length: ' + str(deck.card_count())
    print 'Outcome: ' + outcome

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

#global instances
deck = Deck()
dealer_hand = Hand()
player_hand = Hand()

# get things rolling
deal()
frame.start()



# remember to review the gradic rubric