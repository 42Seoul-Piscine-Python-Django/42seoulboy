class Message:
    msg = {
        "battle": "Encountered a moviemon!",
        "movieball": "Picked up a movieball!",
        "radar": "Picked up a movieradar!",
        "none": "",
    }

    def __init__(self, key):
        self.key = key
        self.log = Message.msg.get(key, "wrong key!")
        self.ammount = 1

    def __str__(self):
        if self.ammount >= 2:
            return f"{self.log} ✖{self.ammount}"
        return self.log

    def __call__(self, key, single=False):
        if key == self.key and not single:
            self.ammount += 1
        else:
            self.ammount = 1
        self.key = key
        self.log = Message.msg.get(key, "")


if __name__ == "__main__":
    m = Message("radar")
    print(m)
    m("radar")
    m("radar")
    print(m)
    m("movieball")
    print(m)
    m("battle", single=True)
    print(m)
    m("battle", single=True)
    print(m)
