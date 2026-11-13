"""Stage and verify the native item descriptions and coin response."""

import json
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from types import FunctionType

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from dk4tool.patch import source_item_cards_and_coin_v1 as patch
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from scripts import stage_rumor_and_cooperation_v1 as prior
from scripts.audit_story_glyph_consistency import load, save
from scripts.bind_shachihoko_description_consumers_v6092b import collect
from scripts.current_item_detail_machine_v20261111 import make_execute
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.probe_item_parent_crops import verify as parent_crops
from scripts.prove_shachihoko_detail_fonts_v6101d import oracle
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_source_item_cards_and_coin_v1 import ARM, COIN, COMMON, GETTER, IDS, OUTPUT, RELEASE, item_table, reference
from scripts.verify_item_interface_research import expected_draws, glyph_codes
from scripts.verify_item_parent_layout import EXPECTED, compose


ROOT = Path('out/source_item_cards_and_coin_staged_20261111_v1')
ROM = ROOT / 'source_item_cards_and_coin_RESEARCH_ONLY.nds'
PREP = ROOT / 'staged_build.json'
PROOF = ROOT / 'stored_verification.json'
ITEM_PLAN = Path('work/analysis/item_interface_plan.json')
AMENDMENTS = {
    2817: dict(english='This tree grows in Southeast Asia. Its sweet, fragrant fruit turns yellow when ripe enough to eat.',
               localization_note='Keep the place name, the fruit qualities and yellow color when ripe and edible.'),
    2825: dict(english='A southern Chinese tree with long oval leaves fermented for tea. Flavor varies by plant part and degree of fermentation.',
               localization_note='Keep the origin, leaf shape, preparation and both causes of flavor differences in three rows.'),
    2831: dict(english='Worked by hand and foot, this loom weaves fabric by interlacing threads.',
               localization_note='Keep the physical operation together and describe the interlacing of threads in natural English.'),
}


def active_rows(manuscript):
    return FunctionType(prior.active_rows.__code__, vars(prior) | {'AMENDMENTS': AMENDMENTS})(manuscript)


def build(arm, common, rows):
    assert tuple(rows) == IDS
    payload, table, pointers = item_table(arm)
    wrapped, coin_owner = patch.coin_wrapper(arm)
    wrapped, owner = patch.extend_item_payload(wrapped, list(rows.values())[1:], table, pointers, payload)
    storage = {n: row['english'].encode('ascii') for n, row in rows.items()}
    directory = sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    pack = FunctionType(prior.relocate.__code__, prior.relocate.__globals__ | {'DIRECTORY': directory})
    new_common, new_arm, rebound, allocation = pack(common, wrapped, rows, storage)
    assert allocation['all_41_blocks_fit_8KiB']
    assert new_arm[:DIRECTORY_OFFSET] == wrapped[:DIRECTORY_OFFSET] and new_arm[TABLE_END:] == wrapped[TABLE_END:]
    return new_arm, new_common, rebound, allocation, owner | {'coin_portrait': coin_owner}


