from enum import Enum
from typing import List, Dict, Set


class GameConfig:
    def __init__(self, num_player: int, num_rounds: int, num_tries_per_round: int):
        self.num_player = num_player
        self.num_rounds = num_rounds
        self.num_tries_per_round = num_tries_per_round


class GamePlayerRole(Enum):
    SECRET_KEEPER = 1
    GUESSER = 2


class GuessAttempt:
    def __init__(self, player_id: int, guess: str, matches: List[int]):
        self.player_id = player_id
        self.guess = guess
        self.matches = matches


class GameRound:
    def __init__(self, player_to_role: Dict[int, GamePlayerRole], secret_word_length: int):
        self.player_to_role = player_to_role
        self.secret_word_length = secret_word_length
        self.attempts = []
        self.current_word_with_markup = ['_'] * secret_word_length
        self.guessed_characters = set()

    def add_attempt(self, attempt: GuessAttempt) -> None:
        self.attempts.append(attempt)
        self.guessed_characters = self.guessed_characters.union(attempt.guess)
        for matched_position in attempt.matches:
            self.current_word_with_markup[matched_position] = attempt.guess

    def get_already_guessed_characters(self) -> Set[str]:
        return self.guessed_characters

    def get_current_word_with_markup(self) -> str:
        return ' '.join(self.current_word_with_markup)

    def get_incorrect_guesses(self) -> Set[str]:
        return {attempt.guess for attempt in self.attempts if len(attempt.matches) == 0}

    def has_guessed_the_word(self) -> bool:
        return '_' not in self.current_word_with_markup

    def calculate_players_scores(self) -> Dict[int, int]:
        """
        Secret keeper wins 10 points per not guessed character.
        Guesser wins 10 points per guessed character.
        Besides these, if guessers win the round, each guesser gets 10 points; if secret keeper wins, it gets x points
        where x is the highest points among guessers
        """
        secret_keeper_player_id = \
            [player_id for player_id, role in self.player_to_role.items() if role == GamePlayerRole.SECRET_KEEPER][0]
        player_to_score = {player_id: 0 for player_id in self.player_to_role.keys()}
        total_guessed_length = 0
        for attempt in self.attempts:
            guessed_length = len(attempt.matches)
            player_to_score[attempt.player_id] += 10 * guessed_length
            total_guessed_length += guessed_length

        if total_guessed_length == self.secret_word_length:
            for player_id in self.player_to_role:
                if player_id != secret_keeper_player_id:
                    player_to_score[player_id] += 10
        else:
            player_to_score[secret_keeper_player_id] += max(player_to_score.values())
            player_to_score[secret_keeper_player_id] += 10 * (self.secret_word_length - total_guessed_length)
        return player_to_score
