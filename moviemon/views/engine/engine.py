from django.conf import settings
from moviemon.utils.game_data import GameData, save_session_data, load_session_data
from moviemon.utils.moviemon import Moviemon
#from moviemon.utils.data import Data
from moviemon.views.battle import battleState

from .map import Tile
from .map import init_map, populate_movieball
from .camera import Camera

import random

class Engine:
    """
    여러... 인자들을 받아 저장후 입력을 받아 계산값 반환
    """

    def __init__(self, size, screen, offset, playerpos, movball, premap=None):
        # Data.load(SAVENAME)
        self.width, self.height = size
        if premap:
            self.map = premap
        else:
            self.map = init_map(self.width, self.height)
        self.px, self.py = playerpos
        self.movball = movball
        self.state = None
        self.camera = Camera(screen, offset)
        self.update()

    def move(self, x, y):
        if 0 <= self.px + x <= self.width - 1:
            self.px += x
        else:
            print("at the border of each side!")
        if 0 <= self.py + y <= self.height - 1:
            self.py += y
        else:
            print("at the border of either bottom or ceiling!")
        self.update()

    def render(self):
        """
        새 2차원 배열에 객체들을 그래픽 처리해 추가하여 반환.
        즉 2차원 배열 + 값들(1차원) = 3차원 배열(?!)
        """
        return self.camera.render(self.map, self.px, self.py)

    def add(self, pos, content):
        self.map[pos[0]][pos[1]].append(content)

    def __coll(self, target):
        if self.map[self.py][self.px].content == target:
            self.map[self.py][self.px].content = ""
            return True

    def collisioncheck(self):
        if self.__coll("movieball"):
            self.movball += 1
        if self.__coll("moviemon"):
            self.state = "battle"


    def update(self):
        self.collisioncheck()
        self.map[self.py][self.px].visit()
        for y in self.map:
            for x in y:
                x.update()
                if x.content == "@":
                    x.content = ""
        self.map[self.py][self.px].content = "@"
        print("pop")
        if True:
        #if random.randint(1, 10) == 1:
            mmap = populate_movieball(
                self.map,
                self.height,
                self.width,
                (self.px, self.py),
                random.randint(1, 4)
            )


if __name__ == "__main__":
    """
    엔진 쇼케이스: wasd로 이동, q/x 로 종료.
    """
    engine = Engine((10, 10), (6, 6), (-3, -3))
    #engine.add((2, 3), Moviemon("123456"))
    import sys

    engine.info()
    while True:
        char = input()
        if char in ["q", "x"]:
            sys.exit()
        elif char == "w":
            engine.move(0, -1)
        elif char == "s":
            engine.move(0, 1)
        elif char == "a":
            engine.move(-1, 0)
        elif char == "d":
            engine.move(1, 0)
        # engine.info()
        engine.render()
    engine.dump()
