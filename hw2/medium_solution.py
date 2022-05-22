from my_package import hard_task

if __name__ == "__main__":
  # Draw AST
  hard_task.build_graph()

  # Read table.tex
  with open('artifacts/easy/table.tex', 'r') as f:
    table = f.read()

  # Before table
  prefix = '\\documentclass{article}\n'
  prefix = prefix + '\\usepackage{graphicx}\n'
  prefix = prefix + '\\begin{document}\n'
  prefix = prefix + '\\includegraphics{{../../ast_graph.png}}\n'

  # After table
  suffix = '\n\\end{document}'

  # Write everything to document.tex
  with open('artifacts/medium/document.tex', 'w') as f:
    f.write(prefix + table + suffix)
