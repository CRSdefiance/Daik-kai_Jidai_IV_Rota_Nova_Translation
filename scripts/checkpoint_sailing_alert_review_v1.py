"""Bind the clean-source sailing alert review to the registered native consumers."""

from collections import Counter
import csv
from hashlib import sha256
from pathlib import Path
import re
import struct

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.sailing_condition_names import LABELS, TABLE
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_sea_event_review_v1 import BASE, GATES, caller_binding
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.register_sea_event_review_v2 import RELEASE
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_literal_notice_callers_v1 import current_copy
from scripts.seal_shared_text_source_v1 import ARM, CLEAN, COMMON, ROOT, reference
from scripts.verify_sea_event_bubbles_focused_v2 import PROOF as BUBBLES


DRAFTS = ROOT / 'sailing_alert_source_drafts.tsv'
DECISIONS = ROOT / 'sailing_alert_decisions.tsv'
OUTPUT = ROOT / 'sailing_alert_contextual_review.json'
STAT_FORMAT = Path('translations/levelup_stat_format_release_v1.json')
IDS = (97, *range(481, 508))
GROUPS = (
    (481, 487, 0x1187C0, 0x325D0, ((0x323B0, 0x323B8), (0x32448, 0x32450)), 7,
        'Four possible hazard names follow the crew call. The two native branches report tornado or whirlpool, '
        'or reefs or drift ice, before the separate captain evasive order reviewed with sea events.'),
    (487, 493, 0x1187A0, 0x3258C, ((0x31FF8, 0x32000),), 11,
        'One crew voice reports the epidemic when that branch fires. The six lines are alternative reports.'),
    (493, 501, 0x118780, 0x325D8, ((0x32508, 0x32518),), 5,
        'One crew voice reports that the wind has stopped. Most variants say there is nothing to do but wait. '
        'No character causes the wind to return in this exchange.'),
    (501, 508, 0x118760, 0x325DC, ((0x32544, 0x3254C),), 7,
        'One crew voice spots sharks and warns the admiral. The encounter does not establish the number of sharks. '
        'The unrest exchange beginning at 508 is a different event.'),
)


def indexed(path):
    with path.open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    assert tuple(int(row['message_ID']) for row in rows) == IDS
    return {int(row['message_ID']): row for row in rows}


def word(data, offset):
    return struct.unpack_from('<I', data, offset)[0]


def branch_target(arm, offset):
    branch = word(arm, offset)
    assert branch & 0x0F000000 == 0x0B000000
    signed = ((branch & 0xFFFFFF) ^ 0x800000) - 0x800000
    return BASE + offset + 8 + signed * 4


