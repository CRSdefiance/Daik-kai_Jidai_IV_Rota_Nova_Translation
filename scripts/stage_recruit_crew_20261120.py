"""Stage the Recruit Crew number rendering and shortfall dialogue as one exchange."""

from pathlib import Path
from struct import pack, unpack_from
from types import FunctionType

from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R6, UC_ARM_REG_R7
from unicorn.arm_const import UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_SP

from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import check_departure_numerals_native_20261119 as ring
from scripts import register_palace_help_20261120 as parent
from scripts import stage_ruin_discovery_display_20261120 as number
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, glyph_codes
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.probe_button_prompt_native import STACK, call
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_mutiny_review_v1 import portrait_sheets, render_portrait
from scripts.verify_personal_gameplay_v841 import get_machine


base, batch = parent.base, parent.batch
BASE, ARM, COMMON, CLEAN = number.BASE, batch.ARM, batch.COMMON, batch.CLEAN
ROOT = Path('work/recruit_crew_20261120_v2')
ROM, PROOF, NATIVE = ROOT / 'Recruit_Crew_RESEARCH_ONLY.nds', ROOT / 'staged.json', ROOT / 'native.json'
CALLS = {0x02057474: ('gold quote', 0x02057484, 0x02053CB0),
         0x020575E0: ('volunteer count', 0x020575F0, 0x02053DCC),
         0x02057648: ('crew shortfall', 0x02057658, 0x02053CB0),
         0x0205766C: ('spare berths', 0x0205767C, 0x02053CB0)}
TABLES = {0x21183A0: (883, -1, 884, 885, 886, 887, 888, 889),
          0x2118380: (890, -1, 891, 892, 893, 894, 895, 896),
          0x2118360: (897, -1, 898, 899, 900, 901, 902, 903),
          0x21181A0: (1035, -1, 1036, 1037, 1038, 1039, 1040, 1041),
          0x2118180: (1042, -1, 1043, 1044, 1045, 1046, 1047, 1048)}
PRICES, COUNTS = (500, 999, 1573, 9999, 13607), (0, 1, 9, 34, 51, 99, 100, 65535)
RECORDS = (*range(883, 905), 907, *range(1035, 1049))
EDITS = {
    890: ("I'll recruit crew for %s gold.", 'Keep the officer’s direct offer and use the name of the action so the full price stays together.'),
    891: ("I'll hire sailors for %s gold.", 'The more casual voice uses hire, preserves the price and leaves the headcount open.'),
    893: ("I'll get us sailors for %s gold.", 'Keep “us” and the rougher speaker’s familiar phrasing, with no promise about the number.'),
    895: ("I'll find sailors for %s gold.", 'The quick, plain offer fits the young voice and keeps the price intact.'),
    1035: ("We're still %s short. Shall I recruit more?", 'Keeps the first officer’s polite offer and states the shortfall in one direct sentence.'),
    1036: ("We're still %s short. Should I recruit more?", 'Keeps the blunt report and the short practical question.'),
    1037: ("We're still %s short. Would you like me to recruit more?", 'Preserves the courteous question after the count.'),
    1038: ("We're still %s short. Want me to round up more sailors?", 'Keeps “round up” for the rougher voice without adding a catchphrase.'),
    1039: ("We're still %s short. Shall I round up some more?", 'The measured question suits the older voice and retains the offer to continue.'),
    1040: ("We're still %s short. Want me to try again?", 'The count conveys that the first attempt fell short. Keep the youthful direct question.'),
    1041: ("We're still %s short. Shall I keep recruiting?", 'Keeps the measured offer while making the continuation clear.'),
}
REASONS = {
    883: 'A matter-of-fact address and refusal fit the default voice.',
    884: '“Looks like” keeps the speaker’s tentative judgment.',
    885: 'The initial hesitation conveys that the speaker is reluctant to report the shortfall.',
    886: '“Short on cash” preserves the gruff speaker’s casual register.',
    887: 'Putting Admiral at the end keeps the report conversational.',
    888: 'The emphatic address conveys the source’s drawn-out complaint.',
    889: 'The trailing thought keeps the source’s hesitant objection.',
    890: 'The first officer gives a direct price and recruitment plan.',
    891: '“Some sailors” keeps the more casual offer open about how many turn up.',
    892: 'The speaker states the amount they will spend without promising a headcount.',
    893: '“Find us” keeps this speaker’s familiar crew-facing tone.',
    894: 'The direct statement suits the speaker’s matter-of-fact decision.',
    895: 'The simpler phrasing keeps the young voice brisk.',
    896: 'The polite officer explains the purpose of the expenditure directly.',
    897: 'The call invites volunteers to sail with the Admiral.',
    898: 'The contraction makes this sound like a call in the Tavern.',
    899: '“Step forward” preserves the explicit invitation to identify oneself.',
    900: 'The speaker calls out to the room in a familiar tone.',
    901: 'The short open call sounds like the more seasoned speaker.',
    902: 'The second sentence preserves the actual command to step forward.',
    903: 'The compact question sounds like a caller addressing the whole room.',
    904: '“Willing to join” distinguishes the volunteers who turned up from the sailors finally assigned.',
    907: 'The crowd gives a short nautical assent in response to the invitation.',
    1042: 'The question offers more recruiting because there is still physical capacity.',
    1043: '“You’ve still got room” suits the more conversational voice.',
    1044: 'The courteous follow-up keeps the same spare-capacity rule.',
    1045: 'The rougher voice still offers to round up more sailors.',
    1046: '“There seems to be room” retains the source’s qualified report.',
    1047: '“Looks like” suits the young speaker and keeps room for more distinct from a requirement.',
    1048: 'The measured offer to try again fits the speaker and preserves spare capacity.',
}


