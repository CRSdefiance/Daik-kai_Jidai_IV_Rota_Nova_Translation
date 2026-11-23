"""Use original native dialogue expansion and rendering to check the staged edits."""
from types import FunctionType

from scripts import stage_rafael_mediterranean_dialogue_20261121 as stage
from scripts import verify_all_routes_next_phrase_wraps_20261118 as native_display


base, native = stage.base, stage.native
ROOT = stage.ROOT / "native_display"
PROOF = ROOT / "native_display.json"


def main():
    assert not ROOT.exists()
    release, stored, draft = map(base.load, (stage.parent.RELEASE, stage.PROOF, stage.review.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert stored["candidate_sha256"] == candidate and stored["whole_parent_inverse"]
    assert stored["manuscript_sha256"] == base.digest(stage.review.OUTPUT)
    assert stored["predecessor_sha256"] == release["candidate_sha256"] == base.digest(stage.parent.ROM)
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, release["own_registered_startup"], captain=3)
    rom = base.NdsImage.open(stage.ROM)
    assert all(ctx.image.read_file(path) == rom.read_file(path) for path in native_display.ASSETS)
    font = rom.read_file("/GRP/KANJI.FNT")
    paint, expand = native_display.clipped_renderer(ctx), native_display.original_expander()
    paragraph = native_display.display.paragraph
    validate = FunctionType(paragraph.__code__, paragraph.__globals__ | {"build": stage})
    rows = {row["id"]: row for row in draft["records"]}
    prior, current = (native.IlnkContainer.parse(image.read_file("/data/SC0.DK4")).blocks for image in (ctx.image, rom))
    verified, previews = [], []
    for group in stored["groups"]:
        path, number = group["file_path"], group["block"]
        assert path == "/data/SC0.DK4"
        block = current[number]
        assert native.digest(block) == group["after"]
        assert native.digest(prior[number]) == group["before"]
        for command in group["commands"]:
            old, new = (bytes.fromhex(command[key]) for key in ("current", "stored"))
            at = command["stored_offset"]
            assert block[at:at + len(new)] == new
            for ident in command["record_ids"]:
                row = rows.pop(ident)
                record = dict(id=ident, file_path=path, block=number, decision=row["decision"],
                              stored_offset=at, stored_command_hex=new.hex())
                if row["decision"] == "retention":
                    assert new == old
                else:
                    selector = row["source_selector"]
                    assert new[:6] == old[:6] == b"\0\x40\xff\xff\0" + bytes([selector])
                    end = new.index(0, 6)
                    assert not stage.review.TOKEN.findall(row["english"]) and not any(new[end:])
                    result = validate(ctx, font, paint, expand, None, {}, row, new[5:end], group["plans"][ident])
                    layout, = result["layouts"]
                    page, = layout["pages"]
                    assert page["native_independent_plane_equal"]
                    pixels = bytes.fromhex(page["native_plane_hex"])
                    previews.append((ident, pixels))
                    record.update(native_pages=1, expanded_hex=layout["expanded_hex"], lines=layout["lines"],
                                  plane_sha256=native.digest(pixels), original_expansion=result["macro_alignment_checks"])
                verified.append(record)
    assert not rows and len(verified) == 195 and len(previews) == 40
    ROOT.mkdir()
    contact = native_display.display.inherited.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(previews)
    base.save(PROOF, dict(candidate_sha256=candidate, stage_proof_sha256=base.digest(stage.PROOF), records=verified,
                         sheets=sheets, offline_native_only=True, newly_rendered_pages=len(previews)))
    print("Verified 40 new native pages and 155 unchanged stored speech commands.")


if __name__ == "__main__":
    main()
