import pickle
import random
from pathlib import Path

from .moviemon import Moviemon

current_slot = "LOCAL"


class Data:
    def __new__(cls, *args, **kwargs):
        """
        싱글톤 패턴 구현
        """
        if not hasattr(cls, "_instance"):  # 클래스 객체에 _instance 속성이 없다면
            print("__new__ is called\n")
            cls._instance = super().__new__(cls)
            # 클래스의 객체를 생성하고 Foo._instance로 바인딩
        return cls._instance  # Foo._instance를 리턴

    def __init__(self, data: dict = None):
        cls = type(self)
        if not hasattr(cls, "_init"):  # init은 한 번만 실행됨
            cls._init = True
            """
            데이터 딕셔너리를 명시하면 덮어씌워줌.
            데이터 구조: (접근법: dump() 또는 data.get("my_moviemons"))
                not_yet_moviemons: 아직 잡지 않은 무비몬 목록
                my_moviemons: 내가 잡은 무비몬 목록
                map: 지도
                movieballs: 무비볼 수
                pos: 플레이어 위치
            함수 목록:
                save, load, load_default_settings
                dump, get
            """

            self.slot = current_slot  # A, B, C 중 하나
            if data:
                self.data = data
            elif self.slot == "LOCAL":
                self.data = self.load_default_settings()
            else:
                self.data = self.load()

    def __make_slot(self):
        # print("\n\n\nCURRENT SLOT:", self.slot)
        n = self.slot.lower()
        sc = len(self.data.get("my_moviemons"))
        tot = len(self.data.get("not_yet_moviemons"))
        score = f"{sc}_{sc + tot}"
        return f"slot{n}_{score}.mmg"

    def save(self, slot="LOCAL"):
        print("SAVING")
        if slot == "LOCAL":
            with open("LOCAL", "wb") as f:
                pickle.dump(self.data, f)
        else:
            with open(self.__make_slot(), "wb") as f:
                pickle.dump(self.data, f)

    def load(self, slot="LOCAL"):
        """
        [과제] 인자로 입력받은 게임데이터 파일을 읽어와 내부 딕셔너리에 저장.
        -> 현재 인스턴스
        """
        print("LOADING")
        if slot == "LOCAL":
            with open("LOCAL", "rb") as f:
                self.data = pickle.load(f)
                return self
        else:
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
        return self.data.get("not_yet_moviemons").choice()

    def load_default_settings(self):
        """
        [과제] 게임데이터 세팅과 IMDB 영화제목을 불러와 저장함.
        settings/moviemon.py의 MOVIE_LOAD_INTERNAL로 API 사용 여부 결정
        -> 현재 인스턴스
        """
        from django.conf import settings

        const = settings.CONSTANTS
        self.data = {
            "pos": const["PLAYER_INIT_POS"],
            "movieballs": const["PLATER_INIT_MOVIEBALLS"],
            "map": [],
        }

        def __load_omdb():
            print("LOADING FROM OMDB...")
            import requests

            try:
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
            except Exception as e:
                raise e

            print("OMDB LIST TURNED OUT:", result)
            return result

        def __load_internal():
            result = dict()
            for k in settings.IMDB_ID_LIST:
                result[k] = Moviemon()
            return result

        # rint("WHY?????????????????\n\nn\n\n\n")
        func = __load_internal if settings.MOVIE_LOAD_INTERNAL else __load_omdb
        self.update("not_yet_moviemons", func())
        self.update("my_moviemons", func())
        self.save(slot="LOCAL")
        # print("******MY DATA IS", self.data, "********")

    def get_strength(self):
        """
        [과제] 플레이어의 '강함' 을 반환. 강함은 플레이어의 보유 무비몬에 따라 결정됨.
        """
        pass

    def get_movie(self, movie_id):
        """
        [과제] 무비몬 id를 입력받아 필요한 모든 정보를 반환
        """
        movmon = self.get("my_moviemons")
        return movmon[movie_id].data

    def update(self, key: str, value, save: bool = True) -> None:
        """
        단일 key-value쌍 수정. 수정과 동시에 저장함.
        저장을 끄고싶다면 (예:여러 수정 후 한번에 저장) save=False로 사용
        """
        try:
            self.data[key] = value
        except Exception as e:
            raise Exception(f"key {key} caused Error {e}")
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
