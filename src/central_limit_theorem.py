import numpy as np
from scipy import stats
from manim import *


class CentralLimitTheorem(Scene):
    def construct(self):
        np.random.seed(42)

        SAMPLE_SIZE = 30
        N_SLOW = 4        # iterations shown step-by-step
        N_TOTAL = 500     # total sample means to collect
        N_BINS = 25

        all_samples = np.random.exponential(1.0, (N_TOTAL, SAMPLE_SIZE))
        all_means = all_samples.mean(axis=1)

        pop_mean = 1.0
        pop_std = 1.0 / np.sqrt(SAMPLE_SIZE)

        mean_min, mean_max = 0.40, 1.80
        bin_edges = np.linspace(mean_min, mean_max, N_BINS + 1)
        bin_width = bin_edges[1] - bin_edges[0]

        final_counts, _ = np.histogram(all_means, bins=bin_edges)
        HIST_Y_MAX = int(final_counts.max() * 1.25)

        title = Text("Central Limit Theorem").to_edge(UP)
        separator = DashedLine(LEFT * 7, RIGHT * 7, stroke_width=1, color=GRAY).move_to(ORIGIN)

        top_axes = Axes(
            x_range=[0, 4.5, 1],
            y_range=[0, 1.05, 0.5],
            x_length=9,
            y_length=2.0,
            tips=False,
            axis_config={"include_numbers": False, "include_ticks": True},
        ).shift(UP * 1.5)

        top_label = Text("Population: Exp(λ = 1)", font_size=20, color=ORANGE).next_to(
            top_axes, UP, buff=0.08
        )

        expo_curve = top_axes.plot(
            lambda x: np.exp(-x), x_range=[0.001, 4.5], color=ORANGE, stroke_width=2.5
        )
        expo_fill = top_axes.get_area(
            expo_curve, x_range=[0.001, 4.5], color=ORANGE, opacity=0.20
        )

        pop_mean_line = DashedLine(
            top_axes.c2p(pop_mean, 0),
            top_axes.c2p(pop_mean, np.exp(-pop_mean)),
            color=YELLOW,
            stroke_width=1.5,
        )
        pop_mean_tex = MathTex(r"\mu=1", font_size=20, color=YELLOW).next_to(
            top_axes.c2p(pop_mean, np.exp(-pop_mean)), UR, buff=0.05
        )

        bottom_axes = Axes(
            x_range=[mean_min, mean_max, 0.5],
            y_range=[0, HIST_Y_MAX, 20],
            x_length=9,
            y_length=2.0,
            tips=False,
            axis_config={"include_numbers": False, "include_ticks": True},
        ).shift(DOWN * 1.7)

        bottom_label = Text(
            f"Distribution of Sample Means  (n = {SAMPLE_SIZE})", font_size=20, color=BLUE_B
        ).next_to(bottom_axes, UP, buff=0.08)

        def make_histogram(means_so_far):
            counts, _ = np.histogram(means_so_far, bins=bin_edges)
            bars = VGroup()
            for i, count in enumerate(counts):
                if count == 0:
                    continue
                p_left = bottom_axes.c2p(bin_edges[i], 0)
                p_right = bottom_axes.c2p(bin_edges[i + 1], 0)
                p_top = bottom_axes.c2p(bin_edges[i], count)
                bar_w = p_right[0] - p_left[0]
                bar_h = max(p_top[1] - p_left[1], 0)
                bar = Rectangle(
                    width=bar_w,
                    height=bar_h,
                    fill_color=BLUE_D,
                    fill_opacity=0.80,
                    stroke_width=0.5,
                    stroke_color=WHITE,
                ).move_to(
                    np.array([p_left[0] + bar_w / 2, p_left[1] + bar_h / 2, 0])
                )
                bars.add(bar)
            return bars

        def make_counter(n):
            return (
                VGroup(
                    Text("Samples:", font_size=22, color=GRAY_A),
                    Text(f"{n}", font_size=26, color=WHITE),
                )
                .arrange(RIGHT, buff=0.15)
                .to_corner(UR)
                .shift(DOWN * 0.3)
            )

        counter = make_counter(0)

        # ANIMATION SEQUENCE

        self.play(Write(title))
        self.wait(0.3)

        self.play(Create(top_axes), Write(top_label), run_time=1)
        self.play(Create(expo_curve), FadeIn(expo_fill), run_time=1.5)
        self.play(Create(pop_mean_line), Write(pop_mean_tex))
        self.wait(0.5)

        self.play(
            Create(separator),
            Create(bottom_axes),
            Write(bottom_label),
            FadeIn(counter),
            run_time=1,
        )
        self.wait(0.5)

        # Slow phase: step-by-step iterations
        current_hist = VGroup()
        self.add(current_hist)

        for i in range(N_SLOW):
            sample = all_samples[i]
            mean_val = all_means[i]

            # Sample dots appear along the top x-axis
            sample_dots = VGroup(
                *[
                    Dot(top_axes.c2p(x, 0), radius=0.055, color=ORANGE)
                    for x in sample
                ]
            )
            self.play(
                AnimationGroup(*[GrowFromCenter(d) for d in sample_dots], lag_ratio=0.04),
                run_time=0.7,
            )

            # Highlight and label the mean
            mean_dot_top = Dot(top_axes.c2p(mean_val, 0), radius=0.12, color=YELLOW)
            mean_vline = DashedLine(
                top_axes.c2p(mean_val, 0),
                top_axes.c2p(mean_val, 0.5),
                color=YELLOW,
                stroke_width=2,
            )
            mean_tex = MathTex(
                rf"\bar{{x}} = {mean_val:.2f}", font_size=22, color=YELLOW
            ).next_to(mean_vline, UP, buff=0.05)

            self.play(
                GrowFromCenter(mean_dot_top),
                Create(mean_vline),
                Write(mean_tex),
                run_time=0.6,
            )
            self.wait(0.3)

            # Drop the mean down to the histogram
            target = bottom_axes.c2p(mean_val, 0)
            self.play(
                mean_dot_top.animate.move_to(target),
                run_time=0.7,
                rate_func=rate_functions.ease_in_cubic,
            )

            # Update histogram and counter
            new_hist = make_histogram(all_means[: i + 1])
            new_counter = make_counter(i + 1)
            self.play(
                Transform(current_hist, new_hist),
                Transform(counter, new_counter),
                FadeOut(sample_dots),
                FadeOut(mean_dot_top),
                FadeOut(mean_vline),
                FadeOut(mean_tex),
                run_time=0.45,
            )
            self.wait(0.4)

        fast_note = Text("Adding many more samples…", font_size=22, color=GRAY_A).next_to(
            title, DOWN, buff=0.10
        )
        self.play(FadeIn(fast_note))

        FAST_BATCH = int(N_TOTAL * 0.05)
        for batch_start in range(N_SLOW, N_TOTAL, FAST_BATCH):
            batch_end = min(batch_start + FAST_BATCH, N_TOTAL)
            new_hist = make_histogram(all_means[:batch_end])
            new_counter = make_counter(batch_end)
            self.play(
                Transform(current_hist, new_hist),
                Transform(counter, new_counter),
                run_time=0.12,
            )

        self.play(FadeOut(fast_note))
        self.wait(0.6)

        # Overlay the theoretical normal curve
        normal_curve = bottom_axes.plot(
            lambda x: stats.norm.pdf(x, loc=pop_mean, scale=pop_std)
            * N_TOTAL
            * bin_width,
            x_range=[mean_min + 0.01, mean_max - 0.01],
            color=RED,
            stroke_width=3,
        )
        normal_label = Text("Normal Curve (CLT)", font_size=20, color=RED).to_corner(DR).shift(
            UP * 0.2
        )

        self.play(Create(normal_curve, run_time=2), Write(normal_label))
        self.wait(1)

        # CLT formula
        clt_formula = MathTex(
            r"\bar{X}_n \xrightarrow{d} \mathcal{N}\!\left(\mu,\,\frac{\sigma^2}{n}\right)"
            r"\quad \text{as } n \to \infty",
            font_size=30,
        ).next_to(top_label, DOWN, buff=0.12)

        self.play(Write(clt_formula))
        self.wait(3)
