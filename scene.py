from manim import *

from manim_voiceover import VoiceoverScene
from manim_voiceover.services.coqui import CoquiService

speech_service = CoquiService()
setup_speech = lambda obj: obj.set_speech_service(speech_service)

n, need = 4, 3


def scene_card(scene, part, text):
    card = Text(f"Part {part}: {text}", font_size=80)
    scene.play(Create(card))
    scene.wait()
    scene.play(Uncreate(card))
    scene.wait(0.5)

class SceneCard1(Scene):
    def construct(self):
        scene_card(self, 1, "Secret Sharing")

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

class ExplainBrokenVariant(VoiceoverScene):
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

class SceneCard2(Scene):
    def construct(self):
        scene_card(self, 2, "Rings and Fields")

class ExplainBasicAlgebraicStructures(VoiceoverScene):
    def construct(self):
        setup_speech(self)

        operations = [
            MathTex("+", font_size=100).shift(2 * (LEFT + UP)),
            MathTex("-", font_size=100).shift(2 * (RIGHT + UP)),
            MathTex(r"\times", font_size=100).shift(2 * (LEFT + DOWN)),
        ]
        with self.voiceover(
            """
            When some sort of mathematical object yields reasonable
            definitions of addition, subtraction, and multiplication 
            """.strip().replace("\n", " ")
        ) as t:
            for mobj in operations:
                self.play(Write(mobj), run_time=t.duration / (len(operations)))
        
        ring_text = Text("Ring", font_size=80)
        with self.voiceover("we call it a") as t:
            self.play(Write(ring_text), run_time=t.duration)
        
        with self.voiceover("ring. ") as t:
            self.wait(t.duration)
        
        place_polynomial = lambda tex: MathTex(tex).shift(2 * (RIGHT + DOWN))
        polynomial = place_polynomial("x")
        with self.voiceover("Polynomials involve") as t:
            self.play(Create(polynomial), run_time=t.duration)
        
        with self.voiceover("using multiplication") as t:
            self.play(
                Transform(polynomial, place_polynomial("a_i x^i")),
                run_time=t.duration
            )
        
        with self.voiceover("and addition") as t:
            self.play(
                Transform(polynomial, place_polynomial("y = \sum_{i=0}^n a_i x^i")),
                run_time=t.duration
            )
        
        with self.voiceover("so a polynomial can be created out of any ring. ") as t:
            self.play(
                Transform(ring_text, Text("For any ring...", font_size=80)),
                run_time=t.duration
            )
        
        with self.voiceover(
            "The integers form a ring, so it makes sense to define polynomials with them. "
        ) as t:
            self.play(
                Transform(ring_text, MathTex(r"x, y, a_i \in \mathbb{Z}", font_size=80)),
                run_time=t.duration
            )

        with self.voiceover(
            """
            The integer ring is a closed system, so a polynomial made with integers
            will always yield integers.
            """.strip().replace("\n", " ")
        ) as t:
            self.play(Unwrite(polynomial), Unwrite(ring_text), run_time=t.duration)
        
        division = MathTex(r"\div", font_size=100).shift(2 * (RIGHT + DOWN))
        operations.append(division)
        with self.voiceover(
            "However, polynomial interpolation requires a division operation. "
        ) as t:
            self.play(Write(division), run_time=t.duration)
        
        with self.voiceover(
            "A mathematical object equipped with all four basic operations"
        ) as t:
            self.wait(t.duration)
        
        field_text = Text("Field", font_size=80)
        with self.voiceover("is called a field. ") as t:
            self.play(Write(field_text), run_time=t.duration)
        
        with self.voiceover(
            """
            The integers do not form a field, because you can divide
            two integers and get something that isn't an integer.
            It's not a closed system. 
            """.strip().replace("\n", " ")
        ) as t:
            self.wait(t.duration)
        
        with self.voiceover(
            """
            In other words, when we choose integer coefficients, we aren't actually dealing
            with only integers. All of our math is still defined in terms of
            """.strip().replace("\n", " ")
        ) as t:
            self.wait(t.duration)
        
        with self.voiceover("the real numbers,") as t:
            self.play(
                Transform(field_text, MathTex(r"\mathbb{R}", font_size=80)),
                run_time=t.duration
            )
        
        with self.voiceover("which do form a field. ") as t:
            self.wait(t.duration)
        
        with self.voiceover("The official term for this is") as t:
            self.wait(t.duration)
        
        with self.voiceover("kludgy hacky worthless screwup garbage. ") as t:
            self.play(
                Transform(field_text, Text("KHWSG", font_size=80)),
                *( Unwrite(i) for i in operations ),
                run_time=t.duration
            )
        
        self.wait(0.5)
        
        self.play(Unwrite(field_text))

        self.wait()

