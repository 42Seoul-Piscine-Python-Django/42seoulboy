from moviemon import Moviemon


class Engine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [
            [Tile() for _ in range(self.height)] for _ in range(self.width)
        ]
        self.px = 4
        self.py = 4

    def info(self):
        """
        화면에 출력, 모드로 방식 결정
        """
        lines = []
        for y in range(self.height):
            l = ""
            for x in range(self.width):
                if (self.px, self.py) == (x, y):
                    l += "@"
                elif self.map[x][y].content:
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
    engine = Engine(10, 10)
    engine.map[2][3].content.append(Moviemon("123456"))
    import sys

    engine.info()
    while True:
        char = input()

        if char == "x":
            sys.exit()
        elif char == "w":
            engine.move(0, -1)
        elif char == "s":
            engine.move(0, 1)
        elif char == "a":
            engine.move(-1, 0)
        elif char == "d":
            engine.move(1, 0)
        engine.info()
