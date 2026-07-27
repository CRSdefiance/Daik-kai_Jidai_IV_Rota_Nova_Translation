from dk4tool.scan.sjis_scan import scan_sjis


def test_scanner_finds_null_terminated_japanese_with_offset():
    text = "出航しますか？"
    data = b"\x01\x02" + text.encode("cp932") + b"\0\x03"
    hit = scan_sjis(data)[0]
    assert hit.offset == 2
    assert hit.decoded == text
    assert hit.terminator == "00"


def test_scanner_ignores_ascii_and_short_noise():
    assert scan_sjis(b"ordinary ASCII\0\x81") == []

