import numpy as np
from manim import *

class LinearRegression:
    def __init__(self):
        self.weight = 0.0
        self.bias = 0.0
        self.history = []

    def predict(self, X):
        """Predict the target values for given input X."""
        return self.weight * X + self.bias

    def compute_loss(self, y_true, y_pred):
        """Compute Mean Squared Error (MSE) loss."""
        return np.mean((y_true - y_pred) ** 2)

    def fit(self, X, y, learning_rate=0.01, epochs=100):
        """Train the model using gradient descent."""
        n = len(X)
        for _ in range(epochs):
            y_pred = self.predict(X)

            d_weight = (-2 / n) * np.sum(X * (y - y_pred))
            d_bias = (-2 / n) * np.sum(y - y_pred)

            self.weight -= learning_rate * d_weight
            self.bias -= learning_rate * d_bias

            self.history.append((self.weight, self.bias))

    def get_history(self):
        """Return the history of the line (slope and intercept)."""
        return self.history

class LinearRegressionAnimation(Scene):
    def construct(self):
        X = np.array([0.5, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0])
        y = 2.5 * X + 2 + np.random.randn(len(X))

        model = LinearRegression()
        model.fit(X, y, learning_rate=0.01, epochs=40)

        weight_tracker = ValueTracker(0.)
        bias_tracker = ValueTracker(0.)

        title_text = Text("Linear Regression").to_edge(UP)

        axes = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 20, 2],
            x_length=7,
            y_length=5,
            axis_config={"include_numbers": True},
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        points = VGroup(*[
            Dot(axes.coords_to_point(x, y), color=BLUE)
            for x, y in zip(X, y)
        ])

        # Initial line
        line = always_redraw(lambda: axes.plot(
            lambda x: weight_tracker.get_value() * x + bias_tracker.get_value(),
            color=RED
        ))

        dashed_lines = VGroup(*[
            always_redraw(lambda i=i: DashedLine(
                start=axes.coords_to_point(X[i], y[i]),
                end=axes.coords_to_point(X[i], weight_tracker.get_value() * X[i] + bias_tracker.get_value()),
                color=RED,
                stroke_width=1.5,
            )) for i in range(len(X))
        ])

        info_text = (
            Text(f"Weight: {weight_tracker.get_value():.2f} Bias: {bias_tracker.get_value():.2f}", font_size=24)
            .next_to(title_text, DOWN, buff=0.2)
            .shift(LEFT * 1.5)
            .add_updater(
                lambda t: t.become(
                    Text(f"Weight: {weight_tracker.get_value():.2f} Bias: {bias_tracker.get_value():.2f}", font_size=24)
                    .next_to(title_text, DOWN, buff=0.2)
                )
            )
        )

        self.play(Write(title_text))
        self.wait(1)

        self.play(Create(axes), Create(axes_labels))
        self.wait(1)

        self.play(Write(info_text))
        self.wait(1)
        
        self.play(AnimationGroup(*[GrowFromCenter(dot) for dot in points], lag_ratio=0.1))
        
        self.play(GrowFromPoint(line, axes.get_origin()))
        self.wait(1)

        self.play(*[GrowFromPoint(dashed, dot) for (dashed, dot) in zip(dashed_lines, points)])
        self.wait(1)

        for epoch, (weight, bias) in enumerate(model.history):
            self.play(
                weight_tracker.animate.set_value(weight),
                bias_tracker.animate.set_value(bias),
                run_time=0.1,
            )

        self.wait(1)