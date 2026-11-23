"""Check the company-name dialogue in the current progressive renderer."""

from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import stage_company_name_dialogue_20261121 as build
from scripts import verify_all_routes_next_phrase_wraps_20261118 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native, review = build.base, build.native, build.review
ROOT = build.ROOT / "native_display"
PROOF = ROOT / "native_display.json"
ASSETS = prior.ASSETS


def contexts(release):
    result = {3: native.RegisteredRuntime(build.parent.RELEASE, release["own_registered_startup"], captain=3)}
    for route, name in enumerate(("rafael", "hodram", "lil")):
        folder = review.ROOT / f"{name}_name_context"
        report = base.load(folder / "capture_report.json")
        assert report["ROM_sha256"] == release["candidate_sha256"]
        assert report["frames"] == 3901 and report["cold_boot"] and not report["savestate_loaded"]
        assert not report["callback_errors"] and not any(v for k, v in report.items() if k.startswith("synthetic_"))
        snapshot = report["read_only_RAM_snapshot"]
        boot, identity = folder / "name_boot.json", folder / "name_identity.json"
        base.save(boot, dict(candidate_sha256=release["candidate_sha256"], cold_boot=True, savestate=False,
                             actual_captain_getter=route, read_only_snapshot=snapshot))
        base.save(identity, dict(candidate=str(build.parent.ROM), candidate_sha256=release["candidate_sha256"],
                                 own_registered_startup_pending=False, clean_input_patch_byte_exact=True))
        result[route] = native.RegisteredRuntime(identity, boot, captain=route)
    return result


def four_default_names(routes, expand):
    names = prior.route_names(routes, expand)
    for route, ctx in routes.items():
        values = ctx.execute(expand, b"FU", route)["cases"]
        assert len(values) == 4
        body, = {row["output_hex"] for row in values}
        names[route]["FU"] = bytes.fromhex(body).decode("ascii")
    assert names[0]["FO"] == "Castor Co." and names[2]["FO"] == "Argot Co."
    return names


def main():
    assert not ROOT.exists()
    stored, draft, release = map(base.load, (build.PROOF, review.OUTPUT, build.parent.RELEASE))
    assert stored["candidate_sha256"] == base.digest(build.ROM)
    assert draft["previous_sha256"] == release["candidate_sha256"] == base.digest(build.parent.ROM)
    assert stored["manuscript_sha256"] == base.digest(review.OUTPUT) and stored["whole_parent_inverse"]
    image = base.NdsImage.open(build.ROM)
    routes = contexts(release)
    assert all(ctx.image.read_file(asset) == image.read_file(asset) for ctx in routes.values() for asset in ASSETS)
    expand = prior.original_expander()
    names = four_default_names(routes, expand)
    arm, font = (image.read_file(asset) for asset in (ASSETS[0], ASSETS[2]))
    paint, mixed = prior.clipped_renderer(routes[3]), prior.prior.original_cp932_renderer(arm)
    source = checked_text(getsource(prior.display.paragraph), {
        '{macro: example for macro in tokens}':
            '{macro: example + " Co." if macro == "FO" and n == 16 else example for macro in tokens}',
    })
    scope = vars(prior.display) | {"build": build}
    exec(compile(source, __file__ + "::actual-defaults-and-width-stress", "exec"), scope)
    paragraph = scope["paragraph"]

    banks = {route: native.IlnkContainer.parse(image.read_file(f"/data/SC{route}.DK4")) for route in routes}
    rows = {(r["file_path"], r["id"]): r for r in draft["records"]}
    modified, retained, pictures, fixes = [], [], [], []
    for group in stored["groups"]:
        route, path, number = (group[k] for k in ("route", "file_path", "block"))
        block = banks[route].blocks[number]
        assert native.digest(block) == group["after"]
        for command in group["commands"]:
            if not command["record_ids"]:
                continue
            ident, = command["record_ids"]
            row = rows[path, ident]
            raw, offset = bytes.fromhex(command["stored"]), command["stored_offset"]
            assert command["word"] == row["native_command_word"] == 0x4000 and block[offset:offset + len(raw)] == raw
            value = raw[5:raw.index(0, 6)]
            assert value[0] == row["source_selector"] < 207
            if row["decision"] == "retention":
                assert command["stored"] == command["current"] and value.hex() == row["current_hex"]
                body = prior.prior.default_text(value[1:], names[route])
                rendered = (paint if body.isascii() else mixed)(arm, font, body)
                assert rendered["complete_consumed_bytes"] == len(body)
                assert all(p["native_independent_plane_equal"] for p in rendered["pages"])
                retained.append(dict(id=ident, file_path=path, stored_hex=value.hex(),
                    page_hashes=[native.digest(bytes.fromhex(p["native_plane_hex"])) for p in rendered["pages"]]))
                continue
            plan = group["plans"][ident]
            result = paragraph(routes[route], font, paint, expand, None, names[route], row, value, plan)
            assert len(result["layouts"]) == 4 and all(len(layout["pages"]) == 1 for layout in result["layouts"])
            old_native = bytes.fromhex(command["current"])
            old_body = prior.prior.default_text(old_native[6:old_native.index(0, 6)], names[route])
            current = bytes.fromhex(result["layouts"][0]["expanded_hex"])
            assert b"Argot Co.." not in current
            if b"Argot Co.." in old_body:
                fixes.append(dict(file_path=path, id=ident, before=old_body.decode("ascii"), after=current.decode("ascii")))
            modified.append(result)
            for layout in result["layouts"]:
                for page in layout["pages"]:
                    pictures.append((f"SC{route} {ident} {layout['scope']}", bytes.fromhex(page["native_plane_hex"])))
    assert {(r["file_path"], r["id"]) for r in modified + retained} == rows.keys()
    assert len(modified) == 12 and len(retained) == 61 and len(pictures) == 48
    assert {r["id"] for r in fixes} == {"DK4_MES_B54_R0031", "DK4_MES_B60_R0020", "DK4_MES_B60_R0046", "DK4_MES_B151_R0103"}
    ROOT.mkdir()
    contact = prior.display.inherited.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(pictures)
    base.save(PROOF, dict(candidate_sha256=stored["candidate_sha256"], stage_proof_sha256=base.digest(build.PROOF),
        native_runtime_assets_byte_identical=True, default_name_macros=names, renderer_assets=ASSETS,
        revision_count=len(modified), fresh_page_count=len(pictures), retention_count=len(retained),
        checked_records=modified, retained_records=retained, punctuation_fixes=fixes, contact_sheets=sheets,
        actual_gameplay=False))
    print(f"Verified {len(pictures)} native pages, {len(retained)} exact retentions and {len(fixes)} punctuation corrections.")


if __name__ == "__main__":
    main()
