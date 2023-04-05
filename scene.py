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
        secret = Text(secret_text, font_size=40)
        self.play(Write(secret))

        with self.voiceover("You want to encrypt the secret in such a way that") as t:
            self.play(
                Transform(
                    secret, Text("dd 82 e9 1a 75 2f", font_size=40).shift(LEFT * 4)
                ),
                run_time=t.duration,
            )

        n = 4
        people = None
        with self.voiceover("there are four total people with shares") as t:
            people = [Circle(radius=0.8) for _ in range(n)]
            people_group = VGroup(*people)
            people_group.arrange_in_grid(cols=1, buff=0.1)
            for person in people:
                person.set_stroke(width=0)
                person.set_fill(RED, opacity=0.5)
                self.play(Create(person), run_time=t.duration / n)

        with self.voiceover("and exactly two shares are necessary") as t:
            self.play(
                people[0].animate.set_fill(GREEN, opacity=0.5), run_time=t.duration
            )

        with self.voiceover("to decrypt the complete secret. ") as t:
            self.play(
                Transform(secret, Text(secret_text, font_size=40).shift(LEFT * 4)),
                people[1].animate.set_fill(GREEN, opacity=0.5),
                run_time=t.duration,
            )

        self.play(Unwrite(secret), people_group.animate.shift(LEFT * 2))

        segment = len(secret_text) // n
        shares = [
            MarkupText(self.pm_hide(secret_text, i, segment), font_size=40)
            for i in range(0, len(secret_text), segment)
        ]
        with self.voiceover(
            "The simplest solution would be to just give each person two thirds of the secret"
        ):
            for person, share in zip(people, shares):
                share.next_to(person, RIGHT, buff=0.1)
                self.play(Write(share), run_time=t.duration / n)

        with self.voiceover("but this gives each participant some information") as t:
            self.wait(t.duration)

        with self.voiceover("about what the final secret is. ") as t:
            for person, share in zip(people, shares):
                self.play(Unwrite(share), run_time=t.duration / (n * 2))
                self.play(Uncreate(person), run_time=t.duration / (n * 2))

        self.wait()

    def pm_hide(self, text, start, length):
        before = text[:start]
        hidden = text[start : start + length]
        after = text[start + length :]
        pango_markup = f"{before}<span color='black'>{hidden}</span>{after}"
        return pango_markup
