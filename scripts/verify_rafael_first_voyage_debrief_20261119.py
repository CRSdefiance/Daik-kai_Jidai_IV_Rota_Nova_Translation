"""Check the revised native pages and the original three name substitutions."""

from types import FunctionType

from scripts import stage_rafael_first_voyage_debrief_20261119 as build
from scripts import verify_forest_expeditions_20261118 as display
from scripts import verify_london_guild_assignments_20261118 as names

base, native = build.base, build.native
ROOT = build.ROOT / "native_display"
PROOF = ROOT / "native_display.json"
STOCK = {"FI": "Rafael", "FA": "Castor", "FO": "Castor Co."}
MAXIMUM = {"FI": "ABCDEFGHIJKLMNOP", "FA": "QRSTUVWXYZABCDEF", "FO": "ABCDEFGHIJKLMNOPQRST"}


def main():
    assert not ROOT.exists()
    stored, draft, release = map(base.load, (build.PROOF, build.review.OUTPUT, build.parent.RELEASE))
    assert stored["candidate_sha256"] == base.digest(build.ROM)
    assert stored["manuscript_sha256"] == base.digest(build.review.OUTPUT)
    assert stored["whole_parent_inverse"] and stored["changed_blocks"] == {"/data/SC0.DK4": [44, 47]}
    ctx = native.RegisteredRuntime(build.parent.RELEASE, release["own_registered_startup"], captain=3)
    image = base.NdsImage.open(build.ROM)
    assets = (native.ARM, "/COMMON/MESFILE.DK4", "/GRP/KANJI.FNT")
    assert all(ctx.image.read_file(p) == image.read_file(p) for p in assets)
    font = image.read_file(assets[-1])
    _, paint = display.early.prior.precedent.planners(ctx.arm)
    expand = names.expander()
    arguments = ctx.execute(expand, b"FI|FA|FO", 6)
    stock_bytes = {bytes.fromhex(r["output_hex"]) for r in arguments["cases"]}
    assert stock_bytes == {b"Maria|Li|Li Clan"}
    model_names = dict(zip(STOCK, next(iter(stock_bytes)).decode("ascii").split("|"), strict=True))
    path = "/data/SC0.DK4"
    bank = native.IlnkContainer.parse(image.read_file(path)).blocks
    rows = {r["id"]: r for r in draft["records"]}
    checked, retained, previews, name_cases = [], [], [], []
    for group in stored["groups"]:
        assert group["file_path"] == path
        block = bank[group["block"]]
        assert native.digest(block) == group["after"]
        for cmd in group["commands"]:
            if not cmd["record_ids"]:
                continue
            chosen = [rows[i] for i in cmd["record_ids"]]
            at, raw = cmd["stored_offset"], bytes.fromhex(cmd["stored"])
            assert block[at:at + len(raw)] == raw
            if all(r["decision"] == "retention" for r in chosen):
                assert cmd["stored"] == cmd["current"]
                retained.extend(dict(id=r["id"], file_path=path, kept_complete_command=cmd) for r in chosen)
                continue
            row, = chosen
            ident = row["id"]
            assert cmd["word"] == 0x4000 and raw[5] == row["source_selector"]
            value = raw[5:raw.index(0, 6)]
            plan = group["plans"][ident]
            result = names.paragraph(ctx, font, paint, expand, None, model_names, row, value, plan)
            tokens = set(build.review.TOKEN.findall(row["english"]))
            assert tokens == set(build.review.TOKEN.findall(bytes.fromhex(row["source_hex"])[1:].decode("cp932")))
            final = result["layouts"][0]["pages"]
            if tokens:
                limits = {n: len(v) for n, v in MAXIMUM.items()}
                assert limits == {"FI": 16, "FA": 16, "FO": build.MAX_COMPANY_CELLS}
                for label, replacements in (("Rafael opening", STOCK), ("maximum supplied widths", MAXIMUM)):
                    supplied = {n: replacements[n] for n in sorted(tokens)}
                    text = build.review.TOKEN.sub(lambda m: supplied[m[0]], value[1:].decode("ascii")).encode("ascii")
                    lines = [names.expected(line, supplied) for line in plan["lines"]]
                    rendered = names.raster(ctx, font, paint, text, lines, 1)
                    result["layouts"].append(dict(scope=label, names=supplied, expanded_hex=text.hex(),
                                                  lines=lines, pages=rendered))
                    if label == "Rafael opening":
                        final = rendered
                    else:
                        previews.append((f"{ident} maximum name widths", bytes.fromhex(rendered[0]["native_plane_hex"])))
                name_cases.append(dict(id=ident, original_tokens=sorted(tokens), exact_current_native_expansions=4,
                                       default_and_maximum_samples_verified=True))
            checked.append(result | dict(target_hex=value.hex(), pages=final, planned_lines=plan["lines"]))
            previews.append((ident, bytes.fromhex(final[0]["native_plane_hex"])))
    assert {r["id"] for r in checked + retained} == rows.keys()
    assert len(checked) == 39 and len(retained) == 93
    assert {r["id"] for r in name_cases} == {f"DK4_MES_B44_R{i:04}" for i in (17, 152, 308, 316, 327)}
    ROOT.mkdir()
    contact = display.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(previews)
    base.save(PROOF, dict(candidate_sha256=stored["candidate_sha256"], stage_proof_sha256=base.digest(build.PROOF),
        revisions=checked, exact_retentions=retained, native_macro_checks=name_cases,
        maximum_name_widths=MAXIMUM, contact_sheets=sheets, actual_gameplay=False))
    print(f"Checked 39 revised pages, five macro records and 93 exact retentions. {len(previews)} previews.")


if __name__ == "__main__":
    main()
