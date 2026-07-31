from pathlib import Path

from dk4tool.rom.manifest import build_manifest


class FakeImage:
    def __init__(self, source: Path):
        self.source = source

    def metadata(self):
        return {
            "size_bytes": self.source.stat().st_size,
            "game_title": "SYNTHETIC",
            "game_code": "TEST",
            "maker_code": "00",
        }

    def iter_files(self):
        yield 1, "/z/file.dat", b"two"
        yield 0, "/a/file.dat", b"one"


def test_manifest_is_deterministic_and_contains_hashes(tmp_path):
    source = tmp_path / "not-a-rom.dat"
    source.write_bytes(b"synthetic container")
    first = build_manifest(FakeImage(source))
    second = build_manifest(FakeImage(source))
    assert first == second
    assert [item["path"] for item in first["files"]] == ["/a/file.dat", "/z/file.dat"]
    assert all(len(item["sha256"]) == 64 for item in first["files"])

