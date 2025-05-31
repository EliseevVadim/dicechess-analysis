import pandas as pd

from core.api import *


def load_games_summary(player_id: str, games_count: int) -> pd.DataFrame:
    games = load_players_games(player_id, games_count)
    games = games['gameHistoryList']
    summary = [
        {
            'game_id': game['gameId'],
            'color': game['color'],
            'opponent_id': game['historyOpponent']['opponentId'],
            'opponent_name': resolve_nickname(str(game['historyOpponent']['opponentId']), NICKNAMES_PATH)
        }
        for game in games
    ]
    return pd.DataFrame(summary)


def load_games_by_ids(game_ids: list[str], user_id: str) -> dict:
    result = dict()
    for game_id in game_ids:
        result[game_id] = load_game(game_id, f"{GAMES_PATH}/{user_id}")
    return result


def get_game_stats(game: list) -> dict:
    if len(game) == 0:
        return {}
    result = []
    for move in game:
        if len(move) == 0:
            continue
        move_as_list = [record['value'] for record in move]
        result.append({
            'color': 'WHITE' if move_as_list[0].isupper() else 'BLACK',
            'is_dirty': len(set(move_as_list)) < 3
        })
    df = pd.DataFrame(result)
    total_moves = len(df)
    if total_moves == 0:
        return {}
    dirty_moves = df['is_dirty'].sum()

    white_moves = df[df['color'] == 'WHITE']
    black_moves = df[df['color'] == 'BLACK']

    dirty_white = white_moves['is_dirty'].sum()
    dirty_black = black_moves['is_dirty'].sum()

    return {
        'total_moves': total_moves,
        'dirty_moves': dirty_moves,
        'dirty_white': dirty_white,
        'dirty_black': dirty_black,
        'dirty_percent': round(100 * dirty_moves / total_moves, 2) if total_moves else 0.0,
        'dirty_white_percent': round(100 * dirty_white / len(white_moves), 2) if len(white_moves) else 0.0,
        'dirty_black_percent': round(100 * dirty_black / len(black_moves), 2) if len(black_moves) else 0.0,
    }


