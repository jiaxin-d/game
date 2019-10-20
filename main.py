from typing import List, Set

from helpers import get_input_with_validation
from game import Game
from models import GameConfig
from players import GamePlayer, HumanGamePlayer, ComputerGamePlayer


def create_player(player_id: int) -> GamePlayer:
    player_name = input(f'What\'s the name for player {player_id}?')
    player_type = get_input_with_validation(
        f'Is {player_name} a human player or a computer player? 1: human; 2: computer', {'1', '2'})

    if player_type == '1':
        return HumanGamePlayer(player_id, player_name)
    elif player_type == '2':
        difficulty = int(get_input_with_validation('What\'s the difficulty level for computer player? (1- 10)',
                                               [str(v) for v in list(range(1, 11))]))
        max_word_length = int(get_input_with_validation('What\'s the max word length for computer player? (1- 20)',
                                                    [str(v) for v in list(range(1, 21))]))
        return ComputerGamePlayer(player_id, player_name, difficulty, max_word_length)
    else:
        raise Exception(f'Invalid player type {player_type}')


def create_players(game_config: GameConfig) -> List[GamePlayer]:
    return [create_player(player_id) for player_id in range(game_config.num_player)]


if __name__ == '__main__':
    config = GameConfig(2, 1, 6)
    players = create_players(config)
    game = Game(config, players)
    game.start_game()