def stage():
    assert not ROOT.exists()
    manuscript, release = map(load, (OUTPUT, RELEASE))
    assert all(digest(path) == value for path, value in manuscript['evidence'].items())
    assert digest(release['candidate']) == release['candidate_sha256']
    image = NdsImage.open(release['candidate'])
    before_arm, before_common = image.read_file(ARM), image.read_file(COMMON)
    assert sha256(before_arm).hexdigest() == release['target_ARM9_sha256']
    assert sha256(before_common).hexdigest() == release['target_COMMON_sha256']
    arm, common, rebound, allocation, ownership = build(before_arm, before_common, active_rows(manuscript))
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    output = bytes(image.rom.save())
    image.replace_file(ARM, before_arm)
    image.replace_file(COMMON, before_common)
    assert bytes(image.rom.save()) == Path(release['candidate']).read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(output)
    saved = NdsImage.open(ROM)
    assert saved.read_file(ARM) == arm and saved.read_file(COMMON) == common
    save(PREP, dict(registered_input=manuscript['registered_input'], research_ROM=str(ROM), research_ROM_sha256=digest(ROM),
        research_ARM9_sha256=sha256(arm).hexdigest(), research_COMMON_sha256=sha256(common).hexdigest(),
        records=[dict(message_ID=n, source=row['source_reference'], previous=row['current_reference'],
            stored=reference(rebound[n]), stored_hex=rebound[n].text.hex()) for n, row in active_rows(manuscript).items()],
        parent_inverse_exact=True, ownership=ownership, storage=allocation, editorial_amendments=AMENDMENTS,
        evidence={str(p): digest(p) for p in (OUTPUT, RELEASE, Path(patch.__file__), Path(__file__))}))
    print(f'Built the staged item ROM. Copied payload is {ownership["new_payload_bytes"]} bytes.')


