"""Check the revised early Hodram pages and both unchanged opaque shouts."""

from pathlib import Path
from types import FunctionType

from scripts import stage_hodram_early_confrontations_20261119 as build
from scripts import verify_london_guild_assignments_20261118 as workflow

base, native, stage = build.base, build.native, build.stage
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"
OPAQUE = {"DK4_MES_B40_R0088", "DK4_MES_B40_R0092"}
OPAQUE_PRIOR = Path("work/Hodram_B0_B41_clean_20261107/storage_inputs_v2/native_pages.json")


def main():
    assert not ROOT.exists()
    stored, draft, release = map(base.load, (build.PROOF, build.review.OUTPUT, build.parent.RELEASE))
    assert stored["candidate_sha256"] == base.digest(build.ROM)
    assert stored["manuscript_sha256"] == base.digest(build.review.OUTPUT)
    assert stored["whole_parent_inverse"] and len(stored["groups"]) == 13
    ctx = native.RegisteredRuntime(build.parent.RELEASE, release["own_registered_startup"], captain=3)
    image = base.NdsImage.open(build.ROM)
    assets = (native.ARM, "/COMMON/MESFILE.DK4", "/GRP/KANJI.FNT")
    assert all(ctx.image.read_file(p) == image.read_file(p) for p in assets)
    font = image.read_file(assets[2])
    prior = base.load(OPAQUE_PRIOR)
    assert prior["font_sha256"] == native.digest(font)
    prior_shouts = {r["id"]: r for r in prior["records"] if r["id"] in OPAQUE}
    painter = workflow.inherited.early.prior.precedent.planners(ctx.arm)[1]
    fe_painter = stage.system.native_painter(ctx)
    names, expand = workflow.current_names(ctx), workflow.expander()
    path = "/data/SC1.DK4"
    bank = native.IlnkContainer.parse(image.read_file(path)).blocks
    rows = {r["id"]: r for r in draft["records"]}
    checked, retained, shouts, previews = [], [], {}, []
    for group in stored["groups"]:
        assert group["file_path"] == path
        block = bank[group["block"]]
        assert native.digest(block) == group["after"]
        for command in group["commands"]:
            chosen = [rows[ident] for ident in command["record_ids"]]
            if not chosen:
                continue
            start, raw = command["stored_offset"], bytes.fromhex(command["stored"])
            assert block[start:start + len(raw)] == raw
            if all(r["decision"] == "retention" for r in chosen):
                assert command["stored"] == command["current"]
                retained.extend(dict(id=r["id"], file_path=path, kept_complete_command=command) for r in chosen)
                for row in chosen:
                    if row["id"] not in OPAQUE:
                        continue
                    value = raw[5:raw.index(0, 6)]
                    assert value.hex() == row["source_hex"] == row["current_hex"]
                    old = prior_shouts[row["id"]]
                    page, = old["complete_native_English_display"]["pages"]
                    assert value.hex() == old["compiled_hex"] and value[1:].hex() == page["consumed_hex"]
                    plane = Path(page["native_plane"]).read_bytes()
                    assert native.digest(plane) == page["native_plane_sha256"] and len(plane) == 216 * 64
                    shouts[row["id"]] = dict(selector=value[0], exact_stored_hex=value.hex(),
                        page=page | {"native_plane_hex": plane.hex()}, prior=OPAQUE_PRIOR.as_posix(),
                        prior_sha256=base.digest(OPAQUE_PRIOR), exact_text_and_font_reuse=True)
                    previews.append((f"{row['id']} original opaque cry", plane))
                continue
            row, = chosen
            assert command["word"] == 0x4000 and raw[5] == row["source_selector"]
            body = raw[5:raw.index(0, 6)]
            plan = group["plans"][row["id"]]
            result = workflow.paragraph(ctx, font, painter, expand, fe_painter, names, row, body, plan)
            primary = result["layouts"][0]
            checked.append(result | dict(target_hex=body.hex(), pages=primary["pages"], planned_lines=plan["lines"]))
            for layout in result["layouts"]:
                for page in layout["pages"]:
                    label = f"{row['id']} {layout['scope']}"
                    previews.append((label, bytes.fromhex(page["native_plane_hex"])))
            if row["id"] == "DK4_MES_B33_R0005":
                expanded = body[1:].replace(b"FA", b"Bergstrom")
                expected = [workflow.expected(line, {"FA": "Bergstrom"}) for line in plan["lines"]]
                checked[-1]["hodram_surname_pages"] = workflow.raster(ctx, font, painter, expanded, expected, 1)
                for page in checked[-1]["hodram_surname_pages"]:
                    previews.append((f"{row['id']} Hodram default surname", bytes.fromhex(page["native_plane_hex"])))
    assert {r["id"] for r in checked + retained} == rows.keys()
    assert len(checked) == 36 and len(retained) == 141 and shouts.keys() == OPAQUE
    assert sum(r["kind"] == "system-FE" for r in checked) == 1
    ROOT.mkdir()
    contact = workflow.inherited.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(previews)
    base.save(PROOF, dict(candidate_sha256=stored["candidate_sha256"], stage_proof_sha256=base.digest(build.PROOF),
        revisions=checked, exact_retentions=retained, contact_sheets=sheets, opaque_retention_display=shouts,
        displayed_native_plans=len(previews), actual_gameplay=False, integration_pending=True, new_editorial_credit=0))
    print(f"Verified 36 revised pages, 141 exact retentions and {len(previews)} native previews.")


if __name__ == "__main__":
    main()