class LooselyExplainWhyIntegersDontWork(VoiceoverScene):
    def construct(self):
        setup_speech(self)

        ax = Axes()
        func = lambda x: (0.2 * (x**2)) + (0.35 * x) - 2
        graph = ax.plot(func, color=PURPLE_B)
        with self.voiceover(
            """
            I'm not going to try to explain it here, since it's just a bunch
            of number theory I don't understand
            """.strip().replace("\n", " ")
        ) as t:
            self.play(Create(ax), run_time=t.duration / 2)
            self.play(Create(graph), run_time=t.duration / 2)

        func = lambda x: (0.25 * (x**2)) + (0.5 * x) - 2
        with self.voiceover(
            """
            but the trick is that using integer coefficients
            limits the space of what polynomials are allowed.
            """.strip().replace("\n", " ")
        ) as t:
            real_real_graph = ax.plot(func, color=PURPLE_B)
            self.play(Transform(graph, real_real_graph), run_time=t.duration)
        
        with self.voiceover(
            """
            This allows someone to take some shares and generate a very short list of possible
            polynomials that fit with both their known shares and the integer coefficient
            restriction. 
            This is why just using integers doesn't work either. 
            """.strip().replace("\n", " ")
        ) as t:
            self.wait(t.duration)
        
        rmduration = 1
        self.play(Unwrite(graph), run_time=rmduration/2)
        self.play(Unwrite(ax), run_time=rmduration/2)

        detailed = MathTex(r"x \in \mathbb{Z} \implies f(x) \in \mathbb{Z}", font_size=100)
        with self.voiceover(
            "To be specific, we've restricted the polynomial to be an integer at each integer value. "
        ) as t:
            self.play(Write(detailed), run_time=t.duration)

        with self.voiceover("This is what integers being rings actually caused - problems. ") as t:
            self.wait(t.duration)

        self.play(Unwrite(detailed))

        self.wait()

class SceneCard3(Scene):
    def construct(self):
        scene_card(self, 3, "Galois Fields")

