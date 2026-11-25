"""Review both fleet alert tables and stage spoken bearings and prose."""

from collections import Counter
from itertools import product
from pathlib import Path
from struct import unpack_from

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
    UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_SP,
)

from dk4tool.patch import fleet_sighting_bearings_v1 as bearings
from dk4tool.patch import pirate_report_bearings_v1 as pirate
from scripts import register_kurushima_encounter_20261115 as parent
from scripts.probe_button_prompt_native import STACK, STOP, machine
from scripts.probe_sighting_layout_v1070 import native_layout
from scripts.sighting_layout_v1069 import IDS, compiled
from scripts.stage_market_conversation_20261115 import (
    ARM, CLEAN, COMMON, DIRECTORY_OFFSET, TABLE_OFFSET, GATES, RegisteredRuntime,
    common_message_entries, digest, files, font_tools, owned_deployment, owned_entries,
    portrait_sheets, reference, render_portrait,
)


base = parent.base
ROOT = Path('work/fleet_sighting_alerts_20261115_v2')
ROM, STORED = ROOT / 'Fleet_Sighting_Alerts_RESEARCH_ONLY.nds', ROOT / 'staged.json'
MANUSCRIPT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/fleet_sighting_alerts_20261115_v2.json')
SIGHTED = 'fleet-sighting-battle-preparation'
ATTACKED = 'fleet-sighting-under-attack'
TABLES = {0x02118560: tuple(range(614, 622)), 0x02118540: (622, -1, 623, 624, 625, 626, 627, 628)}
CONTEXT = {
    SIGHTED: ('One of eight lookout reports when the fleet notices another faction’s ships. The speaker '
              'reports the bearing and their affiliation, then announces preparations for battle.'),
    ATTACKED: ('One of seven lookout reports when the other fleet has already started attacking. The speaker '
               'reports the bearing and affiliation and reacts to the attack in progress.'),
}
REVISIONS = {
    614: ("Fleet spotted %s! They belong to %s! We're getting ready for battle!",
          'A formal report identifies the other fleet and announces preparations.'),
    615: ("Spotted a fleet %s! They belong to %s! We're getting ready for a fight!",
          'A brisk lookout spots the fleet and reports that preparations are starting.'),
    616: ("There's a fleet %s! Ships from %s! Get ready for a fight!",
          'The familiar voice reports the fleet and urges a quick response.'),
    617: ("There's a fleet %s! They sail for %s! We're getting ready for battle!",
          'Keep the alarm and the speaker’s firm announcement of preparations.'),
    618: ("We've got company %s! They're with %s! Get ready for a fight!",
          'The rough lookout’s “got company” keeps the discovery and urgent call to prepare. “They’re with” identifies the fleet.'),
    619: ("Spotted a fleet %s! Ships from %s! We'd best prepare for battle!",
          '“We’d best” keeps the older speaker’s voice while the instructions stay direct.'),
    620: ("I found a fleet %s! Ships from %s! We're gonna fight!",
          'Keep the young lookout’s pride in finding the fleet and the excited announcement.'),
    621: ("Fleet spotted %s! They sail for %s! We're preparing for battle!",
          'This measured report names the other fleet before announcing readiness preparations.'),
    622: ("Fleet spotted %s! They belong to %s! They're attacking us!",
          'Keep the brisk identification and the statement that the attack has begun.'),
    623: ("There's a fleet %s! Ships from %s! They're attacking us!",
          'The familiar phrasing moves straight from the sighting to the current danger.'),
    624: ("Look! A fleet %s! They sail for %s! They're attacking us!",
          'Keep the startled interjection before the identification and attack report.'),
    625: ("Spotted a fleet %s! Ships from %s! They just picked a fight with us!",
          'The rough voice treats the other fleet’s attack as picking a fight.'),
    626: ("There's a fleet %s! They sail for %s! They're coming right at us!",
          'Keep the older voice’s alarm at the fleet coming after them.'),
    627: ("Whoa! A fleet %s! They belong to %s! They're attacking us!",
          'Keep the young lookout startled, with the attackers and bearing clearly identified.'),
    628: ("There's a fleet %s! They belong to %s! They've launched an attack!",
          'The formal voice explicitly reports an attack already launched by the spotted fleet.'),
}
MEANINGS = {
    614: 'The lookout formally reports spotting the named faction’s fleet at the given bearing and says the crew is preparing for battle.',
    615: 'The lookout gives a clipped sighting report and announces preparations for battle.',
    616: 'There is a fleet at that bearing under the named faction. The speaker says to get ready for battle.',
    617: 'The speaker notices the named faction’s fleet at that bearing and announces that the crew will prepare for battle.',
    618: 'The rough-spoken lookout spots the named fleet at that bearing and rallies the crew to get ready to fight.',
    619: 'The older voice spots the fleet and tells the crew to prepare for battle.',
    620: 'The excited young lookout has found the named fleet at the given bearing and exclaims that it is time to fight.',
    621: 'The formal lookout reports detecting the named fleet at that bearing and announces battle preparations.',
    622: 'The lookout spots the named fleet at that bearing and reports that it has initiated an attack.',
    623: 'The lookout spots that fleet at the given bearing and tells the crew that it is attacking.',
    624: 'The speaker cries out at the sight of the fleet at that bearing and realizes it is attacking.',
    625: 'The rough lookout spots the named fleet at the given bearing and reports that it started a fight.',
    626: 'The older lookout sees the named fleet at that bearing and warns that it has started an attack.',
    627: 'The startled young lookout reports that the named fleet is attacking from the stated bearing.',
    628: 'The formal lookout identifies the named fleet by bearing and reports that it has launched an attack.',
}


