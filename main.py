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
    num_players = int(input("How many players will be playing?"))

    while num_players < 2 or num_players > 5:
        print("Invalid input.  Please choose 2 - 5 players")
        num_players = input("How many players will be playing?")

    players = []

    for i in range(num_players):
        name = input("What is player" + str(i + 1) + "'s name?")
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

    # Used to test without causing infinite loop
    # turns = 2

    while not turn_over:

        roll = input("Press r to keep rolling, press q to quit")

        if roll == 'q' and (player.player_score + roll_score < 1000 or num_dice == 0):
            if player.player_score + roll_score < 1000:
                print("Score is less than 1000.  Must continue rolling.")
            else:
                print("All dice have been saved.  Must continue rolling.")
                num_dice = 6
            roll = 'r'

        if roll == 'q':
            turn_over = True
            roll_over = True
            print("Your turn is over")
            return roll_score
        elif roll == 'r' and not roll_over:
            dice = roll_dice(num_dice)
            print(dice)
            score(dice)
            # num_dice -= 1
            # player needs to continue rolling if all dice are saved or score is less than 1000


def score(dice):
    triplet = 0
    scoring = False

    for i in range(7):
        if dice[i] > 0:
            print("You have " + str(dice[i]) + " " + str(i) + "'s")
    print("\n")

    for number, amount in dice.most_common():
        if amount > 0:
            if amount >= 3:
                print("Scoring dice:\n")
                print("You have " + str(amount) + " " + str(number) + "'s")
                del dice[number]
                triplet = number
                scoring = True
            elif number == 1 or number == 5:
                if triplet == 0:
                    print("Scoring dice:\n")
                    scoring = True

                print("You have " + str(amount) + " " + str(number) + "'s")


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
            roll_score = take_turn(game_players[player_number])
            game_players[player_number].player_score = game_players[player_number].player_score + roll_score
            player_number += 1

            if player_number > len(game_players) - 1:
                player_number = 0

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
