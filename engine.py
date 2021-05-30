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
        새 2차원 배열에 객체들을 그래픽 처리해 추가하여 반환.
        """

        def cut_to_screen(self):
            """
            화면을 스크린 크기에 맞춰 잘라 반환
            """
            return self.camera.render(self.map, self.px, self.py)

        return cut_to_screen()


class Tile:
    def __init__(self, content: list = [], visited=False):
        self.content = [c for c in content]
        self.visited = visited

    def __str__(self):
        return " ".join([str(i) for i in self.content])


if __name__ == "__main__":
    """
    엔진 쇼케이스: wasd로 이동, q/x 로 종료.
    """
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
