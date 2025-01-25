from manim import *

FONT_SIZE = 28
EQ_FONT_SIZE = 32
TICKS_AXES_GAP = 0.5

class EuclideanDistance(Scene):
    def construct(self):
        title = Text("Euclidean Distance").to_edge(UP)

        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 6, 1],
            x_length=5,
            y_length=5,
            tips=True,
        ).shift(LEFT * 4)
        axes_labels = axes.get_axis_labels()

        x_ticks = VGroup(
            MathTex("x_1", font_size=FONT_SIZE).move_to(axes.c2p(2, TICKS_AXES_GAP)),
            MathTex("x_2", font_size=FONT_SIZE).move_to(axes.c2p(5, TICKS_AXES_GAP)),
        )
        y_ticks = VGroup(
            MathTex("y_1", font_size=FONT_SIZE).move_to(axes.c2p(TICKS_AXES_GAP, 3)),
            MathTex("y_2", font_size=FONT_SIZE).move_to(axes.c2p(TICKS_AXES_GAP, 4)),
        )

        dot1 = Dot(axes.c2p(2, 3), color=BLUE)
        dot2 = Dot(axes.c2p(5, 4), color=RED)

        label1 = MathTex("(x_1, y_1)", font_size=FONT_SIZE).next_to(dot1, LEFT)
        label2 = MathTex("(x_2, y_2)", font_size=FONT_SIZE).next_to(dot2, RIGHT)

        line = Line(dot1.get_center(), dot2.get_center(), color=YELLOW, buff=0.1)

        # line between (x_1, y_1) and (x_2, y1)
        h_line = DashedLine(start=dot1.get_center(), end=axes.c2p(5, 3), color=GREEN)
        h_line_text = MathTex(
            "x_2 - x_1", font_size=FONT_SIZE, color=GREEN
        ).next_to(h_line, DOWN, buff=0.2)
        # line between (x_2, y_1) and (x_2, y2)
        v_line = DashedLine(start=axes.c2p(5, 3), end=dot2.get_center(), color=GREEN)
        v_line_text = MathTex(
            "y_2 - y_1", font_size=FONT_SIZE, color=GREEN
        ).next_to(v_line, RIGHT, buff=0.2)

        step1 = MathTex(
            "d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}", font_size=EQ_FONT_SIZE
        ).shift(RIGHT * 4 + UP * 2)

        step2 = MathTex(
            "d = \sqrt{(5 - 2)^2 + (4 - 3)^2}", font_size=EQ_FONT_SIZE
        ).next_to(step1, DOWN)

        step3 = MathTex("d = \sqrt{3^2 + 1^2}", font_size=EQ_FONT_SIZE).next_to(
            step2, DOWN
        )

        step4 = MathTex("d = \sqrt{9 + 1}", font_size=EQ_FONT_SIZE).next_to(step3, DOWN)

        step5 = MathTex("d = \sqrt{10}", font_size=EQ_FONT_SIZE).next_to(step4, DOWN)
        distance_label = (
            MathTex("\sqrt{10}", font_size=FONT_SIZE)
            .set_color(YELLOW)
            .move_to(line.get_center() + UP * 0.3)
        )

        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(Create(axes), Create(axes_labels), run_time=2)
        self.wait(1)
        self.play(FadeIn(x_ticks), FadeIn(y_ticks))
        self.wait(1)
        self.play(FadeIn(dot1, label1), FadeIn(dot2, label2))
        self.wait(1)
        self.play(Create(line))
        self.wait(1)
        self.play(Create(h_line), Create(v_line))
        self.play(Write(h_line_text), Write(v_line_text))
        self.wait(1)

        self.play(Write(step1))
        self.play(Write(step2))
        self.play(Write(step3))
        self.play(Write(step4))
        self.play(Write(step5))
        self.play(Write(distance_label))

        self.wait(2)
