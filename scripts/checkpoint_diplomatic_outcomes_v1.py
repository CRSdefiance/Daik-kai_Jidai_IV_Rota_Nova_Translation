"""Bind the diplomatic and scheme outcomes to clean source and native display calls."""

import csv
from collections import Counter
from hashlib import sha256
from itertools import product
from pathlib import Path

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.audit_story_glyph_consistency import load, save, wide_letters
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_literal_notice_formatting_v1 import run_case
from scripts.preflight_shared_dynamic_notice_wrap_v1 import eligible_model, native_catalog
from scripts.register_shared_crew_notices_v1 import RELEASE
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_literal_notice_callers_v1 import CALLS, bindings, current_copy
from scripts.seal_shared_text_source_v1 import ARM, CLEAN, COMMON, ROOT, reference


DRAFTS = ROOT / 'diplomatic_outcome_source_drafts.tsv'
DECISIONS = ROOT / 'diplomatic_outcome_decisions.tsv'
OUTPUT = ROOT / 'diplomatic_outcome_contextual_review.json'
IDS = set(range(349, 383))
GROUPS = (
    ((349,), 'Arrival of an official letter. This receipt precedes different responses, including '
        'the truce, pact and closer-relations branches.'),
    ((350, 351, 352, 353, 354, 355, 382), 'Pact proposal, acceptance against a named opponent or '
        'without one, refusal, failed proposal and termination. The outcomes are alternatives.'),
    ((356, 357, 358, 359, 360, 361), 'Truce offer and alternative agreement or refusal outcomes. '
        'The war declarations are separate statuses for player and nonplayer targets.'),
    ((362, 363, 381), 'Merger response, with entry under the player, express refusal or no reply.'),
    ((364, 365), 'Lure Fleet scheme. A false report reaches the target faction. The success notice '
        'uses the destination-town virtual name getter at 02092744–0209274C.'),
    ((366, 367, 369, 370, 371), 'Forge Papers receipt and possible consequences. Apparent success, '
        'damage to the player’s relations, outbreak of fighting and failure are distinct notices.'),
    ((368,), 'Follow-up to the official letter at 349. The earlier modal identifies the sender.'),
    ((372, 373, 374), 'Bad Rumors scheme. Town and subject are introduced first. Share loss and '
        'the rumor’s failure to persuade are separate outcomes.'),
    ((375, 376, 377, 378, 379, 380), 'Bribe scheme. The broker receives the letter before the separate '
        'price explanation and payment decision. The results distinguish a transfer of share, a share '
        'loss, suspected bribery against the player, and failure.'),
)
CONTEXT = {n: (members, description) for members, description in GROUPS for n in members}
TOWN_ARGUMENTS = {365: (0,), 372: (0,), 375: (0,), 379: (0,)}
GATES = ('source', 'context', 'localization', 'naturalness', 'formatting')


def indexed_tsv(path):
    with path.open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    indexed = {int(row['message_ID']): row for row in rows}
    assert len(rows) == len(indexed) and set(indexed) == IDS
    return indexed


def select_cases(row, towns, companies):
    domains = [towns if i in TOWN_ARGUMENTS.get(row['message_ID'], ()) else companies
               for i in range(row['native_substitution_count'])]
    shapes = {}
    overflows = []
    count = 0
    for arguments in product(*domains):
        expanded = row['english'] % arguments
        lines = eligible_model(expanded, True)
        lengths = tuple(len(line) for line in lines)
        if len(lines) > 3:
            overflows.append((arguments, lines))
        shape = len(lines), tuple(n % 2 for n in lengths)
        score = len(expanded), max(lengths), arguments
        if shape not in shapes or score > shapes[shape][0]:
            shapes[shape] = (score, arguments)
        count += 1
    cases = {args for _, args in shapes.values()}
    cases.add(tuple(domain[0] for domain in domains))
    return count, sorted(cases), overflows


