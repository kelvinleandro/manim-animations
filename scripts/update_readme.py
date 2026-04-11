import os
import re

def update_readme():
    src_dir = 'src'
    readme_path = 'README.md'

    if not os.path.exists(src_dir):
        print(f"Directory {src_dir} does not exist.")
        return

    # Get python files from src/
    files = [f for f in os.listdir(src_dir) if f.endswith('.py') and os.path.isfile(os.path.join(src_dir, f))]
    files.sort()

    # Generate markdown table
    table_lines = [
        "| Animation | Source |",
        "|---|---|"
    ]

    for f in files:
        # formatting name: remove .py, split by _, capitalize each, join with space
        name = f.replace('.py', '')
        name = ' '.join(word.capitalize() for word in name.split('_'))
        table_lines.append(f"| {name} | [{f}](./src/{f}) |")

    table_content = '\n'.join(table_lines) + '\n'

    # Read README.md
    with open(readme_path, 'r', encoding='utf-8') as file:
        readme_content = file.read()

    # Replace content between markers
    pattern = re.compile(r'(<!-- ANIMATIONS_START -->\n).*?(<!-- ANIMATIONS_END -->)', re.DOTALL)
    
    if pattern.search(readme_content):
        new_readme = pattern.sub(rf'\g<1>{table_content}\g<2>', readme_content)
        
        with open(readme_path, 'w', encoding='utf-8') as file:
            file.write(new_readme)
        print("README.md updated successfully.")
    else:
        print("Markers not found in README.md.")

if __name__ == '__main__':
    update_readme()
