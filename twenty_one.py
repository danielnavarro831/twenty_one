import random

player_hold = False
house_hold = False
initial_draw = True
game_over = False

game_num = 1
turn_num = 1
player_victories = 0
house_victories = 0

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

next_card = 0

def reset_game():
    global cards
    global house_hold
    global house_hand
    global player_hold
    global player_hand
    global next_card
    global game_num
    global turn_num
    global initial_draw

    cards = [1, 1, 1, 1,
         2, 2, 2, 2,
         3, 3, 3, 3,
         4, 4, 4, 4,
         5, 5, 5, 5,
         6, 6, 6, 6,
         7, 7, 7, 7,
         8, 8, 8, 8,
         9, 9, 9, 9,
         10, 10, 10, 10,
         10, 10, 10, 10,
         10, 10, 10, 10,
         10, 10, 10, 10]

    next_card = 0
    player_hand = []
    house_hand = []
    player_hold = False
    house_hold = False
    initial_draw = True
    game_num += 1
    turn_num = 1
    play()

def play():
    global initial_draw
    global turn_num
    global game_over
    print("--------------------------------------------------------------")
    print("                       Game: " + str(game_num) + "            *Wins  P:" + str(player_victories) + "  H:" + str(house_victories) + "   /")
    print("-----------------------------------------------------------")
    random.shuffle(cards)
    draw(player_hand)
    draw(house_hand)
    draw(player_hand)
    draw(house_hand)
    initial_draw = False
    while player_hold == False:
        take_turn()
        hold_or_hit()
        turn_num += 1
    while player_hold == True and house_hold == False:
        if game_over == False:
            take_turn()
            house_check()
            turn_num += 1
    if player_hold == True and house_hold == True:
        if game_over == False:
            compare_scores()

def take_turn():
    global turn_num
    print("-------------------------")
    print("   Turn: " + str(turn_num) + "             /")
    print("----------------------")


def draw(hand):
    global next_card
    current_player = ""
    if hand == player_hand:
        player_hand.append(cards[next_card])
        current_player = "Player"
    else:
        house_hand.append(cards[next_card])
        current_player = "House"
    if initial_draw == False:
        print("The " + current_player + " draws: " + str(cards[next_card]))
    else:
        print("The " + current_player + " draws")
    cards.pop(next_card)
    next_card += 1
    if sum(hand) > 21:
        print(current_player + " BUSTS!")
        compare_scores()

def hold_or_hit():
    global player_hold
    loop = True
    while loop == True:
        print("Player Hand: " + str(player_hand) + " = " + str(sum(player_hand)))
        print("House Hand: " + str(house_hand[1:len(house_hand)]) + " = " + str(sum(house_hand[1:len(house_hand)])))
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
        else:
            print("invalid input")

def house_check():
    global house_hold
    if sum(house_hand) < 17:
        draw(house_hand)
    else:
        house_hold = True
        print("The House stays")

def compare_scores():
    global player_victories
    global house_victories
    global game_over
    VictoryScore = 21
    player_score = sum(player_hand)
    house_score = sum(house_hand)
    if player_score == house_score:
        print("Player score: " + str(player_hand) + " = " + str(player_score))
        print("House score: " + str(house_hand) + " = " + str(house_score))
        print("Tie")
    elif player_score > house_score and player_score <= VictoryScore:
        print("Player score: " + str(player_hand) + " = " + str(player_score))
        print("House score: " + str(house_hand) + " = " + str(house_score))
        print("Player wins!")
        player_victories += 1
    elif player_score < house_score and house_score <= VictoryScore:
        print("Player score: " + str(player_hand) + " = " + str(player_score))
        print("House score: " + str(house_hand) + " = " + str(house_score))
        print("House wins!")
        house_victories += 1
    elif player_score > house_score and player_score > VictoryScore:
        print("Player score: " + str(player_hand) + " = " + str(player_score))
        print("House score: " + str(house_hand) + " = " + str(house_score))
        print("House wins!")
        house_victories += 1
    elif house_score > player_score and house_score > VictoryScore:
        print("Player score: " + str(player_hand) + " = " + str(player_score))
        print("House score: " + str(house_hand) + " = " + str(house_score))
        print("Player wins!")
        player_victories += 1
    else:
        print("unforseen situation")
        print("Player score: " + str(player_hand) + " = " + str(player_score))
        print("House score: " + str(house_hand) + " = " + str(house_score))
    loop = True
    while loop == True:
        response = input("Play again? (Yes/No) ")
        response.lower()
        if response == "yes":
            reset_game()
            loop = False
        elif response == "no":
            print("Thanks for playing!")
            game_over = False
            loop = False
        else:
            print("Invalid option")

play()