import os
from project.settings.moviemon import IMDB_LIST, IMDB_LIST_KOR
import shutil
from django.conf import settings

from typing import Dict, List, Tuple

from moviemon.utils.moviemon import Moviemon
from moviemon.views.engine.map import *
from moviemon.views.engine.map import Tile, get_suitable


import requests
import json
import pickle
import random


def make_save_dir():
    if not os.path.isdir("saved_game"):
        os.mkdir("saved_game")


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
        if os.path.isfile("saved_game/slots.bin"):
            with open("saved_game/slots.bin", "rb") as f:
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
            score = "{}/{}".format(
                len(data["captured_list"]), len(data["moviemon"])
            )
            if slots.get(f"{slot}", None) is not None:
                if os.path.isfile(slots[f"{slot}"]["file"]):
                    os.remove(slots[f"{slot}"]["file"])
            file = f"saved_game/slot{slot}_{len(data['captured_list'])}_{len(data['moviemon'])}.mmg"
            with open(file, "wb") as f:
                pickle.dump(data, f)
            slots[f"{slot}"] = {
                "score": score,
                "file": file,
            }
            with open("saved_game/slots.bin", "wb") as f:
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
        shutil.copy(slot["file"], "saved_game/session.bin")
        return True
    except:
        return False


class GameData:
    def __init__(self) -> None:
        self.pos: Tuple[int, int] = settings.PLAYER_INIT_POS
        self.captured_list: List[str] = []
        self.moviemon: Dict[str, Moviemon] = {}
        self.movieballCount: int = settings.PLAYER_INIT_MOVBALL
        self.map: List[List[Tile]] = []

    def get_movie(self, moviemon_id):
        return self.moviemon[moviemon_id]

    def get_random_movie(self):
        id_list = [
            m for m in self.moviemon.keys() if not m in self.captured_list
        ]
        return random.choice(id_list)

    def get_strength(self) -> int:
        # return average of best six moviemon ratings
        ratings = sorted(
            [
                self.moviemon[i].rating
                for i in self.load(load_session_data()).captured_list
            ],
            reverse=True,
        )

        if ratings:
            numsend = min(6, len(ratings))
            return int(sum(ratings[:numsend]) / numsend)
        else:
            return 1

        # sum_captured_rating = 3
        # for i in captured_list:
        #     sum_captured_rating += self.moviemon[i].rating
        # if len(captured_list) == 0:
        #     return int(sum_captured_rating / 1)
        # return int(sum_captured_rating / len(captured_list))

    def dump(self):
        return {
            "pos": self.pos,
            "captured_list": self.captured_list,
            "moviemon": self.moviemon,
            "movieballCount": self.movieballCount,
            "map": self.map,
        }

    @staticmethod
    def load(data):
        result = GameData()
        result.pos = data["pos"]
        result.captured_list = data["captured_list"]
        result.moviemon = data["moviemon"]
        result.movieballCount = data["movieballCount"]
        result.map = data["map"]
        return result

    @staticmethod
    def load_default_settings():
        result = GameData()
        URL = "http://www.omdbapi.com/"

        # f = open("test.json", 'r')
        # data = json.load(f)
        # f.close()

        # for value in data:
        #     # result.captured_list.append(value["imdbID"])
        #     result.moviemon[value["imdbID"]] = Moviemon(
        #         value["Title"],
        #         value["Year"],
        #         value["Director"],
        #         value["Poster"],
        #         float(value["imdbRating"]),
        #         value["Plot"],
        #         value["Actors"],
        #     )
        if settings.IMDB_DIVERSE:
            DB_LIST = random.choice(
                [settings.IMDB_LIST, settings.IMDB_LIST_KOR]
            )
        else:
            DB_LIST = settings.IMDB_LIST
        # DB_LIST = settings.IMDB_LIST_KOR
        for id in DB_LIST:
            params = {"apikey": settings.OMDB_API_KEY, "i": id}
            try:
                data = requests.get(URL, params=params).json()
                result.moviemon[id] = Moviemon(
                    data["Title"],
                    data["Year"],
                    data["Director"],
                    data["Poster"],
                    float(data["imdbRating"]),
                    data["Plot"],
                    data["Actors"],
                )
            except Exception as e:
                assert e
        x, y = settings.GRID_SIZE
        total = min(
            int(x * y * random.randint(7, 11) / 80),
            len(result.moviemon.keys()),
        )
        result.moviemon = get_suitable(
            total,
            result.moviemon,
            max(3, int(total / 3)),
            4,
            max(3, int(total / 3)),
            7,
        )
        result.map = init_map(
            *settings.GRID_SIZE,
            int(random.uniform(0.5, 1) * len(result.moviemon)),
        )
        # print("total result.moviemon:", len(result.moviemon))

        return result
