# Manim Animations

Animations using Manim Community exploring various concepts in computer science, with a special focus on machine learning and statistics

## Current animations

<!-- ANIMATIONS_START -->
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
