import random

from django.conf import settings

from moviemon.utils.moviemon import Moviemon

from .utils import clip

# from moviemon.utils.data import Data

# data = Data()


class Tile:
    def __init__(self, content: str = None):
        """ """
        self.content = content
        self.seen = 0
        self.heat = 0
        self.rgb(152, 161, 154, 4, 3, 3)
        # self.r, self.g, self.b = 182, 191, 184

    def __str__(self):
        return self.content

    def visit(self, heat=16):
        self.heat += heat

    def rgb(self, r, g, b, mulr, mulg, mulb):
        self.r = r - mulr * self.heat
        self.g = g - mulg * self.heat
        self.b = b - mulb * self.heat
        # print(f"{self.heat}, my rgb:{self.r},{self.g},{self.b}")

    def update(self):
        """
        업데이트!
        """
        self.heat = clip(self.heat, (-16, 16))
        if self.heat > 0:
            self.heat -= 1
        elif self.heat < 0:
            self.heat += 1
        self.rgb(152, 161, 154, 4, 3, 3)


def radar(mmap, ppos):
    import math

    def rangeint(x1, y1, x2, y2):
        return int(
            math.sqrt(math.pow(abs(x2 - x1), 2) + math.pow(abs(y2 - y1), 2))
        )

    offset = (-3, -3)
    x, y = ppos[0] + offset[0], ppos[1] + offset[1]
    # radmap = [
    #     ".###.",
    #     "#####",
    #     "#####",
    #     "#####",
    #     ".###.",
    # ]
    radmap = [
        "..###..",
        ".#####.",
        "#######",
        "#######",
        "#######",
        ".#####.",
        "..###..",
    ]
    for i in range(7):
        for j in range(7):
            if radmap[i][j] == "#":
                a, b = max(x + i, 0), max(y + j, 0)
                try:
                    # print(-16 + 5 * rangeint(ppos[0], ppos[1], a, b))
                    mmap[b][a].heat = -20 + 4 * rangeint(ppos[0], ppos[1], a, b)
                    if mmap[b][a].content:
                        mmap[b][a].seen = 1
                except Exception as e:
                    print(e)
                    pass


def init_map(width, height, moviemons):
    """
    타일 객체가 담긴 맵 생성
    """
    mmap = [[Tile() for _ in range(width)] for _ in range(height)]
    ppos = settings.PLAYER_INIT_POS
    height, width = len(mmap), len(mmap[0])
    mmap = populate_moviemon(mmap, height, width, ppos, moviemons)
    mmap = populate_movieball(mmap, height, width, ppos)
    return mmap


def spawn_to_map(mmap, ppos, x, y, content, i):
    if (x, y) != ppos and not mmap[y][x].content and not mmap[y][x].heat:
        mmap[y][x].content = content
        mmap[y][x].seen = 0
        return i + 1
    return i


def populate_moviemon(mmap, height, width, ppos, total):
    i = 0
    while 1:
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        i = spawn_to_map(mmap, ppos, x, y, "moviemon", i)
        if i >= total:
            break
    return mmap


def populate_movieradar(mmap, height, width, ppos, total=None):
    i = 0
    for _ in range(100):
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        i = spawn_to_map(mmap, ppos, x, y, "movieradar", i)
        if i >= total:
            break


def populate_movieball(mmap, height, width, ppos, total=None):
    """
    density: 1 ~ 100 사이의 확률. 다른 값 가져와도 무조건 그 사이야~
    근데 차피 상수에서 가져옴.
    """
    i = 0
    if not total:
        density = settings.MOVIEBALL_POP_PROB * random.randint(9, 11) / 10
        total = int((density / 100) * height * width)  # 밀도 * 가로 * 세로
    # print(f"h:{height} w:{width} we'll populate {total} movieballs!")
    for _ in range(10000):
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        i = spawn_to_map(mmap, ppos, x, y, "movieball", i)
        if i >= total:
            # print(f"populated {i} movieballs")
            return mmap

    # print(f"could not populate all the movieballs; best was: {i}")
    return mmap


def get_suitable(num, mondct, lo, lovar, hi, hivar):
    # mondct = {(k,v) for k,v in mon_dct.items()}
    res, lonow, hinow = dict(), 0, 0
    # res = monlst
    for mid, mm in mondct.items():
        if mm.rating <= lovar and lonow < lo and len(res) < num:
            if settings.IMDB_DIVERSE:
                print(f"adding {mm.title}: rating {mm.rating} for lo")
            res[mid] = mm
            lonow += 1
        if mm.rating >= hivar and hinow < hi and len(res) < num:
            if settings.IMDB_DIVERSE:
                print(f"adding {mm.title}: rating {mm.rating} for hi")
            res[mid] = mm
            hinow += 1
    left = num - len(res)
    for _ in range(1000):
        k = random.choice(list(mondct.keys()))
        if k not in res.keys():
            res[k] = mondct[k]
            left -= 1
        if left <= 0:
            break
    if settings.IMDB_DIVERSE:
        print(f"total {len(res)} movies: {[m.title for m in res.values()]}")
    return res
