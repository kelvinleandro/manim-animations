from manim import *
from scipy.stats import chi2

def change_colors(tex: MathTex, indices: list[int], color: ParsableManimColor) -> None:
    for idx in indices:
        tex[0][idx].set_color(color)

class Autoencoder(Scene):
    def construct(self):
        # PARTE 1: Realização do encoder e decoder
        titulo = Text("Autoencoder")
        titulo.to_edge(UP)

        # vetor_original = Matrix(
        #     [["X_1"], ["X_2"], ["X_3"], ["\\vdots"], ["X_{276}"]], 
        #     element_alignment_corner=ORIGIN
        # ).shift(LEFT*5)
        vetor_original = MathTex(r"""
        \begin{bmatrix}
        X_1 \\
        X_2 \\
        X_3 \\
        \vdots \\
        X_{276}
        \end{bmatrix}
        """).shift(LEFT*5)

        # vetor_espaco_latente = Matrix(
        #     [["Z_1"], ["Z_2"], ["Z_3"], ["\\vdots"], ["Z_q"]], 
        #     element_alignment_corner=ORIGIN, 
        #     element_to_mobject_config={"font_size": 32}
        # )
        vetor_espaco_latente = MathTex(r"""
        \begin{bmatrix}
        Z_1 \\
        Z_2 \\
        Z_3 \\
        \vdots \\
        Z_q
        \end{bmatrix}
        """, font_size=36)

        # vetor_reconstruido = Matrix(
        #     [["\\tilde{X}_1"], ["\\tilde{X}_2"], ["\\tilde{X}_3"], ["\\vdots"], ["\\tilde{X}_{276}"]], 
        #     element_alignment_corner=ORIGIN
        # ).shift(RIGHT*5)
        vetor_reconstruido = MathTex(r"""
        \begin{bmatrix}
        \tilde{X}_1 \\
        \tilde{X}_2 \\
        \tilde{X}_3 \\
        \vdots \\
        \tilde{X}_{276}
        \end{bmatrix}
        """).shift(RIGHT*5)

        # Alterando cores dos indices dos elementos do vetor
        vec_ori_num_idx = [8, 10, 12, 17, 18, 19]
        vec_laten_num_idx = [8, 10, 12, 17]
        vec_rec_num_idx = [9, 12, 15, 21, 22, 23]
        norm_diff_num_idx = [19, 23, 25, 29, 31, 35, 40, 41, 42, 43, 46, 47, 48]
        change_colors(vetor_original, vec_ori_num_idx, BLUE)
        change_colors(vetor_espaco_latente, vec_laten_num_idx, GREEN)
        change_colors(vetor_reconstruido, vec_rec_num_idx, BLUE)

        encoder = Text("Encoder", font_size=24).next_to(vetor_espaco_latente, LEFT, buff=1)
        decoder = Text("Decoder", font_size=24).next_to(vetor_espaco_latente, RIGHT, buff=1)

        box_encoder = SurroundingRectangle(encoder)
        box_decoder = SurroundingRectangle(decoder)

        self.play(Write(titulo))
        self.wait(1)

        self.play(Write(vetor_original))
        self.wait(1.5)

        self.play(ReplacementTransform(vetor_original.copy(), vetor_espaco_latente), run_time=2)
        self.wait(1)

        self.play(FadeIn(encoder))
        self.wait(1)

        self.play(Create(box_encoder))
        self.wait(1.5)
        self.play(FadeOut(box_encoder))
        self.wait(1)

        self.play(ReplacementTransform(vetor_espaco_latente.copy(), vetor_reconstruido), run_time=2)
        self.wait(1)

        self.play(FadeIn(decoder))
        self.wait(1)

        self.play(Create(box_decoder))
        self.wait(1.5)
        self.play(FadeOut(box_decoder))
        self.wait(1)

        self.play(*[
            FadeOut(mob) for mob in [vetor_espaco_latente, encoder, decoder] 
        ])
        self.wait(1)

        # PARTE 2: erro de reconstrução
        titulo_erro_reconstrucao = Text("Autoencoder - Erro de reconstrução").to_edge(UP)

        vetor_norm_diff = MathTex(r"""
        \left\lVert
        \begin{bmatrix}
        X_1 - \tilde{X}_1 \\
        X_2 - \tilde{X}_2 \\
        X_3 - \tilde{X}_3 \\
        \vdots \\
        X_{276} - \tilde{X}_{276}
        \end{bmatrix}
        \right\rVert_2^2
        """)
        change_colors(vetor_norm_diff, norm_diff_num_idx, BLUE)

        vetor_erro = MathTex(r"\left\lVert \ \vec{e} \ \right\rVert^2 = ").next_to(vetor_norm_diff, LEFT, buff=1)

        self.play(
            Transform(titulo, titulo_erro_reconstrucao), 
            TransformMatchingShapes(VGroup(vetor_original, vetor_reconstruido), vetor_norm_diff),
            run_time=2
        )
        self.wait(1)

        self.play(Write(vetor_erro))
        self.wait(1)

        self.play(*[
            FadeOut(mob) for mob in self.mobjects
        ])
        self.wait(1)

        # regiao de teste
        # Mostrar os índices de cada caractere
        # for i, char in enumerate(vetor_original[0]):
        #     self.play(Indicate(vetor_original[0][i]))

        # self.play(*[
        #     FadeOut(mob) for mob in self.mobjects
        # ])
        # self.wait(1)

        # PARTE 3: Classificação
        titulo_classif = Text("Classificação").to_edge(UP)

        graus_liberdade = 4

        axes = Axes(
            x_range=[0, 20, 1],
            y_range=[0, 0.2, 0.01],
            x_length=6,
            y_length=3,
            axis_config={"include_numbers": False, "include_ticks": False},
        )

        chi_curva = axes.plot(lambda x: chi2.pdf(x, graus_liberdade), color=GREEN)

        line = Line(
            start=axes.c2p(9.5, 0), 
            end=axes.c2p(9.5, 0.2), 
            color=GREEN
        )

        area_neg = axes.get_area(
            graph=axes.plot(lambda x: chi2.pdf(x, graus_liberdade), x_range=[0, 9.5], color=BLUE),
            x_range=(0, 9.5),
            color=BLUE
        )

        area_pos = axes.get_area(
            graph=axes.plot(lambda x: chi2.pdf(x, graus_liberdade), x_range=[9.5, 20], color=RED),
            x_range=(9.5, 20),
            color=RED
        )

        seta_sem_crise = Arrow(
            start=axes.c2p(4, 0.075),
            end=axes.c2p(7, 0.215)
        )

        seta_com_crise = Arrow(
            start=axes.c2p(10.5, 0.005),
            end=axes.c2p(15, 0.05)
        )

        sem_crise = Text("SEM CRISE", font_size=18, t2c={"SEM": BLUE}).next_to(seta_sem_crise.get_end(), UP, buff=0.2)
        com_crise = Text("COM CRISE", font_size=18, t2c={"COM": RED}).next_to(seta_com_crise.get_end(), UP, buff=0.2)

        norma_vetor = MathTex(r"\left\lVert \ \vec{e} \ \right\rVert^2", font_size=36).next_to(axes, DOWN, buff=0.5).shift(LEFT * 2)

        self.play(Write(titulo_classif))
        self.wait(1)

        self.play(Create(axes), run_time=2)
        self.wait(1)

        self.play(Create(chi_curva), run_time=3)
        self.wait(2)
        
        self.play(Create(line))
        self.wait(2)
        
        self.play(Create(area_neg, rate_func=linear), run_time=2)
        self.wait(1)

        self.play(Create(seta_sem_crise), Write(sem_crise))
        self.wait(2)

        self.play(Create(area_pos, rate_func=linear), run_time=2)
        self.wait(1)

        self.play(Create(seta_com_crise), Write(com_crise))
        self.wait(2)

        self.play(FadeIn(norma_vetor))
        self.wait(2)

        self.play(norma_vetor.animate.set_color(BLUE))
        self.wait(1)

        self.play(norma_vetor.animate.shift(RIGHT * 4), run_time=2)
        self.wait(1)

        self.play(norma_vetor.animate.set_color(RED))
        self.wait(3)