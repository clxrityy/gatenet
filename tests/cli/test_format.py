from gatenet.cli.format import print_output, _serialize, _print_human
import json


def test_print_output_json():
    data = {"key": "value", "number": 42}
    import io
    import sys

    captured_output = io.StringIO()
    sys.stdout = captured_output

    print_output(data, json_output=True)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue().strip()
    expected_output = json.dumps(data, default=_serialize, indent=2)
    assert output == expected_output


def test_print_output_human():
    dummy_data = {"name": "Test", "value": 123}

    import io
    import sys

    captured_output = io.StringIO()
    sys.stdout = captured_output

    _print_human(data=dummy_data)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue().strip()
    assert "Test" in output
    assert "123" in output
