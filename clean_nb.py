import json
from typing import Any
from pathlib import Path


def clean_cell_source(source: list[str]) -> list[str]:
    clean = []
    for line in source:
        if "# <<<" in line:
            indent = (len(line) - len(line.lstrip())) * " "
            line = line.split("# <<<", maxsplit=1)[1].lstrip()
            if line.strip():
                line = indent + line
        clean.append(line)
    return clean


def clean_cell(cell: dict[str, Any]) -> dict[str, Any]:
    if "outputs" in cell:
        cell["outputs"] = []
    if "execution_count" in cell:
        cell["execution_count"] = None
    if cell["cell_type"] == "code":
        cell["source"] = clean_cell_source(cell["source"])
    return cell


def clean_notebook(filename: str) -> dict[str, Any]:
    nb = json.load(open(filename))
    nb["cells"] = [clean_cell(cell) for cell in nb["cells"]]
    return nb


if __name__ == "__main__":
    src_dir = Path(__file__).parent / "src"
    i_file = src_dir / "solution.ipynb"
    o_file = src_dir / "challenge.ipynb"
    nb = clean_notebook(i_file)
    json.dump(nb, open(o_file, "w"))
