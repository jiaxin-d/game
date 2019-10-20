import os
from typing import Set

from termcolor import colored, cprint

from models import GameRound


def get_input_with_validation(message: str, valid_inputs: Set[str]) -> str:
    input_str = input(message)
    while input_str not in valid_inputs:
        input_str = input(f'Invalid input! Please try again. {message}')
    return input_str


def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def print_hangman(game_round: GameRound) -> None:
    hangman = [colored("/", "blue", attrs=["bold"]),
               colored("\\", "blue", attrs=["bold"]),
               colored("|", "red", attrs=["bold"]),
               colored("-", "red", attrs=["bold"]),
               colored("-", "red", attrs=["bold"]),
               colored("O", "cyan", attrs=["bold"])]
    incorrect_guesses = list(game_round.get_incorrect_guesses())
    to_print = [hangman[i] if i < len(incorrect_guesses) else " " for i in range(len(hangman))]

    pole = colored('|', "magenta", attrs=["bold"])
    cprint("     ___", "magenta")
    cprint("    /   |", "magenta")
    print("    {0}   {1}    Incorrect guesses:".format(to_print[5], pole))
    print("   {0}{1}{2}  {3}    {4}".format(to_print[3], to_print[2], to_print[4], pole, incorrect_guesses))
    print("   {0} {1}  {2}".format(to_print[0], to_print[1], pole))
    cprint("       ___\n", "magenta")


def print_guesses_remaining(tries_left: int):
    print(f'Guessers, you have {tries_left} tries left.')


def print_current_word(game_round: GameRound) -> None:
    print(f'The current word is: {game_round.get_current_word_with_markup()}')


def refresh_screen(game_round: GameRound) -> None:
    clear_screen()
    print_hangman(game_round)
    print_current_word(game_round)
