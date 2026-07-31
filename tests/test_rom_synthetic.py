from ndspy import fnt
from ndspy.rom import NintendoDSRom

from dk4tool.rom.nds import NdsImage


def build_synthetic_rom(path):
    rom = NintendoDSRom()
    rom.name = b"SYNTHETIC\0\0\0"
    rom.idCode = b"TEST"
    rom.developerCode = b"00"
    rom.files = [b"root-data", "出航しますか？".encode("cp932") + b"\0"]
    rom.filenames = fnt.Folder(
        files=["root.dat"],
        folders=[("data", fnt.Folder(files=["message.dat"], firstID=1))],
        firstID=0,
    )
    rom.saveToFile(str(path))


def test_synthetic_rom_open_enumerate_replace_and_resave(tmp_path):
    source = tmp_path / "synthetic.nds"
    output = tmp_path / "rebuilt.nds"
    build_synthetic_rom(source)

    image = NdsImage.open(source)
    files = {path: data for _, path, data in image.iter_files()}
    assert files["/root.dat"] == b"root-data"
    assert files["/data/message.dat"].endswith(b"\0")
    assert image.metadata()["game_code"] == "TEST"

    image.replace_file("/root.dat", b"changed")
    image.replace_file("/__arm9__.bin", b"synthetic arm9")
    image.save(output)
    rebuilt = NdsImage.open(output)
    assert {path: data for _, path, data in rebuilt.iter_files()}["/root.dat"] == b"changed"
    assert rebuilt.read_file("/__arm9__.bin") == b"synthetic arm9"
