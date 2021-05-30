import pickle


class Data:
    @classmethod
    def save(cls, target: dict, filename: str):
        assert type(target) is dict, "input is not dict"
        assert type(filename) is str, "invalid filename"
        try:
            with open(filename, "wb") as f:
                pickle.dump(target, f)
        except Exception as e:
            print(f"exeption {e}!")

    @classmethod
    def load(cls, filename):
        assert type(filename) is str, "invalid filename"
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"exeption {e}!")


if __name__ == "__main__":
    from moviemon import Moviemon

    print("saving")
    test = {"mov": [Moviemon("1234")]}
    Data.save(test, "test")
    print("loading")
    print(Data.load("test"))
