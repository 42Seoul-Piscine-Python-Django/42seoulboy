from .camera import Camera


class Renderer:
    def __init__(self, screen, offset):
        self.camera = Camera(screen, offset)

    def render(self):
        """
        새 2차원 배열에 객체들을 그래픽 처리해 추가하여 반환.
        """
        lines = []
        for y in range(self.height):
            l = ""
            for x in range(self.width):
                if (self.py, self.px) == (y, x):
                    l += "@"
                elif self.map[y][x].content:
                    l += "_"
                else:
                    l += "X"
            lines.append(l)
        pre_render = lines
        for l in pre_render:
            print(l)

        def cut_to_screen():
            """
            화면을 스크린 크기에 맞춰 잘라 반환
            """
            return self.camera.render(pre_render, self.px, self.py)

        return cut_to_screen()
