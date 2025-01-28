from manim import *
from statistics import mode

class KNN(Scene):
    def construct(self):
        title = Text("K-nearest neighbors").to_edge(UP)

        DOT_SIZE = 0.1

        color_to_classes = {
            RED: "Red",
            BLUE: "Blue"
        }

        classes_to_color = {
            "Red": RED,
            "Blue": BLUE
        }
        
        points = [
            (-1, 3, RED),
            (2, 1, BLUE),
            (-2, 2, RED),
            (-1, 2, BLUE),
            (-1, 0, RED),
            (1, 1, RED),
        ]
        new_point = (1, 2, GREEN)

        axes = Axes(
            x_range=[-2, 3, 1],
            y_range=[0, 4, 1],
            x_length=5,
            y_length=5,
            tips=True,
        ).shift(LEFT * 3)
        axes_labels = axes.get_axis_labels(x_label="x_1", y_label="x_2")

        dots = VGroup(*[
            Dot(axes.c2p(point[0], point[1]), color=point[2], radius=DOT_SIZE) for point in points
        ])
        new_dot = Dot(axes.c2p(new_point[0], new_point[1]), color=new_point[2], radius=DOT_SIZE)

        distances = [
            (i + 1, self.calculate_distance(point, new_point), color_to_classes[point[2]])
            for i, point in enumerate(points)
        ]

        # Table creation
        headers = ["i", "Distance", "Class"]
        table_rows = [
            [str(idx), f"{dist:.2f}", cls]
            for idx, dist, cls in distances
        ]
        table = Table(
            table_rows,
            col_labels=[Text(h, font_size=32) for h in headers],
            include_outer_lines=False
        ).scale(0.5).next_to(axes, RIGHT, buff=2)

        for i in range(2, len(points)+2):
            ent = table.get_entries((i, 3))
            ent.set_color(classes_to_color[ent.lines_text.original_text])

        k_1 = Text("K = 1", font_size=28).next_to(table, DOWN, buff=0.4)
        k_3 = Text("K = 3", font_size=28).next_to(table, DOWN, buff=0.4)

        sorted_distances = sorted([dist[1] for dist in distances])
        circle_k_1 = DashedVMobject(Circle(radius=sorted_distances[0] + 2 * DOT_SIZE, color=WHITE), num_dashes=15).move_to(new_dot)
        circle_k_3 = DashedVMobject(Circle(radius=sorted_distances[2] + 2 * DOT_SIZE, color=WHITE), num_dashes=15).move_to(new_dot)

        # for K=1
        smallest_idx = min(range(len(distances)), key=lambda i: distances[i][1])
        rect_1 = SurroundingRectangle(table.get_rows()[smallest_idx+1])
        color_1 = classes_to_color[distances[smallest_idx][2]] 

        # for K=3
        smallest_3_indices = sorted(range(len(distances)), key=lambda i: distances[i][1])[:3]
        smallest_3_classes = [distances[idx][2] for idx in smallest_3_indices]
        color_3 = classes_to_color[mode(smallest_3_classes)]
        rects_3 = VGroup(*[SurroundingRectangle(table.get_rows()[idx+1]) for idx in smallest_3_indices])

        self.play(Write(title))
        self.wait(1)
        self.play(Create(axes), Create(axes_labels), run_time=2)
        self.wait(1)
        self.play(Create(dots))
        self.wait(1)
        self.play(Create(new_dot))
        self.wait(2)

        self.play(Create(table), run_time=3)
        self.wait(2)

        # highlighting distance between dots and the respective table line
        for i, dot in enumerate(dots):
            line = DashedLine(start=new_dot, end=dot, buff=0.1, color=YELLOW)
            rect = SurroundingRectangle(table.get_rows()[i+1])

            self.play(Create(line), run_time=0.25)
            self.play(Create(rect), run_time=0.5)
            self.play(FadeOut(line, rect))
            self.wait(1)

        self.play(Write(k_1))
        self.wait(2)

        # K=1
        self.play(Create(circle_k_1))
        self.wait(1)
        self.play(Create(rect_1))
        self.wait(1)
        self.play(new_dot.animate.set_color(color_1))
        self.wait(1)
        self.play(FadeOut(rect_1))
        self.wait(1)

        # K=3
        self.play(Transform(k_1, k_3))
        self.wait(1)
        self.play(Create(circle_k_3))
        self.wait(2)
        self.play(Create(rects_3))
        self.wait(1)
        self.play(new_dot.animate.set_color(color_3))
        self.wait(1)
        self.play(FadeOut(rects_3))
        self.wait(1)

    @staticmethod
    def calculate_distance(p1, p2):
        return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**(1/2)