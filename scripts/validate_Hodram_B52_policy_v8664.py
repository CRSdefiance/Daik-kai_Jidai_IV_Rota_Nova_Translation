"""Check exact B52 compilers and genuinely changed semantic inputs with frozen guards active."""
import json
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B52_profile_v1 import contract, profile_for, validate_runtime, validate_approved_batch
from dk4tool.dialogue.hodram_B52_layout_v1 import encode_relocatable_dialogue, audit_relocatable_dialogue_record
from dk4tool.dialogue.hodram_B52_names_v1 import validate_scoped_names
from dk4tool.dialogue.hodram_B52_choices_v1 import compile_choices
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B52_policy_validation_v8664')
DOC = Path('translations/hodram_B52_editorial_manuscript_v6.json')
NAMES = Path('translations/hodram_B52_speaker_name_review_v4.json')


def digest(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, default=repr).encode('utf-8'))


if __name__ == '__main__':
    assert not ROOT.exists()
    doc, names = map(read, [DOC, NAMES])
    frozen = contract()
    image = NdsImage.open(doc['current_ROM'])
    validate_runtime(image)
    validate_approved_batch(doc)
    validate_scoped_names(names)
    arm = image.read_file('/__arm9__.bin')
    block = IlnkContainer.parse(image.read_file('/data/SC1.DK4')).blocks[52]
    protected = {Path(p) for p in frozen['dependencies']} | {DOC, NAMES,
        Path('translations/hodram_B52_native_contract_v1.json'), Path('translations/release_stack.json'),
        Path('translations/editorial_review_current_v1.json'), Path('translations/rom_retention_pins.json'),
        Path(doc['current_ROM']), Path('work/clean.nds'), Path(__file__)}
    protected |= {Path('dk4tool/dialogue') / ('hodram_B52_' + name + '_v1.py') for name in ['profile', 'layout', 'plan', 'names', 'choices']}
    before = {str(p): sha(p.read_bytes()) for p in protected}
    positives, negatives = [], []
    ROOT.mkdir(parents=True)

    def reject(label, original, changed, fn, expected=None):
        assert original != changed and digest(original) != digest(changed), label
        try:
            fn(changed)
        except ValueError as error:
            message = str(error)
            assert 'Native dependency changed' not in message and 'Frozen Hodram-B52 contract changed' not in message, (label, message)
            if expected is not None:
                assert expected in message, (label, expected, message)
            negatives.append(dict(label=label, original_sha256=digest(original), changed_sha256=digest(changed),
                actual_changed_input=True, rejected=True, diagnostic=message))
        else:
            raise AssertionError('Changed input accepted:' + label)

    for index, row in enumerate(doc['records']):
        ident, raw, text = row['id'], bytes.fromhex(row['source_hex']), row['planned_English_markup']
        profile = profile_for(arm, block, ident, '/data/SC1.DK4', 'progressive')
        encoded = encode_relocatable_dialogue(raw, text, profile)
        qa = audit_relocatable_dialogue_record(raw, text, profile)
        assert encoded.encoded.hex() == row['compiled_hex'] == frozen['record_bindings'][ident]['compiled_hex']
        assert qa['native_page_count'] == 1 and qa['issues'] == frozen['record_bindings'][ident]['base_QA_issues'] and qa['qa_waivers'] == []
        positives.append(dict(id=ident, source_reference=row['source_reference'], current_reference=row['current_reference'],
                         final_reference=row['final_reference'], compiled_hex=encoded.encoded.hex(), qa=qa))
        for gate in frozen['review_gates']:
            changed = deepcopy(doc)
            changed['records'][index]['review'][gate] = False
            reject(ident + ':gate:' + gate, doc, changed, validate_approved_batch)
        for field, value in {
            'english': row['english'] + ' Unapproved words.', 'logical_English': row['logical_English'] + ' Unapproved words.',
            'context': row['context'] + ' Invented kinship.', 'source_meaning': row['source_meaning'] + ' Invented rank.',
            'speaker': 'Unapproved Captain', 'localization_note': '', 'retention_reason': 'Unreviewed reason',
            'source_hex': (bytes([raw[0] ^ 1]) + raw[1:]).hex(), 'current_hex': row['current_hex'] + '20',
            'compiled_hex': row['compiled_hex'] + '20', 'stored_hex': row['stored_hex'] + '20',
            'source_selector': 254, 'qa_waivers': ['weak-line-ending'], 'qa_waiver_scope': dict(unscoped=True),
            'formatting_approval_reason': '', 'actual_selected_path_coverage': [],
        }.items():
            changed = deepcopy(doc)
            changed['records'][index][field] = value
            reject(ident + ':approved-field:' + field, doc, changed, validate_approved_batch)
        for field in ['source_reference', 'current_reference', 'final_reference']:
            for part in ['offset', 'bytes', 'header_offset', 'record_index']:
                changed = deepcopy(doc)
                changed['records'][index][field][part] += 1
                reject(ident + ':reference:' + field + ':' + part, doc, changed, validate_approved_batch)
        for label, value in [('selector', bytes([raw[0] ^ 1]) + raw[1:]), ('missing-first', raw[:1] + raw[2:]),
                             ('missing-final', raw[:-1]), ('trailing-NUL', raw + b'\0')]:
            reject(ident + ':source:' + label, raw, value, lambda r: encode_relocatable_dialogue(r, text, profile), 'complete source and reviewed logical paragraph required')
        for label, value in [('manual-break', text + '{LB}'), ('raw-LF', text + '\n'), ('alignment', text + '{ALIGN@0}'),
                             ('padding', text + '{PAD}'), ('leading-space', ' ' + text), ('trailing-space', text + ' '),
                             ('Unicode-punctuation', text + '“'), ('missing-final', text[:-1])]:
            reject(ident + ':prose:' + label, text, value, lambda t: encode_relocatable_dialogue(raw, t, profile), 'complete source and reviewed logical paragraph required')
        for field, value in [('window_width_px', 210), ('max_lines', 5), ('default_ascii_width', 7), ('default_multibyte_width', 10),
                             ('guard_linebreaks', False), ('pair_phase_safe_breaks', False), ('leading_speaker_bytes', frozenset({3})),
                             ('literal_prefix_policy', 'forbid'), ('macro_ascii_lengths', dict(FI=7, FA=9, FO=15))]:
            reject(ident + ':profile:' + field, profile, replace(profile, **{field: value}),
                   lambda p: encode_relocatable_dialogue(raw, text, p), 'profile changed')
        reject(ident + ':wrong-file', '/data/SC1.DK4', '/data/SC0.DK4', lambda p: profile_for(arm, block, ident, p), 'file-qualified')
        reject(ident + ':wrong-block', block, bytes([block[0] ^ 1]) + block[1:], lambda b: profile_for(arm, b, ident, '/data/SC1.DK4'), 'file-qualified')
        reject(ident + ':wrong-runtime', arm, bytes([arm[0] ^ 1]) + arm[1:], lambda a: profile_for(a, block, ident, '/data/SC1.DK4'), 'file-qualified')
        reject(ident + ':wrong-consumer', 'progressive', 'FE-paper', lambda c: profile_for(arm, block, ident, '/data/SC1.DK4', c), 'consumer required')
        print('B52_POLICY_SPEECH', ident, 'negative cases', len(negatives), flush=True)

    choices = doc['typed_choice_records']
    choice_raw = compile_choices(choices)
    assert choice_raw.hex() == frozen['choice_object_hex'] and len(choice_raw) == 32
    for index, row in enumerate(choices):
        for gate in frozen['review_gates']:
            changed = deepcopy(choices)
            changed[index]['review'][gate] = False
            reject(row['id'] + ':choice-gate:' + gate, choices, changed, compile_choices)
        for field, value in [('english', row['english'] + ' '), ('option_index', 1 - index), ('source_hex', row['source_hex'] + '20'),
                             ('current_hex', row['current_hex'] + '20'), ('stored_hex', row['stored_hex'] + '20'),
                             ('context', 'Invented family.'), ('speaker', 'Port Worker'), ('source_meaning', ''),
                             ('localization_note', ''), ('retention_reason', ''), ('compiled_choice_label_hex', row['compiled_choice_label_hex'] + '20')]:
            changed = deepcopy(choices)
            changed[index][field] = value
            reject(row['id'] + ':choice-field:' + field, choices, changed, compile_choices)
        for field in ['source_reference', 'current_reference', 'final_reference']:
            changed = deepcopy(choices)
            changed[index][field]['offset'] += 2
            reject(row['id'] + ':choice-reference:' + field, choices, changed, compile_choices)
    for label, changed in [('reverse', list(reversed(choices))), ('duplicate', choices[:1] * 2), ('missing', choices[:1]),
                           ('extra', choices + choices[:1]), ('not-list', tuple(choices))]:
        reject('typed-choice-order-count:' + label, choices, changed, compile_choices)
    for field in ['records', 'typed_choice_records']:
        for label, rows in [('reverse', list(reversed(doc[field]))), ('missing', doc[field][:-1]), ('duplicate', doc[field][:-1] + doc[field][:1])]:
            changed = deepcopy(doc)
            changed[field] = rows
            reject('batch-order:' + field + ':' + label, doc, changed, validate_approved_batch)
    for key, value in [('target_locale', 'en-GB'), ('translation_policy', 'natural-dialogue-v1'), ('file_path', '/data/SC0.DK4'),
                       ('route', 0), ('blocks', [51]), ('encoder', 'raw')]:
        changed = deepcopy(doc)
        changed[key] = value
        reject('batch:' + key, doc, changed, validate_approved_batch, 'metadata required')
    for field in ['records', 'mentioned_components']:
        for index, row in enumerate(names[field]):
            for gate in frozen['review_gates']:
                changed = deepcopy(names)
                changed[field][index]['review'][gate] = False
                reject('names:' + field + ':' + gate, names, changed, validate_scoped_names, 'source-qualified review')
            changed = deepcopy(names)
            changed[field][index]['actor_ID'] += 1
            reject('names:' + field + ':identity', names, changed, validate_scoped_names, 'source-qualified review')
    for field in ['no_new_name_asset_orall207_name_review_credit', 'no_actor34_actual_header_catalogue_orfull_name_review_claim']:
        changed = deepcopy(names)
        changed[field] = False
        reject('names:scope:' + field, names, changed, validate_scoped_names, 'source-qualified review')
    assert len(positives) == 3 and sum(len(p['qa']['issues']) for p in positives) == 1 and len(negatives) > 200
    assert {str(p): sha(p.read_bytes()) for p in protected} == before
    save(ROOT / 'policy_validation.json', dict(contract='translations/hodram_B52_native_contract_v1.json',
        contract_sha256=sha(Path('translations/hodram_B52_native_contract_v1.json').read_bytes()),
        manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), positive_speech_compilers=positives,
        positive_typed_choice_object_hex=choice_raw.hex(), positive_editorial_units=5, positive_scoped_names_andmentioned_component=True,
        negative_cases=negatives, negative_count=len(negatives), every_negative_actual_input_changed_andsemantic_guard_rejected=True,
        all_frozen_dependency_guards_remained_enabled=True, all_protected_files_ROMs_registry_ledger_source_inputs_hash_exact=True,
        protected_hashes=before, one_original_info_zero_warnings_waivers=True,
        all_native_actual_andlong_divergence_versus_focus_limits_preserved=True,
        independent_production_atomic_registered_build_patch_startup_andcredit_pending=True,
        new_native_runs=0, new_emulator_runs=0, new_credit=0, full_goal_complete=False))
    print('B52 policy:3 speech compilers/2 typed choices/scoped names pass;', len(negatives), 'genuinely changed semantic rejections, all frozen guards active. Protected source/ROMs/registry/ledger exact; zero credit.', flush=True)
