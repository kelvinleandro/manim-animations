from manim import *


class Sigmoid(Scene):
    def construct(self):
        # Title
        title = Text("Sigmoid Activation Function", font_size=40)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Axes
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-0.5, 1.5, 0.5],
            axis_config={"color": BLUE, "include_numbers": True},
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label=r"\sigma(x)")

        # Sigmoid Function
        sigmoid_graph = axes.plot(
            lambda x: 1 / (1 + np.exp(-x)),
            color=YELLOW,
        )
        sigmoid_label = axes.get_graph_label(
            sigmoid_graph, label=r"\sigma(x) = \frac{1}{1 + e^{-x}}", direction=UP
        )

        # Display Axes and Sigmoid Graph
        self.play(Create(axes), Write(axes_labels))
        self.play(Create(sigmoid_graph), Write(sigmoid_label), run_time=2)
        self.wait(1)

        # Explanation
        explanation = Text(
            "Sigmoid maps any input to \n"
            "a value between 0 and 1.\n"
            "It is often used in binary classification.",
            font_size=22,
            line_spacing=1.5,
        )
        explanation.shift(LEFT * 3.5 + UP * 1.5)

        self.play(Write(explanation))
        self.wait(2)

        # Highlighting the effect of Sigmoid
        input_values = [-4, 0, 4]
        dots = VGroup()
        dashed_lines = VGroup()
        for x in input_values:
            y = 1 / (1 + np.exp(-x))
            dot = Dot().move_to(axes.c2p(x, y))
            dashed_line = DashedLine(
                start=axes.c2p(x, 0), end=axes.c2p(x, y), color=GREEN
            )
            dots.add(dot)
            dashed_lines.add(dashed_line)

        self.play(
            LaggedStart(
                *[Create(VGroup(dot, line)) for dot, line in zip(dots, dashed_lines)],
                lag_ratio=0.5
            )
        )
        self.wait(3)
