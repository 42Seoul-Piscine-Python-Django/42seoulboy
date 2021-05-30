from utils import clip


class Camera:
    """
    주어진 지도의 일부분을 렌더링하는 클래스 (단일)
    """

    def __init__(
        self,
        width,
        height,
        offset_x,
        offset_y,
    ):
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y

    def snapshot(self):
        pass

    def render(self, map, x, y):
        global debug
        try:
            if debug:
                pass
        except Exception as e:
            debug = False

        width, height = len(map[0]), len(map)
        # print(f"orginal start: x:{px} y:{py}")
        # print("width:", width, "height:", height)
        px = clip(x + self.offset_x, (0, width - self.width))
        py = clip(y + self.offset_y, (0, height - self.height))

        # print(f"adjusted pos: x:{px} y:{py}")
        if debug:
            map[y][x] = 9
        screen = [[0] * self.width for _ in range(self.height)]
        for sy, j in enumerate(range(py, py + self.height)):
            for sx, i in enumerate(range(px, px + self.width)):
                if debug and map[j][i] != 9:
                    map[j][i] = 1
                screen[sy][sx] = map[j][i]
        return screen


if __name__ == "__main__":
    testcam = Camera(4, 4, -2, -1)

    import sys

    x, y = 3, 3
    width = 10
    height = 7
    while True:
        somemap = [[0 for _ in range(10)] for _ in range(7)]  # 너비, 높이
        char = input()

        if char in ["q", "x"]:
            sys.exit()
        elif char == "w":
            y = clip(y - 1, (0, height - 1))
        elif char == "s":
            y = clip(y + 1, (0, height - 1))
        elif char == "a":
            x = clip(x - 1, (0, width - 1))
        elif char == "d":
            x = clip(x + 1, (0, width - 1))
        debug = True
        screen = testcam.render(somemap, x, y)
        for l in screen:
            print("".join([str(i) for i in l]))
        for l in somemap:
            print("".join([str(i) for i in l]))