def sheets(pictures):
    result = []
    for first in range(0, len(pictures), 8):
        subset = pictures[first:first + 8]
        sheet = Image.new('RGB', (1000, 390 * (len(subset) // 2)), '#263238')
        draw = ImageDraw.Draw(sheet)
        for i, (label, panel) in enumerate(subset):
            x, y = 500 * (i % 2), 390 * (i // 2)
            draw.text((x + 6, y + 4), label, fill='white')
            sheet.paste(panel.resize((480, 360), Image.Resampling.NEAREST), (x + 6, y + 24))
        path = ROOT / f'item_sheet_{first // 8 + 1:02}.png'
        sheet.save(path)
        result.append(dict(path=str(path), sha256=digest(path), messages=[label for label, _ in subset]))
    return result


def offline():
    prepared, manuscript, release = map(load, (PREP, OUTPUT, RELEASE))
    assert digest(ROM) == prepared['research_ROM_sha256'] and not PROOF.exists()
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    assert manuscript['registered_input'] == runtime.receipt()
    image = NdsImage.open(ROM)
    arm, common = image.read_file(ARM), image.read_file(COMMON)
    clone = with_components(runtime, arm, common)
    # The fresh cold boot checks the actual copied bytes separately. This
    # offline loader model uses the exact prepared pool on the verified snapshot.
    payload = bytes(MainCodeFile(arm, BASE).sections[3].data[:-48])
    at = POOL - BASE
    assert len(payload) == cache_plan(arm)['payload_bytes']
    clone.raw = clone.raw[:at] + payload + clone.raw[at + len(payload):]
    before_items, after_items = (state.execute(collect, GETTER) for state in (runtime, clone))
    item_plans = {row['item_ID']: row for row in prepared['ownership']['item_paragraphs']}
    for before, after in zip(before_items['cases'], after_items['cases'], strict=True):
        ident = after['item_ID']
        if ident in item_plans:
            selected = item_plans[ident]
            assert after['pointer'] == selected['new_pointer']
            assert after['terminated_rows_hex'] == [row.encode('ascii').hex() for row in selected['compiled_rows']]
        else:
            assert after == before

    rows = active_rows(manuscript)
    for n, row in rows.items():
        raw = row['english'].encode('ascii')
        prior.current_copy(clone, row | {'current_hex': raw.hex()}, BASE + 0x5528C)
        clone.calls.clear()
    font = image.read_file('/GRP/KANJI.FNT')
    raster, _, font_contract = prior.font_tools(image)
    coin = rows[COIN]
    stored_coin = coin['english'].encode('ascii')
    coin_case = prior.renderer()(clone, coin, dict(consumer=0x02053FE4, table=COIN, original_role_argument=None),
                                 stored_coin, 24, ())
    display = coin_case.pop('display')
    assert b' '.join(display.split()) == stored_coin
    plane, glyphs = prior.portrait.render_portrait(raster, arm, font, display)
    assert [chr(glyphs[i]['code']) for i in (0, -1)] == [coin['english'][0], coin['english'][-1]]
    coin_case.update(message_ID=COIN, arguments=[], lines=display.decode('ascii').splitlines(),
                     exact_display_hex=display.hex(), native_ink_sha256=sha256(bytes(pixel == 1 for pixel in plane)).hexdigest(),
                     native_glyphs=len(glyphs))
    coin_sheets = prior.portrait.portrait_sheets(ROOT, [(str(COIN), plane)])

    execute = make_execute(prepared['storage']['new_directory_sha256'], arm)
    expected, _ = oracle()
    parent = parent_crops(arm)
    assert [(row['source_origin'], row['size'], row['destination_origin']) for row in parent['requests']] == EXPECTED
    catalogue = deepcopy(load(ITEM_PLAN))
    cases, pictures = [], []
    for ident, item in item_plans.items():
        catalogue['item_advice_projection'][ident].update(logical=rows[item['message_ID']]['english'],
            compiled='\n'.join(item['compiled_rows']), pointer=item['new_pointer'])
        for page, config in (('main', (0, 4)), ('standalone', (0, 1))):
            for mode in (4, 16):
                native = execute(arm, 'fixture', item_page=page, item_case=config, surface_size=(240, 96),
                                 kanji_font=font, mode=mode, item_resource_index=ident, item_common=common)
                draws = expected_draws(arm, catalogue, page, config, item_index=ident)
                assert native['item_draws'] == draws, (ident, page, native['item_draws'], draws)
                codes = [code for draw in draws for code in glyph_codes(draw['text'], draw['tracking'])]
                assert [row['code'] for row in native['glyph_events']] == codes
                assert native['pixels'] == expected(arm, font, native['glyph_events'], mode, background=0), (ident, page, mode)
                lines = [draw['text'] for draw in draws if (36 if page == 'main' else 24) <= draw['y'] < 84]
                assert lines == item['compiled_rows'] and native['item_actual_common_ids'] == [item['message_ID']]
                assert all(0 <= row['x'] <= 234 and 0 <= row['y'] <= 84 for row in native['glyph_events'])
                composed, cells = compose(native, parent['requests']) if page == 'main' else (None, [])
                cases.append(dict(message_ID=item['message_ID'], item_ID=ident, page=page, mode=mode, lines=lines,
                    native_ink_sha256=sha256(native['pixels']).hexdigest(), native_glyphs=len(codes),
                    original_parent_complete_glyphs=len(cells), full_native_and_independent_pixels=True, draws=draws))
                if mode == 16:
                    from struct import unpack
                    panel = Image.new('RGB', (256, 192))
                    pixels = unpack('<49152H', composed or native['pixels'])
                    panel.putdata([(231, 223, 202) if c == 0 else (121, 112, 99) if c == 14 else (13, 14, 12) for c in pixels])
                    pictures.append((f'{ident:02d}  {rows[item["message_ID"]]["item_name"]}  {page}', panel))
    assert len(cases) == 80 and len(pictures) == 40
    selector = FunctionType(prior.check_selector.__code__, vars(prior) | vars(patch))(arm)
    save(PROOF, prepared | dict(native_portrait_cases=[coin_case], item_cases=cases, selector_cases=selector,
        all_218_native_item_description_getters_checked=True, untouched_item_descriptions_exact=198,
        native_PARENT_crop_contract=parent, font_contract=font_contract,
        sheets=coin_sheets + sheets(pictures),
        evidence=prepared['evidence'] | {str(p): digest(p) for p in (PREP, ITEM_PLAN, Path(make_execute.__code__.co_filename))}))
    print('80 native item renders, one portrait, and all 218 description lookups passed.')


if __name__ == '__main__':
    import sys
    assert sys.argv[1:] in (['build'], ['offline'])
    (stage if sys.argv[1] == 'build' else offline)()

