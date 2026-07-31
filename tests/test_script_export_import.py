from dk4tool.script.export_csv import write_script_csv
from dk4tool.script.import_csv import read_script_csv
from dk4tool.script.model import CSV_COLUMNS


def test_csv_is_excel_safe_and_preserves_id(tmp_path):
    path = tmp_path / "script.csv"
    row = {column: "" for column in CSV_COLUMNS}
    row.update(
        {
            "id": "DK4_TEST",
            "file_path": "/data/test.dat",
            "encoding": "shift_jis",
            "source_offset": "0",
            "source_length": "4",
            "japanese": "出航",
            "status": "untranslated",
            "max_bytes": "4",
            "allow_expand": "false",
            "wrap_width": "32",
        }
    )
    write_script_csv(path, [row])
    assert path.read_bytes().startswith(b"\xef\xbb\xbf")
    assert read_script_csv(path)[0]["id"] == "DK4_TEST"

