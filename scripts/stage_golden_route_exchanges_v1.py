"""Exercise the full Golden Route release text with the original name and amount getters."""

from hashlib import sha256
from inspect import getsource
from pathlib import Path
from struct import unpack_from
from types import FunctionType

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1
from unicorn.arm_const import UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.patch import portrait_scope_table_v1 as selector
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from scripts import review_golden_route_exchanges_v1 as review
from scripts import register_fleet_reports_v1 as fleet_release
from scripts.review_golden_route_exchanges_v3 import OUTPUT
from scripts import stage_fleet_reports_v1 as fleet
from scripts import stage_oasis_and_whale_reports_v1 as oasis
from scripts.preflight_shared_dynamic_notice_wrap_v1 import glyph_codes
from scripts.probe_button_prompt_native import STACK, STOP
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_mutiny_review_v1 import PARENTS, compile_layouts
from scripts.stage_shared_notices_storage_v1 import relocate


base = review.prior
ARM, COMMON, BASE = review.ARM, review.COMMON, review.BASE
ROOT = Path('out/golden_route_exchanges_staged_20261111_v1')
ROM = ROOT / 'golden_route_exchanges_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
PHRASES = {
    3334: ('profitable trade routes.',),
    3340: ('Golden Routes.', 'I hear they pay well'),
    3341: ('profit margins', 'Golden Routes.'),
    3343: ('promising trade routes', 'Golden Routes.'),
    3345: ('trade routes', 'a handsome sum'),
    3347: ('Golden Routes.',),
    3352: ('a port with a guild.',),
    3353: ('a guild,', 'right away.'),
    3354: ('a port with a guild.',),
    3355: ('a port with a guild.',),
    3356: ('with a guild,',),
    3357: ('a port with a guild.',),
    3358: ('a port with a guild!',),
    3359: ('a port with a guild.',),
    3376: ('a port with a guild.',),
    3377: ('the next port with a guild.',),
    3378: ('a port with a guild.',),
    3379: ('a port that has one.',),
    3391: ("I'll pay well.", 'For two years,', 'each month a good comes in,', "I'll match its profit in gold."),
}
PAYOUT_ROWS = (b'For finding a Golden Route,', b'the guild awarded you', b'%s gold.')


def stage(runtime, release, rows, groups, verified=None):
    assert sha256(runtime.arm).hexdigest() == release['target_ARM9_sha256']
    compiler = FunctionType(compile_layouts.__code__, compile_layouts.__globals__ | {'PHRASES': PHRASES})
    storage = compiler({number: row for number, row in rows.items() if not row['original_substitution_count']})
    storage.update({number: row['english'].encode('ascii') for number, row in rows.items()
                   if row['original_substitution_count']})
    assert b' '.join(PAYOUT_ROWS) == storage[3392]
    storage[3392] = b' ' + b'\n  '.join(PAYOUT_ROWS)
    additions = {}
    for group in groups:
        caller, = group['native_callers']
        entry = caller['consumer'] - BASE
        if entry == review.MODAL:
            continue
        first, last = group['first_ID'], group['last_ID']
        argument = group['argument_kind']
        if argument == 'good_amount':
            mode = selector.AMOUNT
        elif argument:
            mode = selector.DYNAMIC
        elif any(b'\n' in storage[number] for number in range(first, last + 1)):
            mode = selector.STATIC
        else:
            continue
        scope = additions.setdefault(PARENTS[entry], {})
        key = group['table'] or first
        assert key not in scope
        scope[key] = mode
    receipt = base.load(review.parent.VERIFICATION / 'stored_verification.json')['ownership']
    amount_owner = base.load(fleet_release.VERIFICATION / 'stored_verification.json')['ownership']
    wrapped, scopes, ownership = selector.transform(runtime.arm, receipt, amount_owner, additions)
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, relocate.__globals__ | {'DIRECTORY': directory})
    common, arm, rebound, allocation = repack(runtime.common, wrapped, rows, storage)
    assert allocation['all_41_blocks_fit_8KiB'] and allocation['touched_blocks'] == [38, 39]
    assert arm[:DIRECTORY_OFFSET] == wrapped[:DIRECTORY_OFFSET] and arm[TABLE_END:] == wrapped[TABLE_END:]
    if verified is None:
        static = {group: tuple(k for k, mode in cases.items() if mode == selector.STATIC) for group, cases in scopes.items()}
        dynamic = {group: tuple(k for k, mode in cases.items() if mode != selector.STATIC) for group, cases in scopes.items()}
        old_guard = base.load(review.parent.predecessor.VERIFICATION / 'stored_verification.json')
        failed_guard = old_guard['ownership']['shared_existing_static_guard']['original_failed_guard_target']
        checks = oasis.verify_scope(arm, static, dynamic, ownership['previous_selector'], failed_guard)
    else:
        assert ownership['target_ARM9_sha256'] == verified['ownership']['target_ARM9_sha256']
        checks = verified['ownership']['selector_checks']
    return arm, common, storage, rebound, allocation, ownership | dict(
        scopes=[[list(group), list(entries.items())] for group, entries in scopes.items()], selector_checks=checks)


