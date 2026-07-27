import hashlib

from dk4tool.rom.hashing import hash_bytes, hash_file


def test_known_hashes(tmp_path):
    data = b"DK4 synthetic test"
    path = tmp_path / "sample.dat"
    path.write_bytes(data)
    expected = {
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }
    assert hash_bytes(data) == expected
    assert hash_file(path) == expected

