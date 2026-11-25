"""Review the nine approach, encounter and village families on the registered ROM."""

from collections import Counter
import csv
from hashlib import sha256

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_sailing_alert_review_v1 import BASE, GATES, branch_target, caller_binding, word
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.register_navigation_prerequisite_review_v1 import RELEASE
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.research_battle_declaration_context_v991c import ptr, text
from scripts.review_literal_notice_callers_v1 import current_copy
from scripts.seal_shared_text_source_v1 import ARM, CLEAN, COMMON, ROOT, reference


IDS = tuple(range(1290, 1357))
INVENTORY = ROOT / 'sea_approach_village_source_current_inventory.json'
DRAFTS = ROOT / 'sea_approach_village_source_drafts.tsv'
DECISIONS = ROOT / 'sea_approach_village_decisions.tsv'
OUTPUT = ROOT / 'sea_approach_village_contextual_review.json'
CONTEXT = {
    1290: ('A coastal settlement comes into view. The Lookout reports the discovery. '
           'The game shows the separate original settlement caption after the report.'),
    1297: ('The First Mate interrupts sailing to report another faction already in a naval battle. '
           'The admiral can aid the named fleet or decline through the original two-choice window. '
           'The same voice table serves both encounter branches.'),
    1305: ('The First Mate warns that the port itself is attacking the player fleet. '
           'The original town-object getter names that port and the caller then applies the original port attack.'),
    1313: ('The Lookout reports a newly sighted village. The original village name appears separately '
           'before the player proceeds with the encounter.'),
    1321: ('The First Mate reports the village sharing food and water with the fleet. '
           'The original effect replenishes the two supplies after the report.'),
    1329: ('The First Mate reports the welcome and its effect on the crew during a village visit. '
           'The youngest variant comments on the food. The other variants refer to the hospitality.'),
    1336: ('The First Mate reports repairs the villagers made. The original effect iterates through '
           'the fleet ship slots, so the report must work for one ship or several.'),
    1343: ('The First Mate reports the number of villagers who came forward during the village visit. '
           'The original number can be one. The youthful variant relays their willingness to come along.'),
    1350: ('The First Mate reports giving the villagers gold as thanks for their help. '
           'The original decimal substitution gives the exact amount, including a possible single unit.'),
}
ARGUMENTS = {1297: 'faction_label', 1305: 'port_label', 1343: 'villager_count', 1350: 'gold_amount'}
DECIMAL_VALUES = (1, 2, 5, 9, 10, 99, 100, 999, 9999, 99999)


def read_rows(path):
    with path.open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    assert tuple(int(row['message_ID']) for row in rows) == IDS
    return {int(row['message_ID']): row for row in rows}


def source_dependencies(clean, arm):
    spans = (
        (0x53CB0, 0x53DCC), (0x77378, 0x773B0), (0x774DC, 0x77524), (0x77690, 0x776BC),
        (0x77978, 0x779A4), (0x78304, 0x78350), (0x783E0, 0x78418), (0x78418, 0x784A0),
        (0x786C8, 0x786CC), (0x78CC0, 0x78CC8), (0xABF50, 0xABFC0),
    )
    for start, stop in spans:
        assert clean[start:stop] == arm[start:stop], (hex(start), hex(stop))
    assert word(arm, 0x786C8) == 0xE3A04007 and word(arm, 0x78CC0) == 0xE3A00007
    assert word(arm, 0x77508) == 0xE3A04001
    assert branch_target(arm, 0x77378) == 0x020CB178
    assert branch_target(arm, 0x77514) == 0x020CB160
    assert branch_target(arm, 0x7831C) == branch_target(arm, 0x783F0) == 0x020ABF50
    assert word(arm, 0x77698) == word(arm, 0x77980) == word(arm, 0x7738C) == 0xE5911008
    return [dict(start=BASE + start, end=BASE + stop, sha256=sha256(arm[start:stop]).hexdigest())
            for start, stop in spans]


def native_labels(cpu, get, root, count, stride, getter):
    values = []
    for index in range(count):
        obj = root + 4 + index * stride
        entry = ptr(cpu, ptr(cpu, obj) + 8)
        assert entry == getter
        pointer = get(entry - BASE, obj)
        raw = text(cpu, pointer)
        assert raw and raw.decode('ascii').strip() == raw.decode('ascii')
        values.append(dict(index=index, getter=entry, pointer=pointer, hex=raw.hex(), label=raw.decode('ascii')))
    return values


