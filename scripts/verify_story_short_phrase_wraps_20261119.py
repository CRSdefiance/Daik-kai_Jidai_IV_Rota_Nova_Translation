"""Check all revised story pages and the exact bytes of each retained record."""

from types import FunctionType

from scripts import stage_story_short_phrase_wraps_20261119 as build
from scripts import verify_forest_expeditions_20261118 as workflow

base, native = build.base, build.native
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"


def main():
    assert not ROOT.exists()
    stored, draft, release = map(base.load, (build.PROOF, build.review.OUTPUT, build.parent.RELEASE))
    assert stored["candidate_sha256"] == base.digest(build.ROM)
    assert stored["manuscript_sha256"] == base.digest(build.review.OUTPUT)
    assert stored["whole_parent_inverse"] and len(stored["groups"]) == 11
    ctx = native.RegisteredRuntime(build.parent.RELEASE, release["own_registered_startup"], captain=3)
    image = base.NdsImage.open(build.ROM)
    assets = (native.ARM, "/COMMON/MESFILE.DK4", "/GRP/KANJI.FNT")
    assert all(ctx.image.read_file(p) == image.read_file(p) for p in assets)
    font = image.read_file(assets[2])
    _, paint = workflow.early.prior.precedent.planners(ctx.arm)
    fe = build.stage.system.native_painter(ctx)
    expand = workflow.progress_expander()
    banks = {f"/data/SC{i}.DK4": native.IlnkContainer.parse(image.read_file(f"/data/SC{i}.DK4")).blocks
             for i in range(4)}
    rows = {(r["file_path"], r["id"]): r for r in draft["records"]}
    checked, retained, previews = [], [], []
    for group in stored["groups"]:
        path, number = group["file_path"], group["block"]
        block = banks[path][number]
        assert native.digest(block) == group["after"]
        for command in group["commands"]:
            chosen = [rows[path, ident] for ident in command["record_ids"]]
            if not chosen:
                continue
            at, raw = command["stored_offset"], bytes.fromhex(command["stored"])
            assert block[at:at+len(raw)] == raw
            if all(r["decision"] == "retention" for r in chosen):
                assert command["stored"] == command["current"]
                retained.extend(dict(id=r["id"], file_path=path, kept_complete_command=command) for r in chosen)
                continue
            row, = chosen
            assert command["word"] == 0x4000 and raw[5] == row["source_selector"]
            assert not build.review.TOKEN.findall(row["english"])
            body = raw[5:raw.index(0, 6)]
            plan = group["plans"][row["id"]]
            result = workflow.validate_paragraph(ctx, font, paint, expand, fe, row, body, plan)
            page, = result["pages"]
            checked.append(result)
            previews.append((f"SC{row['route']} {row['id']}", bytes.fromhex(page["native_plane_hex"])))
    assert {(r["file_path"], r["id"]) for r in checked+retained} == rows.keys()
    assert len(checked) == len(previews) == 19 and len(retained) == 176
    assert sum(r["kind"] == "system-FE" for r in checked) == 3
    ROOT.mkdir()
    contact = workflow.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(previews)
    base.save(PROOF, dict(candidate_sha256=stored["candidate_sha256"], stage_proof_sha256=base.digest(build.PROOF),
        revisions=checked, exact_retentions=retained, contact_sheets=sheets, actual_gameplay=False,
        integration_pending=True, new_editorial_credit=0))
    print("Verified all 19 revised pages and 176 exact retentions.")


if __name__ == "__main__":
    main()
