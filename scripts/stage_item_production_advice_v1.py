"""Stage and verify the native portrait layouts for production and voyage advice."""

from hashlib import sha256
from inspect import getsource
from pathlib import Path
from types import FunctionType

from dk4tool.patch.item_production_advice_v1 import LAST, LITERAL_COPY, PARENT, PRIOR, STACK_KEY, transform
from dk4tool.patch.ship_emergency_wrap_v1 import HOOK
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from scripts import review_item_production_advice_v1 as review
from scripts import stage_mutiny_review_v1 as portrait
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.native_machine_scoped_v764 import machine
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.review_literal_notice_callers_v1 import current_copy
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_shared_notices_storage_v1 import relocate
from scripts.verify_shared_crew_selector_v1 import ARGS, dispatch


ROOT = Path('out/item_production_advice_staged_20261111_v1')
ROM = ROOT / 'item_production_advice_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
PHRASES = {
    3033: ("There's a good chance", 'around the North Sea, too.'),
    3034: ('would do well', 'around the Mediterranean.'),
    3035: ('in the tropics', 'the New World or Africa, too.'),
    3036: ('from Mediterranean flowers', 'must taste good too.'),
    3037: ('shark fins in China', 'shark eggs around the Black Sea,', 'beyond the Mediterranean.'),
    3038: ('the perfect climate', 'for growing pepper.'),
    3039: ('Cloves should thrive', 'The Mediterranean, though?', 'We might have trouble there.'),
    3040: ("We'd make a fortune", 'if we could grow cinnamon', 'in the Mediterranean.'),
    3041: ('sell this spice in Africa...',),
    3042: ('The New World', 'well suited to growing coffee.'),
    3043: ('grow tea in Africa, too.',),
    3044: ('needs tropical conditions', 'try taking it to Africa?'),
    3045: ('grow and sell this', 'in the Mediterranean.', 'Might make us rich, too.'),
    3046: ('turn African ore', 'into a new trade good.'),
    3047: ('in Africa and East Asia.',),
    3048: ("East Asia's main trade goods.",),
    3049: ('the North Sea and Mediterranean', 'plenty of room to grow.'),
    3050: ('find pearls in East Asia too.',),
    3051: ('unusual herbal remedies in China.',),
    3052: ('all sorts of unusual fruit.', 'from the peel of this one.'),
    3053: ('If rats get aboard,', 'come in mighty handy.'),
    3054: ("I wouldn't set sail", 'to ward off scurvy.'),
    3055: ('No sailor can defy the weather.', 'to come in handy.'),
    3056: ('A marvel of Eastern medicine.', 'especially well', 'against infectious diseases.'),
}


def check_selector(arm, storage):
    cpu = machine(arm)
    source = checked_text(getsource(dispatch), {'count=128': 'count=1024'})
    env = dict(dispatch.__globals__)
    exec(compile(source, __file__ + '::guarded-selector', 'exec'), env)
    run = env['dispatch']
    results = []
    for parent, key, template, accepted in (
        *((PARENT, n, value, b'\n' in value) for n, value in storage.items()),
        (PARENT, review.FIRST - 1, storage[review.FIRST], False),
        (PARENT, LAST + 1, storage[LAST], False),
        (0x02053F40, review.FIRST, storage[review.FIRST], False),
        (PARENT, review.FIRST, b' Unprotected row\nNo guard', False),
        (PARENT, review.FIRST, b'\0', False),
    ):
        cpu.mem_write(ARGS[1], template + b'\0')
        destination, registers = run(cpu, HOOK, {0x264: parent, STACK_KEY: key}, (PRIOR, LITERAL_COPY))
        assert destination == (LITERAL_COPY if accepted else PRIOR) and registers == ARGS
        results.append(dict(parent=parent, key=key, stored_template_hex=template.hex(), destination=destination))
    return results


