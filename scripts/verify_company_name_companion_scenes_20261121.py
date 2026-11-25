"""Verify changed pages and observed excerpts without replaying the whole routes."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType

from PIL import Image, ImageDraw

from scripts import replay_company_name_companion_scenes_20261121 as replay
from scripts import replay_late_trade_exchanges_20261118 as live_template
from scripts import stage_company_name_companion_scenes_20261121 as stage
from scripts import verify_company_name_dialogue_20261121 as inherited
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_captain_biographies_v1 import captured, shots


base, native, prior = stage.base, stage.native, inherited.prior
ROOT = stage.EVIDENCE_ROOT / "verified"
OFFLINE, LIVE = ROOT / "offline.json", ROOT / "live.json"
FE_PRIOR = {
    0: Path("translations/rafael_B81_B84_contextual_final_review_v1.json"),
    3: Path("translations/maria330_integrated_final_review_v1.json"),
}


def runtime():
    before = stage.parent.parent
    context = inherited.contexts(base.load(before.RELEASE))
    image = base.NdsImage.open(stage.ROM)
    assert all(c.image.read_file(p) == image.read_file(p) for c in context.values() for p in inherited.ASSETS)
    expander = prior.original_expander()
    names = inherited.four_default_names(context, expander)
    source = checked_text(getsource(prior.display.paragraph), {
        "{macro: example for macro in tokens}":
            '{macro: example + " Co." if macro == "FO" and n == 16 else example for macro in tokens}',
    })
    # This verifier reads already reviewed logical dialogue.
    namespace = vars(prior.display) | {"build": inherited.build}
    exec(compile(source, __file__ + "::expanded-lines", "exec"), namespace)
    font = image.read_file("/GRP/KANJI.FNT")
    paint = prior.clipped_renderer(context[3])
    return image, context, expander, names, font, paint, namespace["paragraph"]


def offline():
    assert not OFFLINE.exists()
    draft, staged = map(base.load, (stage.REVIEW, stage.PROOF))
    assert base.digest(stage.ROM) == staged["candidate_sha256"] and base.digest(stage.REVIEW) == staged["manuscript_sha256"]
    assert staged["whole_parent_inverse"]
    image, contexts, expand, names, font, paint, run = runtime()
    arm = image.read_file(native.ARM)
    mixed = prior.prior.original_cp932_renderer(arm)
    historical = {route: {r["id"]: r for r in base.load(path)["records"]} for route, path in FE_PRIOR.items()}
    rows = {(r["path"], r["block"]): r for r in staged["groups"]}
    decisions, pages, evidence = [], [], {}
    for row in draft["records"]:
        route, path, block, ident = (row[k] for k in ("route", "file_path", "block", "id"))
        group = rows[path, block]
        stored = native.IlnkContainer.parse(image.read_file(path)).blocks[block]
        assert native.digest(stored) == group["after"]
        for snapshot in row["target_pages"]:
            pointer = snapshot["offset"]
            raw = bytes.fromhex(snapshot["exact_command_hex"])
            assert stored[pointer:pointer+len(raw)] == raw
        if row["decision"] == "retention":
            assert [p["exact_command_hex"] for p in row["target_pages"]] == [p["exact_command_hex"] for p in row["installed_pages"]]
            if row["source_selector"] == 254:
                former = historical[route][ident]
                refs = former.get("planned_integrated_native_pages", [former["planned_integrated_reference"]])
                assert former["review"]["formatting"]
                old = []
                for p in row["target_pages"]:
                    raw = bytes.fromhex(p["exact_command_hex"])
                    assert raw[:6] == bytes.fromhex("0040ffff00fe")
                    old.append(raw[5:raw.index(0, 6)].hex())
                assert old == [r["exact_stored_hex"] for r in refs], (ident, old, refs)
                path_ref = FE_PRIOR[route]
                evidence[str(path_ref)] = base.digest(path_ref)
                decisions.append(dict(id=ident, file_path=path, decision="retention", pages=len(old),
                    scope="Byte-identical FE controls and bodies paired to the earlier complete page proof."))
                continue
            raw = bytes.fromhex(row["target_pages"][0]["exact_command_hex"])
            body = prior.prior.default_text(raw[6:raw.index(0, 6)], names[route])
            result = (paint if body.isascii() else mixed)(arm, font, body)
            assert result["complete_consumed_bytes"] == len(body) and all(p["native_independent_plane_equal"] for p in result["pages"])
            decisions.append(dict(id=ident, file_path=path, decision="retention", pages=len(result["pages"]),
                scope="Byte-identical progressive body rendered with the original consumer."))
            continue
        assert len(row["target_pages"]) == 1
        raw = bytes.fromhex(row["target_pages"][0]["exact_command_hex"])
        value = raw[5:raw.index(0, 6)]
        plan = group["plans"][ident]
        result = run(contexts[route], font, paint, expand, None, names[route], row | {"kind": "progressive"}, value, plan)
        for layout in result["layouts"]:
            page, = layout["pages"]
            pages.append((f"{ident} {layout['scope']}", bytes.fromhex(page["native_plane_hex"])))
        existing = bytes.fromhex(row["current_reference"]["exact_command_hex"])
        old = prior.prior.default_text(existing[6:existing.index(0, 6)], names[route])
        counts = len(paint(arm, font, old)["pages"]), len(result["layouts"][0]["pages"])
        decisions.append(result | dict(decision="revision", old_new_page_count=counts,
            scope="Original progressive consumer, checked using default names and name-width stress."))
    assert len(decisions) == 74 and sum(r["decision"] == "revision" for r in decisions) == 3
    assert len(pages) == 6
    ROOT.mkdir(parents=True, exist_ok=True)
    contact = prior.display.inherited.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(pages)
    base.save(OFFLINE, dict(candidate_sha256=staged["candidate_sha256"], defaults=names,
        decisions=decisions, sheets=sheets, historical_FEs=evidence, newly_rendered_pages=len(pages),
        actual_gameplay=False))
    print("Three revisions and six native preview pages passed, with 71 justified retentions.")


def live():
    assert not LIVE.exists()
    proof = base.load(OFFLINE)
    candidate = base.digest(stage.ROM)
    assert proof["candidate_sha256"] == candidate
    names = proof["defaults"]
    image = base.NdsImage.open(stage.ROM)
    arm = image.read_file(native.ARM)
    font = image.read_file("/GRP/KANJI.FNT")
    dummy = type("Runtime", (), {"arm": arm})()
    paint = prior.clipped_renderer(dummy)
    tool = live_template.precedent.quest.prior.TOOL
    holds, evidence, sheets = [], {}, []
    unmasked_FE = []
    for name in ("rafael", "maria"):
        root = replay.ROOT / name
        fixture, path = root / "fixture.json", replay.CAPTURE_ROOT / name / "capture/capture_report.json"
        setup, report = map(base.load, (fixture, path))
        assert setup["candidate_sha256"] == candidate and report["ROM_sha256"] == setup["fixture_sha256"] == base.digest(setup["fixture"])
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert report["scripted_input_schedule"] == base.load(setup["control_plan"])
        route = setup["initialized_route"]
        frames = tool.photos(report)
        masks = [(n, tool.body_masks(pic)) for n, (_, pic) in sorted(frames.items())]
        cursor = 3650 if route == 0 else 4075
        found = []
        for record in setup["selected"]:
            raw = bytes.fromhex(record["stored_hex"])
            if raw[5] == 254:
                unmasked_FE.append(record)
                continue
            body = prior.prior.default_text(raw[6:raw.index(0, 6)], names[str(route)])
            for page in paint(arm, font, body)["pages"]:
                wanted = tool.prior.masks(bytes.fromhex(page["native_plane_hex"]))
                at = next((n for n, bits in masks if n > cursor and bits == wanted), None)
                assert at is not None, (name, record["id"], cursor, body)
                found.append(record | dict(route=route, frame=at, body_hex=body.hex(), capture=frames[at][0]))
                cursor = at
        holds.extend(found)
        sheet = Image.new("RGB", (1024, 404 * ((len(found) + 1) // 2)), "#263238")
        draw = ImageDraw.Draw(sheet)
        for i, row in enumerate(found):
            x, y = 512 * (i % 2), 404 * (i // 2)
            draw.text((x + 5, y + 2), f"{row['id']} at frame {row['frame']}", fill="white")
            cropped = frames[row["frame"]][1].crop((0, 192, 256, 384))
            sheet.paste(cropped.resize((512, 384), Image.Resampling.NEAREST), (x, y+16))
        out = ROOT / f"{name}_observed.png"
        sheet.save(out)
        sheets.append(dict(path=str(out), sha256=base.digest(out)))
        evidence.update({str(p): base.digest(p) for p in (fixture, path, setup["fixture"])})
    assert {"DK4_MES_B84_R0100", "DK4_MES_B84_R0106", "DK4_MES_B116_R0110"} <= {r["id"] for r in holds}
    assert len(holds) == 12
    base.save(LIVE, dict(candidate_sha256=candidate, holds=holds, evidence=evidence, sheets=sheets,
        natural_activation=False, hardware=False, initialized_Rafael_and_Maria=True, preserved_FE_commands_in_Maria_excerpt=unmasked_FE))
    print(f"Matched {len(holds)} complete observed portraits, including all three revisions.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("offline", "live"))
    globals()[cli.parse_args().action]()
