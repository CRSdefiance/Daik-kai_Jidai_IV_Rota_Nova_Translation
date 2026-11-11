"""Stage and verify both native views of the utility and weapon item descriptions."""

from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from struct import unpack
from types import FunctionType, SimpleNamespace

from ndspy.code import MainCodeFile
from PIL import Image

from dk4tool.patch import utility_weapon_item_cards_v1 as patch
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from scripts import stage_rumor_and_cooperation_v1 as dialogue
from scripts import stage_source_item_cards_and_coin_v1 as prior
from scripts import verify_source_item_cards_offline_v2 as model
from scripts.audit_story_glyph_consistency import load, save
from scripts.bind_shachihoko_description_consumers_v6092b import collect
from scripts.current_item_detail_machine_v20261111 import make_execute
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.prove_shachihoko_detail_fonts_v6101d import oracle
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_utility_weapon_item_cards_v1 import ARM, COMMON, GETTER, IDS, OUTPUT, RELEASE, item_table, reference
from scripts.verify_item_interface_research import expected_draws, glyph_codes
from scripts.verify_item_parent_layout import EXPECTED, compose


ROOT = Path('out/utility_weapon_item_cards_staged_20261111_v1')
ROM = ROOT / 'utility_weapon_item_cards_RESEARCH_ONLY.nds'
PREP = ROOT / 'staged_build.json'
PROOF = ROOT / 'stored_verification.json'
AMENDMENTS = {
    2836: ('Squeeze this magic lime as often as you like. It always yields juice to quench the crew’s thirst at sea.',
           'Use two natural sentences and keep both the inexhaustible juice and its benefit at sea.'),
    2837: ('This mystic ring holds the soul of Hermes, travel god and one of the twelve Olympians. It’s said to protect sailors in storms.',
           'Preserve the mystery of the ring, Hermes’s place among the Twelve and his protection against storms.'),
    2838: ('Made by a method from Hua Tuo, a famed physician of China’s Three Kingdoms era. A tiny dose is said to cure any contagious disease.',
           'Keep the claim attributed and the method tied to the renowned Chinese physician.'),
    2842: ('Its S-shaped blade gleams like a golden crescent moon.',
           'Keep the shape, golden gleam and moon image together.'),
    2843: ('An ornate curved sword regarded as the mark of a hero.',
           'Keep the traditional association with heroism and leave how the sword is displayed unstated.'),
    2847: ('At first glance, it’s just an old sword. An admiral who swept pirates from nearby waters is said to have prized it.',
           'Restore the plain first impression and the admiral’s attachment to the blade.'),
    2848: ('A broad crescent blade. A fleet deputy is said to have struck down a sailor on the spot for urging betrayal of the admiral.',
           'Preserve the fleet deputy and leave the target of the sailor’s urging unspecified.'),
    2851: ('This crescent blade has a red tint that brings to mind all the blood it has spilled.',
           'Keep the image of past bloodshed tied to the blade’s color.'),
    2853: ('Zhao Yun, a famed Shu general of the Three Kingdoms era, is said to have used this spear. He was best with a spear.',
           'Restore Zhao Yun’s role and preserve the traditional attribution.'),
    2854: ('An error in a general’s plans cost a close ally’s life. He gave this superb sword to the family as an apology.',
           'Keep the general’s responsibility, the gift to the family and its purpose clear.'),
    2855: ('A red-haired woman pirate famed for her beauty used this sword. It’s prized as a treasure and for its keen edge.',
           'Restore the pirate’s identity and keep both the blade’s keen edge and value as a treasure.'),
    2860: ('The Mongol hero Kublai Khan wielded this superb greatsword. It strikes with tremendous force from above.',
           'Keep the named owner and both observations about the sword.'),
}


def active_rows(manuscript):
    updates = {
        ident: dict(english=text.replace('’', "'"), localization_note=note)
        for ident, (text, note) in AMENDMENTS.items()
    }
    return FunctionType(dialogue.active_rows.__code__, vars(dialogue) | {'AMENDMENTS': updates})(manuscript)


