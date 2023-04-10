from manim import *

from manim_voiceover import VoiceoverScene
from manim_voiceover.services.coqui import CoquiService

speech_service = CoquiService()
setup_speech = lambda obj: obj.set_speech_service(speech_service)

n, need = 4, 3


class ExplainProblem(VoiceoverScene):
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

        people = None
        with self.voiceover("there are four total people with shares") as t:
            people = [Circle(radius=0.8) for _ in range(n)]
            people_group = VGroup(*people)
            people_group.arrange_in_grid(cols=1, buff=0.1)
            for person in people:
                person.set_stroke(width=0)
                person.set_fill(RED, opacity=0.5)
                self.play(Create(person), run_time=t.duration / n)

        with self.voiceover("and exactly three shares are necessary") as t:
            for i in range(need - 1):
                self.play(
                    people[i].animate.set_fill(GREEN, opacity=0.5),
                    run_time=t.duration / (need - 1),
                )

        with self.voiceover("to decrypt the complete secret. ") as t:
            self.play(
                Transform(secret, Text(secret_text, font_size=40).shift(LEFT * 4)),
                people[need - 1].animate.set_fill(GREEN, opacity=0.5),
                run_time=t.duration,
            )

        with self.voiceover("There's a simple solution for needing two shares") as t:
            self.play(
                people[need - 1].animate.set_fill(RED, opacity=0.5), run_time=t.duration
            )

        self.play(Unwrite(secret), people_group.animate.shift(LEFT * 2))

        segment = len(secret_text) // n
        shares = [
            MarkupText(self.pm_hide(secret_text, i, segment), font_size=40)
            for i in range(0, len(secret_text), segment)
        ]
        with self.voiceover("which is just giving each person part of the secret"):
            for person, share in zip(people, shares):
                share.next_to(person, RIGHT, buff=0.1)
                self.play(Write(share), run_time=t.duration / n)

        with self.voiceover("but this gives each participant some information") as t:
            self.wait(t.duration)

        with self.voiceover("about what the final secret is. ") as t:
            for person, share in zip(people, shares):
                self.play(Unwrite(share), run_time=t.duration / (n * 2))
                self.play(Uncreate(person), run_time=t.duration / (n * 2))

        with self.voiceover("We need a different approach. ") as t:
            self.wait(t.duration)

        self.wait()

    def pm_hide(self, text, start, length):
        before = text[:start]
        hidden = text[start : start + length]
        after = text[start + length :]
        pango_markup = f"{before}<span color='black'>{hidden}</span>{after}"
        return pango_markup


def ahide(mobj):
    return mobj.animate.set_opacity(0)

def ashow(mobj):
    return mobj.animate.set_opacity(1)


