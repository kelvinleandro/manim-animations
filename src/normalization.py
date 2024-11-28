from manim import *
import numpy as np

class Normalization(Scene):
    def construct(self):
        means = [5.0, 10.0]
        stds = [2.0, 3.0]

        data = np.column_stack([
            np.random.normal(loc=mean, scale=std, size=15) 
            for mean, std in zip(means, stds)
        ])

        mins = data.min(axis=0)
        maxs = data.max(axis=0)

        centered_data = data - np.mean(data, axis=0)
        normalized_data = centered_data / np.std(data, axis=0)

        axes = Axes(
            x_range=[-10, maxs[0] + 2, 1], 
            y_range=[-10, maxs[1] + 2, 1],
            x_length=10,
            y_length=7,
            axis_config={"include_numbers": False, "include_tip": True, "include_ticks": False}
        )
        axes_labels = axes.get_axis_labels("x", "y")

        dots = VGroup(*[
            Dot(axes.c2p(x, y), color=BLUE) for x, y in data
        ])

        centered_dots = VGroup(*[
            Dot(axes.c2p(x, y), color=BLUE) for x, y in centered_data
        ])

        normalized_dots = VGroup(*[
            Dot(axes.c2p(x, y), color=BLUE) for x, y in normalized_data
        ])

        self.add(axes)
        self.wait(2)

        self.play(AnimationGroup(*[GrowFromCenter(dot) for dot in dots], lag_ratio=0.1))
        self.wait(1)

        self.play(
            AnimationGroup(
                *[dot.animate.move_to(new_dot.get_center()) for dot, new_dot in zip(dots, centered_dots)],
                lag_ratio=0.1
            )
        )
        self.wait(1)

        self.play(
            AnimationGroup(
                *[dot.animate.move_to(new_dot.get_center()) for dot, new_dot in zip(dots, normalized_dots)],
                lag_ratio=0.1
            )
        )
        self.wait(1)
