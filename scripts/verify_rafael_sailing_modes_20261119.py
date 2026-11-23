"""Check every revised sailing tutorial page in its original display consumer."""

from types import FunctionType

from scripts import stage_rafael_sailing_modes_20261119 as build
from scripts import verify_forest_expeditions_20261118 as workflow

base, native = build.base, build.native
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"


def main():
    assert not ROOT.exists()
    staged, draft, release = map(base.load, (build.PROOF, build.review.OUTPUT, build.parent.RELEASE))
    assert staged["candidate_sha256"] == base.digest(build.ROM)
    assert staged["manuscript_sha256"] == base.digest(build.review.OUTPUT)
    assert staged["whole_parent_inverse"] and staged["changed_blocks"] == {"/data/SC0.DK4": [46]}
    ctx = native.RegisteredRuntime(build.parent.RELEASE, release["own_registered_startup"], captain=3)
    image = base.NdsImage.open(build.ROM)
    assets = (native.ARM, "/COMMON/MESFILE.DK4", "/GRP/KANJI.FNT")
    assert all(ctx.image.read_file(p) == image.read_file(p) for p in assets)
    font = image.read_file(assets[2])
    _, paint = workflow.early.prior.precedent.planners(ctx.arm)
    fe = build.stage.system.native_painter(ctx)
    expand = workflow.progress_expander()
    group, = staged["groups"]
    block = native.IlnkContainer.parse(image.read_file(group["file_path"])).blocks[46]
    assert native.digest(block) == group["after"]
    modifiers, retentions, previews = [], [], []
    rows = {r["id"]: r for r in draft["records"]}
    for command in group["commands"]:
        desired = [rows[i] for i in command["record_ids"]]
        if not desired:
            continue
        at, raw = command["stored_offset"], bytes.fromhex(command["stored"])
        assert block[at:at+len(raw)] == raw
        if all(row["decision"] == "retention" for row in desired):
            assert command["stored"] == command["current"]
            retentions.extend(dict(id=row["id"], kept_complete_command=command) for row in desired)
            continue
        row, = desired
        assert command["word"] == 0x4000 and raw[5] == row["source_selector"]
        body = raw[5:raw.index(0, 6)]
        plan = group["plans"][row["id"]]
        result = workflow.validate_paragraph(ctx, font, paint, expand, fe, row, body, plan)
        page, = result["pages"]
        modifiers.append(result)
        previews.append((row["id"], bytes.fromhex(page["native_plane_hex"])))
    assert len(previews) == len(modifiers) == 12 and len(retentions) == 14
    assert sum(r["kind"] == "system-FE" for r in modifiers) == 9
    ROOT.mkdir()
    contact = workflow.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(previews)
    base.save(PROOF, dict(candidate_sha256=staged["candidate_sha256"], stage_proof_sha256=base.digest(build.PROOF),
        revisions=modifiers, exact_retentions=retentions, contact_sheets=sheets, new_gameplay_runs=0,
        current_sprite_headings_unchanged=True, integration_pending=True, new_editorial_credit=0))
    print("Verified 12 revised pages in the original renderers and preserved 14 exact records.")


if __name__ == "__main__":
    main()
