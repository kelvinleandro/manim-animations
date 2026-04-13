import numpy as np
from manim import *


class DeterminantAsArea(Scene):
    def construct(self):
        self._nonzero_det_part()

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
        self.wait(0.4)

        self._zero_det_part()

    def _build_scene_base(self):
        """Return a fresh NumberPlane + unit square + basis vectors."""
        plane = NumberPlane(
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_opacity": 0.5,
                "stroke_width": 1,
            },
            axis_config={"stroke_color": BLUE_B, "stroke_width": 2},
        )
        unit_sq = Polygon(
            ORIGIN, RIGHT, RIGHT + UP, UP,
            fill_color=YELLOW,
            fill_opacity=0.45,
            stroke_color=YELLOW,
            stroke_width=2,
        )
        i_vec = Arrow(ORIGIN, RIGHT, buff=0, color=BLUE,    tip_length=0.22, stroke_width=5)
        j_vec = Arrow(ORIGIN, UP,    buff=0, color=GREEN_B, tip_length=0.22, stroke_width=5)
        return plane, unit_sq, i_vec, j_vec

    def _nonzero_det_part(self):
        A = np.array([[2.0, 1.0], [0.5, 1.5]])

        plane, unit_sq, i_vec, j_vec = self._build_scene_base()

        i_label = MathTex(r"\hat{\imath}", color=BLUE,    font_size=32).next_to(RIGHT,   DR, buff=0.1)
        j_label = MathTex(r"\hat{\jmath}", color=GREEN_B, font_size=32).next_to(UP,      UL, buff=0.1)

        title = Text("Determinant as Area Scaling", font_size=32).to_edge(UP)

        mat_tex = MathTex(
            r"A = \begin{bmatrix} 2 & 1 \\ 0.5 & 1.5 \end{bmatrix}",
            font_size=36,
        ).to_corner(UR).shift(DOWN * 1.6 + LEFT * 0.3)

        det_tex = MathTex(
            r"\det(A) = 2 \times 1.5 - 1 \times 0.5 = \mathbf{2.5}",
            font_size=26,
            color=YELLOW_C,
        ).next_to(mat_tex, DOWN, buff=0.25)

        area_label = MathTex(r"\text{Area} = 1", font_size=30, color=YELLOW).to_corner(DL).shift(UP * 0.3)

        # Initial setup
        self.play(Create(plane), Write(title), run_time=1.5)
        self.play(GrowArrow(i_vec), GrowArrow(j_vec), Write(i_label), Write(j_label))
        self.play(DrawBorderThenFill(unit_sq))
        self.play(Write(area_label))
        self.wait(0.5)

        self.play(Write(mat_tex))
        self.wait(0.3)
        self.play(Write(det_tex))
        self.wait(1)

        # Transformed objects
        # Column convention: A @ î = col1, A @ ĵ = col2
        col1 = np.array([A[0, 0], A[1, 0], 0])   # (2,  0.5)
        col2 = np.array([A[0, 1], A[1, 1], 0])   # (1,  1.5)

        parallelogram = Polygon(
            ORIGIN, col1, col1 + col2, col2,
            fill_color=YELLOW,
            fill_opacity=0.45,
            stroke_color=YELLOW,
            stroke_width=2,
        )

        new_i_vec = Arrow(ORIGIN, col1, buff=0, color=BLUE,    tip_length=0.22, stroke_width=5)
        new_j_vec = Arrow(ORIGIN, col2, buff=0, color=GREEN_B, tip_length=0.22, stroke_width=5)
        new_i_label = MathTex(r"\hat{\imath}'", color=BLUE,    font_size=32).next_to(col1, DR, buff=0.1)
        new_j_label = MathTex(r"\hat{\jmath}'", color=GREEN_B, font_size=32).next_to(col2, UL, buff=0.1)

        new_area_label = MathTex(
            r"\text{Area} = |\det(A)| = 2.5",
            font_size=30, color=YELLOW,
        ).to_corner(DL).shift(UP * 0.3)

        scaling_tex = MathTex(
            r"\text{Area}' = |\det(A)| \cdot \text{Area}",
            font_size=26,
        ).next_to(det_tex, DOWN, buff=0.25)

        self.play(
            plane.animate.apply_matrix(A),
            Transform(unit_sq,  parallelogram),
            Transform(i_vec,    new_i_vec),
            Transform(j_vec,    new_j_vec),
            Transform(i_label,  new_i_label),
            Transform(j_label,  new_j_label),
            Transform(area_label, new_area_label),
            run_time=2.5,
        )
        self.wait(1)
        self.play(Write(scaling_tex))
        self.wait(2)

    def _zero_det_part(self):
        B = np.array([[1.0, 2.0], [1.0, 2.0]])

        plane, unit_sq, i_vec, j_vec = self._build_scene_base()

        title = Text("When det = 0: Space Collapses!", font_size=32, color=RED).to_edge(UP)

        mat_tex = MathTex(
            r"B = \begin{bmatrix} 1 & 2 \\ 1 & 2 \end{bmatrix}",
            font_size=36,
        ).to_corner(UR).shift(DOWN * 1.6 + LEFT * 0.3)

        det_tex = MathTex(
            r"\det(B) = 1 \times 2 - 2 \times 1 = \mathbf{0}",
            font_size=26,
            color=RED_C,
        ).next_to(mat_tex, DOWN, buff=0.25)

        area_label = MathTex(r"\text{Area} = 1", font_size=30, color=YELLOW).to_corner(DL).shift(UP * 0.3)

        self.play(Create(plane), Write(title), run_time=1.5)
        self.play(GrowArrow(i_vec), GrowArrow(j_vec))
        self.play(DrawBorderThenFill(unit_sq))
        self.play(Write(area_label))
        self.wait(0.5)

        self.play(Write(mat_tex))
        self.wait(0.3)
        self.play(Write(det_tex))
        self.wait(1)

        col1 = np.array([B[0, 0], B[1, 0], 0])   # (1, 1)
        col2 = np.array([B[0, 1], B[1, 1], 0])   # (2, 2)

        degenerate_poly = Polygon(
            ORIGIN, col1, col1 + col2, col2,
            fill_color=RED,
            fill_opacity=0.0,
            stroke_color=RED,
            stroke_width=3,
        )

        new_i_vec = Arrow(ORIGIN, col1, buff=0, color=BLUE,    tip_length=0.22, stroke_width=5)
        new_j_vec = Arrow(ORIGIN, col2, buff=0, color=GREEN_B, tip_length=0.22, stroke_width=5)

        new_area_label = MathTex(
            r"\text{Area} = |\det(B)| = 0",
            font_size=30, color=RED,
        ).to_corner(DL).shift(UP * 0.3)

        collapse_tex = Text(
            "Columns are linearly dependent → not invertible",
            font_size=22, color=RED_C,
        ).next_to(det_tex, DOWN, buff=0.25)

        self.play(
            plane.animate.apply_matrix(B),
            Transform(unit_sq,    degenerate_poly),
            Transform(i_vec,      new_i_vec),
            Transform(j_vec,      new_j_vec),
            Transform(area_label, new_area_label),
            run_time=2.5,
        )
        self.wait(1)

        self.play(Write(collapse_tex))
        self.wait(3)