def floating_notice(clean, current, candidate_sha):
    start, stop = 0x7E3F0, 0x7E448
    assert word(clean, start) == 0xE3A00061
    # The registered stat formatter repacks this neighboring notice in Thumb.
    # Verify both owned spans and their inverse before reusing its call proof.
    function_start, function_stop = 0x7E2E8, 0x7E5C4
    restored = bytearray(current[function_start:function_stop])
    patches = load(STAT_FORMAT)['owned_patches']
    assert [row['address'] for row in patches] == [0x0207E3A8, 0x0207E56C]
    for patch in patches:
        offset = patch['address'] - BASE
        before = bytes.fromhex(patch['before_hex'])
        after = bytes.fromhex(patch['after_hex'])
        assert len(before) == len(after)
        assert clean[offset:offset + len(before)] == before
        assert current[offset:offset + len(after)] == after
        i = offset - function_start
        restored[i:i + len(after)] = before
    assert bytes(restored) == clean[function_start:function_stop]
    assert word(clean, 0x7E414) == 0xE5911020 and word(clean, 0x7E418) == 0xE12FFF31
    calls = (0x7E404, 0x7E428, 0x7E444)
    targets = [branch_target(clean, offset) for offset in calls]
    assert targets == [0x0205528C, 0x020ABFCC, 0x02005E4C]
    assert clean[0x7E3A0:0x7E3A4] == current[0x7E3A0:0x7E3A4]
    assert branch_target(clean, 0x7E3A0) == 0x020546B8

    proof = load(BUBBLES)
    assert proof['candidate_sha256'] == candidate_sha
    assert proof['selector_word_restored'] and proof['actual_emulator']
    capture = proof['return_to_sailing_capture']
    png = Path(capture['path'])
    ram_path = png.with_name('frame_010627_arm9_ram.bin')
    ram = ram_path.read_bytes()
    names = [(0x0229F444, 'Gerhard'), (0x0229F478, 'Manuel')]
    observed = []
    for address, name in names:
        expanded = f'{name}、ＬｖＵＰ！'.encode('cp932')
        start_in_ram = address - BASE
        assert ram[start_in_ram:start_in_ram + len(expanded) + 1] == expanded + b'\0'
        observed.append(dict(address=address, actor_name=name, exact_CP932_hex=expanded.hex()))
    return dict(context='The named crewmember gains a level. The original name getter feeds a short floating '
        'Sea View notification. Two actors can gain levels and display notices at the same time.',
        callers=dict(clean_hex=clean[start:stop].hex(), clean_start_PC=BASE + start,
            current_thumb_entry_PC=0x0207E3AC, current_thumb_lookup_PC=0x0207E3DE,
            current_thumb_name_call_PC=0x0207E3EA, current_thumb_formatter_PC=0x0207E3F2,
            clean_lookup_PC=BASE + calls[0], lookup_target=targets[0], name_getter_virtual_slot=0x20,
            clean_formatter_PC=BASE + calls[1], formatter_target=targets[1],
            floating_widget_PC=BASE + calls[2], floating_widget_target=targets[2],
            registered_stat_formatter_inverse_exact=True,
            other_modal_ID=335, other_modal_call_PC=0x0207E3A0, other_modal_consumer=0x020546B8),
        inherited_gameplay=dict(frame=capture['frame'], screenshot=str(png), screenshot_sha256=digest(png),
            RAM=str(ram_path), RAM_sha256=sha256(ram).hexdigest(), visible_notices=observed,
            fixture_scope='Earlier focused bubbles voyage after restoration of its one temporary selector instruction',
            observed_before_translation=True, hardware=False))


