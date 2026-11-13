"""Check every reviewed crew item-action reply in its original portrait consumer."""

from hashlib import sha256
from pathlib import Path
from types import FunctionType

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from scripts import review_crew_item_actions_v1 as review
from scripts import stage_sailing_reactions_v1 as prior
from scripts import stage_sea_event_review_v1 as portrait
from scripts import stage_ship_emergency_review_v1 as selector_checks
from scripts.source_locked_derivation_v5118 import checked_text
from inspect import getsource


ARM, COMMON, BASE = review.ARM, review.COMMON, review.BASE
ROOT = Path('out/crew_item_actions_staged_20261111_v1')
ROM = ROOT / 'crew_item_actions_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
PHRASES = {
    2500: ("Admiral, I can't do my job", 'if you take that away.'),
    2501: ('if you take that away,', "I won't be able to do my job."),
    2502: ("I can't do my job without that.",),
    2503: ("I can't do my job", 'if you take that away.'),
    2504: ("I won't be able to do my job", 'if you take that!'),
    2506: ('use it now, do we?',),
    2508: ('need it right now, though...',),
    2513: ('How do you use this?', 'Looks like nobody knows.'),
    2514: ('Seems no one knows', 'how to use it.'),
    2515: ('How does it work?', 'Nobody seems to know.'),
    2518: ('let your anger pass, I beg you!',),
    2524: ('If you dismiss all the sailors,', "we can't sail!"),
    2525: ('If you fire every sailor,', "we can't sail!"),
    2526: ("We can't sail the ship", 'if you dismiss every sailor!'),
    2527: ('dismiss all the sailors,', "the ship won't go anywhere!"),
    2528: ('if you let everyone go?', "I can't do it alone!"),
}


def stage(runtime, release, rows, groups):
    compiler = FunctionType(prior.compile_layouts.__code__, prior.compile_layouts.__globals__ | {
        'PHRASES': {n: phrases for n, phrases in PHRASES.items() if len(rows[n]['english']) > 36},
    })
    stored = compiler({n: row for n, row in rows.items() if not row['original_substitution_count']})
    stored.update({n: row['english'].encode('ascii') for n, row in rows.items()
                   if row['original_substitution_count']})
    static, dynamic = {}, {}
    for group in groups:
        ids = range(group['first_ID'], group['last_ID'] + 1)
        scope = dynamic if group['runtime_item_name_inputs'] else static
        if scope is static and not any(b'\n' in stored[n] for n in ids):
            continue
        for caller in group['native_callers']:
            key = portrait.PARENTS[caller['consumer'] - BASE]
            if group['table'] not in scope.get(key, ()):
                scope[key] = (*scope.get(key, ()), group['table'])
    latest = release['target_ARM9_sha256']
    predecessor = review.prior.load(review.parent.VERIFICATION / 'stored_verification.json')['ownership']['selector']
    selector = prior.extender
    parameters = {'STATIC': static, 'DYNAMIC': dynamic, 'PRIOR': predecessor}
    assemble = FunctionType(selector.assembly.__code__, vars(selector) | parameters)
    transform = FunctionType(selector.transform.__code__, vars(selector) | parameters | {
        'assembly': assemble, 'SOURCE': latest,
    })
    wrapped, ownership = transform(runtime.arm)
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(prior.relocate.__code__, prior.relocate.__globals__ | {'DIRECTORY': directory})
    common, arm, rebound, allocation = repack(runtime.common, wrapped, rows, stored)
    assert allocation['touched_blocks'] == [26, 27] and allocation['all_41_blocks_fit_8KiB']
    assert arm[:DIRECTORY_OFFSET] == wrapped[:DIRECTORY_OFFSET] and arm[TABLE_END:] == wrapped[TABLE_END:]
    source = checked_text(getsource(selector_checks.verify_scope), {
        'scope = DYNAMIC | STATIC': 'scope = {key: DYNAMIC.get(key, ()) + STATIC.get(key, ()) for key in DYNAMIC.keys() | STATIC.keys()}',
        'offsets = (0x274, 0x27C)': 'offsets = (0x270, 0x274, 0x27C)',
    })
    env = vars(selector_checks) | parameters
    exec(compile(source, __file__ + '::verify-scoped-dispatch', 'exec'), env)
    checks = env['verify_scope'](arm)
    return arm, common, stored, rebound, allocation, ownership | {
        'literal_scopes': list(static.items()), 'dynamic_scopes': list(dynamic.items()), 'selector_checks': checks,
    }