def patch(arm, clean):
    for lo, hi in ((0x57408, 0x576CC), (0x53CB0, 0x53E4C), (0x53F4C, 0x53F9C)):
        assert arm[lo:hi] == clean[lo:hi]
    for address, values in TABLES.items():
        assert arm[address-BASE:address-BASE+32] == clean[address-BASE:address-BASE+32] == pack('<8i', *values)
    section, = [s for s in number.MainCodeFile(arm, BASE).sections if s.ramAddress == number.ITCM]
    helper = bytes(section.data[number.HELPER-number.ITCM:number.END-number.ITCM])
    assert helper.hex() == base.load(number.HELPER_PROOF)['helper_hex']
    output, sites = bytearray(arm), []
    for addr, (context, consumer, wrapper) in CALLS.items():
        at = addr - BASE
        assert number.target(arm, at) == number.NUMBER and number.target(arm, consumer-BASE) == wrapper
        instruction = number.assemble(f'bl {number.HELPER}', addr)
        assert len(instruction) == 4
        output[at:at+4] = instruction
        sites.append(dict(address=addr, purpose=context, original_hex=arm[at:at+4].hex(), current_hex=instruction.hex(),
                          wrapper_call=consumer, wrapper=wrapper, original_target=number.NUMBER, target=number.HELPER))
    new = bytes(output)
    assert all(number.target(new, n-BASE) == number.HELPER for n in CALLS)
    assert number.cache_plan(new) == number.cache_plan(arm)
    return new, sites


def stage():
    assert not ROOT.exists()
    previous = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == previous['candidate_sha256'] and base.digest(base.REGISTRY) == previous['registry_sha256']
    original, image = map(base.NdsImage.open, (CLEAN, parent.ROM))
    assert base.digest(CLEAN) == previous['clean_input_sha256']
    arm, common = (image.read_file(path) for path in (ARM, COMMON))
    target, sites = patch(arm, original.read_file(ARM))
    prior = catalogue(arm, common)
    assert all(prior[n].text.startswith(b' ') and prior[n].text.count(b'%s') == 1 for n in EDITS)
    edited, _, allocations = batch.owned_deployment(common, target, prior,
        {n: (' ' + english).encode('ascii') for n, (english, _) in EDITS.items()})
    image.replace_file(ARM, target)
    image.replace_file(COMMON, edited)
    candidate = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(candidate)
    delta, rebuilt = ROOT / 'translation.xdelta', ROOT / 'clean_rebuilt.nds'
    make_xdelta(CLEAN, ROM, delta)
    apply_xdelta(CLEAN, delta, rebuilt)
    assert rebuilt.read_bytes() == candidate
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), parent_sha256=previous['candidate_sha256'],
        clean_input_sha256=previous['clean_input_sha256'], clean_input_patch_sha256=base.digest(delta),
        target_ARM9_sha256=batch.digest(target), target_COMMON_sha256=batch.digest(edited), calls=sites,
        COMMON_allocations=allocations, whole_parent_inverse=True, clean_input_patch_byte_exact=True))