def stage(release, runtime, rows):
    compiler = FunctionType(portrait.compile_layouts.__code__, portrait.compile_layouts.__globals__ | {
        'PHRASES': {n: phrases for n, phrases in PHRASES.items() if len(rows[n]['english']) > 36},
    })
    storage = compiler(rows)
    wrapped, selector = transform(runtime.arm, release['target_ARM9_sha256'])
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    pack = FunctionType(relocate.__code__, relocate.__globals__ | {'DIRECTORY': directory})
    common, arm, rebound, packing = pack(runtime.common, wrapped, rows, storage)
    assert packing['all_41_blocks_fit_8KiB'] and packing['touched_blocks'] == [33, 34]
    assert arm[:DIRECTORY_OFFSET] == wrapped[:DIRECTORY_OFFSET] and arm[TABLE_END:] == wrapped[TABLE_END:]
    return arm, common, storage, rebound, packing, selector


def main():
    assert not ROOT.exists()
    manuscript, release = load(review.OUTPUT), load(review.RELEASE)
    runtime = review.RegisteredRuntime(review.RELEASE, release['own_registered_startup'], captain=3)
    assert manuscript['registered_input'] == runtime.receipt()
    rows = {row['message_ID']: row for row in manuscript['records']}
    assert tuple(rows) == review.IDS
    arm, common, storage, rebound, allocation, selector = stage(release, runtime, rows)
    dispatches = check_selector(arm, storage)
    staged = with_components(runtime, arm, common)
    raster, _, _ = font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    lookups, cases, pages = [], [], []
    for n, row in rows.items():
        raw = storage[n]
        lookup = current_copy(staged, row | {'current_hex': raw.hex()}, review.BASE + 0x5528C)
        staged.calls.clear()
        lookups.append(dict(message_ID=n, source_reference=row['source_reference'], previous_reference=row['current_reference'],
                            staged_reference=review.reference(rebound[n]), original_stored_lookup=lookup))
        group = dict(consumer=review.DISPATCH, table=n, original_role_argument=None)
        planes = []
        for actor in review.ADVISERS:
            native = portrait.portrait_case(staged, row, group, raw, actor)
            display = native.pop('display')
            assert display == raw and b' '.join(display.split()).decode('ascii') == row['english'], (n, display)
            pixels, glyphs = portrait.render_portrait(raster, arm, kanji, display)
            lines = [line.strip() for line in display.decode('ascii').split('\n')]
            assert ''.join(chr(glyph['code']) for glyph in glyphs) == row['english'].replace(' ', ''), (n, glyphs)
            assert all(any(phrase in line for line in lines) for phrase in PHRASES.get(n, ()))
            planes.append(pixels)
            cases.append(dict(message_ID=n, actor_ID=actor, visible_lines=lines, display_hex=display.hex(),
                              native_ink_sha256=sha256(pixels).hexdigest(), complete_glyphs=len(glyphs), **native))
        assert planes[0] == planes[1]
        pages.append((f'{n}  {row["item_name"]}', planes[0]))

    image = NdsImage.open(runtime.rompath)
    image.replace_file(review.ARM, arm)
    image.replace_file(review.COMMON, common)
    target = bytes(image.rom.save())
    image.replace_file(review.ARM, runtime.arm)
    image.replace_file(review.COMMON, runtime.common)
    assert bytes(image.rom.save()) == Path(runtime.rompath).read_bytes()
    ROOT.mkdir()
    with ROM.open('xb') as stream:
        stream.write(target)
    sheets = portrait.portrait_sheets(ROOT, pages)
    saved = NdsImage.open(ROM)
    assert saved.read_file(review.ARM) == arm and saved.read_file(review.COMMON) == common
    save(PROOF, dict(registered_input=runtime.receipt(), research_ROM=str(ROM), research_ROM_sha256=digest(ROM),
        research_ARM9_sha256=sha256(arm).hexdigest(), research_COMMON_sha256=sha256(common).hexdigest(),
        parent_inverse_exact=True, compiler_owned_phrase_wrap=True, native_selector_cases=dispatches,
        allocation=allocation, ownership=selector, native_original_copies=lookups, native_display_cases=cases,
        sheets=sheets, formatting_pending_visual_review=True, gameplay_pending=True, registered_release_pending=True,
        manuscript_sha256=digest(review.OUTPUT), new_credit=0, full_goal_complete=False))
    print(f'Checked {len(cases)} native portrait cases and {len(lookups)} original loader copies.')


if __name__ == '__main__':
    main()
