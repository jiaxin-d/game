import random
import requests
import string
from typing import List

from helpers import get_input_with_validation
from models import GameRound


class GamePlayer:
    def __init__(self, player_id: int, name: str):
        self.id = player_id
        self.name = name
        self.chosen_word = None

    def guess(self, game_round: GameRound) -> str:
        pass

    def choose_word(self) -> None:
        pass

    def tell_word_length(self) -> int:
        return len(self.chosen_word)

    def tell_secret_word(self) -> str:
        pass

    def check(self, game_round: GameRound, guess: str) -> List[int]:
        pass


class HumanGamePlayer(GamePlayer):
    def guess(self, game_round: GameRound) -> str:
        guess = input('What would you guess this time?')
        while guess in game_round.get_already_guessed_characters():
            guess = input('What would you guess this time?')
        return guess

    def choose_word(self) -> None:
        get_input_with_validation('Please choose a word and keep it to yourself! Have you decided? Yes or No?',
                                  {'yes', 'YES', 'Yes', 'Y', 'y'})

    def tell_word_length(self) -> int:
        return int(input('What\'s the length of the word you chose?'))

    def tell_secret_word(self) -> str:
        return input('Secret keeper. Can you share the word in your mind?')

    def check(self, game_round: GameRound, guess: str) -> List[int]:
        print(f'Secret keeper player, please verify.')
        input_str = input(
            f'Which positions does \'{guess}\' locate in your chosen word? Please give back the positions '
            f'separated by \',\'. The leftmost is position 0.')
        if len(input_str) == 0:
            return []
        return [int(position) for position in input_str.split(',')]


class ComputerGamePlayer(GamePlayer):
    WORD_API = 'http://app.linkedin-reach.io/words'

    def __init__(self, player_id: int, name: str, difficulty: int, max_word_length: int):
        super(ComputerGamePlayer, self).__init__(player_id, name)
        self.difficulty = difficulty
        self.max_word_length = max_word_length

    def guess(self, game_round: GameRound) -> str:
        return random.choice(list(set(string.ascii_lowercase).difference(game_round.get_already_guessed_characters())))

    def choose_word(self) -> None:
        self.chosen_word = random.choice(self.load_all_words())

    def tell_secret_word(self) -> str:
        return self.chosen_word

    def check(self, game_round: GameRound, guess: str) -> List[int]:
        return [position for position, letter in enumerate(self.chosen_word) if letter == guess]

    def load_all_words(self) -> List[str]:
        return requests.get(self.WORD_API, {'difficulty': self.difficulty,
                                            'maxLength': self.max_word_length}).text.split()