def main():
    assert not OUTPUT.exists()
    drafts, decisions = indexed_tsv(DRAFTS), indexed_tsv(DECISIONS)
    assert set(CONTEXT) == IDS
    release = load(RELEASE)
    inventory = load(CALLS)
    assert digest(CLEAN) == release['clean_input_sha256'] == inventory['source_rom_sha256']
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    clean = NdsImage.open(CLEAN)
    clean_arm = clean.read_file(ARM)
    source = common_message_entries(clean.read_file(COMMON), clean_arm)
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    current = owned_entries(runtime.common, runtime.arm, directory)

    ledger = load('translations/editorial_review_current_v1.json')
    credited = ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']
    credited_common = {r['id'] for r in credited if r['file_path'] == COMMON}
    catalog = native_catalog(runtime)
    towns = sorted({r['name'] for r in catalog['towns']}, key=lambda name: (len(name), name))
    companies = sorted({r['name'] for r in catalog['companies']}, key=lambda name: (len(name), name))
    # The registered shared notices qualify 18-byte editable player company names.
    companies.append('Blue Horizon Fleet')
    assert len(companies[-1]) == 18
    records = []
    for number in sorted(IDS):
        ident = f'COMMON_MESSAGE_{number}'
        assert ident not in credited_common
        jp, old = source[number], current[number]
        word_choice = decisions[number]
        current_english = old.text.decode('cp932')
        existing_paragraph = ' '.join(current_english.split())
        retained = not word_choice['replacement_English']
        paragraph = existing_paragraph if retained else word_choice['replacement_English']
        count = jp.text.count(b'%s')
        assert paragraph.isascii() and '\n' not in paragraph and paragraph.strip() == paragraph
        assert paragraph.count('%') == paragraph.count('%s') == count
        assert old.text.count(b'%s') == count == drafts[number]['independent_English'].count('%s')
        assert retained == (paragraph == existing_paragraph)
        calls = bindings(clean_arm, runtime.arm, inventory, number)
        targets = sorted({call['target'] for call in calls})
        assert len(targets) == 1 and targets[0] in {0x020546B8, 0x0205466C}
        members, context = CONTEXT[number]
        row = dict(
            id=ident, file_path=COMMON, message_ID=number,
            source_reference=reference(jp), current_reference=reference(old),
            source_hex=jp.text.hex(), current_hex=old.text.hex(),
            source_Japanese=jp.text.decode('cp932'), current_English=current_english,
            independent_English=drafts[number]['independent_English'], english=paragraph,
            source_meaning=drafts[number]['source_meaning'],
            speaker='Speakerless system notice',
            context=context, related_message_IDs=members,
            localization_note=word_choice['localization_note'],
            decision='retention' if retained else 'revision',
            review={gate: gate != 'formatting' for gate in GATES},
            current_fullwidth_Latin=wide_letters(current_english),
            current_copies=[current_copy(runtime, dict(message_ID=number, current_hex=old.text.hex()), targets[0])],
            exact_source_andcurrent_callers=calls, native_substitution_count=count,
        )
        combinations, selected, overflows = select_cases(row, towns, companies)
        expansions = [run_case(runtime, row, supplied) for supplied in selected]
        legacy_fails = sum(any(len(line) > (36 if i == 0 else 35)
                               for i, line in enumerate(sample['native_wrapper_lines']))
                           for sample in expansions)
        row.update(native_current_wrapper_expansions=expansions,
            current_wrapper_overwidth_samples=legacy_fails,
            paragraph_model_combinations=combinations, paragraph_model_overflows=len(overflows),
            paragraph_model_overflow_example=overflows[0] if overflows else None)
        records.append(row)

    stats = Counter(row['decision'] for row in records)
    evidence = {str(path): digest(path) for path in (DRAFTS, DECISIONS, CALLS, Path(__file__))}
    save(OUTPUT, dict(
        translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=GATES, registered_input=runtime.receipt(),
        source_ROM=str(CLEAN), source_ROM_sha256=release['clean_input_sha256'],
        town_names=towns, company_test_names=companies, records=records, counts=stats,
        original_direct_calls=sum(len(r['exact_source_andcurrent_callers']) for r in records),
        complete_native_expansion_cases=sum(len(r['native_current_wrapper_expansions']) for r in records),
        legacy_wrapper_overwidth_IDs=[r['message_ID'] for r in records if r['current_wrapper_overwidth_samples']],
        paragraph_model_overflow_IDs=[r['message_ID'] for r in records if r['paragraph_model_overflows']],
        paragraph_model_combinations=sum(r['paragraph_model_combinations'] for r in records),
        logical_paragraph_model_is_diagnostic=True,
        gameplay_observed=False, registered_release_pending=True, new_credit=0,
        full_goal_complete=False, evidence=evidence,
    ))
    print(f'{len(records)} contextual decisions: {dict(stats)}')
    print('Current native wrappers exceed width for',
          [r['message_ID'] for r in records if r['current_wrapper_overwidth_samples']])
    print('Three-row paragraph model overflow:',
          [r['message_ID'] for r in records if r['paragraph_model_overflows']])


if __name__ == '__main__':
    main()