def native_displays(ctx, row, group, storage):
    number = row['message_ID']
    native_group = dict(table=group['table'], selector=group['table'], original_role_argument=1,
                        original_actor_voice_choices=group['original_voice_choices'])
    calls = {caller['consumer']: caller for caller in group['native_callers']}
    if BASE + review.CAPTAIN in calls:
        actor = group['slots'].index(number)
        native_group['original_actor_voice_choices'] = [(actor, None, number)]
    else:
        actor = next(i for i, _, n in group['original_voice_choices'] if n == number)
    native_group['original_voice_choices'] = native_group['original_actor_voice_choices']
    for entry, caller in calls.items():
        native_group['source_native_caller'] = caller
        if not row['original_substitution_count']:
            case = portrait.native_stored(ctx, row, native_group, storage)
            display = case.pop('display')
            yield case, display, None
            continue
        for item in group['runtime_item_name_inputs']:
            arg = bytes.fromhex(item['value_hex'])
            if entry == BASE + review.QUEUED:
                result = prior.crew_case(ctx, row, native_group, arg)
            else:
                assert entry == BASE + review.DIRECT
                obj = ctx.actor_root + (0x19E4 if actor == 3 else 4 + 32 * actor)
                consumer = FunctionType(prior.consumer.__code__,
                    prior.consumer.__globals__ | {'portrait_machine': ctx.machine}, argdefs=prior.consumer.__defaults__)
                result = consumer(ctx.arm, ctx.common, ctx.raw, ctx.plan, review.DIRECT, obj, group['table'], arg)
                assert bytes(ctx.calls[0].mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
                ctx.calls.clear()
            assert bytes.fromhex(result['input_hex']) == storage.replace(b'%s', arg), (number, result)
            yield result, bytes.fromhex(result['formatted_hex']), item


def main():
    base = review.prior
    assert not ROOT.exists()
    draft, release = map(base.load, (review.OUTPUT, review.parent.RELEASE))
    runtime = base.RegisteredRuntime(review.parent.RELEASE, release['own_registered_startup'], captain=3)
    assert runtime.receipt() == draft['registered_input']
    rows = {row['message_ID']: row for row in draft['records']}
    groups = {group['first_ID']: group for group in draft['native_context']}
    arm, common, stored, rebound, allocation, ownership = stage(runtime, release, rows, groups.values())
    staged = prior.with_components(runtime, arm, common)
    raster, _, _ = prior.font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    records, pages = [], []
    for n, row in rows.items():
        storage = stored[n]
        lookup = prior.current_copy(staged, row | {'current_hex': storage.hex()}, BASE + 0x5528C)
        staged.calls.clear()
        displays = []
        for native, display, item in native_displays(staged, row, groups[row['native_group_first_ID']], storage):
            expected = row['english'].replace('%s', item['item_name']) if item else row['english']
            assert b' '.join(display.split()).decode('ascii') == expected, (n, display)
            if b'\n' in storage:
                assert display == storage
            lines = [line.strip() for line in display.decode('ascii').split('\n')]
            assert all(any(phrase in line for line in lines) for phrase in PHRASES.get(n, ())), (n, lines)
            pixels, glyphs = prior.render_portrait(raster, arm, kanji, display)
            assert ''.join(chr(g['code']) for g in glyphs) == expected.replace(' ', ''), n
            ink = sha256(pixels).hexdigest()
            if all(item['native_ink_sha256'] != ink for item in displays):
                pages.append((f'{n}/{len(displays) + 1}', pixels))
            displays.append(dict(native=native, item_name=item, display_hex=display.hex(), visible_lines=lines,
                                 complete_glyphs=len(glyphs), native_ink_sha256=ink))
        records.append(dict(message_ID=n, source_reference=row['source_reference'],
            previous_reference=row['current_reference'], staged_reference=base.reference(rebound[n]),
            staged_hex=storage.hex(), original_stored_lookup=lookup, displays=displays))
    assert sum(len(row['displays']) for row in records) == 46 and len(records) == 33
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
    sheets = prior.portrait_sheets(ROOT, pages)
    base.save(PROOF, dict(registered_input=runtime.receipt(), research_ROM=str(ROM), research_ROM_sha256=base.digest(ROM),
        research_ARM9_sha256=sha256(arm).hexdigest(), research_COMMON_sha256=sha256(common).hexdigest(),
        allocation=allocation, ownership=ownership, parent_inverse_exact=True, records=records,
        sheets=sheets, native_pages=len(pages), native_cases=46, manuscript_sha256=base.digest(review.OUTPUT),
        formatting_pending_visual_review=True, gameplay_pending=True, new_credit=0, full_goal_complete=False))
    print(f'33 stored lookups and 46 original consumer cases passed. {len(pages)} distinct pages to review.')


if __name__ == '__main__':
    main()
