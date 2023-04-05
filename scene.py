from manim import *

class Demo(Scene):
    def construct(self):
        square = Square()
        square.rotate(PI / 4)
        self.play(Create(square))
        self.play(Transform(square, Circle()))
        tex = Tex(r'\LaTeX', font_size=100)
        tex.next_to(square)
        self.play(Write(tex))
        self.wait(1)
        self.play(FadeOut(tex), FadeOut(square))
