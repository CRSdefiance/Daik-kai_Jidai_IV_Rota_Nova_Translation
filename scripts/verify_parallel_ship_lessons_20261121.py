"""Check every revised Alexandria page and both copies of the typed menu."""
from types import FunctionType

from scripts import check_typed_story_menu_display_20261121 as menu
from scripts import stage_parallel_ship_lessons_20261121 as stage
from scripts import verify_all_routes_next_phrase_wraps_20261118 as display


base, native = stage.base, stage.native
ROOT = stage.ROOT / "native_display"
PROOF = ROOT / "native_display.json"


def verify_captions(arm, versions):
    source, old, new = versions
    assert [menu.labels(value) for value in (old, new)] == [[b"Yes", b"No"], [b"Listen", b"Skip"]]
    vms, paint, executed = menu.adapters(arm)
    checked = {}
    for name, obj in zip(("clean source", "predecessor", "revised"), versions, strict=True):
        first, second = [vms[2](arm, obj, align) for align in (0, 2)]
        assert first == second and [c["modal_selection"] for c in first["VM_cases"]] == [0, 1, -1]
        assert first["labels"] == [body.decode("cp932") for body in menu.labels(obj)]
        checked[name] = first
    width = checked["revised"]["minimum_width_units"] * 6
    pictures, styles = [], []
    for index, body in enumerate(menu.labels(new)):
        for style in (1, 15):
            pixels, audit = paint(arm, body, style, width, (0, index * 12))
            assert audit["independent_complete_native_pixels_match"] and audit["storage_padding_all_blank"]
            assert audit["visible_cell_center_twice"] == width and audit["extra_flush_stays_within_physical_backing"]
            styles.append(dict(label=body.decode("ascii"), style=style, audit=audit))
            if style == 1:
                pictures.append((body.decode("ascii"), width, pixels))
    path = ROOT / "cesare_lesson_choices.png"
    menu.sheet(pictures, path)
    return dict(versions=checked, styles=styles, executed_addresses=len(executed),
                sheet=dict(path=str(path), sha256=base.digest(path)))


def fresh_context(candidate, route):
    folder = stage.ROOT / f"route{route}_snapshot"
    report = base.load(folder / "capture/capture_report.json")
    assert report["ROM_sha256"] == candidate and report["frames"] == 4000
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["scripted_input_schedule"] == base.load(folder / "inputs.json")
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert base.digest(stage.ROOT / "clean_rebuilt.nds") == candidate
    identity, boot = folder / "candidate.json", folder / "startup.json"
    base.save(identity, dict(candidate=str(stage.ROM), candidate_sha256=candidate,
                            own_registered_startup_pending=False, clean_input_patch_byte_exact=True))
    base.save(boot, dict(candidate_sha256=candidate, cold_boot=True, savestate=False,
                        actual_captain_getter=route, read_only_snapshot=report["read_only_RAM_snapshot"]))
    return native.RegisteredRuntime(identity, boot, captain=route)


def main():
    assert not ROOT.exists()
    stored, draft, parent = map(base.load, (stage.PROOF, stage.review.OUTPUT, stage.parent.RELEASE))
    assert stored["candidate_sha256"] == base.digest(stage.ROM) and stored["whole_parent_inverse"]
    assert stored["manuscript_sha256"] == base.digest(stage.review.OUTPUT)
    assert stored["predecessor_sha256"] == parent["candidate_sha256"]
    image = base.NdsImage.open(stage.ROM)
    routes = {i: fresh_context(stored["candidate_sha256"], i) for i in (0, 2)}
    routes[3] = native.RegisteredRuntime(stage.parent.RELEASE, parent["own_registered_startup"], captain=3)
    assert all(ctx.image.read_file(path) == image.read_file(path) for ctx in routes.values() for path in display.ASSETS)
    expand = display.original_expander()
    names = {3: display.display.current_names(routes[3])}
    paint = display.clipped_renderer(routes[3])
    font = image.read_file("/GRP/KANJI.FNT")
    paragraph = display.display.paragraph
    audit = FunctionType(paragraph.__code__, paragraph.__globals__ | {"build": stage})
    rows = {(row["file_path"], row["id"]): row for row in draft["records"]}
    records, pictures, menu_routes, counts = [], [], [], {}
    menu_versions = None
    ROOT.mkdir()
    for group in stored["groups"]:
        route, path, n = (group[k] for k in ("route", "file_path", "block"))
        block = native.IlnkContainer.parse(image.read_file(path)).blocks[n]
        assert native.digest(block) == group["after"]
        counts[route] = 0
        for command in group["commands"]:
            source, old, new = (bytes.fromhex(command[k]) for k in ("source", "current", "stored"))
            at = command["stored_offset"]
            assert block[at:at+len(new)] == new
            if command["word"] == 0x2100:
                versions = (source, old, new)
                assert menu_versions is None or versions == menu_versions
                menu_versions = versions
                menu_routes.append(route)
            for ident in command["record_ids"]:
                row = rows.pop((path, ident))
                proof = dict(id=ident, route=route, file_path=path, block=n, decision=row["decision"],
                             stored_offset=at, stored_command_hex=new.hex())
                if row["decision"] == "retention":
                    assert new == old
                elif command["word"] == 0x2100:
                    assert row["english"].encode("ascii") in menu.labels(new)
                    proof.update(native_pages=0, native_caption=True)
                else:
                    assert old[:6] == new[:6] == b"\0\x40\xff\xff\0" + bytes([row["source_selector"]])
                    end = new.index(0, 6)
                    assert not any(new[end:])
                    plan = group["plans"][ident]
                    checked = audit(routes[route], font, paint, expand, None, names.get(route, {}), row, new[5:end], plan)
                    layouts = []
                    for layout in checked["layouts"]:
                        page_hashes = []
                        for index, page in enumerate(layout["pages"], 1):
                            assert page["native_independent_plane_equal"]
                            pixels = bytes.fromhex(page["native_plane_hex"])
                            page_hashes.append(native.digest(pixels))
                            pictures.append((f"SC{route} {ident} {layout['scope']} p{index}", pixels))
                        layouts.append(dict(scope=layout["scope"], expanded_hex=layout["expanded_hex"], pages=page_hashes,
                                            lines=layout["lines"]))
                    proof.update(native_pages=plan["expected_native_pages"], layouts=layouts,
                                 original_expansion=checked["macro_alignment_checks"])
                    counts[route] += plan["expected_native_pages"]
                records.append(proof)
    assert not rows and len(records) == 175 and menu_routes == [0, 2]
    caps = verify_captions(routes[3].arm, menu_versions)
    contact = display.display.inherited.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(pictures)
    speech = sum(counts.values())
    base.save(PROOF, dict(candidate_sha256=stored["candidate_sha256"], stage_proof_sha256=base.digest(stage.PROOF),
        records=records, newly_rendered_pages=speech, name_stress_pages=len(pictures)-speech, route_page_counts=counts,
        offline_native_only=True, native_caption_count=4, native_menu_count=2, exact_menu_routes=menu_routes,
        initialized_dependencies={str(i): c.receipt() for i, c in routes.items()},
        menu=caps, sheets=[*sheets, caps["sheet"]]))
    print(f"Verified {speech} revised native speech pages, both name substitutions and four captions.")


if __name__ == "__main__":
    main()
