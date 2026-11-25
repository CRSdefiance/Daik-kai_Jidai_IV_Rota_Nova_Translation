"""Bind the complete unrest and mutiny review to native dialogue and menu branches."""

from collections import Counter
import csv
from hashlib import sha256
import struct
from unicodedata import normalize

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.audit_story_glyph_consistency import load, save, wide_letters
from scripts.checkpoint_sailing_alert_review_v1 import BASE, GATES, branch_target, caller_binding, word
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.native_call_abi_v764 import call
from scripts.register_sailing_alert_review_v2 import RELEASE
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_literal_notice_callers_v1 import current_copy
from scripts.seal_shared_text_source_v1 import ARM, CLEAN, COMMON, ROOT, reference


IDS = tuple(range(508, 573))
DRAFTS = ROOT / 'mutiny_source_drafts.tsv'
DECISIONS = ROOT / 'mutiny_decisions.tsv'
OUTPUT = ROOT / 'mutiny_contextual_review.json'
GROUPS = (
    (509, 516, 0x118740, 0x31C8C, ((0x31BBC, 0x31BC4),), 0x53D44, 1,
        'Early unrest after the sailor begs for land. The crew report fatigue or discontent and advise a port call.'),
    (517, 525, 0x118720, 0x31B4C, ((0x31640, 0x31648),), 0x53D44, 1,
        'The sailor has threatened force. The crew voice reports the imminent confrontation and asks the admiral to decide.'),
    (525, 532, 0x117580, 0x31B58, ((0x31770, 0x31774),), 0x53F0C, 8,
        'Choice 0, with a Boarding Leader assigned. The Boarding Leader challenges the crew. The sailor backs down.'),
    (533, 541, 0x1175A0, 0x31B5C, ((0x3179C, 0x317A4),), 0x53F0C, 8,
        'Choice 0, after the frightened sailor backs down. The Boarding Leader advises reaching port before it happens again.'),
    (541, 548, 0x1186C0, 0x31B64, ((0x318F0, 0x318F4),), 0x53D44, 1,
        'Choice 0, with no Boarding Leader assigned. The crew voice explains why forcing the crew to stand down is unavailable.'),
    (548, 552, 0x116800, 0x31B68, ((0x31904, 0x31908),), 0x53BD8, None,
        'Choice 1. The admiral offers a shared meal to mollify the crew. The player captain determines the four alternate speeches.'),
    (554, 558, 0x116820, 0x31B74, ((0x319F4, 0x319F8), (0x31AD0, 0x31AD4)), 0x53BD8, None,
        'Choice 1 when the offer fails, or choice 2. A sailor calls on the crew to beat the admiral. The captain protests in pain.'),
    (558, 565, 0x118660, 0x31B78, ((0x31A00, 0x31A04), (0x31ADC, 0x31AE0)), 0x53D44, 1,
        'Choice 1 when the offer fails, or choice 2. Another crew voice intervenes after the admiral is struck.'),
    (565, 572, 0x118640, 0x31B7C, ((0x31A50, 0x31A54),), 0x53F0C, 12,
        'Choice 1 when the supplies permit the meal and a Chief Cook is assigned. The cook agrees to prepare it.'),
)
SINGLES = {
    508: ((0x31BB4, 0x31BB8, None), 'Early unrest. A sailor cries out about the long voyage before a crew officer advises docking.'),
    516: ((0x31638, 0x3163C, None), 'The confrontation escalates. A sailor threatens to force a port call before the response menu.'),
    532: ((0x31674, 0x31798, 0x18), 'Choice 0 with a Boarding Leader. A sailor recoils from the personal challenge.'),
    552: ((0x316CC, 0x319E0, 0x40), 'Choice 1 when the meal offer fails. A sailor rejects it before calling for the admiral to be beaten.'),
    553: (None, 'Choice 1 when the offer fails, or choice 2. A sailor urges the others to drag out the admiral and beat them.'),
    572: ((0x316BC, 0x31A8C, 0x58), 'Choice 1 when the offer succeeds. A sailor approves the admiral’s response, with or without a cook’s acknowledgment.'),
}
CHOICES = (
    (0, 0x134E18, '鎮圧する', 'Quell Mutiny', 'Direct suppression. The Boarding Leader determines whether it can proceed.'),
    (1, 0x134E3C, '懐柔する', 'Appease Crew', 'Conciliation. The captain proposes a special meal, with different outcomes.'),
    (2, 0x134E24, '放置する', 'Do Nothing', 'Inaction. The response advances to the assault sequence.'),
)
PRONOUN_IDS = (527, 566)


