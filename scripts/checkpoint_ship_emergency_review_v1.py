"""Bind the leak, fire, and shortage review to the registered sailing callers."""

from collections import Counter
import csv
from hashlib import sha256
import struct
from unicodedata import normalize

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_sailing_alert_review_v1 import BASE, GATES, branch_target, caller_binding, word
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.register_mutiny_review_v1 import RELEASE
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_literal_notice_callers_v1 import current_copy
from scripts.seal_shared_text_source_v1 import ARM, CLEAN, COMMON, ROOT, reference


IDS = tuple(range(573, 614))
DRAFTS = ROOT / 'ship_emergency_source_drafts.tsv'
DECISIONS = ROOT / 'ship_emergency_decisions.tsv'
OUTPUT = ROOT / 'ship_emergency_contextual_review.json'
GROUPS = (
    (573, 580, 0x118620, 0x31604, ((0x31550, 0x31558),), 0x53D44, 13, (),
     'The flagship is taking on water. The original Shipwright role reports a leak or damage to the bottom of its hull.'),
    (580, 585, 0x118600, 0x31608, ((0x315A0, 0x315A8),), 0x53F0C, None, ('named ship',),
     'A different ship has sprung a leak. Its original name getter supplies the ship in the alarm.'),
    (585, 593, 0x1185E0, 0x2DEBC, ((0x2D78C, 0x2D790),), 0x53D44, 15, (),
     'The fire on the flagship has been extinguished. The original Deckhand role supplies the voice.'),
    (593, 601, 0x1185C0, 0x2DEC0, ((0x2D7D8, 0x2D7E0),), 0x53F0C, None, ('named ship',),
     'The fire on a different ship has been extinguished. Keep the ship in the report and the original agency where expressed.'),
    (601, 609, 0x1185A0, 0x81ED0, ((0x81E6C, 0x81EAC),), 0x53D44, 1, ('Water or Food',),
     'The First Mate voice reports that one of the two supplies has run out. The game checks the two supplies in original order.'),
    (610, 614, 0x118580, 0x782C8, ((0x78260, 0x78270), (0x78280, 0x7828C)), 0x53D44, 1,
     ('one or both depleted supplies', 'automatic travel'),
     'Automatic travel stops when supplies run out. The first argument identifies the depleted supplies and the second names the canceled activity.'),
)


def read_rows(path):
    with path.open(encoding='utf-8', newline='') as stream:
        entries = list(csv.DictReader(stream, delimiter='\t'))
    assert tuple(int(row['message_ID']) for row in entries) == IDS
    return {int(row['message_ID']): row for row in entries}


def bind_runtime(runtime, clean):
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    actors = {i: runtime.actor_root + (0x19E4 if i == 3 else 4 + i * 32) for i in range(207)}
    voices = {i: get(0x7E988, pointer) for i, pointer in actors.items()}
    groups = []
    for first, end, table, literal, calls, entry, role, args, context in GROUPS:
        assert clean[table:table + 32] == runtime.arm[table:table + 32]
        slots = struct.unpack_from('<8i', clean, table)
        assert set(slots) - {-1} == set(range(first, end))
        cases = []
        for actor, pointer in actors.items():
            voice = voices[actor]
            expected = first if slots[voice] == -1 else slots[voice]
            assert get(0x53F4C, pointer, BASE + table) == expected
            cases.append((actor, voice, expected))
        assert get(0x53F4C, 0, BASE + table) == first
        groups.append(dict(first_ID=first, last_ID=end - 1, table=BASE + table, table_slots=slots,
            native_callers=[caller_binding(clean, runtime.arm, pc, call, literal, BASE + table, entry) for pc, call in calls],
            consumer=BASE + entry, original_role_argument=role, arguments=args, context=context,
            speaker={13: 'Shipwright', 15: 'Deckhand', 1: 'First Mate', None: 'Crew member selected by the original ship response'}[role],
            original_voice_choices=cases))
    assert sum(len(group['original_voice_choices']) for group in groups) == 1242
    for pc in (0x81E9C, 0x78278):
        assert branch_target(clean, pc) == branch_target(runtime.arm, pc) == 0x020A4C24

    def read_label(pointer):
        return bytes(cpu.mem_read(pointer, 32)).split(b'\0', 1)[0].decode('cp932')

    supplies = [dict(index=i, pointer=get(0xA4C24, i)) for i in range(2)]
    for row in supplies:
        row['English'] = read_label(row['pointer'])
    assert [row['English'] for row in supplies] == ['Water', 'Food']
    labels = []
    for offset, japanese, english in ((0x782CC, '水と食料', 'water and food'), (0x782D0, '自動移動', 'automatic travel')):
        source_ptr, current_ptr = word(clean, offset), word(runtime.arm, offset)
        source_start = source_ptr - BASE
        assert clean[source_start:clean.index(0, source_start)].decode('cp932') == japanese
        assert read_label(current_ptr) == english
        labels.append(dict(literal=BASE + offset, source_pointer=source_ptr, current_pointer=current_ptr,
            Japanese=japanese, English=english))
    assert clean[0x3158C:0x315A0] == runtime.arm[0x3158C:0x315A0]
    assert clean[0x2D7C4:0x2D7D8] == runtime.arm[0x2D7C4:0x2D7D8]
    assert word(clean, 0x31594) == word(clean, 0x2D7CC) == 0xE5911004
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    runtime.calls.clear()
    return groups, dict(supplies=supplies, automatic_travel_literals=labels, ship_name_virtual_slot=4,
        ship_name_getter_call_sites=[0x02031598, 0x0202D7D0])


