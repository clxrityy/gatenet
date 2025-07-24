#!/usr/bin/env python3
"""
Generate a reStructuredText coverage summary table from coverage.xml (pytest-cov output).
Run this script after tests to update docs/source/coverage_summary.rst.
"""
import xml.etree.ElementTree as ET
from pathlib import Path

COVERAGE_XML = Path(__file__).parent.parent.parent / "coverage.xml"
OUTPUT_RST = Path(__file__).parent / "coverage_summary.rst"


def parse_coverage(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    summary = []
    for pkg in root.findall("packages/package"):
        for cls in pkg.findall("classes/class"):
            filename = cls.attrib["filename"]
            lines = cls.find("lines")
            if lines is not None:
                line_elems = lines.findall("line")
                total = len(line_elems)
                covered = sum(1 for l in line_elems if int(l.attrib["hits"]) > 0)
            else:
                total = 0
                covered = 0
            percent = 100.0 * covered / total if total else 100.0
            summary.append((filename, total, covered, percent))
    return summary


def write_rst(summary, out_path):
    with open(out_path, "w") as f:
        f.write("Test Coverage Summary\n=====================\n\n")
        f.write(".. list-table:: File Coverage\n   :header-rows: 1\n   :widths: 40 10 10 10\n\n")
        f.write("   * - File\n     - Statements\n     - Covered\n     - Percent\n")
        for filename, total, covered, percent in sorted(summary):
            f.write(f"   * - {filename}\n     - {total}\n     - {covered}\n     - {percent:.1f}%\n")
        f.write("\nGenerated from coverage.xml.\n")


def main():
    if not COVERAGE_XML.exists():
        print(f"coverage.xml not found at {COVERAGE_XML}")
        return
    summary = parse_coverage(COVERAGE_XML)
    write_rst(summary, OUTPUT_RST)
    print(f"Wrote coverage summary to {OUTPUT_RST}")

if __name__ == "__main__":
    main()
