"""Verify the stored Carlo, Cristina, Samwell, and Jam dialogue against native rendering."""

from inspect import getsource

from PIL import Image

from scripts import stage_rafael_B170_B176_20261121 as stage
from scripts import verify_rafael_B161_B169_20261121 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
display = previous.display
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
EARLIER_ROOT = stage.ROOT.with_name("staged_B170_B176")


def earlier_display(ctx, image, staged):
    source = EARLIER_ROOT / "native_display/native_display.json"
    earlier = base.load(source)
    earlier_stage = EARLIER_ROOT / "stored_proof.json"
    earlier_rom = EARLIER_ROOT / stage.ROM.name
    assert earlier["stage_proof_sha256"] == base.digest(earlier_stage)
    stored = base.load(earlier_stage)
    assert earlier["candidate_sha256"] == stored["candidate_sha256"] == base.digest(earlier_rom)
    assert staged["predecessor_sha256"] == stored["predecessor_sha256"]
    assert earlier["initialized_dependencies"] == ctx.receipt()
    old_image = base.NdsImage.open(earlier_rom)
    assert all(image.read_file(path) == old_image.read_file(path) for path in display.ASSETS)
    assert all(base.digest(item["path"]) == item["sha256"] for item in earlier["fresh_sheets"])
    return earlier, {r["id"]: r for r in earlier["records"]}, {
        ident: plan for group in stored["groups"] for ident, plan in group["plans"].items()}, source


def refresh_sheet(previous_sheets, new_panels):
    (index, plane), = new_panels
    ordinal, slot = divmod(index, 12)
    x, y = 4 + (slot % 3) * 444, 19 + (slot // 3) * 150
    with Image.open(previous_sheets[ordinal]["path"]) as prior_sheet:
        montage = prior_sheet.copy()
    pixels = Image.frombytes("L", (216, 64), bytes(255 if pixel else 0 for pixel in plane))
    ink = pixels.resize((432, 128), Image.Resampling.NEAREST)
    montage.paste("#151711", (x, y, x + 432, y + 128))
    montage.paste("#eee7cb", (x, y), ink.point(lambda a: 255 - a))
    path = ROOT / f"rafael_B170_B176_refined_{ordinal + 1}.png"
    montage.save(path)
    final = previous_sheets.copy()
    final[ordinal] = dict(path=str(path), sha256=base.digest(path))
    return final


verification = checked_text(getsource(previous.verify), {
    'len(entries) == 368 and fe_count == 30': 'len(entries) == 190 and fe_count == 6',
    '    entries, pictures, pagination = [], [], []':
        '    earlier, prior_rows, prior_plans, prior_proof = earlier_display(ctx, image, staged)\n'
        '    entries, reused, new_panels = [], [], []\n'
        '    progressive_ordinal = 0\n'
        '    pagination = earlier["pagination_changes"]',
    '''            elif planned:
                try:
                    layouts, checks = check_progressive(ctx, font, paint, expand, audit, row, body[1:], planned)
                except (ValueError, AssertionError) as error:
                    raise AssertionError((ident, planned["lines"], body)) from error
                entry["layouts"] = []
                entry["original_expansion"] = checks
                count = planned["expected_native_pages"]
                if before.count(b"\\n") >= 4:
                    old_default = stage.TOKEN.sub(lambda m: DEFAULT_NAMES[m[0]], before[1:].decode("ascii")).encode("ascii")
                    old_count = len(paint(ctx.arm, font, old_default)["pages"])
                    if old_count != count:
                        pagination.append(dict(id=ident, previous_pages=old_count, current_pages=count))
                for layout in layouts:
                    hashes = []
                    assert len(layout["pages"]) == count
                    for page_number, page in enumerate(layout["pages"], 1):
                        assert page["native_independent_plane_equal"] and page["all_bitmap_header_input_canaries_exact"]
                        plane = bytes.fromhex(page["native_plane_hex"])
                        pictures.append((f"{ident} {layout['scope']} {page_number}/{count}", plane))
                        hashes.append(native.digest(plane))
                    entry["layouts"].append(dict(scope=layout["scope"], expanded_hex=layout["expanded_hex"],
                                                 lines=layout["lines"], page_sha256=hashes))
                revised_pages += count
                alternate_pages += (len(layouts) - 1) * count''':
        '''            elif planned:
                previous_record = prior_rows[ident]
                prior_command, = previous_record["stored_pages"]
                assert all(prior_command[k] == cmd[k] for k in ("source", "current", "record_ids"))
                count = planned["expected_native_pages"]
                if ident == "DK4_MES_B170_R0206":
                    assert prior_command["stored"] != cmd["stored"] and count == 1 and len(planned["lines"]) == 1
                    (layout,), checks = check_progressive(ctx, font, paint, expand, audit, row, body[1:], planned)
                    page, = layout["pages"]
                    assert page["native_independent_plane_equal"] and page["all_bitmap_header_input_canaries_exact"]
                    plane = bytes.fromhex(page["native_plane_hex"])
                    new_panels.append((progressive_ordinal, plane))
                    entry.update(layouts=[dict(scope=layout["scope"], expanded_hex=layout["expanded_hex"],
                        lines=layout["lines"], page_sha256=[native.digest(plane)])], original_expansion=checks)
                else:
                    assert prior_command["stored"] == cmd["stored"]
                    assert planned == prior_plans[ident] and body.hex() == previous_record["body_hex"]
                    entry.update(layouts=previous_record["layouts"], original_expansion=previous_record["original_expansion"])
                    reused.append(ident)
                revised_pages += count
                alternate_pages += (len(entry["layouts"]) - 1) * count
                progressive_ordinal += len(entry["layouts"]) * count''',
    '''    sheet = prior.precedent.prior.sheet
    make_sheets = FunctionType(sheet.__code__, sheet.__globals__ | {"ROOT": ROOT})
    fresh = make_sheets(pictures, "rafael_B161_B169_progressive", 216)''':
        '    assert len(reused) == 61 and len(new_panels) == 1 and progressive_ordinal == 65\n'
        '    fresh = refresh_sheet(earlier["fresh_sheets"], new_panels)',
    'alternate_name_width_pages=alternate_pages, pagination_changes=pagination, FE_panels=fe_count,':
        'alternate_name_width_pages=alternate_pages, pagination_changes=pagination, FE_panels=fe_count,\n'
        '        rebound_progressive_record_ids=reused, replaced_preview_record_ids=["DK4_MES_B170_R0206"],\n'
        '        earlier_native_display=str(prior_proof),\n'
        '        earlier_native_display_sha256=base.digest(prior_proof),',
})
names = checked_text(getsource(previous.verify_names), {
    '("B161_B165", "B166_B167", "B168_B169")': '("B170_B176",)',
    '    notes[132] = "Officiant matches the registered generic ceremonial role. This speaker formally confers the item, and the exchange gives no specific rank."\n': '',
})
scope = vars(previous) | globals()
for script in (verification, names):
    exec(compile(script, __file__ + "::stored-native-display", "exec"), scope)


if __name__ == "__main__":
    scope["verify"]()
    scope["verify_names"]()