def build(arm, common, rows):
    assert tuple(rows) == IDS
    payload, table, pointers = item_table(arm)
    wrapped, owner = patch.transform(arm, list(rows.values()), table, pointers, payload)
    directory = sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    relocate = FunctionType(dialogue.relocate.__code__, dialogue.relocate.__globals__ | {'DIRECTORY': directory})
    storage = {n: row['english'].encode('ascii') for n, row in rows.items()}
    new_common, new_arm, rebound, allocation = relocate(common, wrapped, rows, storage)
    assert allocation['all_41_blocks_fit_8KiB']
    assert new_arm[:DIRECTORY_OFFSET] == wrapped[:DIRECTORY_OFFSET] and new_arm[TABLE_END:] == wrapped[TABLE_END:]
    return new_arm, new_common, rebound, allocation, owner


def stage():
    assert not ROOT.exists()
    manuscript, release = map(load, (OUTPUT, RELEASE))
    assert all(digest(path) == expected for path, expected in manuscript['evidence'].items())
    assert digest(release['candidate']) == release['candidate_sha256']
    image = NdsImage.open(release['candidate'])
    old_arm, old_common = image.read_file(ARM), image.read_file(COMMON)
    assert sha256(old_arm).hexdigest() == release['target_ARM9_sha256']
    assert sha256(old_common).hexdigest() == release['target_COMMON_sha256']
    rows = active_rows(manuscript)
    arm, common, rebound, allocation, owner = build(old_arm, old_common, rows)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    output = bytes(image.rom.save())
    image.replace_file(ARM, old_arm)
    image.replace_file(COMMON, old_common)
    assert bytes(image.rom.save()) == Path(release['candidate']).read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(output)
    saved = NdsImage.open(ROM)
    assert saved.read_file(ARM) == arm and saved.read_file(COMMON) == common
    save(PREP, dict(registered_input=manuscript['registered_input'], research_ROM=str(ROM),
        research_ROM_sha256=digest(ROM), research_ARM9_sha256=sha256(arm).hexdigest(),
        research_COMMON_sha256=sha256(common).hexdigest(), parent_inverse_exact=True,
        records=[dict(message_ID=n, source=row['source_reference'], previous=row['current_reference'],
                      stored=reference(rebound[n]), stored_hex=rebound[n].text.hex()) for n, row in rows.items()],
        ownership=owner, storage=allocation, editorial_amendments=AMENDMENTS,
        evidence={str(p): digest(p) for p in (OUTPUT, RELEASE, Path(patch.__file__), Path(__file__))}))
    print(f'{len(rows)} cards staged with the original copied allocation and exact parent inverse.')


def native_getters(runtime, clone, prepared):
    at = POOL - BASE
    payload = bytes(MainCodeFile(clone.arm, BASE).sections[3].data[:-48])
    assert len(payload) == cache_plan(clone.arm)['payload_bytes']
    clone.raw = clone.raw[:at] + payload + clone.raw[at + len(payload):]
    before, after = (state.execute(collect, GETTER)['cases'] for state in (runtime, clone))
    plans = {row['item_ID']: row for row in prepared['ownership']['item_paragraphs']}
    assert len(before) == len(after) == 218
    for old, new in zip(before, after, strict=True):
        plan = plans.get(new['item_ID'])
        if plan:
            assert new['pointer'] == plan['new_pointer']
            assert new['terminated_rows_hex'] == [row.encode('ascii').hex() for row in plan['compiled_rows']]
        else:
            assert new == old
    return plans


