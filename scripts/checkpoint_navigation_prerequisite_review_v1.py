"""Bind the complete Auto Move warnings to the original decision and voices."""

from collections import Counter
import csv
from hashlib import sha256
from itertools import product
import struct

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_sailing_alert_review_v1 import BASE, GATES, branch_target, caller_binding, word
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import machine
from scripts.register_ship_emergency_review_v1 import RELEASE
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_literal_notice_callers_v1 import current_copy
from scripts.seal_shared_text_source_v1 import ARM, CLEAN, COMMON, ROOT, reference


IDS = tuple(range(629, 653))
DRAFTS = ROOT / 'navigation_prerequisite_source_drafts.tsv'
DECISIONS = ROOT / 'navigation_prerequisite_decisions.tsv'
OUTPUT = ROOT / 'navigation_prerequisite_contextual_review.json'
GROUPS = (
    (629, 3, 0x118520, 0x9962C, 0x99598, 1, 'First Mate',
     'The admiral confirms an Auto Move destination. The game checks both ports, then finds '
     'no eligible Surveyor in the required crew assignment. The First Mate voice reports the '
     'missing Surveyor. Acknowledging the warning returns to the confirmation.'),
    (637, 1, 0x118500, 0x99630, 0x995A8, 4, 'Surveyor',
     'The admiral confirms an Auto Move destination. An endpoint or the planned connection '
     'fails its route check. The Surveyor voice reports the route failure. Acknowledging the '
     'warning returns to the confirmation.'),
    (645, 2, 0x117820, 0x99634, 0x995B8, 4, 'Surveyor',
     "The admiral confirms an Auto Move destination. The Surveyor requirement passes, then "
     "the second assignment check fails. The Surveyor voice asks the admiral to give the order "
     "from the Captain's Cabin. Acknowledging the warning returns to the confirmation."),
)
PREDICATE_CALLS = {
    0x9964C: 0xCB178, 0x9965C: 0xB4A88, 0x99668: 0xCB178, 0x99678: 0xB4A88,
    0x99684: 0xCB1A8, 0x99698: 0x829C8, 0x996A4: 0xCB1A8, 0x996B8: 0x829C8,
    0x996C8: 0x89AE8, 0x996CC: 0xCB160, 0x996D0: 0x397D8, 0x996E4: 0x897AC,
    0x996F4: 0x89AC8, 0x99708: 0x89AC8,
}


def read_rows(path):
    with path.open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    assert tuple(int(row['message_ID']) for row in rows) == IDS
    return {int(row['message_ID']): row for row in rows}


def bind_predicate(clean, arm):
    # 0x99638 is the separately localized literal for unexpected result codes.
    spans = ((0x994BC, 0x99638), (0x9963C, 0x99740))
    for start, stop in spans:
        assert clean[start:stop] == arm[start:stop]
    for pc, target in PREDICATE_CALLS.items():
        assert branch_target(arm, pc) == BASE + target
    assert branch_target(arm, 0x99554) == 0x02051F4C
    assert branch_target(arm, 0x9956C) == 0x0209963C
    assert branch_target(arm, 0x99614) == 0x02033860

    cpu = machine(arm)
    origin, destination = 7, 11
    ports, fleet = 0x02480000, 0x02490000
    checks = (0x9965C, 0x99678, 0x99698, 0x996B8, 0x996E4)
    failure = (1, 1, 3, 2, 1)
    bound = []
    for passed in product((False, True), repeat=len(checks)):
        results = dict(zip(checks, passed, strict=True))
        visited, cleanup = [], []

        def replace_dependency(u, address, size, _):
            pc = address - BASE
            if pc in results:
                visited.append(pc)
            if pc in (0x996F4, 0x99708):
                cleanup.append(pc)
            if pc in (0x9965C, 0x99678):
                port = origin if pc == 0x9965C else destination
                assert u.reg_read(UC_ARM_REG_R0) == ports + 4 + port * 0x6C
            if pc in (0x99698, 0x996B8):
                purpose = 3 if pc == 0x99698 else 5
                assert u.reg_read(UC_ARM_REG_R1) == purpose
                assert u.reg_read(UC_ARM_REG_R0) == fleet + word(arm, 0x9973C)
            if pc == 0x996E4:
                assert (u.reg_read(UC_ARM_REG_R1), u.reg_read(UC_ARM_REG_R2)) == (origin, destination)
            value = {0x9964C: ports, 0x99668: ports, 0x99684: fleet, 0x996A4: fleet}.get(pc, 0)
            u.reg_write(UC_ARM_REG_R0, int(results.get(pc, value)))
            u.reg_write(UC_ARM_REG_PC, address + 4)

        handles = [cpu.hook_add(UC_HOOK_CODE, replace_dependency, begin=BASE + pc, end=BASE + pc)
                   for pc in PREDICATE_CALLS]
        try:
            call(cpu, 0x9963C, (0, origin, destination, 0))
        finally:
            for handle in handles:
                cpu.hook_del(handle)
        first_failure = next((i for i, passed_gate in enumerate(passed) if not passed_gate), len(checks))
        expected = failure[first_failure] if first_failure < len(checks) else 0
        assert cpu.reg_read(UC_ARM_REG_R0) == expected
        assert visited == list(checks[:first_failure + 1])
        assert cleanup == ([0x99708] if first_failure == 4 else [0x996F4] if expected == 0 else [])
        bound.append(dict(condition_inputs=passed, visited=[BASE + pc for pc in visited], result=expected))
    return dict(entry=BASE + 0x9963C, confirm=0x02051F4C, successful_dispatch=0x02033860,
        conditions=['origin eligible', 'destination eligible', 'purpose 3', 'purpose 5', 'route found'],
        exact_dispatch_and_predicate_spans=[dict(start=BASE + start, stop=BASE + stop,
            sha256=sha256(arm[start:stop]).hexdigest()) for start, stop in spans],
        focused_dependency_results=bound)


