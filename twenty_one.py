import random
import os

#Vars
player_hold = False
house_hold = False
initial_draw = True
game_over = False
bust = False

#Debug vars
debug = "pumpkineater"
debugging_player = False
debugging_house = False
debug_value = 0
forcing_bust = False

victory_score = 21
game_num = 1
turn_num = 1
player_victories = 0
house_victories = 0

#Deck
cards = [1, 1, 1, 1,
         2, 2, 2, 2,
         3, 3, 3, 3,
         4, 4, 4, 4,
         5, 5, 5, 5,
         6, 6, 6, 6,
         7, 7, 7, 7,
         8, 8, 8, 8,
         9, 9, 9, 9,
         10, 10, 10, 10, #Tens
         10, 10, 10, 10, #Jacks
         10, 10, 10, 10, #Queens
         10, 10, 10, 10] #Kings

player_hand = []
house_hand = []

#Debug tools
def enable_debug():
    global debugging_player
    global debugging_house
    global debug_value
    loop = True
    while loop == True:
        response = input("Debug house or player? ")
        response.lower()
        if response == "player":
            debugging_player = True
            loop = False
        elif response == "house":
            debugging_house = True
            loop = False
        else:
            print("Invalid response")
    loop = True
    while loop == True:
        print("Enter a value between 1 and 10")
        print("For aces (11) input 1")
        response = input("Input desired card value: ")
        if(response.isdigit()) and int(response) <= 10:
            debug_value = int(response)
            loop = False
            reset_game()
        else:
            print("Input a valid amount")

def force_bust():
    global forcing_bust
    loop = True
    while loop == True:
        response = input("Force player or house bust? ")
        response.lower()
        forcing_bust = True
        if response == "player":
            draw(player_hand)
            loop = False
        elif response == "house":
            draw(house_hand)
            loop = False
        else:
            ("Invalid response")

def cheat(card_value): #Call method before initial card draw in play()
    global cards
    counter = 0
    for card in cards:
        if card == card_value:
            cards[counter] = cards[0]
            cards[0] = card_value
        counter +=1

def version():
    print("-----------------------------------------------------------------------------------------------------------------------")
    print("                                     21 Card Game - Code by Daniel Navarro                                    ver: 1.13")
    print("-----------------------------------------------------------------------------------------------------------------------")

def rules():
    print("Rules:")
    print("Each player is dealt 2 cards")
    print("Each turn, each player will be asked if they would like to hit (draw) or hold")
    print("The player with the closest score to 21 wins")
    print("Aces will automatically switch between 11 and 1 to accomodate the player's current score")

def reset_game():
    global cards
    global house_hold
    global house_hand
    global player_hold
    global player_hand
    global game_num
    global turn_num
    global initial_draw
    global bust
    global forcing_bust

#Reset deck to 52 cards
    cards = [1, 1, 1, 1,
         2, 2, 2, 2,
         3, 3, 3, 3,
         4, 4, 4, 4,
         5, 5, 5, 5,
         6, 6, 6, 6,
         7, 7, 7, 7,
         8, 8, 8, 8,
         9, 9, 9, 9,
         10, 10, 10, 10, #Tens
         10, 10, 10, 10, #Jacks
         10, 10, 10, 10, #Queens
         10, 10, 10, 10] #Kings
#Initialize Vars
    player_hand = []
    house_hand = []
    player_hold = False
    house_hold = False
    initial_draw = True
    bust = False
    forcing_bust = False
    game_num += 1
    turn_num = 1
#Start the game
    play()

def play():
    global initial_draw
    global turn_num
    global game_over
#Display Game Number Banner
    print("--------------------------------------------------------------")
    print("                       Game: " + str(game_num) + "           * Wins  P:" + str(player_victories) + "  H:" + str(house_victories) + "   /")
    print("-----------------------------------------------------------")
#Shuffle Deck and Deal Cards    
    random.shuffle(cards)
    if debugging_player == True:
        cheat(debug_value)
    draw(player_hand)
    if debugging_house == True:
        cheat(debug_value)
    draw(house_hand)
    draw(player_hand)
    draw(house_hand)
    initial_draw = False
#Hold or Hit?
    while player_hold == False:
        take_turn()
        hold_or_hit()
        turn_num += 1
#House continues if player holds first
    while player_hold == True and house_hold == False:
        take_turn()
        house_check()
        turn_num += 1
#Game Over
    if player_hold == True and house_hold == True:
        if game_over == False:
            compare_scores()

def take_turn():
    global turn_num
    print("-------------------------")
    print("   Turn: " + str(turn_num) + "             /")
    print("----------------------")