def catalogue(arm, common):
    directory = batch.digest(arm[batch.DIRECTORY_OFFSET:batch.TABLE_OFFSET])
    return batch.owned_entries(common, arm, directory)


def semantics(n):
    if n < 890:
        return 'The officer reports to the Admiral that the fleet cannot afford recruitment.'
    if n < 897:
        return 'The officer states what it will cost in gold to recruit sailors.'
    if n < 904:
        return 'The officer asks the people in the Tavern who will sail with the Admiral.'
    if n == 904:
        return 'The officer announces how many people have answered the call.'
    if n == 907:
        return 'The crowd answers the officer’s invitation with an assent.'
    if n < 1042:
        return 'The officer states the remaining shortage relative to required crew and asks whether to recruit again.'
    return 'The officer reports remaining capacity aboard and asks whether to recruit again.'


def last_branch(cpu, cash, cost, total, required, maximum):
    # Start after the original wallet getter and stop at the selected wrapper,
    # leaving the real comparisons and the number formatting call in place.
    for reg, value in ((UC_ARM_REG_R0, cash), (UC_ARM_REG_R8, cost), (UC_ARM_REG_R9, total),
                       (UC_ARM_REG_R7, required), (UC_ARM_REG_R6, maximum), (UC_ARM_REG_SP, STACK)):
        cpu.reg_write(reg, value)
    stops = (0x02057658, 0x0205767C, 0x02057698)
    from unicorn import UC_HOOK_CODE
    from unicorn.arm_const import UC_ARM_REG_R1, UC_ARM_REG_R2

    def stop(u, pc, size, data):
        u.emu_stop()

    hooks = [cpu.hook_add(UC_HOOK_CODE, stop, begin=n, end=n) for n in stops]
    try:
        cpu.emu_start(0x0205762C, 0x020576A0, count=20000)
    finally:
        for h in hooks:
            cpu.hook_del(h)
    at = cpu.reg_read(UC_ARM_REG_PC)
    assert at in stops
    if at == stops[-1]:
        return at, None, b''
    return at, cpu.reg_read(UC_ARM_REG_R1), ring.read_cstring(cpu, cpu.reg_read(UC_ARM_REG_R2))


