import os

import requests
import json

from constants import *
from itertools import groupby

headers = {
    'Authorization': f'{API_KEY}',
    'User-Agent': USER_AGENT
}


def send_authorized_get_request(url):
    response = requests.get(url, headers=headers, cookies=COOKIES)
    try:
        data = json.loads(response.text)
        return data
    except:
        print(response.status_code)
        print(response.text)


def send_authorized_post_request(url, payload):
    response = requests.post(url, json=payload, headers=headers, cookies=COOKIES)
    try:
        data = json.loads(response.text)
        return data
    except:
        print(response.status_code)
        print(response.text)


def load_players_games(player_id: str, games_count: int):
    payload = {
        'filters': {
            'PLAYER_ID': player_id,
            'START_DATE': '1'
        },
        'allowed_times': [],
        'first': 0,
        'isAsc': False,
        'pageSize': games_count,
        'sortColumn': 'DATE',
        'startBets': []
    }
    games = send_authorized_post_request(url=HISTORY_URL, payload=payload)
    return games


def resolve_nickname(player_id: str, nicknames_path: str):
    with open(nicknames_path) as f:
        data = f.read()
    nicknames = dict() if data == '' else json.loads(data)
    if player_id in nicknames:
        return nicknames[player_id]
    result = send_authorized_get_request(f'{PROFILE_URL}/{player_id}')
    try:
        nickname = result['publicProfile']['userName']
    except TypeError:
        nickname = 'BOT' if int(player_id) < 0 else f'DELETED_{player_id}'
    except KeyError as e:
        print(result)
        raise e
    nicknames[player_id] = nickname
    with open(nicknames_path, 'w') as f:
        json.dump(nicknames, f, ensure_ascii=False, indent=4)
    return nickname


def load_game(game_id: str, games_path: str):
    os.makedirs(games_path, exist_ok=True)
    game_file = os.path.join(games_path, f"{game_id}.json")
    if os.path.exists(game_file):
        with open(game_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    result = send_authorized_get_request(f'{GAME_URL}?gameId={game_id}')
    if result is None:
        return []

    game_data = extract_dices_from_game(result['gameMoveHistoryStateMap'])

    with open(game_file, 'w', encoding='utf-8') as f:
        json.dump(game_data, f, ensure_ascii=False, indent=4)

    return game_data


def extract_dices_from_game(game_data: dict) -> list:
    dices = [game_data[record]['dices'] for record in game_data][1:]
    filtered_moves = [next(group) for _, group in
                      groupby(dices, key=lambda x: tuple((m["value"]) for m in x))]
    return filtered_moves
