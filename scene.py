from manim import *

from manim_voiceover import VoiceoverScene
from manim_voiceover.services.coqui import CoquiService

speech_service = CoquiService()
setup_speech = lambda obj: obj.set_speech_service(speech_service)


class Top(VoiceoverScene):
    def construct(self):
        setup_speech(self)

        with self.voiceover(
            "Let's say that you and some friends have an important secret. "
        ) as t:
            self.wait(t.duration)

        secret_text = "Top_Secret._"
        secret = Text("Secret", font_size=40)
        self.play(Write(secret))

        with self.voiceover("You want to encrypt the secret in such a way that") as t:
            self.play(
                Transform(secret, Text("dd82e91a", font_size=40).shift(LEFT * 4)),
                run_time=t.duration,
            )

        n = 4
        people = None
        with self.voiceover("there are four total people with shares") as t:
            top_person = Circle()
            people = [
                Circle().next_to(top_person, DOWN * i),
                for i in range(n)
            ]
            people_group = Group(*people)
            for person in people:
                person.set_stroke(width=0)
                person.set_fill(RED, opacity=0.5)
            self.play(Create(people_group), run_time=t.duration)

        with self.voiceover("and exactly two shares are necessary") as t:
            self.play(
                people[0].animate.set_fill(GREEN, opacity=0.5), run_time=t.duration / 2
            )

        with self.voiceover("to decrypt the complete secret. ") as t:
            self.play(
                Transform(secret, Text("Secret", font_size=40).shift(LEFT * 4)),
                people[1].animate.set_fill(GREEN, opacity=0.5),
                run_time=t.duration,
            )

        self.play(Unwrite(secret))

        shares = [
            Text(text, font_size=40)
            for text in ["_Se cre t._", "Top cre t._", "Top _Se t._", "Top _Se cre"]
        ]
        with self.voiceover(
            "The simplest solution would be to just give each person two thirds of the secret"
        ):
            for person, share in zip(people, shares):
                share.next_to(person, ORIGIN)
                self.play(Write(share), run_time=t.duration / n)

        with self.voiceover("but this gives each participant some information") as t:
            self.wait(t.duration)

        with self.voiceover("about what the final secret is. ") as t:
            for person, share in zip(people, shares):
                self.play(Unwrite(share), run_time=t.duration / (n * 2))
                self.play(Uncreate(person), run_time=t.duration / (n * 2))

        self.wait()