def bind_native(runtime, inventory, clean):
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    actors = {i: runtime.actor_root + (0x19E4 if i == 3 else 4 + 32 * i) for i in range(207)}
    voices = {i: get(0x7E988, pointer) for i, pointer in actors.items()}
    groups = []
    for group in inventory['groups']:
        first, last, table = (group[key] for key in ('first_ID', 'last_ID', 'original_voice_table'))
        slots = group['original_voice_slots']
        offset = table - BASE
        assert clean[offset:offset + 32] == runtime.arm[offset:offset + 32]
        assert {slot for slot in slots if slot >= 0} == set(range(first, last + 1))
        assert group['callers'] == [caller_binding(clean, runtime.arm, row['load_PC'] - BASE,
            row['call_PC'] - BASE, row['literal_address'] - BASE, table, row['consumer'] - BASE)
            for row in group['callers']]
        cases = []
        for actor, pointer in actors.items():
            voice = voices[actor]
            expected = first if slots[voice] == -1 else slots[voice]
            assert get(0x53F4C, pointer, table) == expected
            cases.append((actor, voice, expected))
        assert get(0x53F4C, 0, table) == first
        role = 7 if first in (1290, 1313) else 1
        args = (ARGUMENTS[first],) if first in ARGUMENTS else ()
        groups.append(dict(first_ID=first, last_ID=last, table=table, table_slots=slots,
            native_callers=group['callers'], consumer=group['callers'][0]['consumer'], arguments=args,
            original_role_argument=role, speaker='Lookout' if role == 7 else 'First Mate',
            context=CONTEXT[first], original_voice_choices=cases))
    labels = dict(faction_label=native_labels(cpu, get, get(0xCB160), 20, 76, 0x0203CF9C),
                  port_label=native_labels(cpu, get, get(0xCB178), 90, 108, 0x020B5630))
    assert labels['faction_label'][2]['label'] == 'Bergstrom Fleet'
    assert labels['port_label'][9]['label'] == 'Copenhagen'
    numbers = []
    for n in DECIMAL_VALUES:
        pointer = get(0xABF50, n)
        raw = text(cpu, pointer)
        assert raw.decode('cp932') == str(n).translate(str.maketrans('0123456789', '０１２３４５６７８９'))
        numbers.append(dict(value=n, pointer=pointer, hex=raw.hex(), label=raw.decode('cp932')))
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    runtime.calls.clear()
    return groups, labels | {'decimal': numbers}


def main():
    assert not OUTPUT.exists()
    drafts, decisions = read_rows(DRAFTS), read_rows(DECISIONS)
    release, inventory = load(RELEASE), load(INVENTORY)
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    assert digest(DRAFTS) == inventory['draft_SHA256']
    assert digest(CLEAN) == release['clean_input_sha256'] == inventory['clean_source_SHA256']
    assert release['candidate_sha256'] == inventory['registered_current_SHA256']
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
    spans = source_dependencies(clean_arm, runtime.arm)
    groups, arguments = bind_native(runtime, inventory, clean_arm)
    by_id = {n: group for group in groups for n in range(group['first_ID'], group['last_ID'] + 1)}
    records = []
    for n, exact in zip(IDS, inventory['records'], strict=True):
        jp, old = source[n], current[n]
        assert n == exact['message_ID'] and jp.text.hex() == exact['source_hex'] and old.text.hex() == exact['current_hex']
        assert exact['source_reference'] == reference(jp) and exact['current_reference'] == reference(old)
        prior = ' '.join(exact['current_English'].split())
        revision = decisions[n]['replacement_English']
        english = revision or prior
        group = by_id[n]
        assert english.isascii() and english == ' '.join(english.split()) and bool(revision) == (english != prior)
        assert jp.text.count(b'%s') == old.text.count(b'%s') == english.count('%s') == len(group['arguments'])
        assert '%' not in english.replace('%s', '') and all(token not in english for token in ('FI', 'FA', 'FO', 'FU', 'IC'))
        row = exact | dict(id=f'COMMON_MESSAGE_{n}', file_path=COMMON, english=english,
            independent_English=drafts[n]['independent_English'], source_meaning=drafts[n]['source_meaning'],
            localization_note=decisions[n]['localization_note'], decision='revision' if revision else 'retention',
            speaker=group['speaker'], context=group['context'], original_substitutions=group['arguments'],
            review={gate: gate != 'formatting' for gate in GATES})
        if 1305 <= n <= 1312:
            row['source_meaning'] = row['source_meaning'].replace('named group', 'named port').replace('the group', 'the port')
        row['original_current_native_lookup'] = current_copy(runtime, row, BASE + 0x5528C)
        runtime.calls.pop()
        records.append(row)
    stats = Counter(row['decision'] for row in records)
    assert stats == {'revision': 56, 'retention': 11}
    save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=GATES, registered_input=runtime.receipt(),
        source_ROM=str(CLEAN), source_ROM_sha256=release['clean_input_sha256'], records=records, counts=stats,
        exact_native_groups=groups, original_caller_spans=spans, original_arguments=arguments,
        current_native_lookups=len(records), voice_cases=sum(len(group['original_voice_choices']) for group in groups),
        formatting_pending=True, registered_release_pending=True, new_gameplay=False, new_credit=0,
        full_goal_complete=False, evidence={str(p): digest(p) for p in (DRAFTS, DECISIONS, INVENTORY, RELEASE, __file__)}))
    print(f'{len(records)} contextual decisions, {dict(stats)}, nine native voice tables and three argument sources.')


if __name__ == '__main__':
    main()
