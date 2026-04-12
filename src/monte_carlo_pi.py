import numpy as np
from manim import *


class MonteCarloPi(Scene):
    def construct(self):
        np.random.seed(100)

        N_POINTS = 1000
        BATCH_SIZE = int(N_POINTS * 0.05)
        SCALE = 2.5
        SHIFT = LEFT * 1.8

        pts_x = np.random.uniform(-1, 1, N_POINTS)
        pts_y = np.random.uniform(-1, 1, N_POINTS)
        inside_mask = (pts_x**2 + pts_y**2) <= 1.0

        square = Square(side_length=2 * SCALE, color=WHITE, stroke_width=2).shift(SHIFT)
        circle = Circle(radius=SCALE, color=YELLOW, stroke_width=2.5).shift(SHIFT)

        title = Text("Monte Carlo Method for π").to_edge(UP)

        formula = MathTex(
            r"\pi \approx 4 \cdot \frac{N_{\text{inside}}}{N_{\text{total}}}"
        ).to_edge(DOWN + RIGHT * 1.3)

        def make_stats(total, inside):
            pi_est = 4 * inside / total if total > 0 else 0.0
            total_line = VGroup(
                Text("Total:  ", font_size=26, color=GRAY_A),
                Text(f"{total}", font_size=26),
            ).arrange(RIGHT, buff=0.1)
            inside_line = VGroup(
                Text("Inside:  ", font_size=26, color=GRAY_A),
                Text(f"{inside}", font_size=26, color=GREEN),
            ).arrange(RIGHT, buff=0.1)
            pi_line = MathTex(
                rf"\hat{{\pi}} = {pi_est:.5f}",
                font_size=32,
                color=YELLOW,
            )
            box = VGroup(total_line, inside_line, pi_line).arrange(
                DOWN, aligned_edge=LEFT, buff=0.35
            )
            box.to_corner(UR).shift(DOWN * 0.8 + LEFT * 0.3)
            return box

        stats = make_stats(0, 0)

        self.play(Write(title))
        self.wait(0.4)

        self.play(Create(square), Create(circle), run_time=1.5)
        self.play(Write(formula))
        self.add(stats)
        self.wait(0.8)

        inside_count = 0

        for batch_start in range(0, N_POINTS, BATCH_SIZE):
            batch_end = min(batch_start + BATCH_SIZE, N_POINTS)

            batch_dots = VGroup()
            for i in range(batch_start, batch_end):
                sx = pts_x[i] * SCALE + SHIFT[0]
                sy = pts_y[i] * SCALE
                color = GREEN if inside_mask[i] else RED
                batch_dots.add(Dot(point=np.array([sx, sy, 0]), radius=0.04, color=color))
                if inside_mask[i]:
                    inside_count += 1

            total_count = batch_end
            new_stats = make_stats(total_count, inside_count)

            self.play(
                FadeIn(batch_dots),
                Transform(stats, new_stats),
                run_time=0.35,
            )

        self.wait(1.5)

        pi_estimated = 4 * inside_count / N_POINTS

        result = VGroup(
            MathTex(rf"\hat{{\pi}} = {pi_estimated:.5f}", font_size=44, color=YELLOW),
            MathTex(r"\pi = 3.14159\ldots", font_size=36, color=WHITE),
        ).arrange(DOWN, buff=0.3)
        result.next_to(formula, UP, buff=0.4)

        self.play(Write(result[0]))
        self.play(Write(result[1]))
        self.wait(3)
