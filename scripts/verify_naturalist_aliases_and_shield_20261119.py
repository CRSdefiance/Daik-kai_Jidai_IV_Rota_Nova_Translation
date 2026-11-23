"""Verify each new native page, including expansion and exact retained commands."""

from inspect import getsource

from scripts import stage_naturalist_aliases_and_shield_20261119 as build
from scripts import verify_london_guild_assignments_20261118 as workflow
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage = build.base, build.native, build.stage
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"
PRIOR = build.ROOT.with_name("research_v2") / ROOT.name / PROOF.name


def main():
    assert not ROOT.exists()
    stored, draft, release = map(base.load, (build.PROOF, build.review.OUTPUT, build.parent.RELEASE))
    assert stored["candidate_sha256"] == base.digest(build.ROM)
    assert stored["manuscript_sha256"] == base.digest(build.review.OUTPUT)
    assert stored["whole_parent_inverse"] and len(stored["groups"]) == 7
    ctx = native.RegisteredRuntime(build.parent.RELEASE, release["own_registered_startup"], captain=3)
    image = base.NdsImage.open(build.ROM)
    assets = (native.ARM, "/COMMON/MESFILE.DK4", "/GRP/KANJI.FNT")
    assert all(ctx.image.read_file(p) == image.read_file(p) for p in assets)
    previous = base.load(PRIOR)
    prior_rom = PRIOR.parent.parent / build.ROM.name
    assert base.digest(prior_rom) == previous["candidate_sha256"]
    earlier_stage = PRIOR.parent.parent / build.PROOF.name
    assert base.digest(earlier_stage) == previous["stage_proof_sha256"]
    assert base.load(earlier_stage)["predecessor_sha256"] == stored["predecessor_sha256"]
    earlier = base.NdsImage.open(prior_rom)
    assert all(earlier.read_file(p) == image.read_file(p) for p in assets)
    prior_pages = {(r["file_path"], r["id"]): r for r in previous["revisions"]}
    assert all(base.digest(s["path"]) == s["sha256"] for s in previous["contact_sheets"])
    font = image.read_file(assets[2])
    painter = workflow.inherited.early.prior.precedent.planners(ctx.arm)[1]
    fe_painter = stage.system.native_painter(ctx)
    names, expand = workflow.current_names(ctx), workflow.expander()
    banks = {f"/data/SC{i}.DK4": native.IlnkContainer.parse(image.read_file(f"/data/SC{i}.DK4")).blocks
             for i in range(4)}
    rows = {(r["file_path"], r["id"]): r for r in draft["records"]}
    checked, retained, previews, reused = [], [], [], []
    for group in stored["groups"]:
        path, number = group["file_path"], group["block"]
        block = banks[path][number]
        assert native.digest(block) == group["after"]
        for command in group["commands"]:
            chosen = [rows[path, ident] for ident in command["record_ids"]]
            if not chosen:
                continue
            start, raw = command["stored_offset"], bytes.fromhex(command["stored"])
            assert block[start:start + len(raw)] == raw
            if all(r["decision"] == "retention" for r in chosen):
                assert command["stored"] == command["current"]
                retained.extend(dict(id=r["id"], file_path=path, kept_complete_command=command) for r in chosen)
                continue
            row, = chosen
            assert command["word"] == 0x4000 and raw[5] == row["source_selector"]
            body = raw[5:raw.index(0, 6)]
            plan = group["plans"][row["id"]]
            key = (path, row["id"])
            old = prior_pages[key]
            if old["target_hex"] == body.hex() and old["planned_lines"] == plan["lines"]:
                checked.append(old)
                reused.append(dict(file_path=path, id=row["id"]))
                continue
            result = workflow.paragraph(ctx, font, painter, expand, fe_painter, names, row, body, plan)
            primary = result["layouts"][0]
            checked.append(result | dict(target_hex=body.hex(), pages=primary["pages"], planned_lines=plan["lines"]))
            for layout in result["layouts"]:
                for page in layout["pages"]:
                    label = f"SC{row['route']} {row['id']} {layout['scope']}"
                    previews.append((label, bytes.fromhex(page["native_plane_hex"])))
    assert {(r["file_path"], r["id"]) for r in checked + retained} == rows.keys()
    assert len(checked) == 57 and len(retained) == 173
    assert sum(r["kind"] == "system-FE" for r in checked) == 2
    ROOT.mkdir()
    contact = workflow.inherited.early.contact_sheets
    source = checked_text(getsource(contact), {"before_after_": "refined_"})
    env = contact.__globals__ | {"ROOT": ROOT}
    exec(compile(source, __file__ + "::changed-previews-only", "exec"), env)
    sheets = env[contact.__name__](previews)
    base.save(PROOF, dict(candidate_sha256=stored["candidate_sha256"], stage_proof_sha256=base.digest(build.PROOF),
        revisions=checked, exact_retentions=retained, contact_sheets=previous["contact_sheets"] + sheets,
        actual_gameplay=False, reused_backend=dict(path=PRIOR.as_posix(), sha256=base.digest(PRIOR), rows=reused),
        new_visual_sheets=sheets, displayed_native_plans=len(previews), initialization_captain=3, stress_cases_are_offline=True,
        integration_pending=True, new_editorial_credit=0))
    print(f"Verified {len(checked)} pages and {len(retained)} exact retentions. Rendered {len(previews)} revised layouts and reused {len(reused)} matching native page proofs.")


if __name__ == "__main__":
    main()
