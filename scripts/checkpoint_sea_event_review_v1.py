"""Bind a whole-event Japanese review to the original sea-event voice tables."""

import csv
from collections import Counter
from hashlib import sha256
import struct
from unicodedata import normalize

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.audit_story_glyph_consistency import load, save, wide_letters
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.register_diplomatic_outcomes_v2 import RELEASE
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_literal_notice_callers_v1 import current_copy
from scripts.seal_shared_text_source_v1 import ARM, CLEAN, COMMON, ROOT, reference


BASE = 0x02000000
DRAFTS = ROOT / 'sea_event_source_drafts.tsv'
DECISIONS = ROOT / 'sea_event_decisions.tsv'
OUTPUT = ROOT / 'sea_event_contextual_review.json'
GATES = ('source', 'context', 'localization', 'naturalness', 'formatting')
IDS = range(383, 481)
FOAM = 'Strange bubbles: the lookout reports what is visible, another sailor recalls the rumor, ' \
       'the captain reacts, the sailor explains the danger, and the captain orders evasive action.'
MERMAID = 'Mermaid encounter: a lookout first notices an unidentified swimmer. A second voice ' \
          'then wonders aloud whether it is a mermaid. These are two separate beats.'

# Table/pool/load/call offsets are relative to ARM9. The role value is the
# original queued dispatch input. None marks an actor or captain selector.
GROUPS = (
    (383, 389, 0x1189A0, 0x30FD8, 0x30B0C, 0x30B10, 0x53F0C, None,
        'Immediate storm warning. This branch uses the actual actor and is separate from the sudden-clear-weather variants.'),
    (389, 394, 0x118980, 0x30FD4, 0x30B08, 0x30B10, 0x53F0C, None,
        'Immediate blizzard warning. The same actor-based call chooses a different table for this weather.'),
    (394, 401, 0x118960, 0x32588, 0x31FE8, 0x31FF0, 0x53D44, 1,
        'Scurvy warning. The alternatives describe the same illness with different levels of alarm and certainty.'),
    (401, 409, 0x118940, 0x32590, 0x3204C, 0x32058, 0x53D44, 1,
        'Rat infestation. Most voices worry about provisions. One simply cries for help and one begs for their own food.'),
    (409, 416, 0x118920, 0x32594, 0x320F8, 0x32100, 0x53D44, 7,
        'A storm has arrived after clear weather. Surprise at the sudden change distinguishes this family from the immediate storm warning.'),
    (416, 422, 0x118900, 0x32598, 0x32198, 0x321A0, 0x53D44, 7,
        'The native Aurora condition prompts the speaker to draw the admiral’s attention to the sky. The dialogue leaves what is visible implicit.'),
    (422, 430, 0x1188E0, 0x3259C, 0x321A8, 0x321B0, 0x53D44, 7,
        'Fog is coming in. Some voices only notice it. Others comment on visibility or react with frustration.'),
    (430, 436, 0x1188C0, 0x325A4, 0x32228, 0x32230, 0x53D44, 7,
        'The two native monster cases share the same alarm variants. The speaker reacts to the creature without giving it a species name.'),
    (436, 441, 0x1188A0, 0x325AC, 0x322C0, 0x322D0, 0x53D44, 15,
        'The original Sirens event presents unfamiliar singing. This reaction precedes any identification and is separate from the mermaid exchange.'),
    (441, 449, 0x118880, 0x325B0, 0x322E0, 0x322F0, 0x53D44, 7, MERMAID + ' First beat.'),
    (449, 457, 0x118860, 0x325B4, 0x322F4, 0x322FC, 0x53D44, 15, MERMAID + ' Second beat.'),
    (457, 463, 0x118840, 0x325B8, 0x32328, 0x32338, 0x53D44, 7, FOAM + ' Sighting.'),
    (463, 469, 0x118820, 0x325BC, 0x3233C, 0x32344, 0x53D44, 1, FOAM + ' Recognition.'),
    (469, 470, None, 0x325C0, 0x32348, 0x3234C, 0x53C24, None, FOAM + ' Silent question.'),
    (470, 477, 0x118800, 0x325C4, 0x32350, 0x32358, 0x53D44, 1, FOAM + ' Explanation.'),
    (477, 481, 0x116730, 0x325C8, 0x3235C, 0x32360, 0x53BD8, None,
        FOAM + ' Captain’s order. The same captain table is used for other evasive maneuvers.'),
)


def indexed(path):
    with path.open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    result = {int(row['message_ID']): row for row in rows}
    assert len(result) == len(rows) == len(IDS) and set(result) == set(IDS)
    return result


def caller_binding(clean, current, load_at, call_at, literal, value, consumer):
    assert clean[load_at:call_at + 4] == current[load_at:call_at + 4]
    assert clean[literal:literal + 4] == current[literal:literal + 4]
    ldr, = struct.unpack_from('<I', clean, load_at)
    assert ldr & 0x0F7F0000 == 0x051F0000
    assert load_at + 8 + (ldr & 0xFFF) * (1 if ldr & 0x800000 else -1) == literal
    assert struct.unpack_from('<I', clean, literal)[0] == value
    branch, = struct.unpack_from('<I', clean, call_at)
    assert branch & 0x0F000000 == 0x0B000000
    signed = ((branch & 0xFFFFFF) ^ 0x800000) - 0x800000
    assert call_at + 8 + signed * 4 == consumer
    return dict(load_PC=BASE + load_at, call_PC=BASE + call_at, literal_address=BASE + literal,
        literal_value=value, consumer=BASE + consumer, clean_and_current_hex=clean[load_at:call_at + 4].hex())


