"""Check the stored dialogue, native layouts, substitutions and typed choices."""

from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import stage_rafael_palace_and_alliance_20261121 as first
from scripts import stage_rafael_palace_and_alliance_v2_20261121 as stage
from scripts import verify_rafael_gerhard_tutorial_20261121 as tutorial
from scripts import verify_rafael_ruins_and_proof_20261121 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


base, native, display, town = stage.base, stage.native, precedent.display, precedent.town
PATH = precedent.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"


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
    reference = first.ROOT / "native_display/native_display.json"
    earlier, earlier_stage = map(base.load, (reference, first.PROOF))
    first_image = base.NdsImage.open(first.ROM)
    assert earlier["candidate_sha256"] == earlier_stage["candidate_sha256"] == base.digest(first.ROM)
    assert earlier["stage_proof_sha256"] == base.digest(first.PROOF)
    assert earlier_stage["predecessor_sha256"] == stored["predecessor_sha256"]
    assert all(first_image.read_file(p) == image.read_file(p) for p in display.ASSETS)
    assert all(base.digest(sheet["path"]) == sheet["sha256"] for sheet in earlier["sheets"])
    older_rows = {r["id"]: r for r in earlier["records"]}
    older_menus = {m["block"]: m for m in earlier["menus"]}
    older_plans = {k: v for g in earlier_stage["groups"] for k, v in g["plans"].items()}
    older_pagination = {r["id"]: r for r in earlier["pagination_changes"]}
    arm, font = [image.read_file(p) for p in (native.ARM, "/GRP/KANJI.FNT")]
    paint, expand = display.clipped_renderer(ctx), display.original_expander()
    fe = town.current_fe_painter(SimpleNamespace(arm=arm, image=image))
    names = {"FI": "Rafael", "FA": "Castor", "FO": "Castor Co.", "FU": "Rafael Castor"}
    expanded, = {case["output_hex"] for case in ctx.execute(expand, b"FI FA FO FU", 0)["cases"]}
    assert bytes.fromhex(expanded).decode("ascii") == " ".join(names.values())
    audit = FunctionType(stage.parent.display.audit_company_name.__code__,
                         stage.parent.display.audit_company_name.__globals__ | {"stage": stage})()
    menu_adapters = tutorial.menu.adapters(arm)
    check_menu = FunctionType(tutorial.verify_menu.__code__, tutorial.verify_menu.__globals__ | {"ROOT": ROOT})
    make_sheets = FunctionType(precedent.prior.sheet.__code__, precedent.prior.sheet.__globals__ | {"ROOT": ROOT})
    rows = {r["id"]: r for r in draft["records"]}
    bank = native.IlnkContainer.parse(image.read_file(PATH)).blocks
    entries, ordinary, system, menus, reclaimed, retained_fu = [], [], [], [], [], []
    reused, replaced = [], []
    revised_pages = alternates = fe_count = 0
    ROOT.mkdir(exist_ok=True)
    for group in stored["groups"]:
        block = group["block"]
        assert group["file_path"] == PATH and native.digest(bank[block]) == group["after"]
        originals = {c["source_offset"]: dict(offset=c["source_offset"], whole_command_hex=c["source"])
                     for c in group["commands"]}
        for command in group["commands"]:
            at = command["stored_offset"]
            raw, old, source = [bytes.fromhex(command[k]) for k in ("stored", "current", "source")]
            assert bank[block][at:at + len(raw)] == raw
            if not command["record_ids"]:
                continue
            members = [rows.pop(key) for key in command["record_ids"]]
            if members[0]["source_selector"] is None:
                reference_cmd, = older_rows[members[0]["id"]]["stored_pages"]
                if all(command[k] == reference_cmd[k] for k in ("source", "current", "stored", "record_ids")):
                    menu = older_menus[block] | {"stored_command_offset": at}
                    reused.extend(command["record_ids"])
                else:
                    menu = check_menu(arm, originals, command, members, menu_adapters)
                menus.append(menu | {"block": block})
                entries.extend(dict(id=r["id"], block=block, stored_pages=[command]) for r in members)
                continue
            (row, offset, jp, previous, body), = precedent.parts(source, old, raw, members)
            ident, selector = row["id"], row["source_selector"]
            prefix = bytes([selector])
            assert (prefix + jp).hex() == row["source_hex"] and (prefix + previous).hex() == row["current_hex"]
            entry = dict(id=ident, block=block, stored_pages=[command], body_offset=at + offset,
                         body_hex=(prefix + body).hex(), style_slots=[])
            entries.append(entry)
            plan = group["plans"].get(ident)
            if row["decision"] == "retention":
                assert previous == body and not plan
            else:
                assert plan and (selector == 254 or plan == draft["plans"][ident])
            assert stage.review.logical(body.decode("ascii")) == row["english"]
            tokens = stage.review.TOKEN.findall(row["english"])
            old_entry = older_rows[ident]
            fe_count += selector == 254
            if old_entry["body_hex"] == entry["body_hex"] and older_plans.get(ident) == plan:
                entry.update(old_entry | entry)
                reused.append(ident)
                if tokens == ["FU"]:
                    retained_fu.append(ident)
                if plan:
                    revised_pages += plan["expected_native_pages"]
                    alternates += max(0, len(entry.get("layouts", [])) - 1) * plan["expected_native_pages"]
                    if ident in older_pagination:
                        reclaimed.append(older_pagination[ident])
                continue
            replaced.append(ident)
            if selector == 254:
                assert not stage.review.TOKEN.findall(row["english"])
                view = fe(body)
                assert view["complete_consumed_bytes"] == len(body)
                fitted = tutorial.check_FE_rows(body, view)
                if plan:
                    assert fitted["actual_rows"] == plan["lines"] and plan["expected_native_pages"] == 1
                plane = view["physical"]
                assert len(plane) == 228 * 64
                system.append((ident, plane))
                entry["system"] = [dict(expanded_hex=body.hex(), row_proof=fitted, plane_sha256=native.digest(plane))]
                revised_pages += bool(plan)
                continue
            if plan and tokens:
                result = audit(ctx, font, paint, expand, None, names, row, prefix + body, plan)
                layouts = result["layouts"]
                entry["original_expansion"] = result["macro_alignment_checks"]
            elif plan:
                count = plan["expected_native_pages"]
                pages = display.display.raster(ctx, font, paint, body, plan["lines"], count)
                layouts = [dict(scope="registered default", expanded_hex=body.hex(), lines=plan["lines"], pages=pages)]
                if previous.count(10) >= 4 or count > 1:
                    old_count = len(paint(arm, font, previous)["pages"])
                    if old_count != count:
                        reclaimed.append(dict(id=ident, previous_pages=old_count, current_pages=count))
            elif tokens == ["FU"]:
                result = ctx.execute(expand, body, selector)
                expected = body.replace(b"FU", names["FU"].encode("ascii"))
                assert {case["output_hex"] for case in result["cases"]} == {expected.hex()}
                lines = [line.strip().decode("ascii") for line in expected.splitlines()]
                pages = display.display.raster(ctx, font, paint, expected, lines, 1)
                layouts = [dict(scope="retained full-name substitution", expanded_hex=expected.hex(), lines=lines, pages=pages)]
                entry["original_expansion"] = result
                retained_fu.append(ident)
            else:
                continue
            entry["layouts"] = []
            count = plan["expected_native_pages"] if plan else 1
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
            revised_pages += count if plan else 0
            alternates += (len(layouts) - 1) * count
    assert not rows and len(entries) == 270 and fe_count == 6
    assert [m["block"] for m in menus] == [143, 146, 148] and all(m["count"] == 2 for m in menus)
    assert retained_fu == ["DK4_MES_B143_R0067", "DK4_MES_B146_R0006"]
    fresh_sheets = make_sheets(ordinary, "refined_palace_speech", 216) + make_sheets(system, "refined_palace_speakerless", 228)
    seen = {s["path"] for s in earlier["sheets"]}
    fresh_sheets.extend(m["sheet"] for m in menus if m["sheet"]["path"] not in seen)
    sheets = earlier["sheets"] + fresh_sheets
    base.save(PROOF, dict(candidate_sha256=candidate, stage_proof_sha256=base.digest(stage.PROOF), records=entries,
        revised_speech_pages=revised_pages, alternate_name_width_pages=alternates, FE_panels=fe_count, menus=menus,
        style_objects=[], sheets=sheets, pagination_changes=reclaimed, default_names=names,
        previous_native_proof=str(reference), reused_record_ids=reused, replaced_preview_ids=replaced, fresh_sheets=fresh_sheets,
        full_name_retention_cases=retained_fu, initialized_dependencies=ctx.receipt(),
        runtime_assets=list(display.ASSETS), offline_native_only=True))
    print(f"Verified {revised_pages} revised pages, six speakerless notices, six captions and two retained full-name substitutions.")


def verify_names():
    selectors = {r["source_selector"] for r in base.load(stage.OUTPUT)["records"] if r["kind"] == "progressive"}
    notes = {r["actor_ID"]: r["localization_note"] for r in base.load(stage.review.NAMES)["records"] if r["actor_ID"] in selectors}
    labels = precedent.prior.labels
    source = checked_text(getsource(labels.main), {
        'selectors = {r["source_selector"] for r in review["records"]}':
            'selectors = {r["source_selector"] for r in review["records"] if r["kind"] == "progressive"}',
    })
    scope = vars(labels) | {"stage": stage, "display": SimpleNamespace(PROOF=PROOF, display=display),
                            "NOTES": notes, "PROOF": NAMES}
    exec(compile(source, __file__ + "::names", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
    verify_names()
