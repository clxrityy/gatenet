import json
from pathlib import Path

data = json.loads(Path("coverage.json").read_text())

total = data["totals"]
percent = total["percent_covered_display"]

out = f"""
# Test Coverage

**Total Coverage:** `{percent}%`

- Statements: `{total["num_statements"]}`
- Missing: `{total["missing_lines"]}`

> [Detailed Report](coverage/index.html)
"""

Path("docs/tests.md").write_text(out.strip() + "\n")
