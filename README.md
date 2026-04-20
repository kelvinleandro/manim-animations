# Manim Animations

Animations using Manim Community exploring various concepts in computer science, with a special focus on machine learning and statistics

## Current animations

<!-- ANIMATIONS_START -->
| Animation | Source |
|---|---|
| Autoencoder | [autoencoder.py](./src/autoencoder.py) |
| Automaton To Regex | [automaton_to_regex.py](./src/automaton_to_regex.py) |
| Central Limit Theorem | [central_limit_theorem.py](./src/central_limit_theorem.py) |
| Determinant As Area | [determinant_as_area.py](./src/determinant_as_area.py) |
| Dot Product | [dot_product.py](./src/dot_product.py) |
| Euclidian Distance | [euclidian_distance.py](./src/euclidian_distance.py) |
| Forward Propagation | [forward_propagation.py](./src/forward_propagation.py) |
| Grid Search | [grid_search.py](./src/grid_search.py) |
| K Means | [k_means.py](./src/k_means.py) |
| Knn | [knn.py](./src/knn.py) |
| Linear Regression | [linear_regression.py](./src/linear_regression.py) |
| Log Transformation | [log_transformation.py](./src/log_transformation.py) |
| Markov Chain | [markov_chain.py](./src/markov_chain.py) |
| Monte Carlo Pi | [monte_carlo_pi.py](./src/monte_carlo_pi.py) |
| Normal Distribution | [normal_distribution.py](./src/normal_distribution.py) |
| Normalization | [normalization.py](./src/normalization.py) |
| Relu | [relu.py](./src/relu.py) |
| Sigmoid | [sigmoid.py](./src/sigmoid.py) |
| Svm | [svm.py](./src/svm.py) |
<!-- ANIMATIONS_END -->

## Guide to Running Manim Animations

1. **Ensure you have Python installed.**

2. **Check Manim Dependencies**

   Before proceeding, check the required dependencies for Manim on the Manim Community site:

   👉 https://docs.manim.community/en/stable/installation.html

   Manim requires additional programs like LaTeX for text rendering.

3. **Clone the Repository**

   ```bash
   git clone https://github.com/kelvinleandro/manim-animations
   cd manim-animations
   ```

4. **Create a Virtual Environment (Recommended)**

   ```bash
   python -m venv .venv
   ```

   - Windows:

     ```bash
     .venv\Scripts\activate
     ```

   - Mac/Linux:
     ```bash
     source .venv/bin/activate
     ```

5. **Install Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

6. **Run a Manim Animation**
   ```bash
   manim -pqm script_name.py SceneName
   ```
