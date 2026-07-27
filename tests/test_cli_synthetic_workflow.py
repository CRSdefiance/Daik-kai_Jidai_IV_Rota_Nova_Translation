from ndspy import fnt
from ndspy.rom import NintendoDSRom

from dk4tool.cli import main
from dk4tool.rom.nds import NdsImage
from dk4tool.script.export_csv import write_script_csv
from dk4tool.script.import_csv import read_script_csv


def synthetic_rom(path):
    rom = NintendoDSRom()
    rom.name = b"SYNTHETIC\0\0\0"
    rom.idCode = b"TEST"
    rom.developerCode = b"00"
    rom.files = ["出航しますか？".encode("cp932") + b"\0"]
    rom.filenames = fnt.Folder(files=["message.dat"], firstID=0)
    rom.saveToFile(str(path))


def internal_files(path):
    return {name: data for _, name, data in NdsImage.open(path).iter_files()}


def test_extract_noop_and_single_fixed_replacement(tmp_path):
    clean = tmp_path / "clean.nds"
    csv_path = tmp_path / "script.csv"
    noop = tmp_path / "noop.nds"
    modified = tmp_path / "modified.nds"
    synthetic_rom(clean)

    assert main(["extract-script", str(clean), "--out", str(csv_path)]) == 0
    rows = read_script_csv(csv_path)
    assert len(rows) == 1

    assert (
        main(
            [
                "insert-script",
                str(clean),
                str(csv_path),
                "--out",
                str(noop),
                "--mode",
                "fixed",
            ]
        )
        == 0
    )
    assert internal_files(noop) == internal_files(clean)

    rows[0]["english"] = "Set sail?"
    rows[0]["status"] = "draft"
    write_script_csv(csv_path, rows)
    assert (
        main(
            [
                "insert-script",
                str(clean),
                str(csv_path),
                "--out",
                str(modified),
                "--mode",
                "fixed",
            ]
        )
        == 0
    )
    assert internal_files(modified)["/message.dat"].startswith(b"Set sail?\0")

