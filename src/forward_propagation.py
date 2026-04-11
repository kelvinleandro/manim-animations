from manim import *

class ForwardPropagation(Scene):
    def construct(self):
        title = Text("Forward Propagation").to_edge(UP)

        input_nodes = VGroup(*[Circle(radius=0.3, color=BLUE).shift(DOWN * (i - 1.30)) for i in range(4)])
        input_nodes.arrange(DOWN, buff=1).shift(LEFT*3)
        input_labels = [MathTex(f"x_{i+1}", color=WHITE, font_size=24).next_to(input_nodes[i], LEFT, buff=0.2) for i in range(4)]
        filled_input = input_nodes.copy().set_opacity(0.4)

        hidden_nodes = VGroup(*[Circle(radius=0.3, color=GREEN).shift(DOWN * (i - 0.85)) for i in range(3)])
        hidden_nodes.arrange(DOWN, buff=1)
        hidden_labels = [MathTex(f"h_{i+1}", color=WHITE, font_size=24).next_to(hidden_nodes[i], UP, buff=0.2) for i in range(3)]
        filled_hidden = hidden_nodes.copy().set_opacity(0.4)

        output_nodes = VGroup(*[Circle(radius=0.3, color=RED).shift(DOWN * (i - 0.40)) for i in range(2)])
        output_nodes.arrange(DOWN, buff=1).shift(RIGHT*3)
        output_label = [MathTex(f"y_{i+1}", color=WHITE, font_size=24).next_to(output_nodes[i], UP) for i in range(2)]
        filled_output = output_nodes.copy().set_opacity(0.4)

        output_1 = MathTex("0.85", font_size=28).next_to(output_nodes[0], RIGHT, buff=0.2)
        output_2 = MathTex("0.30", font_size=28).next_to(output_nodes[1], RIGHT, buff=0.2)
        output_result = VGroup(output_1, output_2)

        connections_input_to_hidden = [
            Line(input_nodes[i].get_right(), hidden_nodes[j].get_left())
            for i in range(4)
            for j in range(3)
        ]

        connections_hidden_to_output = [
            Line(hidden_nodes[i].get_right(), output_nodes[j].get_left()) 
            for i in range(3)
            for j in range(2)
        ]

        surrounding = SurroundingRectangle(VGroup(output_nodes[0], output_label[0], output_result[0]), color=YELLOW)

        self.play(Write(title))
        self.wait(1)

        self.play(*[FadeIn(node) for node in input_nodes + hidden_nodes + output_nodes])
        self.play(*[Write(label) for label in input_labels + hidden_labels + output_label])
        self.wait(2)

        self.play(*[Create(line) for line in connections_input_to_hidden + connections_hidden_to_output])
        self.wait(2)

        flashes_ih = [
            ShowPassingFlash(
                conn.copy().set_color(YELLOW),
                time_width=0.5
            ) for conn in connections_input_to_hidden
        ]

        self.play(FadeIn(filled_input), run_time=0.3)
        self.play(*flashes_ih, run_time=1)
        self.play(FadeOut(filled_input), FadeIn(filled_hidden), run_time=0.3)
        self.wait(1)

        flashes_ho = [
            ShowPassingFlash(
                conn.copy().set_color(YELLOW),
                time_width=0.5
            ) for conn in connections_hidden_to_output
        ]

        self.play(*flashes_ho, run_time=1)
        self.play(FadeOut(filled_hidden), FadeIn(filled_output), run_time=0.3)
        self.play(FadeOut(filled_output), Write(output_result))
        self.wait(1)

        self.play(Create(surrounding))
        self.play(FadeOut(surrounding))
        self.wait(2)
