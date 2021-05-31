from django.conf import settings
from typing import Dict, List, Tuple
import requests
import json
import pickle


def save_session_data(data):
    try:
        f = open("session.bin", "wb")
        pickle.dump(data, f)
        f.close()
        return data
    except:
        return None


def load_session_data():
    try:
        f = open("session.bin", "rb")
        data = pickle.load(f)
        f.close()
        return data
    except:
        return None


class GameData:
    px: int = settings.PLAYER_INIT_POSITION[0]
    py: int = settings.PLAYER_INIT_POSITION[1]
    captured_list: List[str] = []
    moviemon: Dict[str, Dict[str, str]] = {}
    mapsize: Tuple[int, int] = settings.GRID_SIZE
    map: List[List[int]] = [
        [0 for _ in range(settings.GRID_SIZE[1])]
        for _ in range(settings.GRID_SIZE[0])
    ]
    movieballCount: int = settings.GRID_SIZE[0] * settings.GRID_SIZE[1] / 10

    def dump(self):
        return {
            "px": self.px,
            "py": self.py,
            "captured_list": self.captured_list,
            "moviemon": self.moviemon,
            "mapsize": self.mapsize,
            "map": self.map,
        }

    def load(data):
        result = GameData()
        result.px = data["px"]
        result.py = data["py"]
        result.captured_list = data["captured_list"]
        result.moviemon = data["moviemon"]
        result.mapsize = data["mapsize"]
        result.map = data["map"]
        return result

    def get_random_movie():
        # TODO
        pass

    def load_default_settings():
        # TODO
        pass

    def get_strength():
        # TODO
        pass

    def get_movie():
        # TODO
        pass
        # return dicts

    def load_default_settings():
        result = GameData()
        URL = "http://www.omdbapi.com/"

        # f = open("test.json", 'r')
        # data = json.load(f)
        # f.close()

        # for key, value in data.items():
        #     result.captured_list.append(key)
        #     result.moviemon[key] = {
        #         "title": value["Title"],
        #         "year": value["Year"],
        #         "director": value["Director"],
        #         "poster": value["Poster"],
        #         "rating": float(value["imdbRating"]),
        #         "plot": value["Plot"],
        #         "actors": value["Actors"],
        # }

        for id in settings.IMDB_LIST:
            params = {"apikey": settings.OMDB_API_KEY, "i": id}
            try:
                data = requests.get(URL, params=params).json()
                result.moviemon[id] = {
                    "title": data["Title"],
                    "year": data["Year"],
                    "director": data["Director"],
                    "poster": data["Poster"],
                    "rating": float(data["imdbRating"]),
                    "plot": data["Plot"],
                    "actors": data["Actors"],
                }
            except Exception as e:
                assert e
        return result
