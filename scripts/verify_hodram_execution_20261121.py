"""Verify the original native text consumer for the Hodram execution scene."""

from types import FunctionType, SimpleNamespace

from scripts import stage_hodram_execution_20261121 as build
from scripts import verify_all_routes_next_phrase_wraps_20261118 as display
from scripts.verify_moonlit_violin_20261121 import bytes_for


base, native, author = build.base, build.native, build.author
ROOT = build.ROOT / "native_display"
PROOF = ROOT / "native_display.json"
NAMES = {"FA": "Bergstrom"}


def main():
    assert not ROOT.exists()
    stored, review = map(base.load, (build.PROOF, author.OUTPUT))
    assert base.digest(build.ROM) == stored["candidate_sha256"]
    assert base.digest(author.PROGRESSIVE) == stored["manuscript_sha256"]
    old, target = map(base.NdsImage.open, (build.parent.ROM, build.ROM))
    assert all(old.read_file(asset) == target.read_file(asset) for asset in display.ASSETS)
    arm, font = (target.read_file(asset) for asset in (display.ASSETS[0], display.ASSETS[2]))
    runtime = SimpleNamespace(arm=arm)
    render, render_mixed = display.clipped_renderer(runtime), display.prior.original_cp932_renderer(arm)
    group, = stored["groups"]
    path = group["file_path"]
    block = native.IlnkContainer.parse(target.read_file(path)).blocks[group["block"]]
    assert native.digest(block) == group["after"]
    previous = native.IlnkContainer.parse(old.read_file(path)).blocks[group["block"]]
    rows = {r["id"]: r for r in review["records"] if r["kind"] == "progressive"}
    styled_rows = [r for r in review["records"] if r["kind"] == "styled"]
    results, previews, glyph_refs = [], [], []
    for cmd in group["commands"]:
        if not cmd["record_ids"]:
            continue
        ident, = cmd["record_ids"]
        row = rows.pop(ident)
        command, before = (bytes.fromhex(cmd[k]) for k in ("stored", "current"))
        raw = bytes_for(command)
        offset = cmd["stored_offset"]
        assert command[:6] == before[:6] == b"\0\x40\xFF\xFF\0" + bytes([row["source_selector"]])
        assert block[offset:offset+len(command)] == command and not any(command[6+len(raw):])
        assert author.TOKEN.findall(raw.decode("cp932")) == author.TOKEN.findall(bytes_for(before).decode("cp932"))
        body = display.prior.default_text(raw, NAMES)
        try_layouts = []
        if row["decision"] == "revision":
            plan = group["plans"][ident]
            encoded = bytes.fromhex(plan["encoded_hex"])
            assert bytes([row["source_selector"]]) + raw in (encoded, encoded + b" ")
            assert author.logical(raw.decode("ascii")) == row["english"] and plan["expected_native_pages"] == 1
            values = [("default", NAMES)]
            if author.TOKEN.findall(row["english"]):
                values += [("16-character surname", {"FA": "ABCDEFGHIJKLMNOP"})]
            for label, names in values:
                text = display.prior.default_text(raw, names)
                lines = [display.display.expected(line, names) for line in plan["lines"]]
                pages = display.display.raster(runtime, font, render, text, lines, 1)
                preview, = pages
                previews.append((f"Hodram {ident} {label}", bytes.fromhex(preview["native_plane_hex"])))
                assert all(page["native_independent_plane_equal"] for page in pages)
                try_layouts.append(dict(scope=label, native_lines=lines, page_hash=native.digest(bytes.fromhex(preview["native_plane_hex"]))))
        else:
            assert command == before and author.logical(raw.decode("cp932")) == row["english"]
            result = (render if body.isascii() else render_mixed)(arm, font, body)
            assert result["complete_consumed_bytes"] == len(body)
            assert all(p["native_independent_plane_equal"] for p in result["pages"])
            if not body.isascii():
                glyph_refs.append(ident)
            try_layouts = [dict(scope="exact retained body", native_pages=len(result["pages"]))]
        results.append(dict(id=ident, file_path=path, block=group["block"], decision=row["decision"],
            stored_offset=offset, stored_command_hex=command.hex(), native_pages=1 if row["decision"] == "revision" else len(result["pages"]),
            layouts=try_layouts))
    assert not rows and len(previews) == 4 and len(results) == 22
    assert glyph_refs == ["DK4_MES_B40_R0088", "DK4_MES_B40_R0092"]
    scan, _, _ = native.scoped_inventory()
    styled = []
    for data in (previous, block):
        commands, _ = scan(arm, data)
        entry, = [c for c in commands if c["word"] == 0x4100]
        styled.append(entry)
    assert styled[0]["whole_command_hex"] == styled[1]["whole_command_hex"]
    raw = bytes.fromhex(styled[1]["whole_command_hex"])
    bodies = author.pairing.text_records(raw, 0x4100)
    assert len(bodies) == len(styled_rows) == 8
    for row, (at, selector, body, slots) in zip(styled_rows, bodies, strict=True):
        assert (selector, slots) == (row["source_selector"], row["native_slots"])
        assert bytes([selector]).hex()+body.hex() == row["current_hex"] and row["decision"] == "retention"
        result = render(arm, font, body)
        assert result["complete_consumed_bytes"] == len(body)
        assert all(p["native_independent_plane_equal"] for p in result["pages"])
        results.append(dict(id=row["id"], file_path=path, block=group["block"], decision="retention",
            stored_offset=styled[1]["offset"], stored_command_hex=raw.hex(),
            body_offset_in_command=at, native_slots=slots, native_pages=len(result["pages"]), original_style_object_exact=True))
    ROOT.mkdir()
    contact = display.display.inherited.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(previews)
    base.save(PROOF, dict(candidate_sha256=stored["candidate_sha256"], stage_proof_sha256=base.digest(build.PROOF),
        full_review_sha256=base.digest(author.OUTPUT), records=results, sheets=sheets, actual_gameplay=False,
        newly_rendered_pages=len(previews), verified_source_script_cries=glyph_refs, exact_styled_variants=8))
    print("Verified four revised native layouts, two source-script cries and all eight retained crew alternatives.")


if __name__ == "__main__":
    main()
