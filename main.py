from dataclasses import dataclass
from collections import Counter


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

    print(players)
    players[0].player_score = players[0].player_score + 800
    print(players[0].player_score)
    print(players)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Test if creating player works
    # player_test("Rumpelstiltskin")
    get_num_players()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
