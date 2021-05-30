from data import Data
from camera import Camera
from moviemon import Moviemon
from tempconst import *  # noqa


class Engine:
    def __init__(
        self,
        width,
        height,
        screen_width,
        screen_height,
        offset_x,
        offset_y,
    ):
        # Data.load(SAVENAME)
        self.width = width
        self.height = height
        self.map = [
            [Tile() for _ in range(self.width)] for _ in range(self.height)
        ]
        self.px = 4
        self.py = 4
        self.camera = Camera(
            screen_width,
            screen_height,
            offset_x,
            offset_y,
        )

    def info(self):
        """
        화면에 출력, 모드로 방식 결정
        """
        lines = []
        for y in range(self.height):
            l = ""
            for x in range(self.width):
                if (self.py, self.px) == (y, x):
                    l += "@"
                elif self.map[y][x].content:
                    l += "X"
                else:
                    l += "."
            lines.append(l)
        for l in lines:
            print(l)

    def add_to_tile(self, x, y, obj):
        self.map[x][y]

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
        지도의 특정 부분을 잘라서 반환함.
        """
        screen = self.camera.render(self.map, self.px, self.py)
        # for l in screen:
        #     print(l)
        lines = []
        for y in range(len(screen)):
            l = ""
            for x in range(len(screen[0])):
                if (self.py, self.px) == (y, x):
                    l += "@"
                elif self.screen[y][x].content:
                    l += "X"
                else:
                    l += "."
            lines.append(l)
        for l in lines:
            print(l)


class Player:
    pass


class Tile:
    def __init__(self, content: list = [], visited=False):
        self.content = [c for c in content]
        self.visited = visited

    def __str__(self):
        return " ".join([str(i) for i in self.content])

    def somefun(self):
        print("hi")


if __name__ == "__main__":
    engine = Engine(
        WIDTH, HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, CAMOFFSET_X, CAMOFFSET_Y
    )
    engine.map[2][3].content.append(Moviemon("123456"))
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
