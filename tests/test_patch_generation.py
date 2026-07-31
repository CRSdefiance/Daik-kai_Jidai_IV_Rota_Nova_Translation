import json

from dk4tool.cli import main
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.hashing import hash_file


def test_xdelta_roundtrip(tmp_path):
    clean = tmp_path / "clean.dat"
    modified = tmp_path / "modified.dat"
    patch = tmp_path / "change.xdelta"
    rebuilt = tmp_path / "rebuilt.dat"
    clean.write_bytes((b"clean synthetic block\n" * 256) + b"tail")
    modified.write_bytes((b"clean synthetic block\n" * 128) + b"translated\n" + (b"x" * 512))

    make_xdelta(clean, modified, patch)
    apply_xdelta(clean, patch, rebuilt)

    assert patch.read_bytes().startswith(b"\xD6\xC3\xC4")
    assert rebuilt.read_bytes() == modified.read_bytes()


def test_cli_rejects_source_that_does_not_match_release_manifest(tmp_path):
    clean = tmp_path / "clean.dat"
    wrong = tmp_path / "wrong.dat"
    modified = tmp_path / "modified.dat"
    patch = tmp_path / "change.xdelta"
    output = tmp_path / "output.dat"
    clean.write_bytes(b"source data")
    wrong.write_bytes(b"wrong source")
    modified.write_bytes(b"translated target")
    make_xdelta(clean, modified, patch)
    (tmp_path / "release_manifest.json").write_text(
        json.dumps(
            {
                "source_rom_sha256": hash_file(clean)["sha256"],
                "modified_rom_sha256": hash_file(modified)["sha256"],
            }
        ),
        encoding="utf-8",
    )

    assert main(["apply-xdelta", str(wrong), str(patch), "--out", str(output)]) == 2
    assert not output.exists()