def encoded_changes():
    return {n: compiled(dict(message_id=n, english=text, native_argument_count=2,
                            source_family=SIGHTED if n < 622 else ATTACKED))
            for n, (text, _) in REVISIONS.items()}


def bearing_controls(arm):
    cpu = machine(arm)
    reached = []

    def stop_at_wrapper(cpu, address, size, unused):
        reached.append(address)
        cpu.emu_stop()

    hook = cpu.hook_add(UC_HOOK_CODE, stop_at_wrapper, begin=bearings.WRAPPER, end=bearings.WRAPPER)
    cases = []
    # Four original call contexts across three sites, plus the two pirate tables.
    for call, tables in (*bearings.CALLSITES.items(), (pirate.CALL, pirate.TABLES)):
        for table in tables:
            cases.extend((call, table, address, localized) for address, _, localized in bearings.BEARINGS)
            cases.extend((call, table, address, None) for address in (0x02145120, 0x02145129, 0x02145154))
    cases.append((pirate.CALL, 0x02118560, bearings.BEARINGS[0][0], None))
    output = []
    for call, table, pointer, expected in cases:
        reached.clear()
        registers = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4)
        values = (1, table, pointer, 0x02465000, 0xA6B7C8D9)
        for register, word in zip(registers, values, strict=True):
            cpu.reg_write(register, word)
        cpu.reg_write(UC_ARM_REG_LR, STOP)
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.mem_write(STACK, b'\x96' * 32)
        cpu.emu_start(call, STOP, count=128)
        actual = tuple(cpu.reg_read(reg) for reg in registers)
        assert reached == [bearings.WRAPPER] and cpu.reg_read(UC_ARM_REG_PC) == bearings.WRAPPER
        assert cpu.reg_read(UC_ARM_REG_LR) == call + 4 and cpu.reg_read(UC_ARM_REG_SP) == STACK
        assert bytes(cpu.mem_read(STACK, 32)) == b'\x96' * 32
        assert actual[:2] == values[:2] and actual[3:] == values[3:]
        if expected is None:
            assert actual[2] == pointer
        else:
            assert bytes(cpu.mem_read(actual[2], len(expected) + 1)) == expected + b'\0'
        output.append(dict(call=call, table=table, source_pointer=pointer, result_pointer=actual[2],
                           spoken_argument=expected.decode('ascii') if expected else None))
    cpu.hook_del(hook)
    assert len(output) == 73
    return output


def original_arguments(ctx):
    cpu, get, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    bearings_by_ptr = {pointer: text for pointer, text, _ in bearings.BEARINGS}
    vectors = ((0, 0), (100, 0), (-100, 0), (0, 100), (0, -100), (100, 100),
               (-100, 100), (100, -100), (-100, -100))
    receipts = []
    for x, y in vectors:
        pointer = get(0x6567C, x & 0xffffffff, y & 0xffffffff)
        raw = bearings_by_ptr[pointer]
        assert bytes(cpu.mem_read(pointer, len(raw) + 1)) == raw + b'\0'
        receipts.append(dict(vector=[x, y], pointer=pointer, text=raw.decode('ascii')))
    assert {row['pointer'] for row in receipts} == bearings_by_ptr.keys()
    companies = {}
    for n in range(20):
        obj = get(0xCB160) + 4 + 76 * n
        vt, = unpack_from('<I', cpu.mem_read(obj, 4))
        getter, = unpack_from('<I', cpu.mem_read(vt + 8, 4))
        pointer = get(getter - bearings.BASE, obj)
        text = bytes(cpu.mem_read(pointer, 64)).split(b'\0', 1)[0]
        assert text.isascii() and text and len(text) <= 16
        companies[n] = text
    assert companies[17] == b'Kurushima' and companies[2] == b'Bergstrom Fleet'
    ctx.calls.clear()
    return receipts, companies