def samples(kind, sources):
    good, town, gold = [sources[name] for name in ('goods', 'towns', 'gold')]
    names = lambda values, indices: tuple(bytes.fromhex(values[index]['hex']) for index in indices)
    numbers = tuple(bytes.fromhex(gold[index]['original_hex']) for index in (0, 2, -1))
    if kind is None:
        return [()]
    if kind == 'good':
        return [(name,) for name in names(good, (13, 65, 74))]
    if kind == 'town_good':
        return [names(town, (port,)) + names(good, (cargo,)) for port, cargo in ((11, 13), (62, 65), (72, 74))]
    if kind == 'good_amount':
        return [(name, count) for name, count in zip(names(good, (13, 74, 65)), numbers, strict=True)]
    assert kind == 'amount'
    return [(amount,) for amount in numbers]


def modal_case(ctx, template, value):
    cpu, get, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    display = {}

    def observe(u, pc, size, _):
        if pc == BASE + 0x54788:
            source = u.reg_read(UC_ARM_REG_R1)
            assert bytes(u.mem_read(source, len(template) + 1)) == template + b'\0'
        elif pc == BASE + 0x54798:
            sp = u.reg_read(UC_ARM_REG_SP)
            assert unpack_from('<I', u.mem_read(sp + 0xC4, 4))[0] == BASE + 0x546E8
            assert bytes(u.mem_read(u.reg_read(UC_ARM_REG_R1), 256)).split(b'\0')[0] == template % (value,)
        else:
            target = unpack_from('<I', ctx.arm, 0x54894)[0]
            display['display'] = bytes(u.mem_read(target, 256)).split(b'\0')[0]
            u.emu_stop()

    for offset in (0x54788, 0x54798, 0x5479C):
        cpu.hook_add(UC_HOOK_CODE, observe, begin=BASE + offset, end=BASE + offset)
    argument = 0x02470000
    cpu.mem_write(argument, value + b'\0')
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_LR, STOP)
    for register, word in ((UC_ARM_REG_R0, 3392), (UC_ARM_REG_R1, argument), (UC_ARM_REG_R2, 0), (UC_ARM_REG_R3, 0)):
        cpu.reg_write(register, word)
    cpu.emu_start(BASE + review.MODAL, STOP, count=3000000)
    assert cpu.reg_read(UC_ARM_REG_PC) == BASE + 0x5479C and 'display' in display
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    ctx.calls.clear()
    return display | dict(original_entry=BASE + review.MODAL, original_file_reads=provider.reads, original_amount_hex=value.hex())


def portrait_with_arguments():
    original = fleet.portrait.portrait_case
    source = checked_text(getsource(original), {
        'def portrait_case(ctx, row, group, stored, actor_id):':
            'def portrait_case(ctx, row, group, stored, actor_id, arguments):',
        '    seen = {}':
            '    pointers = []\n'
            '    for index, argument in enumerate(arguments):\n'
            '        assert b"\\0" not in argument and 0 < len(argument) < 48\n'
            '        pointer = GOLDEN_ARGUMENT_MEMORY + index * 64\n'
            '        cpu.mem_write(pointer, argument + b"\\0")\n'
            '        pointers.append(pointer)\n'
            '    if entry == CAPTAIN_ENTRY:\n'
            '        args = args[:1]\n'
            '    inputs = (*args, *pointers)\n'
            '    inputs += (0,) * (4 - len(inputs))\n'
            '    expanded = stored % arguments if arguments else stored\n'
            '    seen = {}',
        "len(stored) + 1)) == stored + b'\\0'": "len(expanded) + 1)) == expanded + b'\\0'",
        '(*args, 0, 0)': 'inputs',
    })
    env = original.__globals__ | {'GOLDEN_ARGUMENT_MEMORY': 0x02470000, 'CAPTAIN_ENTRY': review.CAPTAIN}
    exec(compile(source, __file__ + '::golden-route-portrait-ABI', 'exec'), env)
    return env['portrait_case']


