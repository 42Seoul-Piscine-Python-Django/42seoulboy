import pickle


class Data:
    def save(self, target: dict, filename: str):
        assert type(target) is dict, "input is not dict"
        assert type(filename) is str, "invalid filename"
        try:
            with open(filename, "wb") as f:
                pickle.dump(target, f)
        except Exception as e:
            print(f"exeption {e}!")

    def load(self, filename):
        assert type(filename) is str, "invalid filename"
        try:
            with open(filename, "rb") as f:
                self.data = pickle.load(f)
                return self
        except Exception as e:
            print(f"exeption {e}!")


if __name__ == "__main__":
    from moviemon import Moviemon

    data = Data()
    print("saving")
    test = {"mov": [Moviemon("1234")]}
    data.save(test, "test")
    print("loading")
    print(data.load("test"))
