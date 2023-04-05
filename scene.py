from manim import *

from manim_voiceover import VoiceoverScene
from manim_voiceover.services.coqui import CoquiService

class Top(VoiceoverScene):
    def construct(self):
        self.set_speech_service(CoquiService())
        
        square = Square()
        square.rotate(PI / 4)

        with self.voiceover("This can draw shapes") as tracker:
            self.play(Create(square), run_time=tracker.duration)

        with self.voiceover("interpolate stuff") as tracker:
            self.play(Transform(square, Circle()), run_time=tracker.duration)
        
        tex = Tex(r"\LaTeX", font_size=100)
        text = Text(r"今日は！", font_size=100)
        tex.next_to(square, LEFT)
        text.next_to(square, RIGHT)

        with self.voiceover("and draw text.") as tracker:
            self.play(Write(tex), Write(text), run_time=tracker.duration)
        
        self.wait()
        self.play(FadeOut(tex), FadeOut(text), FadeOut(square))
        self.wait()