def bind_voices(runtime, clean):
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    actors = {i: runtime.actor_root + (0x19E4 if i == 3 else 4 + i * 32) for i in range(207)}
    voices = {i: get(0x7E988, pointer) for i, pointer in actors.items()}
    assert word(clean, 0x99520) == 0xE3A06001 and word(clean, 0x99524) == 0xE3A04004
    groups = []
    for first, result, table, literal, load_pc, role, speaker, context in GROUPS:
        assert clean[table:table + 32] == runtime.arm[table:table + 32]
        slots = struct.unpack_from('<8i', clean, table)
        assert set(slots) == set(range(first, first + 8))
        assert word(clean, load_pc + 4) == (0xE1A00006 if role == 1 else 0xE1A00004)
        cases = []
        for actor, pointer in actors.items():
            voice = voices[actor]
            expected = slots[voice]
            assert get(0x53F4C, pointer, BASE + table) == expected
            cases.append((actor, voice, expected))
        assert get(0x53F4C, 0, BASE + table) == first
        groups.append(dict(first_ID=first, last_ID=first + 7, predicate_result=result,
            table=BASE + table, table_slots=slots, consumer=0x02053D44,
            native_callers=[caller_binding(clean, runtime.arm, load_pc, load_pc + 8, literal, BASE + table, 0x53D44)],
            original_role_argument=role, speaker=speaker, context=context, original_voice_choices=cases))
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    runtime.calls.clear()
    return groups


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
    predicate = bind_predicate(clean_arm, runtime.arm)
    groups = bind_voices(runtime, clean_arm)
    by_id = {n: group for group in groups for n in range(group['first_ID'], group['last_ID'] + 1)}
    records = []
    for n in IDS:
        jp, old = source[n], current[n]
        japanese, current_text = (row.text.decode('cp932') for row in (jp, old))
        prior = ' '.join(current_text.split())
        revision = decisions[n]['replacement_English']
        english = revision or prior
        assert english.isascii() and english == ' '.join(english.split())
        assert bool(revision) == (english != prior)
        assert not any('%' in body for body in (japanese, current_text, english))
        assert all(not token in english for token in ('FI', 'FA', 'FO', 'FU', 'IC'))
        group = by_id[n]
        row = dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, file_path=COMMON, source_reference=reference(jp),
            current_reference=reference(old), source_hex=jp.text.hex(), current_hex=old.text.hex(),
            source_Japanese=japanese, current_English=current_text, english=english,
            independent_English=drafts[n]['independent_English'], source_meaning=drafts[n]['source_meaning'],
            localization_note=decisions[n]['localization_note'], decision='revision' if revision else 'retention',
            speaker=group['speaker'], context=group['context'], original_substitutions=[],
            review={gate: gate != 'formatting' for gate in GATES})
        row['original_current_native_lookup'] = current_copy(runtime, row, BASE + 0x5528C)
        runtime.calls.pop()
        records.append(row)
    assert records[7]['current_English'] == 'No surveyor is assig'
    assert records[8]['current_English'].startswith('ned,\n')
    stats = Counter(row['decision'] for row in records)
    assert stats == {'revision': 23, 'retention': 1}
    voices = sum(len(group['original_voice_choices']) for group in groups)
    assert voices == 621
    save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=GATES, registered_input=runtime.receipt(),
        source_ROM=str(CLEAN), source_ROM_sha256=release['clean_input_sha256'], records=records, counts=stats,
        exact_native_groups=groups, native_navigation_predicate=predicate, current_native_lookups=len(records),
        voice_cases=voices, new_gameplay=False, formatting_pending=True, registered_release_pending=True, new_credit=0,
        full_goal_complete=False, evidence={str(p): digest(p) for p in (DRAFTS, DECISIONS, RELEASE, __file__)}))
    print(f'{len(records)} contextual decisions, {dict(stats)}, {voices} voice choices and 32 route predicate cases.')


if __name__ == '__main__':
    main()
