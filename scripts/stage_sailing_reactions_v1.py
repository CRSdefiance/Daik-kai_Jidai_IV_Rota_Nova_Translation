"""Verify both native portrait consumers for the reviewed sailing reactions."""

from hashlib import sha256
from inspect import getsource
from itertools import product
from pathlib import Path
from types import FunctionType

from dk4tool.patch import mutiny_static_wrap_v1 as guarded, ship_emergency_wrap_v1 as extender
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from scripts import review_sailing_reactions_v1 as editorial
from scripts.native_machine_scoped_v764 import machine
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.review_literal_notice_callers_v1 import current_copy
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_mutiny_review_v1 import compile_layouts, portrait_sheets, render_portrait
from scripts.stage_sailing_alert_review_v1 import crew_case
from scripts.stage_shared_notices_storage_v1 import relocate
from scripts.verify_shared_crew_selector_v1 import ARGS, dispatch


parent, base = editorial.parent, editorial.parent.base
ARM, COMMON, CLEAN, BASE = editorial.ARM, editorial.COMMON, editorial.CLEAN, editorial.BASE
ROOT = Path('out/sailing_reactions_staged_20261111_v1')
ROM, PROOF = ROOT / 'sailing_reactions_RESEARCH_ONLY.nds', ROOT / 'stored_verification.json'
OUTPUT = editorial.OUTPUT
PRIOR = 0x01FFF234
SCOPE = {
    (0x02053DB8, 0x27C): (0x02116C00, 0x02117180, 0x021171C0, 0x02117220, 0x021172A0),
    (0x02053F40, 0x274): (0x02117240, 0x02117280),
}
PHRASES = {
    2359: ('Do you think it wants', 'to get along with us?', 'Maybe it is gentle after all.'),
    2362: ("I'm starting to think", 'the white whale', "doesn't really want", 'to fight people.'),
    2365: ('Think it just wants to play with us?', "Maybe it's gentle after all."),
    2457: ("the wind's picking up.", 'What a relief!'),
    2462: ('Perhaps it only fought because', 'we humans were foolish enough', 'to treat it like a monster...'),
    2463: ('no choice but to fight', 'it was a monster.', 'I feel sorry for it.'),
    2465: ('I wonder if it fights because', 'treat it like a monster.', 'Maybe the poor thing', 'never had a choice...'),
    2466: ('Maybe it only fights because', 'we decided it was a monster.', 'I feel kind of sorry for it...'),
    2467: ('Perhaps people left it no choice', 'but to fight', "I can't help", 'feeling sorry for it...'),
    2468: ('Think it has to fight', "'cause people call it a monster?", 'Poor thing...'),
    2469: ('Admiral, look over there!', "Something's shining!"),
    2470: ('Admiral, over there!', 'Something is shining!'),
    2471: ('Look over there, Admiral!', "Something's shining!"),
    2472: ('Admiral, look over there!', 'See that glint?'),
    2474: ("There's something", 'shining over there!'),
    2476: ('Admiral, the extra armor', 'kept the reef', 'from damaging the ship!'),
    2478: ("we didn't take a scratch", 'with that extra armor!'),
    2479: ('No damage from the reef, Admiral!', 'Good thing we had that extra armor.'),
    2480: ('With that extra armor,', "we don't have to worry", 'about reef damage!'),
    2481: ('The extra armor kept the ship', 'from taking a scratch.', 'It pays to be prepared!'),
    2484: ('the ram shattered the ice.', 'No damage!'),
    2485: ('Admiral, the ram', 'the drift ice.', 'No damage!'),
    2487: ('The ram shattered the ice, Admiral!', 'What a relief.'),
    2489: ('The ram broke up the drift ice.', "We needn't worry", 'about the ship now!'),
    2491: ('Admiral, the ram shattered', 'the drift ice', 'could damage the ship!'),
    2495: ('This looks valuable.', 'Was it worth the price of the map?'),
    2496: ("Now that's something!", 'How about a good meal later?'),
    2497: ("S-so that's the hidden treasure...", 'Pays to live a long life!'),
    2499: ('What magnificent treasure...', 'I never expected this!', "It's all thanks to you, Admiral."),
}


def transform(source, expected_sha):
    assembly = FunctionType(guarded.assembly.__code__, vars(guarded) | {'SCOPE': SCOPE, 'PRIOR': PRIOR})
    native = FunctionType(extender.transform.__code__, vars(extender) | {
        'SOURCE': expected_sha, 'PRIOR': PRIOR, 'assembly': assembly,
    })
    return native(source)


def stage(runtime, release, rows):
    compiler = FunctionType(compile_layouts.__code__, compile_layouts.__globals__ | {
        'PHRASES': {n: phrases for n, phrases in PHRASES.items() if len(rows[n]['english']) > 36},
    })
    storage = compiler(rows)
    wrapped, selector = transform(runtime.arm, release['target_ARM9_sha256'])
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, relocate.__globals__ | {'DIRECTORY': directory})
    common, arm, rebound, allocation = repack(runtime.common, wrapped, rows, storage)
    assert allocation['touched_blocks'] == [25, 26] and allocation['all_41_blocks_fit_8KiB']
    assert arm[:DIRECTORY_OFFSET] == wrapped[:DIRECTORY_OFFSET] and arm[TABLE_END:] == wrapped[TABLE_END:]
    return arm, common, storage, rebound, allocation, selector


