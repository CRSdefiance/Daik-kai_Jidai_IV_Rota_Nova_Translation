"""Verify the stored dialogue and render every revised page with the native font."""

from inspect import getsource

from scripts import stage_rafael_east_asia_followup_20261121 as stage
from scripts import verify_rafael_pereira_village_20261121 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native, display = stage.base, stage.native, prior.display
ROOT = stage.ROOT / "native_display"
PROOF = ROOT / "native_display.json"
REFERENCE_STAGE = stage.ROOT.with_name("staged_v3")
REFERENCE_DISPLAY = REFERENCE_STAGE / "native_display" / PROOF.name


def load_reference(image, stored):
    earlier, rendered = map(base.load, (REFERENCE_STAGE / stage.PROOF.name, REFERENCE_DISPLAY))
    rom = REFERENCE_STAGE / stage.ROM.name
    assert earlier["candidate_sha256"] == rendered["candidate_sha256"] == base.digest(rom)
    assert rendered["stage_proof_sha256"] == base.digest(REFERENCE_STAGE / stage.PROOF.name)
    assert earlier["predecessor_sha256"] == stored["predecessor_sha256"]
    previous = base.NdsImage.open(rom)
    assert all(previous.read_file(path) == image.read_file(path) for path in display.ASSETS)
    assert all(base.digest(sheet["path"]) == sheet["sha256"] for sheet in rendered["sheets"])
    plans = {ident: plan for group in earlier["groups"] for ident, plan in group["plans"].items()}
    return rendered, plans


def weighted_name_audit():
    paragraph = display.display.paragraph
    source = checked_text(getsource(paragraph), {
        '{macro: example for macro in tokens}':
            '{macro: example + " Co." if macro == "FO" and n == 16 else example for macro in tokens}',
    })
    scope = paragraph.__globals__ | {"build": stage}
    exec(compile(source, __file__ + "::surname-and-derived-company-width", "exec"), scope)
    return scope["paragraph"]


source = checked_text(getsource(prior.main), {
    '    paragraph = display.display.paragraph\n    audit = FunctionType(paragraph.__code__, paragraph.__globals__ | {"build": stage})':
        '    audit = weighted_name_audit()',
    '    revised_pages = 0':
        '''    reference, older_plans = load_reference(image, stored)
    older_rows = {row["id"]: row for row in reference["records"]}
    revised_pages = stress_pages = 0
    pagination, refreshed, reused = [], [], []''',
    '    fe = town.current_fe_painter(SimpleNamespace(arm=ctx.arm, image=image))\n': '',
    '''                if selector == 254:
                    result = fe(body)
                    assert result["complete_consumed_bytes"] == len(body)
                    entry.update(retained_system_panel=True, native_pages=1,
                                 panel_mask_sha256=native.digest(result["physical"]))''':
        '                assert selector != 254',
    '                assert plan["expected_native_pages"] == 1':
        '''                assert 1 <= plan["expected_native_pages"] <= 2
                if ident == "DK4_MES_B78_R0005":
                    previous = old[6:old.index(0, 6)].decode("ascii")
                    expanded = stage.review.TOKEN.sub(lambda m: names[m[0]], previous).encode("ascii")
                    original = paint(ctx.arm, font, expanded)
                    assert original["complete_consumed_bytes"] == len(expanded)
                    assert len(original["pages"]) == 2 and plan["expected_native_pages"] == 1
                    pagination.append(dict(id=ident, previous_pages=2, registered_pages=1))
                earlier = older_rows[ident]
                if earlier["stored_command_hex"] == new.hex() and older_plans.get(ident) == plan:
                    assert earlier["decision"] == "revision"
                    count = earlier["native_pages"]
                    assert count == plan["expected_native_pages"]
                    records.append(earlier | dict(stored_offset=at))
                    revised_pages += count
                    stress_pages += (len(earlier["layouts"]) - 1) * count
                    reused.append(ident)
                    continue
                refreshed.append(ident)''',
    'display.display.raster(ctx, font, paint, body, plan["lines"], 1)':
        'display.display.raster(ctx, font, paint, body, plan["lines"], plan["expected_native_pages"])',
    '''                    page, = layout["pages"]
                    assert page["native_independent_plane_equal"] and page["all_bitmap_header_input_canaries_exact"]
                    pixels = bytes.fromhex(page["native_plane_hex"])
                    previews.append((f"{ident} {layout['scope']}", pixels))
                    screens.append(dict(scope=layout["scope"], expanded_hex=layout["expanded_hex"],
                                        plane_sha256=native.digest(pixels), lines=layout["lines"]))
                entry.update(native_pages=1, layouts=screens)
                revised_pages += 1''':
        '''                    pages = layout["pages"]
                    count = plan["expected_native_pages"]
                    assert len(pages) == count
                    hashes = []
                    for number, page in enumerate(pages, 1):
                        assert page["native_independent_plane_equal"] and page["all_bitmap_header_input_canaries_exact"]
                        pixels = bytes.fromhex(page["native_plane_hex"])
                        title = f"{ident} {layout['scope']}" + (f" {number}/{count}" if count > 1 else "")
                        if "FO" in stage.review.TOKEN.findall(row["english"]):
                            assert b"Co.." not in bytes.fromhex(layout["expanded_hex"])
                            assert b"Co.?" not in bytes.fromhex(layout["expanded_hex"])
                        previews.append((title, pixels))
                        hashes.append(native.digest(pixels))
                    screens.append(dict(scope=layout["scope"], expanded_hex=layout["expanded_hex"],
                                        plane_sha256=hashes[0], page_sha256=hashes, lines=layout["lines"]))
                entry.update(native_pages=count, layouts=screens)
                revised_pages += count
                stress_pages += (len(layouts) - 1) * count''',
    '    assert len(records) == 197 and not rows and revised_pages == 110':
        '''    assert len(records) == 142 and not rows and revised_pages == sum(plan["expected_native_pages"] for plan in draft["plans"].values())
    assert len(pagination) == 1''',
    '    assert sum(bool(r.get("retained_system_panel")) for r in records) == 1\n': '',
    ', and the retained FE notice.': '.',
    'len(previews) - revised_pages': 'stress_pages',
    'sheets=sheets,\n                          initialized_dependencies':
        'sheets=reference["sheets"] + sheets,\n                          initialized_dependencies',
    'runtime_assets=list(display.ASSETS), offline_native_only=True':
        '''runtime_assets=list(display.ASSETS), offline_native_only=True, verified_pagination_changes=pagination,
                          refreshed_ids=refreshed, reused_exact_revision_ids=reused,
                          retained_from_prior_proof=str(REFERENCE_DISPLAY),
                          retained_from_prior_proof_sha256=base.digest(REFERENCE_DISPLAY)''',
})
scope = vars(prior) | globals()
exec(compile(source, __file__ + "::native-pages", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
