import random

from django.conf import settings

from moviemon.utils.moviemon import Moviemon
from moviemon.utils.data import Data

data = Data()


class Tile:
    def __init__(self, content: str = None, visited=False):
        """ """
        self.content = content
        self.visited = visited
        self.heat = 0

    def __str__(self):
        return self.content

    def visit(self, heat=10):
        self.heat = 10

    def update(self):
        """
        업데이트!
        """
        self.heat = max(self.heat - 1, 0)


def init_map(width, height):
    """
    타일 객체가 담긴 맵 생성
    """
    mmap = [[Tile() for _ in range(width)] for _ in range(height)]
    ppos = settings.CONSTANTS["PLAYER_INIT_POS"]
    height, width = len(mmap), len(mmap[0])
    # populate_moviemon(mmap, height, width, ppos)
    populate_movieball(mmap, height, width, ppos)
    return mmap


def populate_moviemon(mmap, height, width, ppos):
    total = len(settings.IMDB_ID_LIST)
    i = 0
    while 1:
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        if (x, y) != ppos and not mmap[x][y].content:
            i += 1
            mmap[x][y].content = "moviemon"
    return mmap


def populate_movieball(mmap, height, width, ppos):
    """
    density: 1 ~ 100 사이의 확률. 다른 값 가져와도 무조건 그 사이야~
    근데 차피 상수에서 가져옴.
    """
    i = 0
    density = (
        settings.CONSTANTS["MOVIEBALL_POP_PROB"] * random.randint(9, 11) / 10
    )
    total = int((density / 100) * height * width)  # 밀도 * 가로 * 세로
    # print(f"h:{height} w:{width} we'll populate {total} movieballs!")
    for _ in range(10000):
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        if (x, y) != ppos and not mmap[x][y].content:
            i += 1
            mmap[x][y].content = "movieball"
        if i >= total:
            # print(f"populated {i} movieballs")
            return mmap

    # print(f"could not populate all the movieballs; best was: {i}")
    return mmap
