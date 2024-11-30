from manim import *

class NormalDistribution(Scene):
    def construct(self):
        title = Text("Normal Distribution").to_edge(UP)

        mean_tracker = ValueTracker(0)
        std_tracker = ValueTracker(1)

        axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[0, 0.5, 0.1],
            x_length=8,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 28}
        ).next_to(title, DOWN, buff=0.3)
        
        axes_labels = axes.get_axis_labels(x_label="x", y_label="P(x)")
        axes_labels[0].set(font_size=28)
        axes_labels[1].set(font_size=28)

        info = (
            MathTex(f"\mu = {mean_tracker.get_value():.1f} \ \sigma = {std_tracker.get_value():.1f}", font_size=28)
            .next_to(axes, LEFT, buff=0.5)
            .add_updater(lambda m: m.become(MathTex(f"\mu = {mean_tracker.get_value():.1f} \ \sigma = {std_tracker.get_value():.1f}", font_size=28)
            .next_to(axes, LEFT, buff=0.5)))
        )

        curve = always_redraw(
            lambda: axes.plot(
                lambda x: self.normal_pdf(x, mean_tracker.get_value(), std_tracker.get_value()),
                x_range=[-10, 10],
                color=BLUE,
            )
        )

        riemann_rectangles = always_redraw(
            lambda: axes.get_riemann_rectangles(
                graph=curve,
                x_range=[
                    mean_tracker.get_value() - std_tracker.get_value(),
                    mean_tracker.get_value() + std_tracker.get_value(),
                ],
                dx=0.25,
                stroke_width=0.5,
                fill_opacity=0.6,
                color=YELLOW,
            )
        )

        annotation_68 = always_redraw(
            lambda: self.get_percentage_annotation(
                axes, mean_tracker.get_value(), std_tracker.get_value(), percentage="68%"
            ).shift(DOWN*0.7)
        )

        annotation_95 = always_redraw(
            lambda: self.get_percentage_annotation(
                axes, mean_tracker.get_value(), 2*std_tracker.get_value(), percentage="95%"
            ).next_to(annotation_68, DOWN, buff=0.2)
        )

        annotation_99 = always_redraw(
            lambda: self.get_percentage_annotation(
                axes, mean_tracker.get_value(), 3*std_tracker.get_value(), percentage="99.7%"
            ).next_to(annotation_95, DOWN, buff=0.2)
        )

        self.play(Write(title))
        self.wait(1)

        self.play(Create(axes), Write(axes_labels))
        self.wait(1)

        self.play(Write(info))
        self.wait(1)

        self.play(Create(curve), run_time=2)
        self.wait(1)

        self.play(Create(riemann_rectangles), FadeIn(annotation_68), FadeIn(annotation_95), FadeIn(annotation_99))
        self.wait(2)

        self.play(mean_tracker.animate.set_value(3), run_time=2)
        self.wait(1)

        self.play(mean_tracker.animate.set_value(0), run_time=2)
        self.wait(1)

        self.play(std_tracker.animate.set_value(2), run_time=2)
        self.wait(1)

        self.play(std_tracker.animate.set_value(3), run_time=2)
        self.wait(1)

    
    def normal_pdf(self, x, mean, std):
        return (1 / (std * (2 * np.pi)**0.5)) * np.exp(-0.5 * ((x - mean) / std)**2)

    def get_percentage_annotation(self, axes, mean, std, percentage):
        start_x = mean - std
        end_x = mean + std

        text = Text(percentage, font_size=20)
        text.move_to(axes.c2p(mean, 0))

        left_line = Line(
            axes.c2p(start_x, 0), text.get_left() + LEFT*0.05, color=WHITE, stroke_width=2
        )
        right_line = Line(
            text.get_right() + RIGHT*0.05, axes.c2p(end_x, 0), color=WHITE, stroke_width=2
        )

        return VGroup(left_line, text, right_line)