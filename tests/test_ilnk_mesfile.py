from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.mesfile import (
    analyze_mesfile,
    encode_mesfile_text,
    export_mesfile_rows,
    rebuild_mesfile,
)


def synthetic_ilnk() -> bytes:
    return IlnkContainer(
        [
            "港へ行きますか？\nはい".encode("cp932") + b"\0ASCII only",
            b"\0" + "交易します".encode("cp932"),
        ]
    ).to_bytes()


def test_ilnk_parse_rebuild_is_exact():
    data = synthetic_ilnk()
    assert IlnkContainer.parse(data).to_bytes() == data


def test_mesfile_analysis_reports_structure_and_controls():
    report = analyze_mesfile(synthetic_ilnk())
    assert report["format"] == "ILNK"
    assert report["block_count"] == 2
    assert report["offset_entry_count"] == 3
    assert report["control_byte_counts"] == {"0A": 1}
    assert report["undecodable_record_count"] == 0
    assert report["insertion_policy"] == "exact-length-only"


def test_mesfile_skips_undecodable_segments_without_modifying_them():
    data = IlnkContainer([b"\x84\x00" + "港".encode("cp932")]).to_bytes()
    rows = export_mesfile_rows(data, "/data/SC0.DK4")
    report = analyze_mesfile(data)
    assert len(rows) == 1
    assert report["undecodable_record_count"] == 1
    assert rebuild_mesfile(data, rows) == data


def test_mesfile_export_preserves_linebreak_token_and_stable_groups():
    rows = export_mesfile_rows(synthetic_ilnk(), "/COMMON/MESFILE.DK4")
    assert len(rows) == 2
    assert rows[0]["japanese"] == "港へ行きますか？{LB}はい"
    assert rows[0]["pointer_group"] == "ILNK:0:0"
    assert rows[1]["pointer_group"] == "ILNK:1:1"


def test_mesfile_rebuild_allows_expansion_and_updates_offsets():
    data = synthetic_ilnk()
    rows = export_mesfile_rows(data, "/COMMON/MESFILE.DK4")
    rows[0]["english"] = "Go to port now?{LB}Yes"
    rows[0]["allow_expand"] = "true"
    rebuilt = rebuild_mesfile(data, rows)
    parsed = IlnkContainer.parse(rebuilt)
    assert parsed.blocks[0].split(b"\0")[0] == encode_mesfile_text("Go to port now?{LB}Yes")
    assert parsed.blocks[0].endswith(b"ASCII only")
    assert parsed.blocks[1] == IlnkContainer.parse(data).blocks[1]


def test_mesfile_noop_rebuild_is_exact():
    data = synthetic_ilnk()
    rows = export_mesfile_rows(data, "/COMMON/MESFILE.DK4")
    assert rebuild_mesfile(data, rows) == data


def test_mesfile_rebuild_rejects_size_change_without_explicit_expansion():
    data = synthetic_ilnk()
    rows = export_mesfile_rows(data, "/COMMON/MESFILE.DK4")
    rows[0]["english"] = "Short"
    try:
        rebuild_mesfile(data, rows)
    except ValueError as error:
        assert "exactly" in str(error)
    else:
        raise AssertionError("expected exact-length rejection")


def test_mesfile_pad_token_safely_fills_exact_length():
    data = synthetic_ilnk()
    rows = export_mesfile_rows(data, "/COMMON/MESFILE.DK4")
    rows[0]["english"] = "Go now!{PAD}"
    rebuilt = rebuild_mesfile(data, rows)
    original = IlnkContainer.parse(data).blocks[0].split(b"\0")[0]
    replacement = IlnkContainer.parse(rebuilt).blocks[0].split(b"\0")[0]
    assert replacement == b"Go now!".ljust(len(original), b" ")
    assert len(replacement) == len(original)


def test_mesfile_aligned_linebreak_preserves_control_offset():
    encoded = encode_mesfile_text("Short{LB@10}Next")
    assert encoded == b"Short    \n Next"


def test_mesfile_aligned_linebreak_rejects_overflow():
    try:
        encode_mesfile_text("Too long{LB@3}")
    except ValueError as error:
        assert "cannot align line break" in str(error)
    else:
        raise AssertionError("expected aligned line-break overflow")
