from random import randint


def clip(value, cliprange: tuple):
    """
    clips value between cliprange. example below:
    clip(10, (1, 3)) -> 3
    clip(1, (20, 30)) -> 20
    """
    assert cliprange[0] <= cliprange[1], "invalid cliprange"
    return max(cliprange[0], min(value, cliprange[1]))


# def movieball(mon_str, player_str):
#     """
#     포획 성공 여부 반환 (무비몬, 플레이어의 힘을 비교)
#     """
#     chances = clip(50 - (mon_str * 10) + (player_str * 5), (1, 90))

#     return randint(1, 100) <= chances


def tester(testdict: dict):
    """
    함수값이 원하는 대로 나오는지 확인하는 함수. 사용할 함수를 먼저 import한 후 쓰세요.
    입력값 양식: (함수 이름): {(입력 파라미터 튜플): 결과값}, ...}
    사용 예시: tester(
            testdict = {
            clip: {(15, (1, 10)): 10},
            movieball: {},
        }
    )
    """

    def process_line(say: str = None, fill: bool = False, br: bool = False):
        if say and fill:
            print(f" {say} ".center(size, c))
        elif say:
            print(c + f" {say} ".center(size - 2) + c)
        else:
            print(c * size)
        if br:
            print("")

    size, score, total, faillist = 30, 0, len(testdict.keys()), list()
    c = "#"
    process_line(f"testing {total} functions", fill=True, br=True)
    for func, tests in testdict.items():
        for case, expected in tests.items():
            result = func(*case)  # unpacks case tuple into parameters to func
            if result == expected:
                score += 1
                c, tell = "O", "TEST SUCCESSFUL"
            else:
                c, tell = "X", "TEST FAILED"
                faillist.append(func.__name__)
            process_line(f"result for <{func.__name__}>", fill=True)
            process_line(f"parameter {case}")
            process_line(f"expected {expected}".ljust(16))
            process_line(f"result : {result}".ljust(16))
            process_line(tell)
            process_line(br=True)

    c = "O" if score == total else "X"
    process_line(f"total score: {score}/{total}", fill=True, br=True)
    assert score == total, f"FAILED FUNCTIONS {faillist}"
    c = "#"
    process_line(f"TEST SUCCESSFUL", fill=True)


if __name__ == "__main__":
    testdict = {
        clip: {
            (15, (1, 10)): 10,
            (3, (11, 15)): 1,
        },
    }
    tester(testdict)

    # for _ in range(50):
    #     m, p = randint(1.0, 10.0), randint(1.0, 20.0)
    #     print(f"m:{m} p:{p} {movieball(m, p)}")