def selector_cases(arm, selector):
    cpu = machine(arm)
    code = checked_text(getsource(dispatch), {'count=128': 'count=1024'})
    env = dict(dispatch.__globals__)
    exec(compile(code, __file__ + '::native-selector-coverage', 'exec'), env)
    run = env['dispatch']
    keys = {table + delta for tables in SCOPE.values() for table in tables for delta in (-32, 0, 32)}
    cases = []
    for parent, table, template in product((0x02053DB8, 0x02053F40, 0x02054014), sorted(keys),
                                           (b' A whole phrase\n  Another phrase.', b'Unscoped\nNo guard', b'One row.')):
        offset = 0x27C if parent == 0x02053DB8 else 0x274
        stack = {0x264: parent, 0x274: 0, 0x27C: 0} | {offset: table}
        cpu.mem_write(ARGS[1], template + b'\0')
        target, registers = run(cpu, extender.HOOK, stack, (PRIOR, extender.LITERAL_COPY))
        active = table in SCOPE.get((parent, offset), ()) and b'\n  ' in template
        assert target == (extender.LITERAL_COPY if active else PRIOR) and registers == ARGS
        cases.append(dict(parent=parent, table=table, selected_literal_rows=active))
    assert sum(row['selected_literal_rows'] for row in cases) == 7
    assert selector['previous_selector'] == PRIOR
    return cases


def native_portrait(runtime, row, group):
    if group['original_role_argument'] is not None:
        return crew_case(runtime, row, group, None)
    n = row['message_ID']
    actor_id = next(i for i, _, message in group['original_voice_choices'] if message == n)
    actor = runtime.actor_root + (0x19E4 if actor_id == 3 else 4 + actor_id * 32)
    run = FunctionType(consumer.__code__, consumer.__globals__ | {'portrait_machine': runtime.machine},
                       argdefs=consumer.__defaults__)
    result = run(runtime.arm, runtime.common, runtime.raw, runtime.plan, group['consumer'], actor, group['table'])
    assert bytes(runtime.calls[0].mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    runtime.calls.clear()
    return result | {'offline_direct_actor': actor_id}


def main():
    assert not ROOT.exists()
    draft, release = map(base.load, (OUTPUT, parent.RELEASE))
    runtime = editorial.previous.RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    assert runtime.receipt() == draft['registered_input']
    rows = {row['message_ID']: row for row in draft['records']}
    groups = {n: group for group in draft['native_context'] for n in range(group['first_ID'], group['last_ID'] + 1)}
    assert set(rows) == set(groups) == set(editorial.DECISIONS)
    arm, common, storage, rebound, allocation, selector = stage(runtime, release, rows)
    scope = selector_cases(arm, selector)
    staged = with_components(runtime, arm, common)
    raster, _, _ = font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    records, pages = [], []
    for n, row in rows.items():
        text = storage[n]
        lookup = current_copy(staged, row | {'current_hex': text.hex()}, BASE + 0x5528C)
        staged.calls.clear()
        native = native_portrait(staged, row, groups[n])
        assert bytes.fromhex(native['input_hex']) == text
        display = bytes.fromhex(native['formatted_hex'])
        assert b' '.join(display.split()).decode('ascii') == row['english']
        if b'\n' in text:
            assert display == text
        lines = [line.strip() for line in display.decode('ascii').split('\n')]
        assert all(any(phrase in line for line in lines) for phrase in PHRASES.get(n, ()))
        pixels, glyphs = render_portrait(raster, arm, kanji, display)
        assert ''.join(chr(g['code']) for g in glyphs) == row['english'].replace(' ', '')
        records.append(dict(message_ID=n, source_reference=row['source_reference'], previous_reference=row['current_reference'],
            staged_reference=editorial.previous.reference(rebound[n]), original_stored_lookup=lookup,
            native=native, staged_hex=text.hex(), display_hex=display.hex(), visible_lines=lines,
            complete_glyphs=len(glyphs), native_ink_sha256=sha256(pixels).hexdigest()))
        pages.append((n, pixels))
    image = NdsImage.open(runtime.rompath)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    target = bytes(image.rom.save())
    image.replace_file(ARM, runtime.arm)
    image.replace_file(COMMON, runtime.common)
    assert bytes(image.rom.save()) == Path(runtime.rompath).read_bytes()
    ROOT.mkdir()
    with ROM.open('xb') as stream:
        stream.write(target)
    sheets = portrait_sheets(ROOT, pages)
    base.save(PROOF, dict(registered_input=runtime.receipt(), research_ROM=str(ROM), research_ROM_sha256=base.digest(ROM),
        research_ARM9_sha256=sha256(arm).hexdigest(), research_COMMON_sha256=sha256(common).hexdigest(),
        allocation=allocation, ownership=selector, selector_scope=scope, parent_inverse_exact=True,
        records=records, sheets=sheets, manuscript_sha256=base.digest(OUTPUT), native_pages=len(pages),
        formatting_pending_visual_review=True, gameplay_pending=True, new_credit=0, full_goal_complete=False))
    print(f'{len(records)} native portraits and loader cases passed. {len(scope)} scoped selector checks.')


if __name__ == '__main__':
    main()
