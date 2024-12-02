from manim import *

FONT_SIZE = 24
LABEL_BUFF = 0.2
ARROW_STROKE_WIDTH = 3
ARROW_TIP_LENGTH = 0.1
TRANSFORM_RUN_TIME = 2


class AutomatonToRegex(Scene):
    def construct(self):
        title = MathTex("\\text{Automaton} \Rightarrow \\text{Regex}").to_edge(UP)

        dot = Dot()
        a = Text("a", font_size=FONT_SIZE)
        b = Text("b", font_size=FONT_SIZE)

        # PART 1: Creating initial automaton

        q0_dot = dot.copy().shift(LEFT * 4)
        q0_text = MathTex("q_o", font_size=FONT_SIZE).next_to(
            q0_dot, UP, buff=LABEL_BUFF
        )
        start_indicator = MathTex("\\rightarrow", font_size=FONT_SIZE).next_to(
            q0_dot, LEFT, buff=0.3
        )

        q1_dot = dot.copy().shift(LEFT * 2)
        q1_text = MathTex("q_1", font_size=FONT_SIZE).next_to(
            q1_dot, UP, buff=LABEL_BUFF
        )

        q2_dot = dot.copy()
        q2_text = MathTex("q_2", font_size=FONT_SIZE).next_to(
            q2_dot, UP, buff=LABEL_BUFF
        )

        q3_dot = dot.copy().shift(RIGHT * 2)
        q3_text = MathTex("q_3", font_size=FONT_SIZE).next_to(
            q3_dot, UP, buff=LABEL_BUFF
        )

        q4_dot = dot.copy().shift(RIGHT * 4)
        final_indicator = Circle(radius=0.15, color=WHITE, stroke_width=2).move_to(
            q4_dot.get_center()
        )
        final_state = VGroup(q4_dot, final_indicator)
        q4_text = MathTex("q_4", font_size=FONT_SIZE).next_to(
            final_state, UP, buff=LABEL_BUFF
        )

        arrow_q0_q1 = Arrow(
            start=q0_dot.get_right(),
            end=q1_dot.get_left(),
            stroke_width=ARROW_STROKE_WIDTH,
            max_tip_length_to_length_ratio=ARROW_TIP_LENGTH,
        )
        text_q0_q1 = b.copy().next_to(arrow_q0_q1, UP, buff=LABEL_BUFF)
        arrow_q1_q1 = (
            Arc(radius=0.15, start_angle=PI, angle=PI)
            .move_to(q1_dot.get_bottom())
            .add_tip(tip_length=0.1, tip_width=0.1)
        )
        text_q1_q1 = a.copy().next_to(arrow_q1_q1, DOWN, buff=LABEL_BUFF)
        arrow_q1_q2 = Arrow(
            start=q1_dot.get_right(),
            end=q2_dot.get_left(),
            stroke_width=ARROW_STROKE_WIDTH,
            max_tip_length_to_length_ratio=ARROW_TIP_LENGTH,
        )
        text_q1_q2 = b.copy().next_to(arrow_q1_q2, UP, buff=LABEL_BUFF)
        arrow_q2_q3 = Arrow(
            start=q2_dot.get_right() + UP * 0.1,
            end=q3_dot.get_left() + UP * 0.1,
            stroke_width=ARROW_STROKE_WIDTH,
            max_tip_length_to_length_ratio=ARROW_TIP_LENGTH,
        )
        text_q2_q3 = b.copy().next_to(arrow_q2_q3, UP, buff=LABEL_BUFF)
        arrow_q3_q2 = Arrow(
            start=q3_dot.get_left() + DOWN * 0.1,
            end=q2_dot.get_right() + DOWN * 0.1,
            stroke_width=ARROW_STROKE_WIDTH,
            max_tip_length_to_length_ratio=ARROW_TIP_LENGTH,
        )
        text_q3_q2 = a.copy().next_to(arrow_q3_q2, DOWN, buff=LABEL_BUFF)
        arrow_q3_q4 = Arrow(
            start=q3_dot.get_right(),
            end=final_state.get_left(),
            stroke_width=ARROW_STROKE_WIDTH,
            max_tip_length_to_length_ratio=ARROW_TIP_LENGTH,
        )
        text_q3_q4 = b.copy().next_to(arrow_q3_q4, UP, buff=LABEL_BUFF)
        arrow_q4_q2 = CurvedArrow(
            start_point=final_state.get_left() + UP * 0.2,
            end_point=q2_dot.get_right() + UP * 0.4 + RIGHT * 0.1,
            tip_length=0.2,
        )
        text_q4_q2 = a.copy().next_to(arrow_q4_q2, UP, buff=LABEL_BUFF)

        self.play(Write(title))
        self.wait(1)

        self.play(Create(q0_dot), Write(q0_text), Write(start_indicator))

        self.play(GrowArrow(arrow_q0_q1), Write(text_q0_q1))
        self.play(Create(q1_dot), Write(q1_text))
        self.play(Create(arrow_q1_q1), Write(text_q1_q1))

        self.play(GrowArrow(arrow_q1_q2), Write(text_q1_q2))
        self.play(Create(q2_dot), Write(q2_text))

        self.play(GrowArrow(arrow_q2_q3), Write(text_q2_q3))
        self.play(Create(q3_dot), Write(q3_text))
        self.play(GrowArrow(arrow_q3_q2), Write(text_q3_q2))

        self.play(GrowArrow(arrow_q3_q4), Write(text_q3_q4))
        self.play(Create(final_state), Write(q4_text))
        self.play(Create(arrow_q4_q2), Write(text_q4_q2))
        self.wait(1)

        # PART 2: eliminating loop in q1

        new_q1_q2 = Text("a*b", font_size=FONT_SIZE, color=BLUE).move_to(text_q1_q2)

        group_to_remove = VGroup(arrow_q1_q1, text_q1_q1, text_q1_q2)

        self.play(group_to_remove.animate.set_color(BLUE))
        self.play(
            ReplacementTransform(group_to_remove, new_q1_q2),
            run_time=TRANSFORM_RUN_TIME,
        )
        self.play(new_q1_q2.animate.set_color(WHITE))

        self.wait(1)

        # PART 3: eliminating q1

        arrow_q0_q2 = Arrow(
            start=q0_dot.get_right(),
            end=q2_dot.get_left(),
            stroke_width=ARROW_STROKE_WIDTH,
            tip_length=0.2,
            color=BLUE,
        )
        text_q0_q2 = Text("ba*b", font_size=FONT_SIZE, color=BLUE).next_to(
            arrow_q0_q2, UP, buff=LABEL_BUFF
        )

        group_to_remove = VGroup(
            arrow_q0_q1, text_q0_q1, q1_dot, q1_text, new_q1_q2, arrow_q1_q2
        )

        self.play(group_to_remove.animate.set_color(BLUE))
        self.play(
            ReplacementTransform(group_to_remove, VGroup(arrow_q0_q2, text_q0_q2)),
            run_time=TRANSFORM_RUN_TIME,
        )
        self.play(
            text_q0_q2.animate.set_color(WHITE), arrow_q0_q2.animate.set_color(WHITE)
        )

        self.wait(1)

        # PART 4: eliminating q2

        arrow_q0_q3 = Arrow(
            start=q0_dot.get_right(),
            end=q3_dot.get_left(),
            stroke_width=ARROW_STROKE_WIDTH,
            tip_length=0.2,
        )
        text_q0_q3 = Text("ba*bb", font_size=FONT_SIZE).next_to(
            arrow_q0_q3, UP, buff=LABEL_BUFF
        )

        arrow_q3_q3 = (
            Arc(radius=0.15, start_angle=PI, angle=PI)
            .move_to(q3_dot.get_bottom())
            .add_tip(tip_length=0.1, tip_width=0.1)
        )
        text_q3_q3 = Text("ab", font_size=FONT_SIZE).next_to(
            arrow_q3_q3, DOWN, buff=LABEL_BUFF
        )

        arrow_q4_q3 = CurvedArrow(
            start_point=final_state.get_bottom() + DOWN * 0.1,
            end_point=arrow_q3_q4.get_start() + DOWN * 0.2,
            tip_length=0.2,
            angle=-PI / 4,
        )
        text_q4_q3 = Text("ab", font_size=FONT_SIZE).next_to(
            arrow_q4_q3, DOWN, buff=LABEL_BUFF
        )

        group_to_remove = VGroup(
            arrow_q0_q2,
            text_q0_q2,
            q2_dot,
            q2_text,
            arrow_q2_q3,
            text_q2_q3,
            arrow_q3_q2,
            text_q3_q2,
            arrow_q4_q2,
            text_q4_q2,
        )

        group_to_create = VGroup(
            arrow_q0_q3, text_q0_q3, arrow_q3_q3, text_q3_q3, arrow_q4_q3, text_q4_q3
        )

        self.play(group_to_remove.animate.set_color(BLUE))
        self.play(
            ReplacementTransform(group_to_remove, group_to_create),
            run_time=TRANSFORM_RUN_TIME,
        )
        self.play(group_to_create.animate.set_color(WHITE))

        self.wait(1)

        # PART 5: eliminating q3 loop

        new_q4_q3 = CurvedArrow(
            start_point=final_state.get_bottom() + DOWN * 0.1,
            end_point=q3_dot.get_bottom() + DOWN * 0.1,
            tip_length=0.2,
            angle=-PI / 4,
        )
        new_text_q4_q3 = Text("ab(ab)*", font_size=FONT_SIZE).next_to(
            new_q4_q3, DOWN, buff=LABEL_BUFF
        )

        new_text_q0_q3 = Text("ba*bb(ab)*", font_size=FONT_SIZE).move_to(text_q0_q3)

        group_to_remove = VGroup(
            arrow_q3_q3, text_q3_q3, arrow_q4_q3, text_q4_q3, text_q0_q3
        )
        group_to_create = VGroup(new_q4_q3, new_text_q4_q3, new_text_q0_q3).set_color(BLUE)

        self.play(group_to_remove.animate.set_color(BLUE))
        self.play(
            ReplacementTransform(group_to_remove, group_to_create),
            run_time=TRANSFORM_RUN_TIME,
        )
        self.play(group_to_create.animate.set_color(WHITE))

        self.wait(1)

        # PART 6: eliminating q3

        arrow_q4_q4 = (
            Arc(radius=0.15, start_angle=PI, angle=PI)
            .move_to(final_state.get_bottom() + DOWN * 0.1)
            .add_tip(tip_length=0.1, tip_width=0.1)
        )
        text_q4_q4 = Text("ab(ab)*b", font_size=FONT_SIZE).next_to(
            arrow_q4_q4, DOWN, buff=LABEL_BUFF
        )

        arrow_q0_q4 = Arrow(
            start=q0_dot.get_right(),
            end=final_state.get_left(),
            stroke_width=ARROW_STROKE_WIDTH,
            tip_length=0.2,
        )
        text_q0_q4 = Text("ba*bb(ab)*b", font_size=FONT_SIZE).next_to(
            arrow_q0_q4, UP, buff=LABEL_BUFF
        )

        group_to_remove = VGroup(
            arrow_q0_q3,
            new_text_q0_q3,
            q3_dot,
            q3_text,
            arrow_q3_q4,
            text_q3_q4,
            new_q4_q3,
            new_text_q4_q3,
        )
        group_to_create = VGroup(
            arrow_q4_q4, text_q4_q4, arrow_q0_q4, text_q0_q4
        ).set_color(BLUE)

        self.play(group_to_remove.animate.set_color(BLUE))
        self.play(
            ReplacementTransform(group_to_remove, group_to_create),
            run_time=TRANSFORM_RUN_TIME,
        )
        self.play(group_to_create.animate.set_color(WHITE))

        self.wait(1)

        # PART 7: eliminating q4 loop

        new_q0_q4 = Arrow(
            start=q0_dot.get_right(),
            end=final_state.get_left(),
            stroke_width=ARROW_STROKE_WIDTH,
            tip_length=0.2,
        )
        new_text_q0_q4 = Text("ba*bb(ab)*b(ab(ab)*b)*", font_size=FONT_SIZE).next_to(
            new_q0_q4, UP, buff=LABEL_BUFF
        )

        group_to_remove = VGroup(arrow_q4_q4, text_q4_q4, arrow_q0_q4, text_q0_q4)

        self.play(group_to_remove.animate.set_color(BLUE))
        self.play(
            ReplacementTransform(
                group_to_remove, VGroup(new_q0_q4, new_text_q0_q4).set_color(BLUE)
            ),
            run_time=TRANSFORM_RUN_TIME,
        )
        self.play(
            new_q0_q4.animate.set_color(WHITE), new_text_q0_q4.animate.set_color(WHITE)
        )

        self.wait(1)

        # PART 8: remove arrows and states

        to_fade_out = VGroup(
            start_indicator, q0_dot, q0_text, new_q0_q4, final_state, q4_text
        )

        self.play(FadeOut(to_fade_out))
        self.wait(2)
