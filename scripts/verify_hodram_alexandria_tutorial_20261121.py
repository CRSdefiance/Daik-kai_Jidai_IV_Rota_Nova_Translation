"""Check every revised speech page, name expansion, and both native captions."""
from types import FunctionType

from dk4tool.dialogue.reviewed_choice_object_v2 import labels
from scripts import check_typed_story_menu_display_20261121 as menu
from scripts import stage_hodram_alexandria_tutorial_20261121 as stage
from scripts import verify_all_routes_next_phrase_wraps_20261118 as display


base, native = stage.base, stage.native
ROOT = stage.ROOT / "native_display"
PROOF = ROOT / "native_display.json"
NAMES = {"FI": "Hodram", "FA": "Bergstrom"}


def context(parent):
    last = base.load(stage.parent.live.PROOF)
    report = base.load(stage.parent.live.replay.REPORT)
    assert last["candidate_sha256"] == report["ROM_sha256"] == parent["candidate_sha256"]
    assert last["evidence"][str(stage.parent.live.replay.REPORT)] == base.digest(stage.parent.live.replay.REPORT)
    snapshot = last["staged_native_event"]["read_only_snapshot"]
    assert snapshot == report["read_only_RAM_snapshot"] and snapshot["read_only_export"]
    boot = ROOT / "ordinary_Hodram_snapshot.json"
    base.save(boot, dict(candidate_sha256=parent["candidate_sha256"], cold_boot=True, savestate=False,
                        actual_captain_getter=1, read_only_snapshot=snapshot))
    return native.RegisteredRuntime(stage.parent.RELEASE, boot, captain=1)


def check_menu(arm, command, rows):
    old, new = [bytes.fromhex(command[key]) for key in ("current", "stored")]
    assert labels(old) == [b"Listen.", b"Skip"] and labels(new) == [b"Listen", b"Skip"]
    vms, paint, executed = menu.adapters(arm)
    versions = []
    for key, obj in (("clean source", bytes.fromhex(command["source"])), ("predecessor", old), ("revised", new)):
        a, b = [vms[2](arm, obj, align) for align in (0, 2)]
        assert a == b and [c["modal_selection"] for c in a["VM_cases"]] == [0, 1, -1]
        assert a["labels"] == [value.decode("cp932") for value in labels(obj)]
        versions.append(dict(version=key, native=a, raw=obj.hex()))
    assert versions[1]["native"]["native_menu_rectangle"] == versions[2]["native"]["native_menu_rectangle"]
    width = versions[2]["native"]["minimum_width_units"] * 6
    proofs, pictures = [], []
    for index, (logical, body) in enumerate(zip(rows, labels(new), strict=True)):
        assert logical["english"].encode("ascii") == body
        for style in (1, 15):
            pixels, audit = paint(arm, body, style, width, (0, index * 12))
            assert audit["independent_complete_native_pixels_match"] and audit["storage_padding_all_blank"]
            assert audit["extra_flush_stays_within_physical_backing"] and audit["visible_cell_center_twice"] == width
            proofs.append(dict(id=logical["id"], style=style, native=audit))
            if style == 1:
                pictures.append((logical["id"] + " " + logical["english"], width, pixels))
    path = ROOT / "cesare_tutorial_choices.png"
    menu.sheet(pictures, path)
    return dict(object_versions=versions, caption_planes=proofs, checked_instruction_addresses=len(executed),
                sheet=dict(path=str(path), sha256=base.digest(path)))


def main():
    assert not ROOT.exists()
    registered, stored, draft = map(base.load, (stage.parent.RELEASE, stage.PROOF, stage.review.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] and stored["whole_parent_inverse"]
    assert stored["predecessor_sha256"] == registered["candidate_sha256"]
    assert stored["manuscript_sha256"] == base.digest(stage.review.OUTPUT)
    ROOT.mkdir()
    ctx = context(registered)
    target = base.NdsImage.open(stage.ROM)
    assert all(ctx.image.read_file(name) == target.read_file(name) for name in display.ASSETS)
    expand, paint = display.original_expander(), display.clipped_renderer(ctx)
    assert {c["output_hex"] for c in ctx.execute(expand, b"FI FA", 1)["cases"]} == {b"Hodram Bergstrom".hex()}
    font = target.read_file("/GRP/KANJI.FNT")
    paragraph = display.display.paragraph
    audit = FunctionType(paragraph.__code__, paragraph.__globals__ | {"build": stage})
    rows = {row["id"]: row for row in draft["records"]}
    bank = native.IlnkContainer.parse(target.read_file("/data/SC1.DK4")).blocks
    records, pictures, speech_count, choice = [], [], 0, None
    for group in stored["groups"]:
        path, number = group["file_path"], group["block"]
        assert path == "/data/SC1.DK4" and native.digest(bank[number]) == group["after"]
        for command in group["commands"]:
            original, compiled = [bytes.fromhex(command[key]) for key in ("current", "stored")]
            at = command["stored_offset"]
            assert bank[number][at:at+len(compiled)] == compiled
            owned = [rows.pop(ident) for ident in command["record_ids"]]
            if command["word"] == 0x2100:
                assert choice is None
                choice = check_menu(ctx.arm, command, owned)
            for row in owned:
                ident = row["id"]
                note = dict(id=ident, file_path=path, block=number, decision=row["decision"],
                            stored_offset=at, stored_command_hex=compiled.hex())
                if command["word"] == 0x2100:
                    note.update(native_pages=0, native_caption=True)
                elif row["decision"] == "retention":
                    assert original == compiled
                else:
                    assert original[:6] == compiled[:6] == b"\0\x40\xff\xff\0" + bytes([row["source_selector"]])
                    last = compiled.index(0, 6)
                    assert not any(compiled[last:])
                    plan = group["plans"][ident]
                    checked = audit(ctx, font, paint, expand, None, NAMES, row, compiled[5:last], plan)
                    output = []
                    for layout in checked["layouts"]:
                        page_hashes = []
                        for index, page in enumerate(layout["pages"], 1):
                            assert page["native_independent_plane_equal"]
                            pixels = bytes.fromhex(page["native_plane_hex"])
                            page_hashes.append(native.digest(pixels))
                            pictures.append((f"{ident} {layout['scope']} p{index}", pixels))
                        output.append(dict(scope=layout["scope"], expanded_hex=layout["expanded_hex"], pages=page_hashes))
                    note.update(layouts=output, native_pages=plan["expected_native_pages"],
                                original_expansion=checked["macro_alignment_checks"])
                    speech_count += plan["expected_native_pages"]
                records.append(note)
    assert len(records) == 48 and not rows and choice is not None
    sheets = FunctionType(display.display.inherited.early.contact_sheets.__code__,
                          display.display.inherited.early.contact_sheets.__globals__ | {"ROOT": ROOT})(pictures)
    base.save(PROOF, dict(candidate_sha256=candidate, stage_proof_sha256=base.digest(stage.PROOF), records=records,
                         newly_rendered_pages=speech_count, name_stress_pages=len(pictures)-speech_count,
                         native_caption_count=2, menu=choice, offline_native_only=True,
                         sheets=[*sheets, choice["sheet"]]))
    print(f"Verified {speech_count} revised pages, the substituted name, and both native menu captions.")


if __name__ == "__main__":
    main()
