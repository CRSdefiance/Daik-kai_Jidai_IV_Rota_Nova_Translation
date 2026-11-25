"""Check every selected phrase and bound the four inherited speech allocations."""

from inspect import getsource
from types import FunctionType

from scripts import generic_name_macro_owned_v5886b as macro
from scripts import stage_story_phrase_continuity_20261118 as build
from scripts import verify_late_trade_exchanges_20261118 as routes
from scripts import verify_london_guild_assignments_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native = build.base, build.native
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"


def hodram_context():
    report = base.load(build.ROOT / "hodram_snapshot/capture_report.json")
    snapshot, = report["read_only_capture_RAM_snapshots"]
    candidate = base.digest(build.ROM)
    assert report["ROM_sha256"] == candidate == base.digest(build.ROOT / "clean_rebuilt.nds")
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["scripted_input_schedule"] == base.load(build.ROOT / "hodram_snapshot_inputs.json")
    boot = build.ROOT / "hodram_native_context.json"
    identity = build.ROOT / "hodram_native_ROM_identity.json"
    base.save(boot, dict(candidate_sha256=candidate, cold_boot=True, savestate=False, actual_captain_getter=1,
                        read_only_snapshot=snapshot))
    base.save(identity, dict(candidate=str(build.ROM), candidate_sha256=candidate, native_audit_only=True,
                            own_registered_startup_pending=False, clean_input_patch_byte_exact=True))
    return native.RegisteredRuntime(identity, boot, captain=1)


def main():
    assert not ROOT.exists()
    stored, draft, parent = map(base.load, (build.PROOF, build.review.OUTPUT, build.parent.RELEASE))
    assert stored["candidate_sha256"] == base.digest(build.ROM)
    assert stored["predecessor_sha256"] == parent["candidate_sha256"] == base.digest(build.parent.ROM)
    assert stored["whole_parent_inverse"] and stored["manuscript_sha256"] == base.digest(build.review.OUTPUT)
    image = base.NdsImage.open(build.ROM)
    maria = native.RegisteredRuntime(build.parent.RELEASE, parent["own_registered_startup"], captain=3)
    contexts = {1: hodram_context(), 2: routes.lil_context(), 3: maria}
    assets = (native.ARM, "/COMMON/MESFILE.DK4", "/GRP/KANJI.FNT")
    assert all(ctx.image.read_file(path) == image.read_file(path) for path in assets for ctx in contexts.values())
    namespace = vars(macro).copy()
    source = checked_text(getsource(macro.expand), {
        "assert identity==prefix and captain==2": "assert identity == prefix and captain in (1, 2, 3)",
    })
    exec(compile(source, __file__ + "::original-name-wrapper", "exec"), namespace)
    expand = namespace["expand"]
    expanded = contexts[1].execute(expand, b"FI", 1)
    assert {bytes.fromhex(case["output_hex"]) for case in expanded["cases"]} == {b"Hodram"}
    names = {1: {"FI": "Hodram"}, 2: routes.current_names(contexts[2]), 3: display.current_names(maria)}

    font = image.read_file(assets[2])
    _, paint = display.inherited.early.prior.precedent.planners(maria.arm)
    paragraph = FunctionType(display.paragraph.__code__, vars(display) | {"build": build})
    rows = {(row["file_path"], row["id"]): row for row in draft["records"]}
    modified, retained, pictures, pagination = [], [], [], {}
    for group in stored["groups"]:
        route, path, n = (group[k] for k in ("route", "file_path", "block"))
        block = native.IlnkContainer.parse(image.read_file(path)).blocks[n]
        assert native.digest(block) == group["after"]
        for cmd in group["commands"]:
            if not cmd["record_ids"]:
                continue
            ident, = cmd["record_ids"]
            row = rows[path, ident]
            raw, pos = bytes.fromhex(cmd["stored"]), cmd["stored_offset"]
            assert cmd["word"] == 0x4000 and block[pos:pos + len(raw)] == raw
            value = raw[5:raw.index(0, 6)]
            assert value[0] == row["source_selector"] < 207
            if row["decision"] == "retention":
                assert cmd["stored"] == cmd["current"] and value.hex() == row["current_hex"]
                assert not build.review.TOKEN.search(row["english"])
                surface = paint(maria.arm, font, value[1:])
                assert surface["complete_consumed_bytes"] == len(value) - 1
                pages = surface["pages"]
                assert len(pages) == 1 and pages[0]["first_visible_origin"] == [0, 0]
                retained.append(dict(id=ident, file_path=path, stored_hex=value.hex(), pages=pages))
                for page in pages:
                    pictures.append((f"SC{route} {ident} unchanged", bytes.fromhex(page["native_plane_hex"])))
                continue
            if route == 0:
                assert not build.review.TOKEN.search(row["english"])
            result = paragraph(contexts.get(route, maria), font, paint, expand, None, names.get(route, {}), row,
                               value, group["plans"][ident])
            modified.append(result)
            for layout in result["layouts"]:
                for page in layout["pages"]:
                    pictures.append((f"SC{route} {ident} {layout['scope']}", bytes.fromhex(page["native_plane_hex"])))
            if ident == "DK4_MES_B143_R0380":
                old = bytes.fromhex(cmd["current"])
                before = paint(maria.arm, font, old[6:old.index(0, 6)])
                pagination[ident] = [len(before["pages"]), len(result["layouts"][0]["pages"])]
                assert pagination[ident] == [2, 1]
    assert {(r["file_path"], r["id"]) for r in modified + retained} == rows.keys()
    assert len(modified) == 27 and len(retained) == 4 and len(pictures) == 43 and len(pagination) == 1
    ROOT.mkdir()
    contact = display.inherited.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(pictures)
    base.save(PROOF, dict(candidate_sha256=stored["candidate_sha256"], stage_proof_sha256=base.digest(build.PROOF),
        native_runtime_assets_byte_identical=True, default_name_macros=names, renderer_assets=assets,
        revision_count=len(modified), fresh_page_count=39, retention_page_count=4, checked_records=modified,
        retained_records=retained, pagination_before_after=pagination, contact_sheets=sheets, actual_gameplay=False))
    print("Rendered 39 revised and stress-test pages, plus four exact retentions.")


if __name__ == "__main__":
    main()
