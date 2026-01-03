from pathlib import Path
import mkdocs_gen_files

PACKAGE = "gatenet"
SRC = Path(PACKAGE)

for path in SRC.rglob("*.py"):
    if path.name == "__init__.py":
        continue

    module_path = path.with_suffix("").as_posix().replace("/", ".")
    doc_path = Path("api", *path.parts).with_suffix(".md")

    with mkdocs_gen_files.open(doc_path, "w") as f:
        f.write(f"# `{module_path}`\n\n")
        f.write(f"::: {module_path}\n")

    mkdocs_gen_files.set_edit_path(doc_path, path)