def main():
    assert not ROOT.exists()
    draft, release = map(base.load, (OUTPUT, review.parent.RELEASE))
    runtime = base.RegisteredRuntime(review.parent.RELEASE, release['own_registered_startup'], captain=3)
    assert draft['registered_input'] == runtime.receipt()
    rows = {row['message_ID']: row for row in draft['records']}
    groups = {group['first_ID']: group for group in draft['native_context']}
    arm, common, storage, rebound, allocation, ownership = stage(runtime, release, rows, groups.values())
    portrait = fleet.portrait
    ctx = portrait.with_components(runtime, arm, common)
    render, _, font = portrait.font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    original_portrait = portrait_with_arguments()
    pages, records = [], []
    for number, row in rows.items():
        template = storage[number]
        lookup = portrait.current_copy(ctx, row | {'current_hex': template.hex()}, BASE + 0x5528C)
        ctx.calls.clear()
        group = groups[row['native_group_first_ID']]
        caller, = group['native_callers']
        entry, kind = caller['consumer'] - BASE, group['argument_kind']
        table = group | {'consumer': caller['consumer']} if group['table'] else None
        actor = next((i for i, _, msg in group['original_voice_choices'] if msg == number), None)
        displays = []
        for index, args in enumerate(samples(kind, draft['initialized_argument_samples'])):
            try:
                if entry == review.MODAL:
                    native = modal_case(ctx, template, args[0])
                else:
                    native = original_portrait(ctx, row, table, template, actor, args)
            except AssertionError as error:
                raise AssertionError((number, entry, args)) from error
            display = native.pop('display')
            expected = row['english'].encode('ascii')
            if args:
                render_args = args
                if kind == 'good_amount':
                    render_args = (args[0], args[1].decode('cp932').translate(
                        str.maketrans('０１２３４５６７８９', '0123456789')).encode('ascii'))
                expected %= render_args
            assert b' '.join(display.split()) == expected, (number, display, expected)
            if b'\n' in template:
                assert display == (template % args if args else template), number
            lines = display.decode('cp932').split('\n')
            assert all(any(phrase in line for line in lines) for phrase in PHRASES.get(number, ())), (number, lines)
            try:
                pixels, glyphs = portrait.render_portrait(render, arm, kanji, display)
            except AssertionError as error:
                raise AssertionError((number, lines, args)) from error
            assert [glyph['code'] for glyph in glyphs] == glyph_codes(expected)
            pages.append((f'{number}/{index + 1}' if args else number, pixels))
            displays.append(dict(native=native, argument_hex=[value.hex() for value in args],
                normalized_visible_hex=expected.hex(), display_hex=display.hex(),
                visible_lines=[line.strip() for line in lines], complete_glyphs=len(glyphs),
                native_ink_sha256=sha256(pixels).hexdigest()))
        records.append(dict(message_ID=number, source_reference=row['source_reference'],
            previous_reference=row['current_reference'], staged_reference=base.reference(rebound[number]),
            staged_hex=template.hex(), original_stored_lookup=lookup, displays=displays))
    assert len(records) == 73 and len(pages) == 117
    image = review.parent.base.NdsImage.open(runtime.rompath)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    target = bytes(image.rom.save())
    image.replace_file(ARM, runtime.arm)
    image.replace_file(COMMON, runtime.common)
    assert bytes(image.rom.save()) == Path(runtime.rompath).read_bytes()
    ROOT.mkdir()
    with ROM.open('xb') as stream:
        stream.write(target)
    sheets = portrait.portrait_sheets(ROOT, pages)
    base.save(PROOF, dict(registered_input=runtime.receipt(), research_ROM=str(ROM), research_ROM_sha256=base.digest(ROM),
        research_ARM9_sha256=sha256(arm).hexdigest(), research_COMMON_sha256=sha256(common).hexdigest(),
        allocation=allocation, ownership=ownership, parent_inverse_exact=True, records=records, font=font,
        sheets=sheets, native_pages=len(pages), native_cases=len(pages), manuscript_sha256=base.digest(OUTPUT),
        formatting_pending_visual_review=True, gameplay_pending=True, new_credit=0, full_goal_complete=False))
    print(f'{len(records)} stored lookups and {len(pages)} original display cases passed.')


if __name__ == '__main__':
    main()