def main():
    assert not ROOT.exists() and not MANUSCRIPT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    ctx = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    clean = base.NdsImage.open(CLEAN)
    clean_arm = clean.read_file(ARM)
    arm, common = ctx.arm, ctx.common
    for table, slots in TABLES.items():
        at = table - bearings.BASE
        assert unpack_from('<8i', clean_arm, at) == unpack_from('<8i', arm, at) == slots
    assert arm[0x6567C:0x65794] == clean_arm[0x6567C:0x65794]
    target_arm, runtime = bearings.install(arm, clean_arm, release['target_ARM9_sha256'])
    controls = bearing_controls(target_arm)
    directions, companies = original_arguments(ctx)
    source = common_message_entries(clean.read_file(COMMON), clean_arm)
    old = owned_entries(common, arm, digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    changes = encoded_changes()
    target, installed, allocation = owned_deployment(common, arm, old, changes)
    raster, _, font = font_tools(ctx.image)
    kanji = ctx.image.read_file('/GRP/KANJI.FNT')
    cpu = machine(target_arm)
    rows, cases, pages = [], [], []
    counts = Counter()
    credited = {(r['file_path'], r['id']) for r in base.load(base.LEDGER)[base.CONTEXT]['integrated_record_keys']}
    for n in IDS:
        ident = f'COMMON_MESSAGE_{n}'
        assert (COMMON, ident) in credited
        a, b, c = source[n], old[n], installed[n]
        assert all(row.text.count(b'%s') == row.text.count(b'%') == 2 for row in (a, b, c))
        english, note = REVISIONS[n]
        family = SIGHTED if n < 622 else ATTACKED
        rows.append(dict(id=ident, message_ID=n, file_path=COMMON, speaker='Lookout selected by the game',
                         context=CONTEXT[family], source_meaning=MEANINGS[n], localization_note=note,
                         Japanese=a.text.decode('cp932'), previous_English=b.text.decode('ascii').strip(),
                         english=english, decision='revision', source_reference=reference(a),
                         current_reference=reference(b), staged_reference=reference(c), source_hex=a.text.hex(),
                         current_hex=b.text.hex(), staged_hex=c.text.hex(), review=dict.fromkeys(GATES, True)))
        for (_, short, heading), (company_id, company) in product(bearings.BEARINGS, companies.items()):
            formatted, lines = native_layout(cpu, c.text, n, heading, company)
            assert len(lines) <= 3, (n, heading, company, lines)
            assert any(heading.decode('ascii') in line for line in lines), (n, heading, company, lines)
            assert any(company.decode('ascii') in line for line in lines), (n, heading, company, lines)
            if len(lines[-1].split()) < 2:
                raise AssertionError((n, lines))
            if len(lines[-1]) <= 9:
                counts['brief_final_phrase'] += 1
            row = dict(message_ID=n, bearing=short.decode('ascii'), spoken_bearing=heading.decode('ascii'),
                       company_ID=company_id, company=company.decode('ascii'), lines=lines,
                       formatted_hex=formatted.hex(), native_printf_wrap_and_canaries=True)
            if (short, company_id) in ((b'vicinity', 9), (b'E', 17), (b'NW', 2)):
                plane, _ = render_portrait(raster, target_arm, kanji, formatted)
                row['plane_sha256'] = digest(plane)
                pages.append((f"{n} {row['bearing']} {row['company']}", plane))
            cases.append(row)
    assert len(rows) == 15 and len(cases) == 2700 and len(pages) == 45
    assert not any(b'\n' in text for text in changes.values())
    ROOT.mkdir()
    image = base.NdsImage.open(parent.ROM)
    before = files(image)
    for path, content in ((ARM, target_arm), (COMMON, target)):
        image.replace_file(path, content)
    after = files(image)
    assert after.keys() == before.keys() and {p for p in before if before[p] != after[p]} == {ARM, COMMON}
    image.save(ROM)
    for path in (ARM, COMMON):
        image.replace_file(path, before[path])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    sha = base.digest(ROM)
    base.save(MANUSCRIPT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=list(GATES), records=rows, candidate_sha256=sha,
        previous_sha256=release['candidate_sha256']))
    base.save(STORED, dict(candidate_sha256=sha, previous_sha256=release['candidate_sha256'],
        target_ARM9_sha256=digest(target_arm), target_COMMON_sha256=digest(target), allocations=allocation,
        bearings=runtime, bearing_controls=controls, original_compass_cases=directions,
        original_faction_names={n: name.decode('ascii') for n, name in companies.items()},
        native_cases=cases, sheets=portrait_sheets(ROOT, pages), font=font,
        layout_findings=dict(counts), whole_parent_inverse=True, manuscript_sha256=base.digest(MANUSCRIPT)))
    print('Staged 15 alerts with 73 call checks, 2,700 native grid cases and 45 preview pages.')


if __name__ == '__main__':
    main()

