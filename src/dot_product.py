import numpy as np
from manim import *


class DotProductAsProjection(Scene):
    def construct(self):
        A_VEC = np.array([3.0, 0.0, 0.0])
        B_MAG = 2.5
        theta = ValueTracker(PI / 4)

        def b_vec():
            t = theta.get_value()
            return np.array([B_MAG * np.cos(t), B_MAG * np.sin(t), 0])

        def proj_point():
            """Foot of perpendicular from tip of B onto A's axis."""
            a_hat = A_VEC / np.linalg.norm(A_VEC)
            return float(np.dot(b_vec(), a_hat)) * a_hat

        def dot_product():
            return float(np.dot(b_vec(), A_VEC))

        plane = NumberPlane(
            background_line_style={"stroke_color": BLUE_D, "stroke_opacity": 0.4, "stroke_width": 1},
            axis_config={"stroke_color": BLUE_B, "stroke_width": 2},
        )
        title = Text("Dot Product as Projection", font_size=32).to_edge(UP)

        a_arrow = Arrow(ORIGIN, A_VEC, buff=0, color=BLUE, tip_length=0.25, stroke_width=5)
        a_label = MathTex(r"\vec{A}", color=BLUE, font_size=36).next_to(A_VEC, RIGHT, buff=0.1)

        b_arrow = always_redraw(lambda: Arrow(
            ORIGIN, b_vec(), buff=0, color=ORANGE, tip_length=0.25, stroke_width=5
        ))
        b_label = MathTex(r"\vec{B}", color=ORANGE, font_size=36)
        b_label.add_updater(lambda m: m.next_to(
            b_vec(), UL if b_vec()[1] >= 0 else DL, buff=0.12
        ))

        proj_visual = always_redraw(lambda: (
            Dot(ORIGIN, radius=0.1, color=GREEN)
            if np.linalg.norm(proj_point()) < 0.08
            else Arrow(ORIGIN, proj_point(), buff=0, color=GREEN, tip_length=0.20, stroke_width=4)
        ))
        proj_label = MathTex(r"\mathrm{proj}_{\vec{A}}\vec{B}", font_size=22, color=GREEN)

        def _update_proj_label(m):
            p = proj_point()
            if np.linalg.norm(p) < 0.1:
                m.set_opacity(0)
            else:
                m.set_opacity(1).next_to(p + np.array([0, -0.25, 0]), DOWN, buff=0.03)

        proj_label.add_updater(_update_proj_label)

        # Dashed perpendicular line from B tip to projection foot
        perp_line = always_redraw(lambda: (
            VMobject()
            if np.linalg.norm(b_vec() - proj_point()) < 0.1
            else DashedLine(b_vec(), proj_point(), color=GRAY_A, stroke_width=2, dash_length=0.15)
        ))

        # Right-angle marker at the projection foot
        def _make_right_angle():
            b = b_vec()
            p = proj_point()
            if abs(b[1]) < 0.15 or np.linalg.norm(p) < 0.06:
                return VMobject()
            s = 0.13
            yd = np.sign(b[1]) * s                                   # toward B (perpendicular)
            xd = -np.sign(p[0]) * s if abs(p[0]) > 0.06 else -s     # toward origin along A
            pts = [
                p + np.array([0, yd, 0]),
                p + np.array([xd, yd, 0]),
                p + np.array([xd, 0, 0]),
            ]
            return VMobject().set_points_as_corners(pts).set_stroke(color=GRAY_B, width=1.5)

        right_angle = always_redraw(_make_right_angle)

        # Angle arc
        def _make_arc():
            t = theta.get_value() % (2 * PI)
            if t < 0.04 or abs(t - 2 * PI) < 0.04:
                return VMobject()
            return Arc(radius=0.5, start_angle=0, angle=t, color=YELLOW, stroke_width=2)

        angle_arc = always_redraw(_make_arc)

        theta_label = MathTex(r"\theta", color=YELLOW, font_size=28)

        def _update_theta_label(m):
            t = theta.get_value() % (2 * PI)
            if t < 0.04 or abs(t - 2 * PI) < 0.04:
                m.set_opacity(0)
            else:
                m.set_opacity(1).move_to(np.array([
                    0.85 * np.cos(t / 2),
                    0.85 * np.sin(t / 2),
                    0,
                ]))

        theta_label.add_updater(_update_theta_label)

        formula = MathTex(
            r"\vec{A} \cdot \vec{B} = |\vec{A}|\,|\vec{B}|\cos\theta",
            font_size=30,
        ).to_corner(UR).shift(DOWN * 1.5 + LEFT * 0.25)

        eq_lbl = MathTex(r"\vec{A}\cdot\vec{B} =", font_size=26, color=GRAY_A).next_to(
            formula, DOWN, buff=0.15
        ).align_to(formula, LEFT)
        dot_val = DecimalNumber(dot_product(), num_decimal_places=2, font_size=26, color=YELLOW_C).next_to(
            eq_lbl, RIGHT, buff=0.1
        )
        dot_val.add_updater(lambda m: m.set_value(dot_product()))

        theta_lbl = MathTex(r"\theta =", font_size=26, color=GRAY_A).next_to(
            eq_lbl, DOWN, buff=0.12
        ).align_to(formula, LEFT)
        theta_val = DecimalNumber(
            np.degrees(PI / 4), num_decimal_places=0, font_size=26, color=YELLOW_C
        ).next_to(theta_lbl, RIGHT, buff=0.10)
        theta_val.add_updater(lambda m: m.set_value(np.degrees(theta.get_value())))
        deg_sym = MathTex(r"^\circ", font_size=24, color=YELLOW_C).next_to(theta_val, RIGHT, buff=0.02)
        deg_sym.add_updater(lambda m: m.next_to(theta_val, RIGHT, buff=0.02))

        panel = VGroup(formula, eq_lbl, dot_val, theta_lbl, theta_val, deg_sym)

        # Status label (BL) with sign-change-only updates
        _prev_sign = [None]
        status = Text("A · B > 0  (same direction)", font_size=24, color=GREEN_B).to_corner(DL).shift(UP * 0.3)

        def _update_status(mob):
            dp = dot_product()
            cat = "zero" if abs(dp) < 0.3 else ("pos" if dp > 0 else "neg")
            if cat == _prev_sign[0]:
                return
            _prev_sign[0] = cat
            if cat == "zero":
                mob.become(Text("A · B = 0  (perpendicular!)", font_size=24, color=RED).to_corner(DL).shift(UP * 0.3))
            elif cat == "pos":
                mob.become(Text("A · B > 0  (same direction)", font_size=24, color=GREEN_B).to_corner(DL).shift(UP * 0.3))
            else:
                mob.become(Text("A · B < 0  (opposite direction)", font_size=24, color=RED_C).to_corner(DL).shift(UP * 0.3))

        status.add_updater(_update_status)

        # ANIMATION SEQUENCE

        self.play(Create(plane), Write(title), run_time=1.5)
        self.wait(0.3)

        self.play(GrowArrow(a_arrow), Write(a_label))
        self.wait(0.3)
        self.play(GrowArrow(b_arrow), Write(b_label))
        self.wait(0.3)

        self.play(Create(angle_arc), Write(theta_label))
        self.wait(0.5)

        self.play(Create(perp_line), Create(right_angle))
        self.play(Create(proj_visual), Write(proj_label))
        self.wait(0.5)

        self.play(Write(formula))
        self.play(FadeIn(VGroup(eq_lbl, dot_val, theta_lbl, theta_val, deg_sym)))
        self.play(FadeIn(status))
        self.wait(1.5)

        # 45° → 90°
        self.play(theta.animate.set_value(PI / 2), run_time=2, rate_func=smooth)
        self.wait(1.2)

        # 90° → 180°
        self.play(theta.animate.set_value(PI), run_time=2, rate_func=smooth)
        self.wait(1)

        # 180° → 270°
        self.play(theta.animate.set_value(3 * PI / 2), run_time=2, rate_func=smooth)
        self.wait(0.5)

        # 270° → 360°
        self.play(theta.animate.set_value(2 * PI), run_time=2, rate_func=smooth)
        self.wait(2)
