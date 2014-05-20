# implementation of card game - Memory

import simplegui
import random

cards = []
card_is_showing = []
matched_card_indexes = []
card_range = 8
turns = 0
card_width = 50
card_half_width = card_width / 2
card_height = 100
card_half_height = card_height / 2
clicks_pos = []
click_count = 0

def initialize_cards():
    global cards
    cards = range(1, card_range + 1) + range(1, card_range + 1)
    random.shuffle(cards)

# helper function to initialize globals
def new_game():
    global card_is_showing
    global matched_card_indexes
    global turns
    initialize_cards()
    card_is_showing = []
    matched_card_indexes = []
    turns = 0
    click_count = 0
    for card in cards:
        card_is_showing.append(False)
        matched_card_indexes.append(False)
     
# define event handlers
def mouseclick(pos):
    global card_is_showing
    global click_count
    global clicks_pos
    global last_clicked_index
    global turns
    
    clicked_card_index = pos[0] / card_width
    if (len(clicks_pos) == 1 and clicks_pos[0] == clicked_card_index):
        return #clicked on card that is already turned
    elif matched_card_indexes[clicked_card_index] == True:
        return #clicked on an already matched card
    elif len(clicks_pos) >= 2:
        card_is_showing[clicks_pos[0]] = False
        card_is_showing[clicks_pos[1]] = False
        clicks_pos = []
        
    clicks_pos.append(clicked_card_index)
    card_is_showing[clicked_card_index] = True
    
    if len(clicks_pos) >= 2 and (cards[clicks_pos[0]] == cards[clicks_pos[1]]):
        matched_card_indexes[clicks_pos[0]] = True
        matched_card_indexes[clicks_pos[1]] = True   
        
    click_count += 1
    if (click_count % 2 == 0 and click_count != 0):
        turns += 1
                       
# cards are logically 50x100 pixels in size    
def draw(canvas):
    x = 0
    index = 0
    label.set_text("Turns = " + str(turns))
    for card in cards:
        if (card_is_showing[index] == False and matched_card_indexes[index] == False):
            canvas.draw_polygon([(x, 0), (x + card_width - 1, 0), (x + card_width - 1, card_height), (x,card_height)], 1, 'Blue', 'Blue')
        else:
            canvas.draw_text(str(card), [x + card_half_width - 2, card_half_height], 24, "White")
        x += card_width
        index += 1

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric