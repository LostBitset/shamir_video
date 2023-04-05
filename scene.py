from manim import *

from manim_voiceover import VoiceoverScene
from manim_voiceover.services.coqui import CoquiService


class ExplainProblem(VoiceoverScene):
    def construct(self):
        self.set_speech_service(CoquiService())

        with self.voiceover(
            "Let's say that you and some friends have an important secret. "
        ) as t:
            self.wait(t.duration)

        secret = Text("Secret", font_size=40)
        self.play(Write(secret))

        with self.voiceover("You want to encrypt the secret in such a way that") as t:
            self.play(
                Transform(secret, Text("etcrSe", font_size=40).shift(LEFT * 4)),
                run_time=t.duration,
            )

        people = None
        with self.voiceover("there are three total people with shares") as t:
            middle_person = Circle()
            people = [
                Circle().next_to(middle_person, UP),
                middle_person,
                Circle().next_to(middle_person, DOWN),
            ]
            for person in people:
                person.set_stroke(width=0)
                person.set_fill(RED, opacity=0.5)
                self.play(Create(person), run_time=t.duration / 3)

        with self.voiceover("and exactly two shares are necessary") as t:
            self.play(
                people[0].animate.set_fill(GREEN, opacity=0.5), run_time=t.duration
            )

        with self.voiceover("to decrypt the complete secret. ") as t:
            self.play(
                Transform(secret, Text("Secret", font_size=40).shift(LEFT * 4)),
                people[1].animate.set_fill(GREEN, opacity=0.5),
                run_time=t.duration,
            )

        self.play(Unwrite(secret))

        shares = [Text(text, font_size=40) for text in ["Se cr", "cr et", "Se et"]]
        with self.voiceover(
            "The simplest solution would be to just give each person two thirds of the secret"
        ):
            for person, share in zip(people, shares):
                share.next_to(person, ORIGIN)
                self.play(Write(share), run_time=t.duration / 3)

        with self.voiceover("but this gives each participant some information") as t:
            self.wait(t.duration)

        with self.voiceover("about what the final secret is. ") as t:
            for person, share in zip(people, shares):
                self.play(Unwrite(share), run_time=t.duration / 6)
                self.play(Uncreate(person), run_time=t.duration / 6)

        self.wait()
