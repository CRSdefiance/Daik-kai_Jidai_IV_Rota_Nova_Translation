"""Verify exact progressive glyphs and every retained modal page in the batch."""

from types import FunctionType

from scripts import stage_rafael_athens_and_maria_crew_20261122 as stage
from scripts import verify_palace_london_glyphs_20261122 as glyphs
from scripts import verify_all_routes_next_phrase_wraps_20261118 as display
from scripts.stage_hamburg_ceramics_cross_route_20261120 import current_fe_painter


base, native = stage.base, stage.native
GLYPH_PROOF = stage.ROOT / "glyph_and_sheet_verification.json"
check_glyphs = FunctionType(glyphs.verify.__code__, vars(glyphs) | dict(stage=stage, OUTPUT=GLYPH_PROOF))


def check_modal():
    draft, stored, release = map(base.load, (stage.REVIEW, stage.PROOF, stage.parent.RELEASE))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"]
    assert stored["draft_sha256"] == base.digest(stage.REVIEW)
    assert stored["predecessor_sha256"] == release["candidate_sha256"]
    image = base.NdsImage.open(stage.ROM)
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, release["own_registered_startup"], captain=3)
    assert all(ctx.image.read_file(asset) == image.read_file(asset) for asset in display.ASSETS)
    paint = current_fe_painter(ctx)
    records, pictures = [], []
    owners = {(r["file_path"], r["id"]): r for r in draft["records"] if r["source_selector"] == 254}
    for group in stored["groups"]:
        path, route, block = (group[key] for key in ("file_path", "route", "block"))
        bank = native.IlnkContainer.parse(image.read_file(path))
        payload = bank.blocks[block]
        assert native.digest(payload) == group["after"]
        for command in group["commands"]:
            raw = bytes.fromhex(command["stored"])
            if command["word"] != 0x4000 or raw[5] != 254:
                continue
            assert raw.startswith(bytes.fromhex("0040ffff00fe")) and command["current"] == command["stored"]
            ident = command.get("retained_continuation_of")
            second = ident is not None
            if not second:
                ident, = command["record_ids"]
            owner = owners[path, ident]
            at = command["stored_offset"]
            assert payload[at:at + len(raw)] == raw and not any(raw[raw.index(0, 6):])
            original = owner.get("retained_FE_pages", [])
            if original:
                assert raw[5:raw.index(0, 6)].hex() == original[int(second)]["exact_stored_hex"]
            else:
                assert not second
            body = raw[6:raw.index(0, 6)]
            page = paint(body)
            membership = stage.typed.forest.system.check_FE_rows(body, page)
            assert page["complete_consumed_bytes"] == len(body)
            plane = page["physical"]
            assert all(not any(plane[y*228+216:(y+1)*228]) for y in range(64))
            cropped = b"".join(plane[y*228:y*228+216] for y in range(64))
            pictures.append((f"SC{route} {ident} / page {1 + second}", cropped))
            records.append(dict(route=route, block=block, id=ident, second_page=second,
                stored_offset=at, exact_command_hex=raw.hex(), row_membership=membership,
                physical_plane_sha256=native.digest(plane), physical_plane_hex=plane.hex()))
    assert len(records) == 10 and sum(r["second_page"] for r in records) == 2
    assert {(r["route"], r["id"]) for r in records} == {(r["route"], r["id"]) for r in owners.values()}
    contact = display.display.inherited.early.contact_sheets
    root = stage.ROOT / "retained_FE"
    root.mkdir(exist_ok=True)
    sheets = FunctionType(contact.__code__, contact.__globals__ | dict(ROOT=root))(pictures)
    for sheet in sheets:
        original = stage.Path(sheet["path"])
        renamed = original.with_name(f"retained_FE_{original.name}")
        assert not renamed.exists()
        original.rename(renamed)
        sheet["path"] = str(renamed)
        assert base.digest(renamed) == sheet["sha256"]
    base.save(stage.FE_PROOF, dict(candidate_sha256=candidate, records=records, sheets=sheets,
        original_modal_consumer=True, complete_stored_page_count=len(records)))
    print("Verified all ten modal pages, including both original two-page Maria sequences.", flush=True)


if __name__ == "__main__":
    check_glyphs()
    check_modal()
