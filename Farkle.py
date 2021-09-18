from dataclasses import dataclass
from collections import Counter
import random


@dataclass
class Player:
    """Class for holding the player attributes"""
    player_name: str
    reached_10000: bool = False
    player_score: int = 0


# This function prompts for the number of players and the name of each player
# The output is a list of players
def get_num_players():
    index = 0

    try:
        num_players = int(input("How many players will be playing?\n"))
    except ValueError:
        num_players = int(input("Invalid input.  Please choose 2 - 5 players.\n How many players will be playing?\n"))

    while num_players < 2 or num_players > 5:
        num_players = int(input("Invalid input.  Please choose 2 - 5 players.\n How many players will be playing?\n"))

    players = []

    for index in range(num_players):
        name = input("What is player" + str(index + 1) + "'s name?\n")
        players.append(Player(name))

    return players


# This function takes an int value for number of dice and generates a random value between 1 and 6
# The output is a counter of dice with those values (using the collections module)
def roll_dice(number_of_dice):
    dice = Counter([random.randint(1, 6) for i in range(0, number_of_dice)])
    return dice


# This function takes a Player and processes that player's turn for them
# The output is an int value for this_turn_score
def take_turn(player):
    turn_over = False
    roll_over = False
    num_dice = 6
    roll_score = 0
    this_turn_score = 0

    while not turn_over:

        roll = input("Press r to keep rolling, press q to quit\n")

        # If all dice have been saved or their score is less than 1000, player must re-roll
        if num_dice == 0:
            # If current player has already won, no need to force roll
            if player.player_score >= 10000:
                if player == calculate_winner(game_players):
                    roll = 'q'
            else:
                num_dice = 6
                print("\nAll dice have been saved.  You must keep rolling")
                roll = 'r'
        elif roll == 'q' and (player.player_score + this_turn_score < 1000):
            print("\nScore is less than 1000.  Must continue rolling.")
            roll = 'r'

        if roll == 'q':
            turn_over = True
            roll_over = True
            print("Your turn is over\n")
            return this_turn_score
        elif roll == 'r' and not roll_over:
            dice = roll_dice(num_dice)
            roll_score, num_dice = scoring(dice, num_dice)
            if not roll_score:
                roll_over = True
                turn_over = True
                this_turn_score = 0
            else:
                this_turn_score += roll_score
                print("Your current roll score is " + str(this_turn_score))
                print("If you stopped now, your total score would be " + str(player.player_score + this_turn_score)
                      + "\n")

    return this_turn_score


# This function takes the counter and the number of dice, calculates the score for a roll and tracks number of dice
# that are left.
# Output is the score for the roll and the number of dice that haven't been saved
def scoring(dice, num_dice):
    triplet = 0
    double_triplet = 0  # this is for the case of six of the same value
    # Scoring values
    ones = 0
    fives = 0

    scoring_dice = False
    score = 0
    i = 0

    for i in range(7):
        if dice[i] > 0:
            print("You have " + str(dice[i]) + " " + str(i) + "'s")
    print("\n")

    print("Scoring dice:\n")

    # This uses the most_common() function of collections to avoid going through all possible dice values
    for number, amount in dice.most_common():
        if amount == 6:
            print("You have two triplets of " + str(number) + "s")
            double_triplet = number
            scoring_dice = True
        elif amount >= 3:
            print("You have a triplet of " + str(number) + "s")

            # We only want three in this triplet but other scoring dice of the same value must be scored
            if amount > 3:
                if number == 1:
                    ones = amount - 3
                    print("You have " + str(ones) + " additional " + str(number) + "s")
                if number == 5:
                    fives = amount - 3
                    print("You have " + str(fives) + " additional " + str(number) + "s")

            # We don't want to recount the triplet if they are 1s or 5s
            del dice[number]
            triplet = number
            scoring_dice = True
        elif number == 1:
            ones = amount
            print("You have " + str(ones) + " " + str(number) + "'s")
            scoring_dice = True
        elif number == 5:
            fives = amount
            print("You have " + str(fives) + " " + str(number) + "'s")
            scoring_dice = True

    if not scoring_dice:
        print("You have no scoring dice.  Your turn is over\n")
        score = 0
        return score, num_dice
    else:
        # No good reason not to save two triplets
        if double_triplet:
            score += (2 * triplet_score(double_triplet))
            print("\nSaving both triplets")
            num_dice = 0
        # Prompt player which dice they'd like to save
        else:
            if triplet:
                keep_dice = input("\nWould you like to keep your triplet of " + str(triplet) + "s? y or n\n")
                while keep_dice not in ('y', 'n'):
                    keep_dice = input("Please type either y or n.  Would you like to keep your triplet of "
                                      + str(triplet) + "s? y or n\n")
                if keep_dice == 'y':
                    score += triplet_score(triplet)
                    num_dice -= 3
                    print("You now have " + str(num_dice) + " dice remaining\n")
                keep_dice = 'n'
            if ones:
                keep_dice = input("\nWould you like to keep your 1s? y or n\n")
                while keep_dice not in ('y', 'n'):
                    keep_dice = input("Please type either y or n. Would you like to keep your 1s? y or n\n")
                if keep_dice == 'y':
                    score += ones * 100
                    num_dice -= ones
                    print("You now have " + str(num_dice) + " dice remaining\n")
                keep_dice = 'n'
            if fives:
                keep_dice = input("\nWould you like to keep your 5s? y or n\n")
                while keep_dice not in ('y', 'n'):
                    keep_dice = input("Please type either y or n.  Would you like to keep your 5s? y or n\n")
                if keep_dice == 'y':
                    score += fives * 50
                    num_dice -= fives
                    print("You now have " + str(num_dice) + " dice remaining\n")
                keep_dice = 'n'

    return score, num_dice


# Takes the number of the dice in the triplet
# Output is the triplet score for that number
def triplet_score(triplet):
    if triplet == 1:
        triplet_value = 1000
    else:
        triplet_value = triplet * 100
    return triplet_value


# Takes the list of Players and finds the one with the highest score
# Outputs the winning Player
def calculate_winner(players):
    winner = players[0]

    for i in range(1 - (len(players))):
        if players[i].player_score > winner.player_score:
            winner = players[i]
    print("Congratulations!! " + winner.player_name + " is the winner!!!")


if __name__ == '__main__':
    game_over = False

    # Get the number and list of players
    game_players = get_num_players()

    player_number = 0

    while not game_over:
        # If the current player has reached 10000, then all other players have played their final turn
        if not game_players[player_number].reached_10000:
            print("\n" + game_players[player_number].player_name + "'s turn\n")
            turn_score = take_turn(game_players[player_number])
            # Add the current turn's score to the players game score
            game_players[player_number].player_score = game_players[player_number].player_score + turn_score

            for i in range(len(game_players)):
                print(game_players[i].player_name + " has " + str(game_players[i].player_score)
                      + " points")

            if game_players[player_number].player_score >= 10000 and reached_10000 == False:
                game_players[player_number].reached_10000 = True
                reached_10000 = True
                print(game_players[player_number].player_name + " has reached 10000. All other players take their "
                                                                "final turn")
            player_number += 1

            if player_number > len(game_players) - 1:
                player_number = 0
        else:
            game_over = True

    # All players have had their final turn after a player reached 10000 points so calculate winner
    game_winner = calculate_winner(game_players)