def main():
    assert not OUTPUT.exists()
    source_drafts, decisions = indexed(DRAFTS), indexed(DECISIONS)
    release = load(RELEASE)
    assert digest(CLEAN) == release['clean_input_sha256']
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    clean = NdsImage.open(CLEAN)
    clean_arm = clean.read_file(ARM)
    source = common_message_entries(clean.read_file(COMMON), clean_arm)
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    current = owned_entries(runtime.common, runtime.arm, directory)
    ledger = load('translations/editorial_review_current_v1.json')
    ctx = ledger['contextual_story_natural_dialogue_pass_v1871']
    integrated = {r['id'] for r in ctx['integrated_record_keys'] if r['file_path'] == COMMON}
    assert all(f'COMMON_MESSAGE_{n}' not in integrated for n in IDS)
    for lo, hi in ((0x53BD8, 0x53C90), (0x53D44, 0x53DC4), (0x53F0C, 0x53F9C)):
        assert clean_arm[lo:hi] == runtime.arm[lo:hi]

    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    roster = {i: runtime.actor_root + (0x19E4 if i == 3 else 4 + i * 32) for i in range(207)}
    voices = {i: get(0x7E988, actor) for i, actor in roster.items()}
    assert set(voices.values()) == set(range(8))
    groups, records = [], []
    choices = 0
    for start, end, table, pool, pc, call, consumer, role, context in GROUPS:
        members = list(range(start, end))
        slots = ()
        selectors = []
        binding = caller_binding(clean_arm, runtime.arm, pc, call, pool,
            BASE + table if table else start, consumer)
        other_callers = [caller_binding(clean_arm, runtime.arm, site, next_call, pool, BASE + table, consumer)
                         for site, next_call in ((0x323BC, 0x323C0), (0x32454, 0x32458))] if start == 477 else []
        if table:
            count = 4 if start == 477 else 8
            assert clean_arm[table:table + 4 * count] == runtime.arm[table:table + 4 * count]
            slots = struct.unpack_from(f'<{count}i', clean_arm, table)
            assert set(slots) - {-1} == set(members)
            if start == 477:
                assert get(0x53C6C, BASE + table) == slots[3]
            else:
                for i, actor in roster.items():
                    slot = slots[voices[i]]
                    selected = get(0x53F4C, actor, BASE + table)
                    assert selected == (start if slot == -1 else slot)
                    selectors.append((i, voices[i], selected))
                assert get(0x53F4C, 0, BASE + table) == start
                choices += len(selectors)
        groups.append(dict(first_ID=start, last_ID=end-1, context=context, selector=BASE + table if table else start,
            table_slots=slots, original_role_argument=role, source_native_caller=binding,
            additional_source_callers=other_callers, original_actor_voice_choices=selectors,
            current_native_captain_slot=3 if start == 477 else None))
        for n in members:
            jp, old = source[n], current[n]
            old_text = old.text.decode('cp932')
            old_paragraph = ' '.join(normalize('NFKC', old_text).split())
            revision = decisions[n]['replacement_English']
            english = revision or old_paragraph
            assert english.isascii() and '\n' not in english and english.strip() == english
            assert bool(revision) == (english != old_paragraph), n
            assert all(b'%' not in row.text for row in (jp, old)) and '%' not in english
            row = dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, file_path=COMMON,
                source_reference=reference(jp), current_reference=reference(old),
                source_hex=jp.text.hex(), current_hex=old.text.hex(), source_Japanese=jp.text.decode('cp932'),
                current_English=old_text, english=english, independent_English=source_drafts[n]['independent_English'],
                source_meaning=source_drafts[n]['source_meaning'], context=context, native_group_first_ID=start,
                original_selector_slots=[i for i, number in enumerate(slots) if number == n],
                speaker=('Player admiral selected by captain index' if consumer in (0x53BD8, 0x53C24)
                         else 'Crew member selected by original voice class'),
                localization_note=decisions[n]['localization_note'],
                decision='revision' if revision else 'retention',
                review={gate: gate != 'formatting' for gate in GATES},
                inherited_fullwidth_Latin=wide_letters(old_text),
                original_substitution_count=0)
            row['original_current_native_lookup'] = current_copy(runtime, row, BASE + 0x5528C)
            runtime.calls.pop()
            records.append(row)

    assert [r['message_ID'] for r in records] == list(IDS) and choices == 14 * 207
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    stats = Counter(row['decision'] for row in records)
    save(OUTPUT, dict(
        translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=GATES,
        registered_input=runtime.receipt(), source_ROM=str(CLEAN), source_ROM_sha256=release['clean_input_sha256'],
        exact_native_event_groups=groups, records=records, counts=stats, original_voice_selector_cases=choices,
        current_native_lookups=len(records), prior_blizzard_and_bubble_proofs_preserved=True,
        all_current_captain_alternatives_played=False, actual_gameplay=False, formatting_pending=True,
        registered_release_pending=True, new_credit=0, full_goal_complete=False,
        evidence={str(path): digest(path) for path in (DRAFTS, DECISIONS, OUTPUT.with_name('remaining_COMMON_source_catalog.json.gz'))},
    ))
    print(f'{len(records)} contextual decisions, {dict(stats)}, {choices} original voice choices.')


if __name__ == '__main__':
    main()