def main():
    assert not OUTPUT.exists()
    drafts, decisions = read_rows(DRAFTS), read_rows(DECISIONS)
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
    credited = {row['id'] for row in ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']
                if row['file_path'] == COMMON}
    assert not {f'COMMON_MESSAGE_{n}' for n in IDS} & credited
    del ledger
    groups, arguments = bind_runtime(runtime, clean_arm)
    lone = dict(context='A hungry sailor speaks about dizziness and feeling unable to go on. The source does not describe a collapse.',
        speaker='Sailor selected by the original fleet', arguments=(),
        native_callers=[caller_binding(clean_arm, runtime.arm, 0x30808, 0x3080C, 0x30FC4, 609, 0x53FE4)])
    by_id = {n: group for group in groups for n in range(group['first_ID'], group['last_ID'] + 1)} | {609: lone}
    records = []
    for n in IDS:
        jp, old = source[n], current[n]
        japanese, current_text = (row.text.decode('cp932') for row in (jp, old))
        prior = ' '.join(normalize('NFKC', current_text).split())
        revision = decisions[n]['replacement_English']
        english = revision or prior
        group = by_id[n]
        assert english.isascii() and english == ' '.join(english.split())
        assert bool(revision) == (english != prior)
        assert japanese.count('%s') == current_text.count('%s') == english.count('%s') == len(group['arguments'])
        assert english.count('%') == len(group['arguments']) and not any(t in english for t in ('FA','FI','FO','FU','IC'))
        row = dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, file_path=COMMON, source_reference=reference(jp),
            current_reference=reference(old), source_hex=jp.text.hex(), current_hex=old.text.hex(), source_Japanese=japanese,
            current_English=current_text, english=english, independent_English=drafts[n]['independent_English'],
            source_meaning=drafts[n]['source_meaning'], localization_note=decisions[n]['localization_note'],
            decision='revision' if revision else 'retention', speaker=group['speaker'], context=group['context'],
            review={gate: gate != 'formatting' for gate in GATES}, original_substitutions=group['arguments'])
        row['original_current_native_lookup'] = current_copy(runtime, row, BASE + 0x5528C)
        runtime.calls.pop()
        records.append(row)
    stats = Counter(row['decision'] for row in records)
    save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=GATES, registered_input=runtime.receipt(),
        source_ROM=str(CLEAN), source_ROM_sha256=release['clean_input_sha256'], records=records, counts=stats,
        exact_native_groups=groups, single_sailor_consumer=lone, arguments=arguments, current_native_lookups=len(records),
        voice_cases=1242, new_gameplay=False, formatting_pending=True, registered_release_pending=True, new_credit=0,
        full_goal_complete=False, evidence={str(p): digest(p) for p in (DRAFTS, DECISIONS, RELEASE, __file__)}))
    print(f'{len(records)} contextual decisions, {dict(stats)}, 1,242 voice choices and the original argument sources.')


if __name__ == '__main__':
    main()