class ExplainBasicPolynomialIdea(VoiceoverScene):
    def construct(self):
        setup_speech(self)

        ax = Axes()
        func = lambda x: (0.35 * (x**2)) + x + 1
        graph = ax.plot(func, color=PURPLE_B)
        with self.voiceover("Let's consider a second-degree polynomial") as t:
            self.play(Create(ax), run_time=t.duration / 2)
            self.play(Create(graph), run_time=t.duration / 2)

        func = lambda x: -2
        with self.voiceover("We'll set the constant term equal to our secret") as t:
            constant_graph = ax.plot(func, color=PURPLE_B)
            self.play(Transform(graph, constant_graph), run_time=t.duration)

        func = lambda x: (0.2 * (x**2)) + (0.35 * x) - 2
        with self.voiceover("The other coefficients will be chosen randomly") as t:
            real_graph = ax.plot(func, color=PURPLE_B)
            self.play(Transform(graph, real_graph), run_time=t.duration)

        line_time = 0.85
        dots_with_lines = []
        with self.voiceover(
            "Now, shares will consist of points that appear on the polynomial"
        ) as t:
            for x in range(1, n + 1):
                point = ax.coords_to_point(x, func(x))
                dot = Dot(point)
                line = ax.get_vertical_line(point)
                self.play(Create(line), run_time=(t.duration/n) * line_time)
                self.play(Create(dot), run_time=(t.duration/n) * (1-line_time))
                dots_with_lines.append((dot, line))
        
        with self.voiceover(
            """
            Because, this is a second-degree polynomial, it can be completely
            determined from any three points that lie on it. 
            """.strip().replace("\n", " ")
        ) as t:
            for to_hide in range(n):
                dot, line = dots_with_lines[to_hide]
                self.play(ahide(dot), run_time=0)
                self.play(ahide(line), run_time=t.duration / (n * 3))
                self.wait(t.duration / (n * 3))
                self.play(ashow(line), run_time=t.duration / (n * 3))
                self.play(ashow(dot), run_time=0)
        
        to_hide_transition = n - 2
        with self.voiceover(
            "This reconstruction process is where linear algebra comes in. "
        ) as t:
            bdot, bline = dots_with_lines[to_hide_transition]
            self.play(ahide(bdot), run_time=0)
            self.play(ahide(bline), run_time=t.duration/(n*3))
            self.remove(bdot, bline)

        self.wait()

        rmduration = 1
        self.play(
            Uncreate(graph),
            *( Uncreate(line) for (_, line) in dots_with_lines if line is not bline ),
            run_time=rmduration/2
        )
        self.play(
            *( Uncreate(dot) for (dot, _) in dots_with_lines if dot is not bdot ),
            run_time=0
        )
        self.play(Uncreate(ax), run_time=rmduration/2)

        self.wait()

class ExplainPolynomialInterpolation(VoiceoverScene):
    def construct(self):
        setup_speech(self)

        polynomialfn = lambda shift: MathTex(
            r"f(x) = a_2 x^2 + a_1 x + a_0"
        ).shift(shift)
        middle_polynomial = polynomialfn(ORIGIN)
        with self.voiceover("Here's our polynomial with unknown coefficients. ") as t:
            self.play(Write(middle_polynomial), run_time=t.duration)
        
        up_polynomial, dn_polynomial = polynomialfn(UP), polynomialfn(DOWN)
        with self.voiceover("We have three points that we're interpolating") as t:
            self.play(
                Write(up_polynomial),
                Write(dn_polynomial),
                run_time=t.duration
            )
        
        with self.voiceover("so let's sub in the known x and y pairs. ") as t:
            self.play(
                Transform(up_polynomial, MathTex(
                    r"y_0 = a_2 x_0^2 + a_1 x_0 + a_0",
                ).shift(UP)),
                Transform(middle_polynomial, MathTex(
                    r"y_1 = a_2 x_1^2 + a_1 x_1 + a_0",
                ).shift(ORIGIN)),
                Transform(dn_polynomial, MathTex(
                    r"y_2 = a_2 x_1^2 + a_1 x_1 + a_0",
                ).shift(DOWN)),
                run_time=t.duration,
            )
        
        with self.voiceover("This is a linear system of equations") as t:
            self.wait(t.duration)
        
        matrix_form = MathTex(
            r"""
            \begin{bmatrix}
            1 & x_0 & x_0^2 \\
            1 & x_1 & x_1^2 \\
            1 & x_2 & x_2^2
            \end{bmatrix}
            \begin{bmatrix}
            a_0 \\ a_1 \\ a_2
            \end{bmatrix}
            =
            \begin{bmatrix}
            y_0 \\ y_1 \\ y_2
            \end{bmatrix}
            """.strip().replace("\n", " ")
        )
        with self.voiceover("so let's represent it as a matrix. ") as t:
            self.play(
                *(
                    Unwrite(i)
                    for i in [up_polynomial, middle_polynomial, dn_polynomial]
                ),
                run_time=t.duration/2
            )
            self.play(Write(matrix_form), run_time=t.duration/2)

        with self.voiceover(
            """
            We can find the coefficients by solving this system,
            which is something we already know how to do. 
            """.strip().replace("\n", " ")
        ) as t:
            self.wait(t.duration)
        
        general_form = MathTex(
            r"""
            \begin{bmatrix}
            1 & x_0^1 & \cdots & x_0^n \\
            1 & x_1^1 & \cdots & x_1^n \\
            \vdots & \vdots & \ddots & \vdots \\
            1 & x_n^1 & \cdots & x_n^n
            \end{bmatrix}
            \begin{bmatrix}
            a_0 \\ a_1 \\ a_2 \\ \vdots \\ a_n
            \end{bmatrix}
            =
            \begin{bmatrix}
            y_0 \\ y_1 \\ y_2 \\ \vdots \\ y_n
            \end{bmatrix}
            """
        )
        with self.voiceover(
            "Here it is in the general case, for an n-degree polynomial. "
        ) as t:
            self.play(Unwrite(matrix_form), run_time=t.duration/2)
            self.play(Write(general_form), run_time=t.duration/2)
        
        with self.voiceover(
            """
            This method does actually work,
            but it isn't possible in the real world,
            because it relies on us being able to represent real numbers
            with perfect precision. 
            """.strip().replace("\n", " ")
        ) as t:
            self.wait(t.duration)
        
        with self.voiceover("This isn't something we can actually do. ") as t:
            self.play(Unwrite(general_form), run_time=t.duration)

        self.wait()

