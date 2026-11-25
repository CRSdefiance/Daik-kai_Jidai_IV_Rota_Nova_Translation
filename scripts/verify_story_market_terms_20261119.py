"""Verify every revised market-story page on its original display path."""
from inspect import getsource

from scripts import stage_story_market_terms_20261119 as build
from scripts import verify_rafael_first_voyage_debrief_20261119 as previous
from scripts.source_locked_derivation_v5118 import checked_text

base, native = build.base, build.native
ROOT = build.ROOT / "native_display"
PROOF = ROOT / "native_display.json"


def main():
    assert not ROOT.exists()
    stored, draft, release = map(base.load, (build.PROOF, build.review.OUTPUT, build.parent.RELEASE))
    assert stored["candidate_sha256"] == base.digest(build.ROM)
    assert stored["manuscript_sha256"] == base.digest(build.review.OUTPUT)
    assert stored["whole_parent_inverse"]
    assert stored["changed_blocks"] == {f"/data/SC{i}.DK4": list(blocks)
                                        for i, blocks in enumerate(build.paired.BLOCKS) if blocks}
    ctx = native.RegisteredRuntime(build.parent.RELEASE, release["own_registered_startup"], captain=3)
    image = base.NdsImage.open(build.ROM)
    assets = (native.ARM, "/COMMON/MESFILE.DK4", "/GRP/KANJI.FNT")
    assert all(ctx.image.read_file(path) == image.read_file(path) for path in assets)
    font = image.read_file(assets[-1])
    prior_root = build.ROOT.with_name("staged_v2")
    prior_path = prior_root / "native_display" / PROOF.name
    prior = base.load(prior_path)
    prior_rom = prior_root / build.ROM.name
    assert prior["candidate_sha256"] == base.digest(prior_rom)
    assert prior["stage_proof_sha256"] == base.digest(prior_root / build.PROOF.name)
    assert base.load(prior_root / build.PROOF.name)["predecessor_sha256"] == stored["predecessor_sha256"]
    earlier = base.NdsImage.open(prior_rom)
    assert all(earlier.read_file(path) == image.read_file(path) for path in assets)
    earlier_rows = {(row["file_path"], row["id"]): row for row in prior["revisions"]}
    earlier_macros = {(row["file_path"], row["id"]): row for row in prior["native_macro_checks"]}
    reused = []
    display, names = previous.display, previous.names
    _, paint = display.early.prior.precedent.planners(ctx.arm)
    expand = names.expander()
    fe = build.stage.system.native_painter(ctx)
    model_names = names.current_names(ctx)
    rows = {(r["file_path"], r["id"]): r for r in draft["records"]}
    banks = {path: native.IlnkContainer.parse(image.read_file(path)).blocks for path in stored["changed_blocks"]}
    checked, retained, previews, macro_cases = [], [], [], []
    for group in stored["groups"]:
        path = group["file_path"]
        block = banks[path][group["block"]]
        assert native.digest(block) == group["after"]
        for command in group["commands"]:
            if not command["record_ids"]:
                continue
            selected = [rows[path, ident] for ident in command["record_ids"]]
            at, raw = command["stored_offset"], bytes.fromhex(command["stored"])
            assert block[at:at + len(raw)] == raw
            if all(row["decision"] == "retention" for row in selected):
                assert command["stored"] == command["current"]
                retained.extend(dict(id=row["id"], file_path=path, kept_complete_command=command) for row in selected)
                continue

            row, = selected
            ident = row["id"]
            assert command["word"] == 0x4000 and raw[5] == row["source_selector"]
            value = raw[5:raw.index(0, 6)]
            plan = group["plans"][ident]
            old = earlier_rows[path, ident]
            if (old["target_hex"], old["planned_lines"]) == (value.hex(), plan["lines"]):
                checked.append(old)
                reused.append(dict(file_path=path, id=ident))
                if (path, ident) in earlier_macros:
                    macro_cases.append(earlier_macros[path, ident])
                continue
            result = names.paragraph(ctx, font, paint, expand, fe, model_names, row, value, plan)
            tokens = build.review.workflow.TOKEN.findall(row["english"])
            assert tokens == build.review.workflow.TOKEN.findall(bytes.fromhex(row["source_hex"])[1:].decode("cp932"))
            final = result["layouts"][0]["pages"]
            title = f"SC{group['route']} {ident}"
            if tokens:
                assert tokens == ["FI"] and (group["route"], ident) == (0, "DK4_MES_B66_R0031")
                text = build.review.workflow.TOKEN.sub(lambda m: previous.STOCK[m[0]],
                                                      value[1:].decode("ascii")).encode("ascii")
                lines = [names.expected(line, previous.STOCK) for line in plan["lines"]]
                final = names.raster(ctx, font, paint, text, lines, 1)
                result["layouts"].append(dict(scope="Rafael default", names={"FI": "Rafael"},
                                              expanded_hex=text.hex(), lines=lines, pages=final))
                widest, = (layout for layout in result["layouts"] if layout["scope"] == "offline 16-cell name")
                previews.append((title + " 16-cell name", bytes.fromhex(widest["pages"][0]["native_plane_hex"])))
                macro_cases.append(dict(id=ident, file_path=path, original_tokens=tokens,
                                        native_registered_default_and_1_15_16_cell_stress=True,
                                        supplied_Rafael_default=True))
            checked.append(result | dict(target_hex=value.hex(), pages=final, planned_lines=plan["lines"]))
            previews.extend((title + (f" page {i}" if len(final) > 1 else ""), bytes.fromhex(page["native_plane_hex"]))
                            for i, page in enumerate(final, 1))
    assert {(row["file_path"], row["id"]) for row in checked + retained} == rows.keys()
    assert len(checked) == 34 and len(retained) == 168 and len(macro_cases) == 1
    assert [row["id"] for row in checked if row["kind"] == "system-FE"] == ["DK4_MES_B170_R0241"]
    assert len(reused) == 32 and len(previews) == 2
    ROOT.mkdir()
    contact = display.early.contact_sheets
    source = checked_text(getsource(contact), {"before_after_": "phrase_refinement_"})
    scope = contact.__globals__ | {"ROOT": ROOT}
    exec(compile(source, __file__ + "::fresh_refinements", "exec"), scope)
    fresh = scope["contact_sheets"](previews)
    assert all(base.digest(sheet["path"]) == sheet["sha256"] for sheet in prior["contact_sheets"])
    sheets = prior["contact_sheets"] + fresh
    base.save(PROOF, dict(candidate_sha256=stored["candidate_sha256"], stage_proof_sha256=base.digest(build.PROOF),
                         revisions=checked, exact_retentions=retained, native_macro_checks=macro_cases,
                         contact_sheets=sheets, fresh_contact_sheets=fresh, reused_exact_pages=reused,
                         previous_native_proof=str(prior_path), previous_native_proof_sha256=base.digest(prior_path),
                         prior_sheets_cover_exact_reused_pages_and_include_two_superseded_previews=True,
                         actual_gameplay=False))
    print(f"Verified {len(checked)} revised records and {len(retained)} byte-exact retentions. {len(previews)} fresh previews and {len(reused)} exact reuses.")


if __name__ == "__main__":
    main()
