from django.conf import settings

from moviemon.utils.moviemon import Moviemon
from moviemon.utils.data import Data
from moviemon.views.battle import battleState

from .map import Tile
from .map import init_map
from .camera import Camera


class Engine:
    """
    여러... 인자들을 받아 저장후 입력을 받아 계산값 반환
    """

    def __init__(self, size, screen, offset, playerpos, premap=None):
        # Data.load(SAVENAME)
        self.width, self.height = size
        if premap:
            self.map = premap
        else:
            self.map = init_map(self.width, self.height)
        self.px, self.py = playerpos
        self.camera = Camera(screen, offset)

    def move(self, x, y):
        if 0 <= self.px + x <= self.width - 1:
            self.px += x
        else:
            print("at the border of each side!")
        if 0 <= self.py + y <= self.height - 1:
            self.py += y
        else:
            print("at the border of either bottom or ceiling!")

    def render(self):
        """
        새 2차원 배열에 객체들을 그래픽 처리해 추가하여 반환.
        즉 2차원 배열 + 값들(1차원) = 3차원 배열(?!)
        """
        return self.camera.render(self.map, self.px, self.py)
        # return self.camera.render(self.map, self.px, self.py)

        # lines = []
        # for y in range(self.height):
        #     l = ""
        #     for x in range(self.width):
        #         if (self.py, self.px) == (y, x):
        #             l += "O"
        #         elif self.map[y][x].content:
        #             l += "?"
        #         else:
        #             l += "X"
        #     lines.append(l)
        # pre_render = lines
        # for l in pre_render:
        #     print(l)

        def cut_to_screen():
            """
            화면을 스크린 크기에 맞춰 잘라 반환
            """
            return self.camera.render(pre_render, self.px, self.py)

        return cut_to_screen()

    def add(self, pos, content):
        self.map[pos[0]][pos[1]].append(content)

    def __coll(self, target):
        if self.map[self.py][self.px].content == target:
            self.map[self.py][self.px].content = ""
            return True

    def collisioncheck(self, data: Data):
        if self.__coll("movieball"):
            data.add("movieballs", 1)

        # if self.__coll("moviemon"):
        #     battleState = await
        # if self.map[self.py][self.px].content == "movieball":
        #     self.map[self.py][self.px].content = ""
        #     data.add("movieballs", 1)

        if self.map[self.py][self.px].content == "moviemon":
            self.map[self.py][self.px].content = ""

    def update(self):
        self.map[self.py][self.px].visit()
        for y in self.map:
            for x in y:
                x.update()
                if x.content == "@":
                    x.content = ""
        self.map[self.py][self.px].content = "@"


if __name__ == "__main__":
    """
    엔진 쇼케이스: wasd로 이동, q/x 로 종료.
    """

    engine = Engine((10, 10), (6, 6), (-3, -3))
    engine.add((2, 3), Moviemon("123456"))
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