class Top(VoiceoverScene):
    def construct(self):
        setup_speech(self)

        ax = Axes()
        func = lambda x: (0.35 * (x**2)) + x + 1
        graph = ax.plot(func, color=PURPLE_B)
        with self.voiceover(
            "Let's make a small adjustment to the way we generate our polynomial. "
        ) as t:
            self.play(Create(ax), run_time=t.duration / 2)
            self.play(Create(graph), run_time=t.duration / 2)

        func = lambda x: -2
        with self.voiceover(
            "We'll still set the constant term equal to our secret"
        ) as t:
            constant_graph = ax.plot(func, color=PURPLE_B)
            self.play(Transform(graph, constant_graph), run_time=t.duration)

        func = lambda x: (0.2 * (x**2)) + (0.35 * x) - 2
        with self.voiceover("and choose the remaining coefficients at random") as t:
            real_graph = ax.plot(func, color=PURPLE_B)
            self.play(Transform(graph, real_graph), run_time=t.duration)
        
        self.wait(0.25)

        func = lambda x: (0.25 * (x**2)) + (0.5 * x) - 2
        with self.voiceover(
            "but this time they'll be random integers. "
        ) as t:
            real_real_graph = ax.plot(func, color=PURPLE_B)
            self.play(Transform(graph, real_real_graph), run_time=t.duration)
        
        line_time = 0.85
        dots_with_lines = []
        with self.voiceover(
            """
            This ensures that the shares generated will be integers as well,
            keeping us from having to store them with impossible precision. 
            """.strip().replace("\n", " ")
        ) as t:
            for x in range(1, n + 1):
                point = ax.coords_to_point(x, func(x))
                dot = Dot(point)
                line = ax.get_vertical_line(point)
                self.play(Create(line), run_time=(t.duration/n) * line_time)
                self.play(Create(dot), run_time=(t.duration/n) * (1-line_time))
                dots_with_lines.append((dot, line))

        with self.voiceover("Formalizing why requires a step back. ") as t:
            rmduration = t.duration
            self.play(
                Uncreate(graph),
                *( Uncreate(line) for (_, line) in dots_with_lines ),
                run_time=rmduration/2
            )
            self.play(
                *( Uncreate(dot) for (dot, _) in dots_with_lines ),
                run_time=0
            )
            self.play(Uncreate(ax), run_time=rmduration/2)

        self.wait()
