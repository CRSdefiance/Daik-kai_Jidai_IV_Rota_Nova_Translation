from dk4tool.scan.utf16_scan import scan_utf16le


def test_utf16le_scanner_finds_japanese():
    text = "交易します"
    data = b"\x01\x01" + text.encode("utf-16le") + b"\0\0"
    hits = scan_utf16le(data)
    assert any(hit.offset == 2 and hit.decoded == text for hit in hits)

