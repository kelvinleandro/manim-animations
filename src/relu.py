from manim import *


class ReLU(Scene):
    def construct(self):
        # Title
        title = Text("ReLU Activation Function", font_size=40)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 4, 1],
            axis_config={"color": BLUE},
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="ReLU(x)")

        # ReLU Function
        relu_graph = axes.plot(
            lambda x: max(0, x),
            color=YELLOW,
        )
        relu_label = axes.get_graph_label(
            relu_graph,
            label=Text("ReLU(x) = max(0, x)", font_size=24),
            x_val=1,
            buff=1,
        )

        # Display Axes and ReLU Graph
        self.play(Create(axes), Write(axes_labels))
        self.play(Create(relu_graph), Write(relu_label), run_time=2)
        self.wait(1)

        # Explanation
        explanation = Text(
            "ReLU(x) = max(0, x)\n\n"
            "ReLU sets all negative values to 0\n"
            "and keeps positive values unchanged.",
            font_size=22,
            line_spacing=1.5,
        )
        explanation.shift(LEFT * 3.5)

        self.play(Write(explanation))

        # Highlighting the effect of ReLU
        input_values = [-2, 0, 2]
        dots = VGroup()
        for x in input_values:
            dot = Dot().move_to(axes.c2p(x, max(0, x)))
            dots.add(dot)

        self.play(LaggedStart(*[Create(dot) for dot in dots], lag_ratio=0.5))
        self.wait(3)