def indexed(path):
    with path.open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    assert tuple(int(row['message_ID']) for row in rows) == IDS
    return {int(row['message_ID']): row for row in rows}


def arm_immediate(instruction):
    assert instruction & 0x0FE00000 == 0x03A00000
    rotate = 2 * ((instruction >> 8) & 15)
    value = instruction & 255
    return ((value >> rotate) | (value << (32 - rotate))) & 0xFFFFFFFF


def exact_singles(arm, current):
    singles = {}
    for n, (call, context) in SINGLES.items():
        if call is None:
            bindings = [caller_binding(arm, current, pc, end, 0x31B70, n, 0x53FE4)
                        for pc, end in ((0x319EC, 0x319F0), (0x31AC8, 0x31ACC))]
        else:
            pc, end, slot = call
            assert arm_immediate(word(arm, pc)) == n
            assert branch_target(arm, end) == 0x02053FE4
            if slot is None:
                assert (word(arm, pc) >> 12) & 15 == 1 and pc + 4 == end
            else:
                assert word(arm, pc + 4) == 0xE58D0000 | slot
                assert word(arm, end - 4) == 0xE59D1000 | slot
            bindings = [dict(immediate_PC=BASE + pc, call_PC=BASE + end, message_ID=n, stack_slot=slot,
                consumer=0x02053FE4, immediate_hex=arm[pc:pc + (4 if slot is None else 8)].hex(),
                final_load_and_call_hex=arm[end - 4:end + 4].hex())]
        singles[n] = dict(context=context, native_callers=bindings,
            speaker='Sailor selected from the original fleet by the game')
    return singles


def pointer_aliases(arm, address):
    encoded = struct.pack('<I', address)
    return [offset for offset in range(0, len(arm) - 3, 4) if arm[offset:offset + 4] == encoded]


def menu_labels(arm, current):
    table = 0x1150B8
    call = caller_binding(arm, current, 0x31720, 0x31734, 0x31B50, BASE + table, 0x51E7C)
    assert pointer_aliases(arm, BASE + table) == pointer_aliases(current, BASE + table) == [0x31B50]
    assert [arm_immediate(word(arm, at)) for at in (0x3165C,)] == [3]
    assert word(arm, 0x31660) == 0xE58D000C and word(arm, 0x31724) == 0xE59D100C
    choices = []
    for index, offset, japanese, english, context in CHOICES:
        field = table + 4 * index
        pointer = BASE + offset
        original = japanese.encode('cp932') + b'\0'
        assert word(arm, field) == word(current, field) == pointer
        assert pointer_aliases(arm, pointer) == pointer_aliases(current, pointer) == [field]
        assert arm[offset:offset + len(original)] == current[offset:offset + len(original)] == original
        choices.append(dict(id=f'ARM9_MUTINY_CHOICE_{index}', file_path=ARM, choice_index=index,
            source_reference=dict(pointer_field=BASE + field, literal_offset=offset, terminator_offset=offset + len(original) - 1),
            current_reference=dict(pointer_field=BASE + field, literal_offset=offset, terminator_offset=offset + len(original) - 1),
            source_hex=original.hex(), current_hex=original.hex(), source_Japanese=japanese, current_English=japanese,
            english=english, source_meaning=context, localization_note='Use a short English action label for the existing branch.',
            speaker='Mutiny response menu', context=context, decision='revision',
            review={gate: gate != 'formatting' for gate in GATES}))
    return dict(native_caller=call, original_result_branches=[0x02031754, 0x02031904, 0x02031AAC],
        original_choice_order_preserved=True, records=choices)


