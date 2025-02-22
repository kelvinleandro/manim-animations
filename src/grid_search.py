from manim import *
import numpy as np


class GridSearch3D(ThreeDScene):
    def construct(self):
        title = Text("Grid Search for Hyperparameter Tuning", font_size=40)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        intro_text = Text(
            "Suppose we have two\n"
            "hyperparameters and aim to\n"
            "optimize a specific metric\n"
            "in our model",
            font_size=32,
        ).shift(LEFT * 3)

        self.play(Write(intro_text))
        self.wait(3)
        self.play(Unwrite(intro_text))
        self.wait(1)

        # Hyperparameter grid (3x3)
        hyperparams_1 = [1, 2, 3, 4]
        hyperparams_2 = [1, 2, 3, 4]

        # Create 3D axes
        axes_3d = ThreeDAxes(
            x_range=[0, 5, 0.05],
            y_range=[0, 5, 0.05],
            z_range=[0, 1, 0.1],
            axis_config={"color": BLUE, "include_ticks": False},
        )
        axes_3d_labels = axes_3d.get_axis_labels(
            x_label=Text("Hyperparam 1"),
            y_label=Text("Hyperparam 2"),
            z_label=Text("Accuracy"),
        )

        # Hiding z-axis and z-label initially
        axes_3d.z_axis.set_opacity(0)
        axes_3d_labels[2].set_opacity(0)

        # Start with a top view (z = 0)
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=0.5)

        # Create 3D points (initially at z = 0)
        points_3d = VGroup()
        for h1 in hyperparams_1:
            for h2 in hyperparams_2:
                point = Dot3D().move_to(axes_3d.c2p(h1, h2, 0))
                points_3d.add(point)

        question_text = Text(
            "Which combination of\nhyperparameters yields\nthe best performance?",
            t2c={"best": BLUE},
            line_spacing=1.5,
            font_size=22,
        ).next_to(axes_3d, LEFT, buff=0.3)

        # Display 3D axes and points (top view)
        self.play(Create(axes_3d), Write(axes_3d_labels))
        self.play(LaggedStart(*[Create(point) for point in points_3d], lag_ratio=0.1))
        self.wait(1)

        self.play(Write(question_text))
        self.wait(2)

        self.play(FadeOut(points_3d), FadeOut(question_text))
        self.wait(1)

        # Change camera orientation to show 3D axes properly
        self.move_camera(phi=75 * DEGREES, theta=-45 * DEGREES, run_time=2)

        # Showing z-axis and z-label
        self.play(
            axes_3d.z_axis.animate.set_opacity(1),
            axes_3d_labels[2].animate.set_opacity(1),
        )

        self.wait(1)

        MEAN_X1, MEAN_Y1 = 2.5, 2.5
        MEAN_X2, MEAN_Y2 = 4, 4
        MEAN_X3, MEAN_Y3 = 1, 1

        def gaussian_function(u, v):
            return (
                np.exp(-((u - MEAN_X1) ** 2 + (v - MEAN_Y1) ** 2))
                + 0.3
                * np.exp(
                    -(((u - MEAN_X2) ** 2 + (v - MEAN_Y2) ** 2) / (2 * (0.2) ** 2))
                )
                + 0.45
                * np.exp(
                    -(((u - MEAN_X3) ** 2 + (v - MEAN_Y3) ** 2) / (2 * (0.5) ** 2))
                )
            )

        # Create the 3D surface
        surface = Surface(
            lambda u, v: axes_3d.c2p(u, v, gaussian_function(u, v)),
            u_range=[0.2, 5],
            v_range=[0.2, 5],
            resolution=15,
            fill_opacity=0.7,
        )
        surface.set_fill_by_value(axes_3d, colorscale=[RED, BLUE], axis=2)
        self.play(Create(surface))
        self.wait(2)

        # Rotate the scene for a better view
        self.begin_ambient_camera_rotation(rate=0.35)
        self.wait(7)

        max_point = Dot3D(
            axes_3d.c2p(2.5, 2.5, gaussian_function(2.5, 2.5)), radius=0.25
        )
        self.play(Create(max_point))
        self.wait(2)

        self.stop_ambient_camera_rotation()
        self.wait(1)

        self.play(FadeOut(surface))
        self.wait(2)

        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=2)
        # Hiding z-axis and z-label
        self.play(
            axes_3d.z_axis.animate.set_opacity(0),
            axes_3d_labels[2].animate.set_opacity(0),
        )
        self.wait(2)

        line_x = Line3D(
            start=axes_3d.c2p(2.5, 0, 0), end=axes_3d.c2p(2.5, 2.5, 0), color=GREEN
        )
        line_y = Line3D(
            start=axes_3d.c2p(0, 2.5, 0), end=axes_3d.c2p(2.5, 2.5, 0), color=GREEN
        )
        best_x = MathTex("x").move_to(axes_3d.c2p(2.5, -0.25, 0))
        best_y = MathTex("y").move_to(axes_3d.c2p(-0.25, 2.5, 0))

        self.play(
            Create(VGroup(line_x, line_y)), Write(VGroup(best_x, best_y)), run_time=2
        )
        self.wait(2)

        best_combination_text = Text("Best combination: ", font_size=42).shift(
            RIGHT * 3 + UP * 2
        )
        best_h1_text = MathTex(r"\text{Hyperparameter}_1 = x", font_size=42).next_to(
            best_combination_text, DOWN, buff=0.2
        )
        best_h2_text = MathTex(r"\text{Hyperparameter}_2 = y", font_size=42).next_to(
            best_h1_text, DOWN, buff=0.2
        )

        self.play(
            Write(VGroup(best_combination_text, best_h1_text, best_h2_text)), run_time=2
        )
        self.wait(3)
