from manim import *
import numpy as np

TEXT_FONT_SIZE = 32
AXIS_LABEL_FONT_SIZE = 24


class LogTransform(Scene):
    def construct(self):
        np.random.seed(42)
        title = Text("Log Transformation").to_edge(UP)
        original_eq = MathTex(
            "\lambda e^{-\lambda x}", font_size=TEXT_FONT_SIZE
        ).move_to(RIGHT * 3 + UP * 2)
        log_eq = MathTex("ln(\lambda) -\lambda x", font_size=TEXT_FONT_SIZE).next_to(
            original_eq, DOWN, buff=2
        )
        arrow = Arrow(
            start=original_eq.get_bottom(),
            end=log_eq.get_top(),
            buff=0.3,
            stroke_width=4,
        )
        arrow_text = Text("Applying log", font_size=TEXT_FONT_SIZE).next_to(
            arrow, RIGHT, buff=0.3
        )

        data = np.random.exponential(scale=5, size=1000)
        log_transformed_data = np.log(data + 1)
        og_hist, og_bin_edges = np.histogram(data, bins=30, density=True)
        log_hist, log_bin_edges = np.histogram(
            log_transformed_data, bins=30, density=True
        )

        original_axes = Axes(
            x_range=[0, max(data) + 1, 10],
            y_range=[0, max(og_hist) + 0.1, 0.1],
            x_length=8,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 20},
        ).to_edge(LEFT)
        original_labels = original_axes.get_axis_labels(
            x_label=MathTex("x", font_size=AXIS_LABEL_FONT_SIZE),
            y_label=Text("Density", font_size=AXIS_LABEL_FONT_SIZE),
        )

        original_rectangles = VGroup()
        for height, left_edge, right_edge in zip(
            og_hist, og_bin_edges[:-1], og_bin_edges[1:]
        ):
            rect = Rectangle(
                width=original_axes.c2p(right_edge, 0)[0]
                - original_axes.c2p(left_edge, 0)[0],
                height=original_axes.c2p(0, height)[1] - original_axes.c2p(0, 0)[1],
                color=BLUE,
                fill_opacity=0.6,
            ).move_to(
                original_axes.c2p((left_edge + right_edge) / 2, 0), aligned_edge=DOWN
            )
            original_rectangles.add(rect)

        log_axes = Axes(
            x_range=[0, max(log_transformed_data) + 1, 1],
            y_range=[0, max(log_hist) + 0.1, 0.1],
            x_length=8,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 20},
        ).to_edge(LEFT)
        log_labels = log_axes.get_axis_labels(
            x_label=MathTex("log(x+1)", font_size=AXIS_LABEL_FONT_SIZE),
            y_label=Text("Density", font_size=AXIS_LABEL_FONT_SIZE),
        )

        log_rectangles = VGroup()
        for height, left_edge, right_edge in zip(
            log_hist, log_bin_edges[:-1], log_bin_edges[1:]
        ):
            rect = Rectangle(
                width=log_axes.c2p(right_edge, 0)[0] - log_axes.c2p(left_edge, 0)[0],
                height=log_axes.c2p(0, height)[1] - log_axes.c2p(0, 0)[1],
                color=GREEN,
                fill_opacity=0.6,
            ).move_to(log_axes.c2p((left_edge + right_edge) / 2, 0), aligned_edge=DOWN)
            log_rectangles.add(rect)

        self.play(Write(title))
        self.wait(2)
        self.play(Create(original_axes), Write(original_labels), run_time=2)
        self.play(Create(original_rectangles), run_time=2)
        self.wait(2)

        self.play(Write(original_eq))
        self.wait()
        self.play(GrowArrow(arrow), Write(arrow_text))
        self.wait()
        self.play(Write(log_eq))
        self.wait()

        self.play(
            Transform(original_axes, log_axes),
            Transform(original_labels, log_labels),
            Transform(original_rectangles, log_rectangles),
            run_time=3,
        )
        self.wait(2)
