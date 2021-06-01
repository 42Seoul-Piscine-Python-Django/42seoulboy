import os
import shutil
from django.conf import settings

from typing import Dict, List, Tuple

from moviemon.utils.moviemon import Moviemon
from moviemon.views.engine.map import *
from moviemon.views.engine.map import Tile


import requests
import json
import pickle


def make_save_dir():
    if not os.path.isdir('saved_game'):
        os.mkdir('saved_game')


def save_session_data(data):
    make_save_dir()
    try:
        f = open("saved_game/session.bin", "wb")
        pickle.dump(data, f)
        f.close()
        return data
    except:
        return None


def load_session_data():
    try:
        f = open("saved_game/session.bin", "rb")
        data = pickle.load(f)
        f.close()
        return data
    except:
        return None


def load_slot_info():
    try:
        if os.path.isfile('saved_game/slots.bin'):
            with open('saved_game/slots.bin', "rb") as f:
                return pickle.load(f)
        return {}
    except Exception as e:
        print(e)
        return {}


def save_slot(slot):
    data = load_session_data()
    slots = load_slot_info()
    if data is not None:
        try:
            score = "{}/{}".format(len(data['captured_list']),
                                   len(data['moviemon']))
            file = f"saved_game/slot{slot}_{len(data['captured_list'])}_{len(data['moviemon'])}.mmg"
            with open(file, "wb") as f:
                pickle.dump(data, f)
            if slots.get(f'slot{slot}', None) is not None:
                if os.path.isfile(slots[f'slot{slot}']['file']):
                    os.remove(slots[f'slot{slot}']['file'])
            slots[f'{slot}'] = {
                "score": score,
                "file": file,
            }
            with open('saved_game/slots.bin', "wb") as f:
                pickle.dump(slots, f)
            return True
        except Exception as e:
            print(e)
    return False


def load_slot(slot):
    slots = load_slot_info()
    slot = slots.get(slot, None)
    if slot == None:
        return False
    try:
        shutil(slot['file'], "saved_game/session.bin")
        return True
    except:
        return False


class GameData():
    def __init__(self) -> None:
        self.pos: Tuple[int, int] = settings.PLAYER_INIT_POS
        self.captured_list: List[str] = []
        self.moviemon: Dict[str, Moviemon] = {}
        self.movieballCount: int = 10
        self.map: List[List[Tile]] = []

    def dump(self):
        return {
            "pos": self.pos,
            "captured_list": self.captured_list,
            "moviemon": self.moviemon,
            "movieballCount": self.movieballCount,
            "map": self.map
        }

    @ staticmethod
    def load(data):
        result = GameData()
        result.pos = data["pos"]
        result.captured_list = data["captured_list"]
        result.moviemon = data["moviemon"]
        result.movieballCount = data["movieballCount"]
        result.map = data["map"]
        return result

    @ staticmethod
    def load_default_settings():
        result = GameData()
        URL = "http://www.omdbapi.com/"

        f = open("test.json", 'r')
        data = json.load(f)
        f.close()

        for value in data:
            # result.captured_list.append(value["imdbID"])
            result.moviemon[value["imdbID"]] = Moviemon(
                value["Title"],
                value["Year"],
                value["Director"],
                value["Poster"],
                float(value["imdbRating"]),
                value["Plot"],
                value["Actors"],
            )
        result.map = init_map(*settings.GRID_SIZE)
        # print(game.)
        # for id in settings.IMDB_LIST:
        #     params = {
        #         "apikey": settings.OMDB_API_KEY,
        #         "i": id
        #     }
        #     try:
        #         data = requests.get(URL, params=params).json()
        #         result.moviemon[id] = Moviemon(
        #             value["Title"],
        #             value["Year"],
        #             value["Director"],
        #             value["Poster"],
        #             float(value["imdbRating"]),
        #             value["Plot"],
        #             value["Actors"],
        #         )
        #     except Exception as e:
        #         assert e

        return result
