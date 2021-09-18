from dataclasses import dataclass
from collections import Counter
import random


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

@dataclass
class Player:
    """Class for holding the player attributes"""
    player_name: str
    winning_player: bool = False
    player_score: int = 0


def player_test(name):
    player_one = Player(name)
    print(player_one)
    print("Player one's score is " + str(player_one.player_score))
    print("Player one's name is " + player_one.player_name)
    print(player_one.winning_player)


def get_num_players():
    index = 0

    try:
        num_players = int(input("How many players will be playing?"))
    except ValueError:
        num_players = int(input("Invalid input.  Please choose 2 - 5 players.\n How many players will be playing?"))

    while num_players < 2 or num_players > 5:
        num_players = int(input("Invalid input.  Please choose 2 - 5 players.\n How many players will be playing?"))

    players = []

    for index in range(num_players):
        name = input("What is player" + str(index + 1) + "'s name?")
        players.append(Player(name))

    # print(players)
    # players[0].player_score = players[0].player_score + 800
    # print(players[0].player_score)
    # print(players)

    return players


def roll_dice(number_of_dice):
    dice = Counter([random.randint(1, 6) for i in range(0, number_of_dice)])
    return dice


def take_turn(player):
    turn_over = False
    roll_over = False
    num_dice = 6
    roll = 'r'
    roll_score = 0
    this_turn_score = 0

    # Used to test without causing infinite loop
    # turns = 2

    while not turn_over:

        roll = input("Press r to keep rolling, press q to quit")

        if roll == 'q' or ((player.player_score + this_turn_score < 1000) or num_dice == 0):
            if player.player_score + this_turn_score < 1000:
                print("Score is less than 1000.  Must continue rolling.")
            else:
                print("All dice have been saved.  Must continue rolling.")
                num_dice = 6
            roll = 'r'

        if roll == 'q':
            turn_over = True
            roll_over = True
            print("Your turn is over")
            return this_turn_score
        elif roll == 'r' and not roll_over:
            dice = roll_dice(num_dice)
            print(dice)
            roll_score, num_dice = scoring(dice, num_dice)
            if not roll_score:
                roll_over = True
                turn_over = True
                this_turn_score = 0
            else:
                this_turn_score += roll_score
                print(player.player_name + "'s current roll score is " + str(this_turn_score))
                print("If you stopped now, your total score would be " + str(player.player_score + this_turn_score))
            # num_dice -= 1
            # player needs to continue rolling if all dice are saved or score is less than 1000

    return this_turn_score


# This function calculates the score for a roll
# It takes in the list of dice and returns the score
def scoring(dice, num_dice):
    triplet = 0
    ones = 0
    fives = 0
    scoring_dice = False
    score = 0
    keep_dice = 'n'

    # dice tests
    # dice = Counter({2: 4, 1: 1, 5: 1})
    # dice = Counter({1: 6})
    # dice = Counter({5: 5, 6: 1})

    for i in range(7):
        if dice[i] > 0:
            print("You have " + str(dice[i]) + " " + str(i) + "'s")
    print("\n")

    print("Scoring dice:")

    for number, amount in dice.most_common():
        if amount >= 3:
            print("You have a triplet of " + str(number) + "s")
            if amount > 3:
                if number == 1:
                    print("You have " + str(amount) + " " + str(number) + "s")
                    ones = amount - 3
                if number == 5:
                    print("You have " + str(amount) + " " + str(number) + "s")
                    fives = amount
            del dice[number]
            triplet = number
            scoring_dice = True
        elif number == 1:
            if triplet == 1:
                ones = amount - 3
            else:
                ones = amount
            print("You have " + str(ones) + " " + str(number) + "'s")
            scoring_dice = True
        elif number == 5:
            if triplet == 5:
                fives = amount - 3
            else:
                fives = amount
            print("You have " + str(fives) + " " + str(number) + "'s")
            scoring_dice = True

    if not scoring_dice:
        print("You have no scoring dice.  Your turn is over")
        score = 0
        return score, num_dice
    else:
        if triplet:
            keep_dice = input("Would you like to keep your triplet of " + str(triplet) + "s? y or n")
            if keep_dice == 'y':
                score += triplet_score(triplet)
                num_dice -= 3
                print("You now have " + str(num_dice) + " dice remaining")
            keep_dice = 'n'
        if ones:
            keep_dice = input("Would you like to keep your 1s? y or n")
            if keep_dice == 'y':
                score += ones * 100
                num_dice -= ones
                print("You now have " + str(num_dice) + " dice remaining")
            keep_dice = 'n'
        if fives:
            keep_dice = input("Would you like to keep your 5s? y or n")
            if keep_dice == 'y':
                score += fives * 50
                num_dice -= fives
                print("You now have " + str(num_dice) + " dice remaining")
            keep_dice = 'n'

    return score, num_dice


# Takes an int and returns the triplet score
def triplet_score(triplet):
    if triplet == 1:
        triplet_value = 1000
    else:
        triplet_value = triplet * 100
    return triplet_value


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game_over = False

    # Test if creating player works
    # player_test("Rumpelstiltskin")
    game_players = get_num_players()

    print(game_players)

    player_number = 0

    while not game_over:
        if not game_players[player_number].winning_player:
            print("\n" + game_players[player_number].player_name + "'s turn\n\n")
            turn_score = take_turn(game_players[player_number])
            game_players[player_number].player_score = game_players[player_number].player_score + turn_score
            for i in range(len(game_players)):
                print(game_players[i].player_name + " has " + str(game_players[i].player_score)
                      + " points")
            player_number += 1

            if player_number > len(game_players) - 1:
                player_number = 0

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