def exact_groups(runtime, clean):
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    actors = {i: runtime.actor_root + (0x19E4 if i == 3 else 4 + 32 * i) for i in range(207)}
    voices = {i: get(0x7E988, pointer) for i, pointer in actors.items()}
    groups = []
    for first, end, table, literal, sites, entry, role, context in GROUPS:
        count = 4 if entry == 0x53BD8 else 8
        stop = table + 4 * count
        assert clean[table:stop] == runtime.arm[table:stop]
        slots = struct.unpack_from(f'<{count}i', clean, table)
        assert set(slots) - {-1} == set(range(first, end))
        cases = []
        if entry == 0x53BD8:
            assert get(0x53C6C, BASE + table) == slots[3]
        else:
            for actor, pointer in actors.items():
                voice = voices[actor]
                expected = slots[voice] if slots[voice] != -1 else first
                assert get(0x53F4C, pointer, BASE + table) == expected
                cases.append((actor, voice, expected))
            assert get(0x53F4C, 0, BASE + table) == first
        callers = [caller_binding(clean, runtime.arm, pc, call, literal, BASE + table, entry)
                   for pc, call in sites]
        groups.append(dict(first_ID=first, last_ID=end - 1, table=BASE + table, table_slots=slots,
            native_callers=callers, original_role_argument=role, context=context, original_voice_choices=cases,
            consumer=BASE + entry, original_captain_index=3 if count == 4 else None,
            speaker={1: 'First Mate voice alternative', 8: 'Boarding Leader voice alternative',
                     12: 'Chief Cook voice alternative', None: 'Admiral selected by the player captain index'}[role]))
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    runtime.calls.clear()
    return groups


def pronouns(runtime, clean, source, groups, rows):
    start, stop = 0x53914, 0x53AC4
    assert sha256(clean[start:stop]).hexdigest() == '71f0a5626d1992a8e2a2f0fb5a287bb42d719c0861488c64aec7ea5fe5386d87'
    assert runtime.arm[0x7E9B8:0x7E9D0] == clean[0x7E9B8:0x7E9D0]
    manifest = load(runtime.release['manifest'])
    guards = manifest['relocations'][ARM]['common_literal_prefix']['changes']
    reconstructed = bytearray(runtime.arm[start:stop])
    for offset in (0x5397C, 0x53A44):
        change = next(row for row in guards if row['offset'] == offset)
        assert word(runtime.arm, offset) == change['after'] and word(clean, offset) == change['before']
        at = offset - start
        reconstructed[at:at + 4] = clean[offset:offset + 4]
    assert bytes(reconstructed) == clean[start:stop]

    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    input_at, output_at = 0x02450020, 0x02451020
    cases = []
    for n in PRONOUN_IDS:
        group = next(group for group in groups if group['first_ID'] <= n <= group['last_ID'])
        for actor_id, _, selected in group['original_voice_choices']:
            if selected != n:
                continue
            actor = runtime.actor_root + 4 + actor_id * 32
            kind = get(0x7E9B8, actor)
            assert kind in (0, 1)
            pronoun = ('アタシ' if kind else '僕').encode('cp932')
            japanese = source[n].text
            english = rows[n]['english'].encode('ascii')
            assert japanese.count(b'IC') == 1 and b' me!' in english
            for text, expected in ((japanese, japanese.replace(b'IC', pronoun)), (english, english)):
                cpu.mem_write(input_at - 16, b'\xA5' * 16 + text + b'\0' + b'\xA5' * 16)
                cpu.mem_write(output_at - 16, b'\xA5' * 560)
                call(cpu, start, (output_at, input_at, actor))
                assert bytes(cpu.mem_read(input_at - 16, len(text) + 33)) == b'\xA5' * 16 + text + b'\0' + b'\xA5' * 16
                assert bytes(cpu.mem_read(output_at - 16, 560)) == (
                    b'\xA5' * 16 + expected + b'\0' + b'\xA5' * (543 - len(expected)))
            cases.append(dict(message_ID=n, actor_ID=actor_id, pronoun_kind=kind,
                japanese_first_person=pronoun.decode('cp932'), english_first_person='me'))
    assert Counter(row['message_ID'] for row in cases) == {527: 7, 566: 7}
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    runtime.calls.clear()
    return dict(native_parser=BASE + start, native_first_person_selector=0x0207E9B8,
        clean_parser_recovered_with_only_registered_literal_guards=True, cases=cases,
        source_pronoun_meaning_preserved_as_english_object_me=True, unrelated_runtime_macro_behavior_unchanged=True)


