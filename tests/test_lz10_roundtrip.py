from dk4tool.scan.compression_probe import (
    compress_lz10,
    compress_lz10_literals,
    decompress_lz10,
    is_lz10,
)


def test_literal_lz10_roundtrip():
    payload = ("港へ行きますか？" * 4).encode("cp932")
    compressed = compress_lz10_literals(payload)
    assert is_lz10(compressed)
    assert decompress_lz10(compressed) == payload


def test_greedy_lz10_roundtrip_and_compression():
    payload = (b"translated subtitle on a black background\x00" * 100) + bytes(range(64))
    compressed = compress_lz10(payload)
    assert decompress_lz10(compressed) == payload
    assert len(compressed) < len(compress_lz10_literals(payload))
