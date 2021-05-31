import pickle
import random
from django.conf import settings
from pathlib import Path


class Data:
    def __init__(self, slot: str = None, data: dict = None):
        """
        A,B,C 슬롯 중 하나 명시. 파일이 존재하지 않으면 자동으로 생성해줌.
        데이터 구조: (접근법: dump() 또는 data.get("my_moviemons"))
            not_yet_moviemons: 아직 잡지 않은 무비몬 목록
            my_moviemons: 내가 잡은 무비몬 목록
            pos: 플레이어 위치
        함수 목록:
            save, load, load_default_settings
            dump, get

        """
        assert type(slot) is str and slot in [
            "A",
            "B",
            "C",
        ], "슬롯 인자는 대문자로 A,B,C 슬롯 중 하나여야함!"
        self.slot = slot
        if data:
            self.data = data
        else:
            try:
                self.data = self.load()
            except Exception as e:
                self.data = self.load_default_settings()

    def __get_slot(self):
        n = self.slot.lower()
        try:
            sc = self.data.get("my_moviemons")
            tot = self.data.get("not_yet_moviemons")
            score = f"{sc}_{sc + tot}"
            return f"slot{n}_{score}.mmg"
        except Exception as e:
            return f"slot{n}_0_9999.mmg"

    def save(self):
        with open(self.__get_slot(), "wb") as f:
            pickle.dump(self.data, f)

    def load(self):
        """
        [과제] 인자로 입력받은 게임데이터 파일을 읽어와 내부 딕셔너리에 저장.
        -> 현재 인스턴스
        """
        with open(self.__get_slot(), "rb") as f:
            self.data = pickle.load(f)
            return self

    def dump(self):
        """
        [과제] 저장하고 있는 게임정보 딕셔너리를 반환
        """
        return self.data

    def get(self, target, whenfail=None):
        """
        인스턴트 자체를 딕셔너리처럼 이용하여 검색.
        예시: data = Data(); data.get("pos") -> (1,1)
        """
        return self.data.get(target, whenfail)

    def get_random_movie(self):
        """
        [과제] 아직 잡지 않은 랜덤한 무비몬 반환
        """
        return self.data[""]

    def load_default_settings(self):
        """
        [과제] 게임데이터 세팅과 IMDB 영화제목을 불러와 저장함.
        settings/moviemon.py의 MOVIE_LOAD_INTERNAL로 API 사용 여부 결정
        -> 현재 인스턴스
        """

        def __load_omdb():
            import requests

            for movieid in settings.IMDB_LIST:
                params = {"apikey": settings.OMDB_API_KEY, "i": movieid}
                result = dict()
                data = requests.get(settings.OBDB_URL, params=params).json()
                result[movieid] = Moviemon(
                    title=data["Title"],
                    year=data["Year"],
                    director=data["Director"],
                    poster=data["Poster"],
                    rating=float(data["imdbRating"]),
                    plot=data["Plot"],
                    actors=data["Actors"],
                )
            return result

        def __load_internal():
            return {(k, Moviemon()) for k in settings.IMDB_ID_LIST}

        func = __load_internal if settings.MOVIE_LOAD_INTERNAL else __load_omdb
        self.update("not_yet_moviemons", func())

    def get_strength(self):
        """
        [과제] 플레이어의 '강함' 을 반환. 강함은 플레이어의 보유 무비몬에 따라 결정됨.
        """
        pass

    def get_movie(self):
        """
        [과제] 무비몬 id를 입력받아 필요한 모든 정보를 반환
        """
        pass
        # return dicts

    def update(self, key: str, value, save: bool = True) -> None:
        """
        단일 key-value쌍 수정. 수정과 동시에 저장함.
        저장을 끄고싶다면 (예:여러 수정 후 한번에 저장) save=False로 사용
        """
        self.data[key] = value
        if save:
            self.save()


if __name__ == "__main__":
    """
    사용례
    """
    from moviemon import Moviemon

    print("test 딕셔너리를 생성")
    test = {
        "pos": (3, 2),
        "movieballs": 10,
        "not_yet_moviemons": [
            Moviemon(54321, "옥자", "some.image.url1", "8.5"),
            Moviemon(3454321, "설국열차", "some.image.url2", "7"),
        ],
        "my_moviemons": [
            Moviemon(12345, "괴물", "some.image.url", "9.5"),
        ],
        "map_list": [],
    }
    # 빈 데이터 생성
    empt = Data("B")
    # 미리 데이터를 입력하여 데이터 생성
    data = Data("A")
    data = Data("A", data=test)
    print(data.slot)
    print("게임데이터 수정")
    # data.update("pos", (3, 3))
    # data.update("pos", (3, 4))
    # data.update("pos", (3, 3))
    print("파일에 test 딕셔너리 저장함")
    data.save()
    print("게임데이터 불러오기")
    data.load()
    for k, v in data.dump().items():
        print(f"접근 키:{k}, 접근 결과:{v}")