def main():
    assert not OUTPUT.exists()
    drafts, decisions = indexed(DRAFTS), indexed(DECISIONS)
    release = load(RELEASE)
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    assert digest(CLEAN) == release['clean_input_sha256']
    clean = NdsImage.open(CLEAN)
    clean_arm = clean.read_file(ARM)
    source = common_message_entries(clean.read_file(COMMON), clean_arm)
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    current = owned_entries(runtime.common, runtime.arm, directory)
    ledger = load('translations/editorial_review_current_v1.json')
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    ctx = ledger['contextual_story_natural_dialogue_pass_v1871']
    credited = {(row['file_path'], row['id']) for row in ctx['integrated_record_keys']}
    assert not {(COMMON, f'COMMON_MESSAGE_{n}') for n in IDS} & credited
    assert not {(ARM, f'ARM9_MUTINY_CHOICE_{n}') for n in range(3)} & credited
    del ledger, ctx

    for lo, hi in ((0x3160C, 0x31B80), (0x31B84, 0x31C90), (0x51E7C, 0x51F64), (0x53BD8, 0x54018)):
        assert clean_arm[lo:hi] == runtime.arm[lo:hi]
    groups = exact_groups(runtime, clean_arm)
    single = exact_singles(clean_arm, runtime.arm)
    menu = menu_labels(clean_arm, runtime.arm)
    by_id = {n: group for group in groups for n in range(group['first_ID'], group['last_ID'] + 1)}
    assert not by_id.keys() & single.keys() and by_id.keys() | single.keys() == set(IDS)
    records, corrupted = [], []
    for n in IDS:
        japanese, old = source[n], current[n]
        jp, old_text = (entry.text.decode('cp932') for entry in (japanese, old))
        paragraph = ' '.join(normalize('NFKC', old_text).split())
        replacement = decisions[n]['replacement_English']
        english = replacement or paragraph
        assert english.isascii() and english == ' '.join(english.split())
        assert bool(replacement) == (english != paragraph), n
        macros = ['IC'] if n in PRONOUN_IDS else []
        assert jp.count('IC') == len(macros) and 'IC' not in english and 'IC' not in old_text
        assert '%' not in jp and '%' not in english
        group = by_id.get(n, single.get(n))
        row = dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, file_path=COMMON,
            source_reference=reference(japanese), current_reference=reference(old),
            source_hex=japanese.text.hex(), current_hex=old.text.hex(), source_Japanese=jp, current_English=old_text,
            english=english, independent_English=drafts[n]['independent_English'], source_meaning=drafts[n]['source_meaning'],
            localization_note=decisions[n]['localization_note'], decision='revision' if replacement else 'retention',
            review={gate: gate != 'formatting' for gate in GATES}, source_native_macros=macros,
            native_substitution_localization='IC first-person pronoun expressed as me' if macros else None,
            inherited_fullwidth_Latin=wide_letters(old_text),
            speaker=group['speaker'], context=group['context'],
            original_selector_slots=[i for i, number in enumerate(group.get('table_slots', ())) if number == n])
        row['original_current_native_lookup'] = current_copy(runtime, row, BASE + 0x5528C)
        runtime.calls.pop()
        records.append(row)
        if paragraph in ('Something strange has appeared at sea.', 'Somethin', 'g strange has appeared at sea.'):
            corrupted.append(n)
    stats = Counter(row['decision'] for row in records)
    assert len(corrupted) == 26 and {532, 533} <= set(corrupted)
    assert sum(len(group['original_voice_choices']) for group in groups) == 1449
    pronoun_proof = pronouns(runtime, clean_arm, source, groups, {row['message_ID']: row for row in records})
    save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=GATES, registered_input=runtime.receipt(),
        source_ROM=str(CLEAN), source_ROM_sha256=release['clean_input_sha256'], records=records, counts=stats,
        exact_native_crew_groups=groups, native_sailor_calls=single, original_choice_menu=menu,
        native_lookup_count=len(records), wrong_current_text_IDs=corrupted, localized_IC_first_person=pronoun_proof,
        old_role_label_corrections=[545, 546, 547], no_new_gameplay=True, formatting_pending=True,
        registered_release_pending=True, new_credit=0, full_goal_complete=False,
        evidence={str(p): digest(p) for p in (DRAFTS, DECISIONS, RELEASE, __file__)}))
    print(f"{len(records)} dialogue decisions ({stats['revision']} revisions, {stats['retention']} retentions) and 3 menu labels.")
    print('Exact current lookup for all dialogue, 1,449 voice choices, 26 incorrect lines and 14 native first-person cases.')


if __name__ == '__main__':
    main()
