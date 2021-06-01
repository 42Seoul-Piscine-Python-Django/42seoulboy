class Keys:

    states = {
        "title": {
            "a": {"do": "redirect", "args": "worldmap"},
            "b": {"do": "load"},
        },
        "worldmap": {
            "up": {"do": "move", "args": (0, -1)},
            "down": {"do": "move", "args": (0, 1)},
            "left": {"do": "move", "args": (-1, 0)},
            "right": {"do": "move", "args": (1, 0)},
            "start": {"do": "redirect", "args": "option"},
            "select": {"do": "redirect", "args": "moviedex"},
        },
        "before_battle": {
            "a": {"do": "battle"},
        },
        "battle": {},
        "moviedex": {},
        "detail": {},
        "option": {},
        "load": {},
        "save": {},
    }

    def __new__(cls, *args, **kwargs):
        """
        클래스를 바로 사용하거나. 인스턴스 생성 후 keys(<현재 페이지 이름>, <키입력>)식으로 사용
        예)
        인스턴스: k = Keys(); k("worldmap", "up") -> {"do": "move", "args": (0, 1)}
        클래스 : Keys("worldmap", "up") -> {"do": "move", "args": (0, 1)}
        Keys() -> <__main__.Keys object at 0x10d747d00>
        """
        try:
            state, called = args[0], args[1]
        except Exception as e:
            pass
        # print(f"cls:{cls}, state:{state}, called:{called}")
        if len(args):
            if len(args) == 2:
                # print("******RETURNING DICT SEARCH*********")
                return cls.states.get(state).get(called) or {}
            # print("*******RETURNING EMPTY DICT******")
            return {}
        # print("******RETURNING INSTANCE*********")
        return super().__new__(cls)

    def __call__(self, state, called):
        return self.states.get(state).get(called)


if __name__ == "__main__":
    # using class directly
    print(Keys("worldmap", "select"))
    print(Keys("worldmap", "b"))
    print(Keys())
    # using instances
    keys = Keys()
    inpt = "up"
    print(keys("worldmap", inpt))
