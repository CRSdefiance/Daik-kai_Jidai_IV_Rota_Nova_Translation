"""Verify the stored dialogue with the original font, name processor and renderer."""

from inspect import getsource
from types import FunctionType

from scripts import generic_name_macro_owned_v5886b as macro
from scripts import stage_rafael_early_phrase_wraps_20261118 as build
from scripts import verify_london_guild_assignments_20261118 as precedent
from scripts.source_locked_derivation_v5118 import checked_text

base, native = build.base, build.native
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"
ASSETS = (native.ARM, "/COMMON/MESFILE.DK4", "/GRP/KANJI.FNT")


def default_text(body, names):
    return build.review.TOKEN.sub(lambda m: names[m[0]], body.decode("ascii")).encode("ascii")


def verify():
    assert not ROOT.exists()
    stored, draft, parent = map(base.load, (build.PROOF, build.review.OUTPUT, build.parent.RELEASE))
    assert base.digest(build.ROM) == stored["candidate_sha256"]
    assert stored["predecessor_sha256"] == base.digest(build.parent.ROM) == parent["candidate_sha256"]
    assert stored["whole_parent_inverse"]
    assert stored["manuscript_sha256"] == base.digest(build.review.OUTPUT)
    image = base.NdsImage.open(build.ROM)
    boot = build.parent.stage.ROOT / "rafael_native_context.json"
    identity = build.parent.stage.ROOT / "rafael_native_ROM_identity.json"
    ctx = native.RegisteredRuntime(identity, boot, captain=0)
    assert all(ctx.image.read_file(asset) == image.read_file(asset) for asset in ASSETS)
    body_renderer = precedent.inherited.early.prior.precedent.planners(ctx.arm)[1]
    font = image.read_file(ASSETS[2])
    source = checked_text(getsource(macro.expand), {
        "assert identity==prefix and captain==2": "assert identity == prefix and captain == 0",
    })
    symbols = vars(macro).copy()
    exec(compile(source, __file__ + "::original-name-processor", "exec"), symbols)
    expand = symbols["expand"]
    names = {"FI": "Rafael", "FA": "Castor"}
    for token, name in names.items():
        report = ctx.execute(expand, token.encode("ascii"), 0)
        assert len(report["cases"]) == 4 and {c["output_hex"] for c in report["cases"]} == {name.encode("ascii").hex()}

    rows = {row["id"]: row for row in draft["records"]}
    paragraph = FunctionType(precedent.paragraph.__code__, vars(precedent) | {"build": build})
    contact = precedent.inherited.early.contact_sheets
    archive = native.IlnkContainer.parse(image.read_file("/data/SC0.DK4"))
    modified, retained, pictures = [], [], []
    for group in stored["groups"]:
        block = archive.blocks[group["block"]]
        assert native.digest(block) == group["after"]
        for command in group["commands"]:
            if not command["record_ids"]:
                continue
            ident, = command["record_ids"]
            row = rows[ident]
            raw, offset = bytes.fromhex(command["stored"]), command["stored_offset"]
            assert block[offset:offset + len(raw)] == raw and command["word"] == row["native_command_word"]
            value = raw[5:raw.index(0, 6)]
            assert value[0] == row["source_selector"]
            if row["decision"] == "retention":
                assert command["stored"] == command["current"] and value.hex() == row["current_hex"]
                resolved = default_text(value[1:], names)
                rendered = body_renderer(ctx.arm, font, resolved)
                assert rendered["complete_consumed_bytes"] == len(resolved)
                assert all(page["native_independent_plane_equal"] for page in rendered["pages"])
                retained.append(dict(id=ident, file_path=row["file_path"], stored_hex=value.hex(),
                    pages=[dict(page=p["page"], native_plane_sha256=native.digest(bytes.fromhex(p["native_plane_hex"])))
                           for p in rendered["pages"]]))
            else:
                plan = group["plans"][ident]
                result = paragraph(ctx, font, body_renderer, expand, None, names, row, value, plan)
                diagnostics = plan["diagnostics"]
                assert all(d["severity"] == "warning" and d["code"] == "line-break-count" for d in diagnostics)
                page = result["layouts"][0]["pages"][0]
                assert len(result["layouts"]) == 1 and len(result["layouts"][0]["pages"]) == 1
                pictures.append((ident, bytes.fromhex(page["native_plane_hex"])))
                modified.append(result | {"informational_source_row_differences": diagnostics})
    assert {r["id"] for r in modified + retained} == rows.keys()
    assert len(modified) == len(pictures) == 12 and len(retained) == 148

    ROOT.mkdir()
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(pictures)
    base.save(PROOF, dict(candidate_sha256=stored["candidate_sha256"], stage_proof_sha256=base.digest(build.PROOF),
        native_runtime_assets_byte_identical=True, default_name_macros=names, renderer_assets=ASSETS,
        revision_count=len(modified), fresh_page_count=len(pictures), **{"retention_count": len(retained)},
        checked_records=modified, retained_records=retained, contact_sheets=sheets, actual_gameplay=False,
        previous_initialized_rafael_context=dict(path=str(boot), sha256=base.digest(boot),
            identity=str(identity), identity_sha256=base.digest(identity))))
    print("Verified all 12 revised pages and 148 exact retentions.")


if __name__ == "__main__":
    verify()
