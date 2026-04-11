import numpy as np
from manim import *
from sklearn.svm import SVC
from sklearn.datasets import make_blobs


def get_endpoints(w, b, c, x_range, y_range):
    """Find the two intersections of wx+by+b=c with the bounding box."""
    x_min, x_max = x_range
    y_min, y_max = y_range
    pts = []
    
    if abs(w[1]) > 1e-6:
        y1 = (c - b - w[0]*x_min) / w[1]
        if y_min - 1e-4 <= y1 <= y_max + 1e-4: pts.append((x_min, y1))
        y2 = (c - b - w[0]*x_max) / w[1]
        if y_min - 1e-4 <= y2 <= y_max + 1e-4: pts.append((x_max, y2))
        
    if abs(w[0]) > 1e-6:
        x1 = (c - b - w[1]*y_min) / w[0]
        if x_min - 1e-4 <= x1 <= x_max + 1e-4: pts.append((x1, y_min))
        x2 = (c - b - w[1]*y_max) / w[0]
        if x_min - 1e-4 <= x2 <= x_max + 1e-4: pts.append((x2, y_max))
        
    unique_pts = []
    for p in pts:
        if not any(abs(p[0]-up[0]) < 1e-3 and abs(p[1]-up[1]) < 1e-3 for up in unique_pts):
            unique_pts.append(p)
            
    if len(unique_pts) >= 2:
        return unique_pts[0], unique_pts[1]
        
    return (x_min, (c - b - w[0]*x_min) / (w[1] + 1e-8)), (x_max, (c - b - w[0]*x_max) / (w[1] + 1e-8))


class SVM(Scene):
    def construct(self):
        # Data
        X, y = make_blobs(
            n_samples=30, centers=2, cluster_std=0.9, random_state=7
        )
        X -= X.mean(axis=0)

        clf = SVC(kernel="linear", C=1.0)
        clf.fit(X, y)

        w = clf.coef_[0]
        b = clf.intercept_[0]
        margin = 2 / np.linalg.norm(w)
        support_indices = clf.support_

        # Axes
        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1

        x_range_span = x_max - x_min
        y_range_span = y_max - y_min
        
        scale_factor = min(8.0 / x_range_span, 5.0 / y_range_span)
        x_length = x_range_span * scale_factor
        y_length = y_range_span * scale_factor

        axes = Axes(
            x_range=[x_min, x_max, 1],
            y_range=[y_min, y_max, 1],
            x_length=x_length,
            y_length=y_length,
            axis_config={"include_numbers": False, "include_ticks": False},
        ).shift(DOWN * 0.3)

        x_range_plot = (x_min, x_max)
        y_range_plot = (y_min, y_max)

        title = Text("Support Vector Machine").to_edge(UP)

        COLOR_A = BLUE
        COLOR_B = RED

        dots = VGroup()
        for i, (xi, yi) in enumerate(zip(X, y)):
            color = COLOR_A if yi == 0 else COLOR_B
            dot = Dot(axes.coords_to_point(xi[0], xi[1]), color=color, radius=0.07)
            dots.add(dot)

        # Decision boundary (initial: random line, then SVM line)
        pt0, pt1 = get_endpoints(w, b, 0, x_range_plot, y_range_plot)
        boundary_p0 = axes.coords_to_point(*pt0)
        boundary_p1 = axes.coords_to_point(*pt1)
        
        wrong_line = Line(
            axes.coords_to_point(x_min, y_min),
            axes.coords_to_point(x_max, y_max),
            color=WHITE, stroke_width=2.5
        )

        boundary = Line(boundary_p0, boundary_p1, color=WHITE, stroke_width=2.5)

        # Margin lines
        margin_val = 1.0

        mp0, mp1 = get_endpoints(w, b, margin_val, x_range_plot, y_range_plot)
        mp2, mp3 = get_endpoints(w, b, -margin_val, x_range_plot, y_range_plot)
        
        pm0 = axes.coords_to_point(*mp0)
        pm1 = axes.coords_to_point(*mp1)
        pm2 = axes.coords_to_point(*mp2)
        pm3 = axes.coords_to_point(*mp3)

        margin_line_pos = DashedLine(pm0, pm1, color=COLOR_A, stroke_width=1.8)
        margin_line_neg = DashedLine(pm2, pm3, color=COLOR_B, stroke_width=1.8)

        # Margin band (filled area between the two margin lines)
        margin_band = Polygon(
            pm0, pm1, pm3, pm2,
            fill_color=YELLOW,
            fill_opacity=0.12,
            stroke_width=0,
        )

        # Support vector dots (highlighted)
        sv_circles = VGroup()
        for idx in support_indices:
            xi = X[idx]
            color = COLOR_A if y[idx] == 0 else COLOR_B
            circle = Circle(
                radius=0.15,
                color=YELLOW,
                stroke_width=2,
            ).move_to(axes.coords_to_point(xi[0], xi[1]))
            sv_circles.add(circle)

        # Margin width brace
        center_x = np.mean(X[:, 0])
        center_y = (-w[0] * center_x - b) / (w[1] + 1e-8)
        p_bound = np.array([center_x, center_y])
        
        w_norm_sq = w[0]**2 + w[1]**2
        
        p_pos = p_bound + (w * margin_val) / w_norm_sq
        p_neg = p_bound - (w * margin_val) / w_norm_sq

        brace_start = axes.coords_to_point(p_pos[0], p_pos[1])
        brace_end   = axes.coords_to_point(p_neg[0], p_neg[1])
        
        margin_brace = BraceBetweenPoints(brace_start, brace_end)
        margin_text  = margin_brace.get_tex(r"\text{margin}", buff=0.15).scale(0.7)

        # Labels
        label_sv = (
            Text("Support Vectors", font_size=22, color=YELLOW)
            .to_corner(DR)
            .shift(UP * 0.3)
        )
        label_boundary = (
            Text("Decision Boundary", font_size=22, color=WHITE)
            .to_corner(DL)
            .shift(UP * 0.3)
        )


        # ANIMATION SEQUENCE
        # 1. Title
        self.play(Write(title))
        self.wait(0.5)

        # 2. Axes + scatter dots
        self.play(Create(axes), run_time=1.5)
        self.play(
            AnimationGroup(*[GrowFromCenter(d) for d in dots], lag_ratio=0.06),
            run_time=2,
        )
        self.wait(1)

        # 3. Show a "bad" separating line first
        self.play(Create(wrong_line), run_time=1)
        self.wait(0.8)

        # 4. Transform it into the SVM boundary
        self.play(
            ReplacementTransform(wrong_line, boundary),
            run_time=1.5,
        )
        self.play(Write(label_boundary))
        self.wait(1)

        # 5. Reveal margin band + dashed lines
        self.play(FadeIn(margin_band), run_time=0.8)
        self.play(
            Create(margin_line_pos),
            Create(margin_line_neg),
            run_time=1.2,
        )
        self.wait(1)

        # 6. Highlight support vectors
        self.play(
            AnimationGroup(*[Create(c) for c in sv_circles], lag_ratio=0.2),
            run_time=1.2,
        )
        self.play(Write(label_sv))
        self.wait(1)

        # 7. Show margin brace
        self.play(
            GrowFromCenter(margin_brace),
            Write(margin_text),
            run_time=1,
        )
        self.wait(1)

        # 8. Pulse the margin band to reinforce the concept of maximisation
        self.play(
            margin_band.animate.set_fill(opacity=0.35),
            run_time=0.5,
        )
        self.play(
            margin_band.animate.set_fill(opacity=0.12),
            run_time=0.5,
        )
        self.wait(2)