def voices_and_conditions(runtime, clean_arm):
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    actors = {i: runtime.actor_root + (0x19E4 if i == 3 else 4 + i * 32) for i in range(207)}
    voices = {i: get(0x7E988, pointer) for i, pointer in actors.items()}
    assert set(voices.values()) == set(range(8))
    assert clean_arm[0x82E74:0x82E98] == runtime.arm[0x82E74:0x82E98]
    conditions = []
    for i, (japanese, english) in enumerate(LABELS):
        field = TABLE + 4 * i
        clean_pointer = word(clean_arm, field)
        clean_end = clean_arm.index(0, clean_pointer - BASE)
        assert clean_arm[clean_pointer - BASE:clean_end].decode('cp932') == japanese
        current_pointer = word(runtime.arm, field)
        assert get(0x82E74, i, 0) == current_pointer
        assert bytes(cpu.mem_read(current_pointer, len(english) + 1)) == english.encode('ascii') + b'\0'
        conditions.append(dict(index=i, field=BASE + field, clean_pointer=clean_pointer,
            current_pointer=current_pointer, Japanese=japanese, English=english))
    assert set(conditions[i]['English'] for i in range(16, 20)) == {'Tornado', 'Whirlpool', 'Reefs', 'Drift Ice'}
    assert all(branch_target(clean_arm, offset) == 0x02082E74 for offset in (0x323A8, 0x32440))
    for lo, hi in ((0x3238C, 0x323B0), (0x323EC, 0x32448)):
        assert clean_arm[lo:hi] == runtime.arm[lo:hi]
    assert [word(clean_arm, at) for at in (0x3238C, 0x32398, 0x323FC, 0x32400)] == [
        0xE3A00010, 0xE3A00011, 0x23A00013, 0x33A00012]
    groups = []
    for first, end, table, literal, sites, role, context in GROUPS:
        assert clean_arm[table:table + 32] == runtime.arm[table:table + 32]
        slots = struct.unpack_from('<8i', clean_arm, table)
        assert set(slots) - {-1} == set(range(first, end))
        cases = []
        for actor, pointer in actors.items():
            voice = voices[actor]
            expected = slots[voice] if slots[voice] != -1 else first
            assert get(0x53F4C, pointer, BASE + table) == expected
            cases.append((actor, voice, expected))
        assert get(0x53F4C, 0, BASE + table) == first
        callers = [caller_binding(clean_arm, runtime.arm, pc, call, literal, BASE + table, 0x53D44)
                   for pc, call in sites]
        assert all(any(word(clean_arm, i) == 0xE3A00000 + role for i in range(pc, call, 4))
                   for pc, call in sites)
        groups.append(dict(first_ID=first, last_ID=end - 1, table=BASE + table, table_slots=slots,
            native_callers=callers, original_role_argument=role, context=context, original_voice_choices=cases))
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    runtime.calls.clear()
    return groups, conditions


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
    credited = {row['id'] for row in ctx['integrated_record_keys'] if row['file_path'] == COMMON}
    assert not {f'COMMON_MESSAGE_{n}' for n in IDS} & credited
    del ledger, ctx

    floating = floating_notice(clean_arm, runtime.arm, release['candidate_sha256'])
    groups, conditions = voices_and_conditions(runtime, clean_arm)
    by_id = {n: group for group in groups for n in range(group['first_ID'], group['last_ID'] + 1)}
    records = []
    for n in IDS:
        clean_row, old = source[n], current[n]
        japanese, old_text = (entry.text.decode('cp932') for entry in (clean_row, old))
        replacement = decisions[n]['replacement_English']
        old_paragraph = ' '.join(old_text.split())
        english = replacement or old_paragraph
        assert english.isascii() and english == ' '.join(english.split())
        assert bool(replacement) == (english != old_paragraph)
        arguments = re.findall(r'%s', japanese)
        assert arguments == re.findall(r'%s', old_text) == re.findall(r'%s', english)
        assert english.count('%') == len(arguments)
        group = by_id.get(n)
        row = dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, file_path=COMMON,
            source_reference=reference(clean_row), current_reference=reference(old),
            source_hex=clean_row.text.hex(), current_hex=old.text.hex(), source_Japanese=japanese,
            current_English=old_text, english=english, independent_English=drafts[n]['independent_English'],
            source_meaning=drafts[n]['source_meaning'], localization_note=decisions[n]['localization_note'],
            decision='revision' if replacement else 'retention',
            review={gate: gate != 'formatting' for gate in GATES},
            original_substitutions=['named actor'] if n == 97 else ['sailing condition name'] if arguments else [],
            speaker='Floating system notice' if n == 97 else 'Crew member selected by original voice class',
            context=floating['context'] if n == 97 else group['context'],
            original_selector_slots=[] if n == 97 else [i for i, msg in enumerate(group['table_slots']) if msg == n])
        row['original_current_native_lookup'] = current_copy(runtime, row, BASE + 0x5528C)
        runtime.calls.pop()
        records.append(row)
    neighbor_ids = (335, *range(477, 481), 508)
    context = [dict(message_ID=n, source_reference=reference(source[n]), current_reference=reference(current[n]),
        source_hex=source[n].text.hex(), current_hex=current[n].text.hex(),
        Japanese=source[n].text.decode('cp932'), current=current[n].text.decode('cp932'),
        has_existing_credit=f'COMMON_MESSAGE_{n}' in credited) for n in neighbor_ids]
    stats = Counter(row['decision'] for row in records)
    assert stats == {'revision': 24, 'retention': 4}
    assert sum(len(group['original_voice_choices']) for group in groups) == 828
    save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=GATES, registered_input=runtime.receipt(),
        source_ROM=str(CLEAN), source_ROM_sha256=release['clean_input_sha256'], records=records, counts=stats,
        exact_native_crew_groups=groups, exact_floating_notice_consumer=floating, condition_labels=conditions,
        neighboring_context=context, current_native_lookups=len(records), native_crew_voice_cases=828,
        new_gameplay=False, formatting_pending=True, registered_release_pending=True, new_credit=0,
        full_goal_complete=False, evidence={str(path): digest(path) for path in
            (DRAFTS, DECISIONS, BUBBLES, STAT_FORMAT, Path(__file__))}))
    print(f'{len(records)} contextual decisions ({stats["revision"]} revisions, {stats["retention"]} retentions).')
    print('Exact original lookup for all messages, 828 voice choices, 26 condition names and two prior floating notices.')


if __name__ == '__main__':
    main()