def offline():
    prepared, manuscript, release = map(load, (PREP, OUTPUT, RELEASE))
    assert digest(ROM) == prepared['research_ROM_sha256'] and not PROOF.exists()
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    assert manuscript['registered_input'] == runtime.receipt()
    image = NdsImage.open(ROM)
    arm, common = image.read_file(ARM), image.read_file(COMMON)
    clone = with_components(runtime, arm, common)
    plans = native_getters(runtime, clone, prepared)
    rows = active_rows(manuscript)
    for n, row in rows.items():
        dialogue.current_copy(clone, row | {'current_hex': row['english'].encode('ascii').hex()}, BASE + 0x5528C)
        clone.calls.clear()
    font = image.read_file('/GRP/KANJI.FNT')
    assert font == NdsImage.open(release['candidate']).read_file('/GRP/KANJI.FNT')
    execute = make_execute(prepared['storage']['new_directory_sha256'], arm)
    expected, _ = oracle()
    parent = FunctionType(model.parent_crops.__code__, vars(model) | {
        'stage': SimpleNamespace(ROM=ROM, NdsImage=NdsImage),
    })(arm)
    assert [(row['source_origin'], row['size'], row['destination_origin']) for row in parent['requests']] == EXPECTED
    catalogue = deepcopy(load(prior.ITEM_PLAN))
    cases, pictures = [], []
    for ident, item in plans.items():
        row = rows[item['message_ID']]
        catalogue['item_advice_projection'][ident].update(logical=row['english'],
            compiled='\n'.join(item['compiled_rows']), pointer=item['new_pointer'])
        for page, config in (('main', (0, 4)), ('standalone', (0, 1))):
            for mode in (4, 16):
                native = execute(arm, 'fixture', item_page=page, item_case=config, surface_size=(240, 96),
                                 kanji_font=font, mode=mode, item_resource_index=ident, item_common=common)
                draws = expected_draws(arm, catalogue, page, config, item_index=ident)
                assert native['item_draws'] == draws
                codes = [code for draw in draws for code in glyph_codes(draw['text'], draw['tracking'])]
                assert [glyph['code'] for glyph in native['glyph_events']] == codes
                assert native['pixels'] == expected(arm, font, native['glyph_events'], mode, background=0)
                lines = [draw['text'] for draw in draws if (36 if page == 'main' else 24) <= draw['y'] < 84]
                assert lines == item['compiled_rows'] and native['item_actual_common_ids'] == [item['message_ID']]
                assert ' '.join(lines) == row['english']
                assert all(0 <= glyph['x'] <= 234 and 0 <= glyph['y'] <= 84 for glyph in native['glyph_events'])
                composed, cells = compose(native, parent['requests']) if page == 'main' else (None, [])
                cases.append(dict(message_ID=item['message_ID'], item_ID=ident, page=page, mode=mode,
                    lines=lines, native_ink_sha256=sha256(native['pixels']).hexdigest(), native_glyphs=len(codes),
                    original_parent_complete_glyphs=len(cells), full_native_and_independent_pixels=True, draws=draws))
                if mode == 16:
                    panel = Image.new('RGB', (256, 192))
                    pixels = unpack('<49152H', composed or native['pixels'])
                    panel.putdata([(231, 223, 202) if c == 0 else (121, 112, 99) if c == 14 else (13, 14, 12) for c in pixels])
                    pictures.append((f'{ident:02d}  {row["item_name"]}  {page}', panel))
    assert len(cases) == 4 * len(IDS) and len(pictures) == 2 * len(IDS)
    sheets = FunctionType(prior.sheets.__code__, vars(prior) | {'ROOT': ROOT})(pictures)
    save(PROOF, prepared | dict(item_cases=cases, all_218_native_item_description_getters_checked=True,
        untouched_item_descriptions_exact=218 - len(IDS), native_PARENT_crop_contract=parent, sheets=sheets,
        evidence=prepared['evidence'] | {str(p): digest(p) for p in (PREP, prior.ITEM_PLAN, Path(make_execute.__code__.co_filename))}))
    print(f'{len(cases)} native renders and all 218 item-description getters passed.')


if __name__ == '__main__':
    import sys
    assert sys.argv[1:] in (['build'], ['offline'])
    (stage if sys.argv[1] == 'build' else offline)()