def native():
    assert not NATIVE.exists()
    previous, staged = map(base.load, (parent.RELEASE, PROOF))
    reference = RegisteredRuntime(parent.RELEASE, previous['own_registered_startup'], captain=3)
    original, old, new = map(base.NdsImage.open, (CLEAN, parent.ROM, ROM))
    source_arm, old_arm, arm = (r.read_file(ARM) for r in (original, old, new))
    common = new.read_file(COMMON)
    assert patch(old_arm, source_arm)[0] == arm and staged['candidate_sha256'] == base.digest(ROM)
    source = batch.common_message_entries(original.read_file(COMMON), source_arm)
    prior, table = (catalogue(code, r.read_file(COMMON)) for code, r in ((old_arm, old), (arm, new)))

    ctx = with_components(reference, arm, common)
    raw = bytearray(ctx.raw)
    for addr in CALLS:
        at = addr-BASE
        assert raw[at:at+4] == old_arm[at:at+4]
        raw[at:at+4] = arm[at:at+4]
    ctx.raw = bytes(raw)
    old_cpu, _ = get_machine(old_arm, reference.raw)
    cpu, get = get_machine(arm, ctx.raw)
    cases = {pc: PRICES if i == 0 else COUNTS for i, pc in enumerate(CALLS)}
    verify_numbers = FunctionType(ring.verify_numbers.__code__, vars(ring) | {'CASES': cases})
    formatter_contracts = verify_numbers(old_cpu, cpu)
    assert len(formatter_contracts) == 32 * sum(map(len, cases.values()))
    branches = []
    for args, expected in [((499, 500, 5, 10, 50), (None, 0)), ((500, 500, 5, 10, 50), (0x21181A0, 5)),
                           ((500, 500, 10, 10, 50), (0x2118180, 40)), ((999, 500, 49, 10, 50), (0x2118180, 1)),
                           ((999, 500, 50, 10, 50), (None, 0))]:
        before, after = [last_branch(m, *args) for m in (old_cpu, cpu)]
        assert before[:2] == after[:2] and after[1] == expected[0]
        assert ring.normalize(before[2]) == after[2] == (str(expected[1]).encode('ascii') if expected[0] else b'')
        branches.append(dict(args=args, call=after[0], voice_table=after[1], before_hex=before[2].hex(), after_hex=after[2].hex()))
    actors = get(0xCB184)
    voice_cases = []
    for address, values in TABLES.items():
        for i in range(40):
            actor = actors+4+i*32
            voice = get(0x7E988, actor)
            expected = values[voice] if values[voice] >= 0 else values[0]
            assert get(0x53F4C, actor, address) == expected
            voice_cases.append(dict(table=address, actor_index=i, voice=voice, message_ID=expected))
        assert get(0x53F4C, 0, address) == values[0]
    loader, load_message, _ = ctx.machine(arm, common, ctx.raw, ctx.plan)
    rs, art, previews = [], [], []
    painter, _, _ = font_tools(new)
    font = new.read_file('/GRP/KANJI.FNT')
    wrap = FunctionType(native_layout.__code__, native_layout.__globals__ |
                        {'call': lambda *a: call(*a, instruction_limit=2_000_000)}, argdefs=native_layout.__defaults__)
    for n in RECORDS:
        original_body, current, final = (a[n].text for a in (source, prior, table))
        assert original_body.count(b'%s') == current.count(b'%s') == final.count(b'%s') <= 1
        pointer = load_message(0x5528C, n)
        assert bytes(loader.mem_read(pointer, len(final) + 1)) == final + b'\0'
        numeric = bool(final.count(b'%s'))
        samples = PRICES if 890 <= n <= 896 else COUNTS if numeric else (None,)
        entry = 0x02053E38 if n == 904 else 0x02053D24 if numeric else 0x02054014 if n == 907 else 0x02053DB8
        cases_for_record = []
        for value in samples:
            args = (str(value),) if numeric else ()
            wrapped, lines = wrap(cpu, final, n, args, parent=entry)
            assert 1 <= len(lines) <= 4 and all(lines)
            assert b' '.join(wrapped.split()) == b' '.join((final % tuple(a.encode('ascii') for a in args)).split())
            if 890 <= n <= 896:
                assert any(f'{value} gold' in line for line in lines), (n, value, lines)
            include = (value in (None, max(samples), 1573, 34, 51) if n in EDITS or numeric else False)
            receipt = dict(value=value, lines=lines, wrapped_hex=wrapped.hex(), one_page=True)
            if include:
                plane, glyphs = render_portrait(painter, arm, font, wrapped.replace(b'\r', b''))
                codes = [g['code'] for g in glyphs]
                assert codes == glyph_codes(wrapped) and all(c < 128 for c in codes)
                receipt['ink_sha256'] = batch.digest(plane)
                art.append((f'Recruit Crew / {n} / {value}', plane))
            cases_for_record.append(receipt)
        localized, reason = EDITS[n] if n in EDITS else (final.decode('ascii').strip(), REASONS[n])
        assert localized == final.decode('ascii').strip()
        rs.append(dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, file_path=COMMON,
            speaker='Tavern patrons' if n == 907 else 'Recruiting officer', english=localized,
            context='Recruit Crew runs from quote or refusal, through the call and reply, to the volunteer count and the two remaining-crew questions.',
            source_meaning=semantics(n), localization_note=reason, decision='revision' if n in EDITS else 'retention',
            source_Japanese=original_body.decode('cp932'), source_reference=batch.reference(source[n]), source_hex=original_body.hex(),
            current_reference=batch.reference(prior[n]), current_hex=current.hex(), final_reference=batch.reference(table[n]),
            final_hex=final.hex(), native_layouts=cases_for_record, runtime_substitutions=['original decimal amount'] if numeric else [],
            review=dict.fromkeys(batch.GATES, True)))
    previews.extend(portrait_sheets(ROOT, art))
    base.save(NATIVE, dict(candidate_sha256=base.digest(ROM), parent_sha256=previous['candidate_sha256'], records=rs,
        original_ring_cases=formatter_contracts, supplied_threshold_paths=branches, original_voice_cases=voice_cases,
        native_preview_count=len(art), sheets=previews, original_loader_cases=len(rs)))
    print(f'{len(rs)} decisions, {len(art)} complete pages and {len(formatter_contracts)} format-ring checks.')


if __name__ == '__main__':
    import sys

    {'stage': stage, 'native': native}[sys.argv[1]]()
