"""Verify final stored text, speakerless pages, choice menus and companion style aliases."""

from inspect import getsource
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.reviewed_actor_style_object_v1 import unpack
from scripts import stage_rafael_ruins_and_proof_20261121 as stage
from scripts import verify_rafael_followup_encounters_20261121 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native, display, town = stage.base, stage.native, prior.display, prior.town
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
REFERENCE = stage.ROOT.with_name("staged_v2")
PATH = "/data/SC0.DK4"


def verify_names():
    notes = {r["actor_ID"]: r["localization_note"] for r in base.load(stage.review.NAMES)["records"]}
    notes[135] = ("Officiant is the registered role for the guardian of the Vishnu temple. The original short "
                  "name and this exchange give no particular priestly rank.")
    code = checked_text(getsource(prior.labels.main), {
        'selectors = {r["source_selector"] for r in review["records"]}':
            'selectors = {r["source_selector"] for r in review["records"] if r["kind"] == "progressive" '
            'and r["source_selector"] not in (207, 208)}',
    })
    scope = vars(prior.labels) | {"stage": stage, "display": SimpleNamespace(PROOF=PROOF, display=display),
                                 "NOTES": notes, "PROOF": NAMES}
    exec(compile(code, __file__ + "::names", "exec"), scope)
    scope["main"]()


def parts(source, current, target, rows):
    if rows[0]["native_command_word"] != 0x4100:
        row, = rows
        assert target[:6] == current[:6] == source[:6] == bytes.fromhex("0040ffff00") + bytes([row["source_selector"]])
        values = []
        for command in (source, current, target):
            end = command.index(0, 6)
            assert len(command) % 2 == 0 and not any(command[end:])
            values.append(command[6:end])
        return [(row, 5, *values)]
    assert target[18:20] == current[18:20] == source[18:20] == b"\0\xd0"
    source_slots, source_bodies = unpack(source)
    old_slots, old_bodies = unpack(current)
    new_slots, new_bodies = unpack(target)
    assert len(source_bodies) == len(old_bodies) == len(new_bodies) == len(rows)
    bodies = []
    for row in rows:
        i = row["native_slots"][0]
        for offsets in (source_slots, old_slots, new_slots):
            assert [slot for slot, at in enumerate(offsets) if at == offsets[i]] == row["native_slots"]
        bodies.append((row, 20 + new_slots[i], source_bodies[source_slots[i]], old_bodies[old_slots[i]], new_bodies[new_slots[i]]))
    return bodies