def draw(hand):
    global bust
    global player_hold
    global house_hold
    current_player = ""
    if hand == player_hand:
        if forcing_bust == True:
            player_hand.append(22)
        else:
            player_hand.append(cards[0])
        current_player = "Player"
    else:
        if forcing_bust == True:
            house_hand.append(22)
        else:
            house_hand.append(cards[0])
        current_player = "House"
    if initial_draw == False:
        print("The " + current_player + " draws: " + str(hand[-1]))
    else:
        print("The " + current_player + " draws")
#Check if ace
    if hand[-1] == 1:
        check_ace_value(hand)
    cards.pop(0)
#BUST!
    if sum(hand) > 21:
        bust = True
        check_ace_value(hand)
        if sum(hand) > 21:
            print(current_player + " BUSTS!")
            player_hold = True
            house_hold = True
            compare_scores()
        else:
            bust = False

def hide_hand(hand):
    display = ["?"]
    counter = 0
    for card in hand:
        if counter != 0:
            display.append(card)
        counter +=1
    return display
    

def hold_or_hit():
    global player_hold
    loop = True
    while loop == True:
#Ask the player
        print("Player Hand: " + str(player_hand) + " = " + str(sum(player_hand)))
        if debugging_house == True:
            print("House Hand: " + str(house_hand) + " = " + str(sum(house_hand)))
        else:
            print("House Hand: " + str(hide_hand(house_hand)) + " = " + str(sum(house_hand[1:len(house_hand)])))
#Player Response        
        response = input("Hold or Hit? ")
        response.lower()
        if response == "hold":
            house_check()
            loop = False
            player_hold = True
        elif response == "hit":
            draw(player_hand)
            house_check()
            loop = False
        elif response == "bust":
            force_bust()
            loop = False
        else:
            print("invalid input")

def house_check():
    global house_hold
    global game_over
#Casino Requirement
    if game_over == False:
        if sum(house_hand) < 17:
            draw(house_hand)
        else:
            house_hold = True
            print("The House stays")

def check_ace_value(hand):
    hand_total = sum(hand)
    counter = 0
    if bust == True:
        for card in hand:
            if hand[counter] == 11:
                if hand_total - 10 <= victory_score:
                    hand[counter] = 1
            counter +=1
    else:
        for card in hand:
            if hand[counter] == 1:
                if hand_total + 10 <= victory_score:
                    hand[counter] = 11
            counter +=1

def compare_scores():
    global player_victories
    global house_victories
    global game_over
    global victory_score
    global debugging_player
    global debugging_house
#Show Hands
    player_score = sum(player_hand)
    house_score = sum(house_hand)
#Check Win Conditions
    if player_score == house_score:
        print("Player score: " + str(player_hand) + " = " + str(player_score))
        print("House score: " + str(house_hand) + " = " + str(house_score))
        print("Tie")
    elif player_score > house_score and player_score <= victory_score:
        print("Player score: " + str(player_hand) + " = " + str(player_score))
        print("House score: " + str(house_hand) + " = " + str(house_score))
        print("Player wins!")
        player_victories += 1
    elif player_score < house_score and house_score <= victory_score:
        print("Player score: " + str(player_hand) + " = " + str(player_score))
        print("House score: " + str(house_hand) + " = " + str(house_score))
        print("House wins!")
        house_victories += 1
    elif player_score > house_score and player_score > victory_score:
        print("Player score: " + str(player_hand) + " = " + str(player_score))
        print("House score: " + str(house_hand) + " = " + str(house_score))
        print("House wins!")
        house_victories += 1
    elif house_score > player_score and house_score > victory_score:
        print("Player score: " + str(player_hand) + " = " + str(player_score))
        print("House score: " + str(house_hand) + " = " + str(house_score))
        print("Player wins!")
        player_victories += 1
    else:
        print("unforseen situation")
        print("Player score: " + str(player_hand) + " = " + str(player_score))
        print("House score: " + str(house_hand) + " = " + str(house_score))
#Play Again?    
    loop = True
    debugging_player = False
    debugging_house = False
    while loop == True:
        response = input("Play again? (Yes/No) ")
        response.lower()
        if response == "yes":
            reset_game()
            loop = False
        elif response == "no":
            print("Thanks for playing!")
            game_over = True
            loop = False
        elif response == debug:
            enable_debug()
            loop = False
        else:
            print("Invalid option")

def set_window_size():
    os.system('mode con: cols=120 lines=40')

#Set Window Size
set_window_size()
#Display Title and Version
version()
#Display Rules
rules()
#Initialize Game
play()