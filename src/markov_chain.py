from manim import *

class MarkovChain(Scene):
    def construct(self):
        title = Text("Markov Chain").to_edge(UP)

        sunny_state = Circle(radius=1, color=YELLOW).shift(LEFT * 3)
        rainy_state = Circle(radius=1, color=BLUE).shift(RIGHT * 3)
        
        sunny_label = Text("Sunny", font_size=24).move_to(sunny_state.get_center())
        rainy_label = Text("Rainy", font_size=24).move_to(rainy_state.get_center())
        
        sunny_to_rainy = Arrow(start=sunny_state.get_right() + UP * 0.3, end=rainy_state.get_left() + UP * 0.3, buff=0.2)
        rainy_to_sunny = Arrow(start=rainy_state.get_left() + DOWN * 0.3, end=sunny_state.get_right() + DOWN * 0.3, buff=0.2)
        
        sunny_to_rainy_label = MathTex("0.2").next_to(sunny_to_rainy, UP)
        rainy_to_sunny_label = MathTex("0.4").next_to(rainy_to_sunny, DOWN)

        sunny_to_sunny = Arc(
            radius=0.5,
            start_angle=PI / 3,
            angle=4 * PI / 3,
        ).next_to(sunny_state, LEFT, buff=0.2)
        sunny_to_sunny.add_tip(tip_length=0.2)

        rainy_to_rainy = Arc(
            radius=0.5,
            start_angle=2*PI/3,
            angle=-4*PI/3,
        ).next_to(rainy_state, RIGHT, buff=0.2)
        rainy_to_rainy.add_tip(tip_length=0.2)

        sunny_to_sunny_label = MathTex("0.8").next_to(sunny_to_sunny, LEFT, buff=0.2)
        rainy_to_rainy_label = MathTex("0.6").next_to(rainy_to_rainy, RIGHT, buff=0.2)

        self.play(Write(title))
        self.wait(1)
        
        self.play(Create(sunny_state), Create(rainy_state))
        self.wait(1)

        self.play(Write(sunny_label), Write(rainy_label))
        self.wait(1)

        self.play(Create(sunny_to_rainy), Write(sunny_to_rainy_label))
        self.wait(1)

        self.play(Create(rainy_to_sunny), Write(rainy_to_sunny_label))
        self.wait(1)

        self.play(Create(sunny_to_sunny), Write(sunny_to_sunny_label))
        self.wait(1)

        self.play(Create(rainy_to_rainy), Write(rainy_to_rainy_label))
        self.wait(1)
