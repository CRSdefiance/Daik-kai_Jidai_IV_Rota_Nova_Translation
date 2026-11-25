"""Verify changed dialogue and original menu and FE consumers in Rafael's follow-up scenes."""

from inspect import getsource
from types import SimpleNamespace

from PIL import Image, ImageDraw

from scripts import review_rafael_east_asia_nameplates_20261121 as labels
from scripts import stage_rafael_followup_encounters_20261121 as stage
from scripts import verify_rafael_gerhard_tutorial_20261121 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native, display, town = stage.base, stage.native, prior.display, prior.town
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
REFERENCE = stage.ROOT.with_name("staged_v1")
PATH = "/data/SC0.DK4"


def sheet(previews, prefix, width):
    sheets = []
    for first in range(0, len(previews), 12):
        subset = previews[first:first + 12]
        step = width * 2 + 12
        montage = Image.new("RGB", (step * 3, ((len(subset) + 2) // 3) * 150), "#273138")
        draw = ImageDraw.Draw(montage)
        for index, (label, mask) in enumerate(subset):
            left, top = (index % 3) * step + 4, (index // 3) * 150
            draw.text((left, top + 3), label, fill="white")
            ink = Image.frombytes("L", (width, 64), bytes(255 if pixel else 0 for pixel in mask))
            ink = ink.resize((width * 2, 128), Image.Resampling.NEAREST)
            montage.paste("#151711", (left, top + 19, left + width * 2, top + 147))
            montage.paste("#eee7cb", (left, top + 19), ink.point(lambda a: 255 - a))
        path = ROOT / f"{prefix}_{first // 12 + 1}.png"
        montage.save(path)
        sheets.append(dict(path=str(path), sha256=base.digest(path)))
    return sheets


def review_nameplates():
    notes = {r["actor_ID"]: r["localization_note"] for r in base.load(stage.review.NAMES)["records"]}
    source = checked_text(getsource(labels.main), {
        'selectors = {r["source_selector"] for r in review["records"]}':
            'selectors = {r["source_selector"] for r in review["records"] if r["kind"] == "progressive"}',
    })
    scope = vars(labels) | {"stage": stage, "display": SimpleNamespace(PROOF=PROOF, display=display),
                            "NOTES": notes, "PROOF": NAMES}
    exec(compile(source, __file__ + "::names", "exec"), scope)
    scope["main"]()


def verify():
    assert not PROOF.exists()
    stored, draft, receipt = map(base.load, (stage.PROOF, stage.OUTPUT, stage.parent.RELEASE))
    candidate = base.digest(stage.ROM)
    assert stored["candidate_sha256"] == candidate and stored["whole_parent_inverse"]
    assert stored["predecessor_sha256"] == receipt["candidate_sha256"] == base.digest(stage.parent.ROM)
    assert stored["manuscript_sha256"] == base.digest(stage.OUTPUT)
    dependency = base.load(stage.parent.display.PROOF)["initialized_dependencies"]
    assert all(base.digest(dependency[key]) == dependency[key + "_sha256"] for key in ("release_proof", "startup_proof"))
    ctx = native.RegisteredRuntime(dependency["release_proof"], dependency["startup_proof"], captain=0)
    image = base.NdsImage.open(stage.ROM)
    assert all(ctx.image.read_file(path) == image.read_file(path) for path in display.ASSETS)
    prior_stage = REFERENCE / stage.PROOF.name
    prior_rom = REFERENCE / stage.ROM.name
    reference, reference_stage = map(base.load, (REFERENCE / "native_display/native_display.json", prior_stage))
    assert reference["candidate_sha256"] == reference_stage["candidate_sha256"] == base.digest(prior_rom)
    assert reference["stage_proof_sha256"] == base.digest(prior_stage)
    assert reference_stage["predecessor_sha256"] == stored["predecessor_sha256"]
    predecessor = base.NdsImage.open(prior_rom)
    assert all(predecessor.read_file(path) == image.read_file(path) for path in display.ASSETS)
    assert all(base.digest(s["path"]) == s["sha256"] for s in reference["sheets"])
    prior_rows = {r["id"]: r for r in reference["records"]}
    prior_menus = {m["block"]: m for m in reference["menus"]}
    prior_plans = {k: v for group in reference_stage["groups"] for k, v in group["plans"].items()}
    prior_pagination = {r["id"]: r for r in reference["pagination_changes"]}
    arm, font = [image.read_file(path) for path in (native.ARM, "/GRP/KANJI.FNT")]
    paint, expand = display.clipped_renderer(ctx), display.original_expander()
    expanded, = {case["output_hex"] for case in ctx.execute(expand, b"FI FA FO", 0)["cases"]}
    names = dict(zip(("FI", "FA", "FO"), bytes.fromhex(expanded).decode("ascii").split(" ", 2), strict=True))
    assert names == {"FI": "Rafael", "FA": "Castor", "FO": "Castor Co."}
    audit = prior.precedent.name_audit()
    fe = town.current_fe_painter(SimpleNamespace(arm=arm, image=image))
    rows = {row["id"]: row for row in draft["records"]}
    bank = native.IlnkContainer.parse(image.read_file(PATH)).blocks
    records, ordinary, system, menus, reclaim, reused = [], [], [], [], [], []
    revised = alternate = 0
    fe_count = 0
    ROOT.mkdir(exist_ok=True)
    for block in stored["groups"]:
        n = block["block"]
        assert block["file_path"] == PATH and native.digest(bank[n]) == block["after"]
        for command in block["commands"]:
            at = command["stored_offset"]
            old, raw, source = [bytes.fromhex(command[key]) for key in ("current", "stored", "source")]
            assert bank[n][at:at + len(raw)] == raw
            if not command["record_ids"]:
                continue
            members = [rows.pop(ident) for ident in command["record_ids"]]
            if members[0]["source_selector"] is None:
                assert old == raw
                earlier = prior_rows[members[0]["id"]]["stored_pages"][0]
                assert all(earlier[key] == command[key] for key in ("source", "current", "stored", "record_ids"))
                menus.append(prior_menus[n] | {"stored_command_offset": at})
                records.extend(dict(id=r["id"], block=n, decision=r["decision"], stored_pages=[command]) for r in members)
                continue
            row, = members
            ident, selector = row["id"], row["source_selector"]
            end = raw.index(0, 6)
            assert raw[:6] == old[:6] == source[:6] == bytes.fromhex("0040ffff00") + bytes([selector])
            assert not any(raw[end:]) and len(raw) % 2 == 0
            entry = dict(id=ident, block=n, decision=row["decision"], stored_pages=[command])
            records.append(entry)
            body, plan = raw[6:end], block["plans"].get(ident)
            if row["decision"] == "retention":
                assert raw == old and plan is None and raw[5:end].hex() == row["current_hex"]
            else:
                assert raw != old and plan == draft["plans"][ident]
            earlier = prior_rows[ident]
            if earlier["stored_pages"][0]["stored"] == command["stored"] and prior_plans.get(ident) == plan:
                entry.update(earlier | {"stored_pages": [command]})
                reused.append(ident)
                fe_count += selector == 254
                if plan:
                    count = plan["expected_native_pages"]
                    revised += count
                    alternate += (len(entry["layouts"]) - 1) * count
                    if ident in prior_pagination:
                        reclaim.append(prior_pagination[ident])
                continue
            if selector == 254:
                fe_count += 1
                expected = stage.review.TOKEN.sub(lambda m: names[m[0]], body.decode("ascii")).encode("ascii")
                if expected != body:
                    cases = ctx.execute(expand, body, 0)["cases"]
                    assert {case["output_hex"] for case in cases} == {expected.hex()}
                view = fe(expected)
                assert view["complete_consumed_bytes"] == len(expected)
                rows_fit = prior.check_FE_rows(expected, view)
                plane = view["physical"]
                assert len(plane) == 228 * 64
                entry["system"] = [dict(expanded_hex=expected.hex(), row_proof=rows_fit, plane_sha256=native.digest(plane))]
                system.append((ident, plane))
            if not plan:
                continue
            assert stage.review.logical(body.decode("ascii")) == row["english"]
            count = plan["expected_native_pages"]
            if stage.review.TOKEN.findall(row["english"]):
                check = audit(ctx, font, paint, expand, None, names, row, raw[5:end], plan)
                layouts = check["layouts"]
                entry["original_expansion"] = check["macro_alignment_checks"]
            else:
                pages = display.display.raster(ctx, font, paint, body, plan["lines"], count)
                layouts = [dict(scope="registered default", expanded_hex=body.hex(), lines=plan["lines"], pages=pages)]
                previous = old[6:old.index(0, 6)]
                if previous.count(10) >= 4 or count > 1:
                    old_count = len(paint(arm, font, previous)["pages"])
                    if old_count != count:
                        reclaim.append(dict(id=ident, previous_pages=old_count, current_pages=count))
            entry["layouts"] = []
            for layout in layouts:
                hashes = []
                assert len(layout["pages"]) == count
                for index, page in enumerate(layout["pages"], 1):
                    assert page["native_independent_plane_equal"] and page["all_bitmap_header_input_canaries_exact"]
                    plane = bytes.fromhex(page["native_plane_hex"])
                    ordinary.append((f"{ident} {layout['scope']} {index}/{count}", plane))
                    hashes.append(native.digest(plane))
                entry["layouts"].append(dict(scope=layout["scope"], expanded_hex=layout["expanded_hex"],
                                             lines=layout["lines"], page_sha256=hashes))
            revised += count
            alternate += (len(layouts) - 1) * count
    assert not rows and len(records) == 261 and len(menus) == 3 and fe_count == 7
    sheets = reference["sheets"] + sheet(ordinary, "refined_speech", 216) + sheet(system, "refined_speakerless", 228)
    base.save(PROOF, dict(candidate_sha256=candidate, stage_proof_sha256=base.digest(stage.PROOF), records=records,
        revised_speech_pages=revised, alternate_name_width_pages=alternate, FE_panels=fe_count, menus=menus,
        sheets=sheets, pagination_changes=reclaim, default_names=names, initialized_dependencies=ctx.receipt(),
        previous_native_proof=str(REFERENCE / "native_display/native_display.json"), reused_record_ids=reused,
        runtime_assets=list(display.ASSETS), offline_native_only=True))
    print(f"Verified {revised} revised speech pages, {alternate} alternate-name layouts and {fe_count} FE panels.")
    review_nameplates()


if __name__ == "__main__":
    verify()

