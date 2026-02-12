import os
import ast
from src._agents.architect_node.presenter import find_entry_point
from src.config import REPO_PATH, llm


class ProjectSummarizer:
    def __init__(self):
        self.repo_path = os.path.abspath(REPO_PATH)

    def get_context(self):

        readme_candidates = ["README.md", "README.txt", "readme.md"]
        for name in readme_candidates:
            path = os.path.join(self.repo_path, name)
            if os.path.exists(path):
                print(f"Found Documentation: {name}")
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    return f"PROJECT DOCUMENTATION (from {name}):\n\n" + f.read()[:2000] 

        print("No, can't README found. Generating own analysis...")
        return self.get_summary()

    def get_summary(self):
        
        """
        Scans code to guess what the project does.
        """
        
        start_file = find_entry_point(self.repo_path)
        if not start_file:
            return "Project Analysis Failed: No Entry Point found."

        full_start_path = os.path.join(self.repo_path, start_file)
        
        
        imports = self.get_from_imports(full_start_path)
        tech_stack = ", ".join(imports) if imports else "Standard Python"
        
        docstring = self.doc_string(full_start_path)

        
        files_names = self.file_names()

        return f"""
PROJECT AUTO-ANALYSIS (No README Found)
---------------------------------------
1. **Entry Point:** `{start_file}`
2. **Tech Stack:** {tech_stack} (Detected from imports)
3. **Key Modules:** {', '.join(files_names)}
4. **Developer Description:** "{docstring}"
"""

    def get_from_imports(self, file_path):
        """Extracts top-level imports for identify."""
        
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                tree = ast.parse(f.read())
            
            libs = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        libs.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        libs.add(node.module.split('.')[0])
            
            
            stdlib = {'os', 'sys', 'json', 'time', 'math', 'random', 're', 'collections'}
            return list(libs - stdlib)
        except:
            return []

    def doc_string(self, file_path):
        """Reads the very first comment/docstring in the file."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                tree = ast.parse(f.read())
            return ast.get_docstring(tree) or "No description provided in code."
        except:
            return "Could not read file."

    def file_names(self):
        """Returns the 5 largest python files (likely the core logic)."""
        file_sizes = []
        for root, _, files in os.walk(self.repo_path):
            for f in files:
                if f.endswith(".py") and "venv" not in root:
                    path = os.path.join(root, f)
                    size = os.path.getsize(path)
                    file_sizes.append((f, size))
        
        
        file_sizes.sort(key=lambda x: x[1], reverse=True)
        return [f[0] for f in file_sizes[:5]]



