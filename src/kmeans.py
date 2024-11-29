import numpy as np
from manim import *
from sklearn.datasets import make_blobs

class KMeans:
    def __init__(self, n_clusters, max_iters=300, tolerance=1e-4, random_state=None):
        self.n_clusters = n_clusters
        self.max_iters = max_iters
        self.tolerance = tolerance
        self.random_state = random_state
        self.centroids = None # Final centroids
        self.history = [] # History of centroids at each iteration
        self.labels = None # Cluster assignments for each data point

    def initialize_centroids(self, X):
        np.random.seed(self.random_state)
        indices = np.random.choice(len(X), self.n_clusters, replace=False)
        return X[indices]

    def compute_distances(self, X, centroids):
        distances = np.zeros((X.shape[0], self.n_clusters))
        for i, centroid in enumerate(centroids):
            distances[:, i] = np.linalg.norm(X - centroid, axis=1)
        return distances

    def assign_clusters(self, distances):
        return np.argmin(distances, axis=1)

    def update_centroids(self, X, labels):
        new_centroids = np.zeros((self.n_clusters, X.shape[1]))
        for k in range(self.n_clusters):
            cluster_points = X[labels == k]
            if len(cluster_points) > 0:
                new_centroids[k] = cluster_points.mean(axis=0)
        return new_centroids

    def fit(self, X):
        self.centroids = self.initialize_centroids(X)
        self.history.append(self.centroids.copy())
        for iteration in range(self.max_iters):
            distances = self.compute_distances(X, self.centroids)
            labels = self.assign_clusters(distances)
            new_centroids = self.update_centroids(X, labels)
            self.history.append(new_centroids.copy())
            if np.all(np.abs(new_centroids - self.centroids) <= self.tolerance):
                break
            self.centroids = new_centroids
        self.labels = labels

    def predict(self, X):
        distances = self.compute_distances(X, self.centroids)
        return self.assign_clusters(distances)

    def get_history(self):
        return self.history


class KMeansAnimation(Scene):
    def construct(self):
        # synthetic dataset
        X, _ = make_blobs(n_samples=30, centers=3, cluster_std=1.5, random_state=42)

        kmeans = KMeans(n_clusters=3, max_iters=10, random_state=42)
        kmeans.fit(X)
        history = kmeans.get_history()

        axes = Axes(
            x_range=[-15, 15, 5],
            y_range=[-15, 15, 5],
            x_length=6,
            y_length=6,
            axis_config={"include_numbers": False, "include_ticks": False},
        )

        points_group = VGroup(
            *[
                Dot(axes.coords_to_point(x, y), color=GRAY, radius=0.05)
                for x, y in X
            ]
        )

        centroid_dots = VGroup(
            *[
                Dot(axes.coords_to_point(x, y), color=RED, radius=0.10)
                for x, y in history[0]
            ]
        )

        title = Text("KMeans Clustering").to_edge(UP)

        self.play(Write(title), Create(axes), run_time=2)
        self.wait(1)

        self.play(FadeIn(points_group))
        self.wait(1)

        self.play(FadeIn(centroid_dots))
        self.wait(1)

        for iteration, centroids in enumerate(history[1:], start=1):
            distances = kmeans.compute_distances(X, centroids)
            labels = kmeans.assign_clusters(distances)

            # Update point colors based on cluster assignment
            for i, dot in enumerate(points_group):
                color = [BLUE, GREEN, ORANGE][labels[i]]
                self.play(dot.animate.set_color(color), run_time=0.025)

            self.wait(1)
            self.play(
                *[
                    centroid.animate.move_to(axes.coords_to_point(x, y))
                    for centroid, (x, y) in zip(centroid_dots, centroids)
                ],
                run_time=1
            )

        self.wait(2)