class ExplainPrimeFields(VoiceoverScene):
    def construct(self):
        setup_speech(self)

        with self.voiceover(
                "Let's try and find a field that, unlike the real numbers, is finite. "
        ) as t:
            self.wait(t.duration)
        
        modular_eqn = MathTex(r"3 + 4 = 7", font_size=90)
        with self.voiceover("This necessitates modular arithmetic. ") as t:
            self.play(Write(modular_eqn), run_time=t.duration)
        
        with self.voiceover(
            "We can do math \"modulo\" some number n, where numbers essentially wrap around"
        ) as t:
            self.play(
                Transform(
                    modular_eqn,
                    MathTex(r"3 + 4 \equiv 2 \mod 5", font_size=90)
                ),
                run_time=t.duration
            )
        
        with self.voiceover("so here, seven reduces to two modulo five. ") as t:
            self.wait(t.duration)
        
        self.play(Unwrite(modular_eqn))

        m = 5
        cycles = 11
        cycle_fmt = lambda i: MathTex(
            f"{i % m} + 1 \equiv {(i + 1) % m} \mod {m}",
            font_size=90
        )
        cycle_eqn = cycle_fmt(0)
        with self.voiceover(
            """
            When working modulo n, no matter what,
            we only have n possible numbers to deal with.
            In other words, we are operating on a finite
            set of values. 
            """.strip().replace("\n", " ")
        ) as t:
            cycle_time = t.duration / cycles
            for i in range(cycles):
                if i == 0:
                    self.play(
                        Write(cycle_eqn),
                        run_time=cycle_time
                    )
                self.play(
                    Transform(cycle_eqn, cycle_fmt(i)),
                    run_time=cycle_time
                )

        with self.voiceover(
            "This lets us define addition, subtraction, and multiplication"
        ) as t:
            self.play(Unwrite(cycle_eqn))

        operations = [
            MathTex("+", font_size=100).shift(2 * (LEFT + UP)),
            MathTex("-", font_size=100).shift(2 * (RIGHT + UP)),
            MathTex(r"\times", font_size=100).shift(2 * (LEFT + DOWN)),
        ]
        with self.voiceover(
            """
            making the integers modulo any number form a ring, not a field. 
            """.strip().replace("\n", " ")
        ) as t:
            for mobj in operations:
                self.play(Write(mobj), run_time=t.duration / (len(operations)))
        
        with self.voiceover(
            "Division is necessarily defined as the inverse of multiplication"
        ) as t:
            self.wait(t.duration)
        
        composite_eqn = MathTex(
            r"x \cdot 2 \equiv 1 \mod 4",
            font_size=90
        )
        with self.voiceover(
            "and sometimes, this just isn't possible. "
        ) as t:
            self.play(Write(composite_eqn), run_time=t.duration)
        
        with self.voiceover(
            "Finding x here, which is equivalent to dividing one by two, is impossible. "
        ) as t:
            self.wait(t.duration)
        
        with self.voiceover("Here's the general rule that defines division") as t:
            self.play(
                Transform(
                    composite_eqn,
                    MathTex(
                        r"\frac{a}{b} \cdot b \equiv a \mod n",
                        font_size=90
                    )
                ),
                run_time=t.duration
            )
        
        with self.voiceover("and let's just solve for what a over b is. ") as t:
            self.play(
                Transform(
                    composite_eqn,
                    MathTex(
                        r"x \cdot b \equiv a \mod n",
                        font_size=90
                    )
                ),
                run_time=t.duration
            )
        
        with self.voiceover(
            "We can see that if x divides into n, we have to end up with zero instead of a. "
        ) as t:
            self.play(
                Transform(
                    composite_eqn,
                    MathTex(
                        r"x \cdot b \equiv 0 \mod n",
                        font_size=90
                    )
                ),
                run_time=t.duration
            )

        with self.voiceover("Thus, we need n to be prime. ") as t:
            self.wait(t.duration)
        
        self.play(Unwrite(composite_eqn))

        division = MathTex(r"\div", font_size=100).shift(2 * (RIGHT + DOWN))
        operations.append(division)
        with self.voiceover(
            "This is actually all we need to ensure division is always possible. "
        ) as t:
            self.play(Write(division), run_time=t.duration)
        
        prime_field = MathTex("\mathbb{Z} \mod p", font_size=100)
        with self.voiceover(
            "That's it. The integers, modulo some prime p, form a finite field. "
        ) as t:
            self.play(
                Write(prime_field),
                run_time=t.duration
            )
        
        with self.voiceover(
            "We typically call these \"prime fields\", and write them like this. "
        ) as t:
            self.play(
                Transform(
                    prime_field,
                    MathTex(r"\mathbb{Z}_p", font_size=100)
                ),
                run_time=t.duration
            )
        
        rmduration = 2
        to_rm = [prime_field, *operations]
        rm_time = rmduration / len(to_rm)
        for i in to_rm:
            self.play(Unwrite(i), run_time=rm_time)

        self.wait()

class ExplainGaloisFields(VoiceoverScene):
    def construct(self):
        setup_speech(self)

        with self.voiceover(
            "As it turns out, you can't just have a finite field with any number of elements"
        ) as t:
            self.wait(t.duration)
        
        with self.voiceover(
            "but they don't have to be prime either. "
        ) as t:
            self.wait(t.duration)
        
        gf = MathTex(r"p^m", font_size=100)
        with self.voiceover(
            """
            The number of elements in a finite field must be
            a prime number p to some natural power m.
            """.strip().replace("\n", " ")
        ) as t:
            self.play(Write(gf), run_time=t.duration)
        
        with self.voiceover("These are often called \"prime powers\". ") as t:
            self.wait(t.duration)
        
        with self.voiceover(
            "We call any field with a finite number of elements a Galois field. "
        ) as t:
            self.play(
                Transform(
                    gf,
                    MathTex(r"GF(p^m)", font_size=100)
                ),
                run_time=t.duration
            )

        with self.voiceover("So, what happens when m isn't equal to one?") as t:
            self.wait(t.duration)
        
        with self.voiceover(
            """
            Those are called extension fields, and are incredibly important
            to cryptography, closely tied to linear algebra, and unbelievably beautiful.
            But that's for part 2. 
            """):
            self.wait(t.duration)
        
        with self.voiceover("But for our secret sharing algorithm, prime fields work just fine. "):
            self.play(
                Transform(
                    gf,
                    MathTex(r"GF(p)", font_size=100)
                ),
                run_time=t.duration
            )
        
        with self.voiceover(
            """
            That's it. We solved the secret sharing problem.
            Just use polynomial interpolation on prime fields. 
            This algorithm is called "Shamir's Secret Sharing",
            after Adi Shamir. 
            """.strip().replace("\n", " ")
        ) as t:
            self.play(Unwrite(gf), run_time=t.duration)

        self.wait()