def main():
    assert not PROOF.exists()
    stored, draft, release = map(base.load, (stage.PROOF, stage.OUTPUT, stage.parent.RELEASE))
    candidate = base.digest(stage.ROM)
    assert stored["candidate_sha256"] == candidate and stored["whole_parent_inverse"]
    assert stored["predecessor_sha256"] == release["candidate_sha256"] == base.digest(stage.parent.ROM)
    assert stored["manuscript_sha256"] == base.digest(stage.OUTPUT)
    dependency = base.load(stage.parent.display.PROOF)["initialized_dependencies"]
    assert all(base.digest(dependency[k]) == dependency[k + "_sha256"] for k in ("release_proof", "startup_proof"))
    ctx = native.RegisteredRuntime(dependency["release_proof"], dependency["startup_proof"], captain=0)
    image = base.NdsImage.open(stage.ROM)
    assert all(ctx.image.read_file(p) == image.read_file(p) for p in display.ASSETS)
    previous_stage = REFERENCE / stage.PROOF.name
    previous_native = REFERENCE / "native_display/native_display.json"
    previous_rom = REFERENCE / stage.ROM.name
    before, viewed = map(base.load, (previous_stage, previous_native))
    assert before["candidate_sha256"] == viewed["candidate_sha256"] == base.digest(previous_rom)
    assert before["predecessor_sha256"] == stored["predecessor_sha256"]
    assert viewed["stage_proof_sha256"] == base.digest(previous_stage)
    precedent_image = base.NdsImage.open(previous_rom)
    assert all(precedent_image.read_file(p) == image.read_file(p) for p in display.ASSETS)
    assert all(base.digest(s["path"]) == s["sha256"] for s in viewed["sheets"])
    earlier = {row["id"]: row for row in viewed["records"]}
    earlier_menus = {(row["block"], row["source_command_offset"]): row for row in viewed["menus"]}
    earlier_plans = {k: v for group in before["groups"] for k, v in group["plans"].items()}
    earlier_pagination = {row["id"]: row for row in viewed["pagination_changes"]}
    arm, font = [image.read_file(p) for p in (native.ARM, "/GRP/KANJI.FNT")]
    paint, expand = display.clipped_renderer(ctx), display.original_expander()
    fe = town.current_fe_painter(SimpleNamespace(arm=arm, image=image))
    names = {"FI": "Rafael", "FA": "Castor", "FO": "Castor Co."}
    expanded, = {case["output_hex"] for case in ctx.execute(expand, b"FI FA FO", 0)["cases"]}
    assert bytes.fromhex(expanded).decode("ascii") == " ".join(names.values())
    audits = prior.prior.precedent.name_audit()
    make_sheets = FunctionType(prior.sheet.__code__, prior.sheet.__globals__ | {"ROOT": ROOT})
    rows = {r["id"]: r for r in draft["records"]}
    bank = native.IlnkContainer.parse(image.read_file(PATH)).blocks
    entries, ordinary, system, menus, reclaimed, style_objects = [], [], [], [], [], []
    revised_pages = alternates = fe_count = 0
    reused = []
    ROOT.mkdir(exist_ok=True)
    for group in stored["groups"]:
        block = group["block"]
        assert group["file_path"] == PATH and native.digest(bank[block]) == group["after"]
        for command in group["commands"]:
            at = command["stored_offset"]
            raw, old, source = [bytes.fromhex(command[k]) for k in ("stored", "current", "source")]
            assert bank[block][at:at + len(raw)] == raw
            if not command["record_ids"]:
                continue
            members = [rows.pop(key) for key in command["record_ids"]]
            if members[0]["source_selector"] is None:
                reference = earlier[members[0]["id"]]["stored_pages"][0]
                assert all(reference[key] == command[key] for key in ("source", "current", "stored", "record_ids"))
                menu = earlier_menus[block, command["source_offset"]]
                menus.append(menu | {"stored_command_offset": at})
                entries.extend(dict(id=row["id"], block=block, stored_pages=[command]) for row in members)
                continue
            style = command["word"] == 0x4100
            if style:
                style_objects.append(dict(block=block, source_offset=command["source_offset"], current_offset=at,
                                          slot_owner_sets=[row["native_slots"] for row in members]))
            for row, offset, jp, previous, body in parts(source, old, raw, members):
                ident, selector = row["id"], row["source_selector"]
                prefix = b"" if style else bytes([selector])
                assert (prefix + jp).hex() == row["source_hex"] and (prefix + previous).hex() == row["current_hex"]
                entry = dict(id=ident, block=block, stored_pages=[command], body_offset=at + offset,
                             body_hex=(prefix + body).hex(), style_slots=row["native_slots"] if style else [])
                entries.append(entry)
                plan = group["plans"].get(ident)
                if row["decision"] == "retention":
                    assert previous == body
                    plan = None
                else:
                    assert plan is not None
                    if selector != 254:
                        assert plan == draft["plans"][ident]
                logical = stage.review.logical
                assert logical(body.decode("ascii")) == row["english"]
                previous_entry = earlier[ident]
                previous_plan = earlier_plans.get(ident) if row["decision"] == "revision" else None
                if previous_entry["body_hex"] == entry["body_hex"] and previous_plan == plan:
                    entry.update(previous_entry | entry)
                    reused.append(ident)
                    fe_count += selector == 254
                    if plan:
                        revised_pages += plan["expected_native_pages"]
                        alternates += max(0, len(entry.get("layouts", [])) - 1) * plan["expected_native_pages"]
                        if ident in earlier_pagination:
                            reclaimed.append(earlier_pagination[ident])
                    continue
                if selector == 254:
                    fe_count += 1
                    assert not stage.review.TOKEN.findall(row["english"])
                    view = fe(body)
                    assert view["complete_consumed_bytes"] == len(body)
                    rows_fit = prior.prior.check_FE_rows(body, view)
                    plane = view["physical"]
                    assert len(plane) == 228 * 64
                    if plan:
                        assert rows_fit["actual_rows"] == plan["lines"] and plan["expected_native_pages"] == 1
                        assert b"\xfe" + body in (bytes.fromhex(plan["encoded_hex"]), bytes.fromhex(plan["encoded_hex"]) + b" ")
                    system.append((ident, plane))
                    entry["system"] = [dict(expanded_hex=body.hex(), row_proof=rows_fit, plane_sha256=native.digest(plane))]
                    revised_pages += bool(plan)
                    continue
                if not plan:
                    continue
                count = plan["expected_native_pages"]
                if stage.review.TOKEN.findall(row["english"]):
                    result = audits(ctx, font, paint, expand, None, names, row, bytes([selector]) + body, plan)
                    layouts = result["layouts"]
                    entry["original_expansion"] = result["macro_alignment_checks"]
                else:
                    pages = display.display.raster(ctx, font, paint, body, plan["lines"], count)
                    layouts = [dict(scope="registered default", expanded_hex=body.hex(), lines=plan["lines"], pages=pages)]
                    if previous.count(10) >= 4 or count > 1:
                        old_count = len(paint(arm, font, previous)["pages"])
                        if old_count != count:
                            reclaimed.append(dict(id=ident, previous_pages=old_count, current_pages=count))
                entry["layouts"] = []
                for layout in layouts:
                    hashes = []
                    assert len(layout["pages"]) == count
                    for number, page in enumerate(layout["pages"], 1):
                        assert page["native_independent_plane_equal"] and page["all_bitmap_header_input_canaries_exact"]
                        plane = bytes.fromhex(page["native_plane_hex"])
                        ordinary.append((f"{ident} {layout['scope']} {number}/{count}", plane))
                        hashes.append(native.digest(plane))
                    entry["layouts"].append(dict(scope=layout["scope"], expanded_hex=layout["expanded_hex"],
                                                 lines=layout["lines"], page_sha256=hashes))
                revised_pages += count
                alternates += (len(layouts) - 1) * count
    assert len(entries) == 255 and not rows and len(menus) == 4 and fe_count == 22 and len(style_objects) == 2
    sheets = viewed["sheets"] + make_sheets(ordinary, "final_speech", 216) + make_sheets(system, "final_speakerless", 228)
    base.save(PROOF, dict(candidate_sha256=candidate, stage_proof_sha256=base.digest(stage.PROOF), records=entries,
        revised_speech_pages=revised_pages, alternate_name_width_pages=alternates, FE_panels=fe_count, menus=menus,
        style_objects=style_objects, sheets=sheets, pagination_changes=reclaimed, default_names=names,
        previous_native_proof=str(previous_native), reused_record_ids=reused,
        initialized_dependencies=ctx.receipt(), runtime_assets=list(display.ASSETS), offline_native_only=True))
    print(f"Verified {revised_pages} revised pages, all {fe_count} FE panels, 12 captions and both companion objects.")
    verify_names()


if __name__ == "__main__":
    main()

