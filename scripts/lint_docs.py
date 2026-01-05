import ast
import sys
from pathlib import Path

REQUIRE_EXAMPLES = True


def has_examples(doc: str) -> bool:
    return ("Examples:" in doc) | (">>>" in doc or "```" in doc)


def lint_file(path: Path) -> list[str]:
    errors = []
    tree = ast.parse(path.read_text())

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name.startswith("_"):
                continue

            doc = ast.get_docstring(node)
            if not doc:
                errors.append(f"{path}:{node.lineno} Missing docstring for {node.name}")
                continue

            if REQUIRE_EXAMPLES and not has_examples(doc):
                errors.append(
                    f"{path}:{node.lineno} Missing examples in docstring for {node.name}"
                )
    return errors


def main():
    errors: list[str] = []

    for path in Path("./gatenet").rglob("*.py"):
        errors.extend(lint_file(path))

    if errors:
        print("\n".join(errors))
        sys.exit(1)


if __name__ == "__main__":
    main()
