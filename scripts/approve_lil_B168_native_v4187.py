"""Approve the complete Mikhail exchange using source-bound progressive and FE proofs."""
import re
from collections import Counter
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

from dk4tool.dialogue import lil_B168_layout_v3 as codec
from dk4tool.dialogue.lil_B168_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B168_native_approval_v4187')
INPUT = Path('translations/lil_B168_editorial_manuscript_v6.json')
OUTPUT = Path('translations/lil_B168_editorial_manuscript_v7.json')
FONT = Path('work/analysis/lil_B168_fonts_v4185/all54_native_planes432_macro_cases_and26_consumer_negatives.json')


def validate_source_macros(raw, english):
    source = re.findall(rb'FI|FA|FO', raw[1:])
    target = [x.encode('ascii') for x in re.findall(r'\{MACRO:(FI|FA|FO)\}', english)]
    if source != target:
        raise ValueError('Complete source FI/FA/FO substitutions and order are required')


if __name__ == '__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    doc, font = deepcopy(read(INPUT)), read(FONT)
    assert font['manuscript_sha256'] == sha(INPUT.read_bytes())
    assert len(font['cases']) == 54 and font['current_original_macro_alignment_calls'] == 432
    assert len(font['source_consumer_negative_controls']) == 26
    assert font['all54_complete_native_independent_planes_pass']
    assert (font['progressive_planes'], font['FE_planes']) == (51, 3)
    image = NdsImage.open(doc['current_ROM'])
    arm = image.read_file('/__arm9__.bin')
    block = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[168]
    assert sha(Path(doc['current_ROM']).read_bytes()) == doc['current_ROM_sha256'] == font['candidate_sha256']
    assert sha(arm) == font['ARM9_sha256'] == doc['required_runtime_ARM9_sha256']
    sheets = []
    for sheet in font['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
        sheets.append({**sheet, 'viewed_in_full_current_turn': True,
                       'review': 'Viewed complete current sheet. Complete edge/internal glyphs, natural phrase flow and four-row bounds; Mikhail brag/reversal, ambiguous tease, recruitment objections, touching cue/protest and FE instructions retain source meaning. Native preview, not gameplay.'})
    assert len(sheets) == 7
    cases = {c['id']: c for c in font['cases']}
    invariants, macro_counts = [], Counter()
    for row in doc['records']:
        raw = bytes.fromhex(row['source_hex'])
        fe = row['kind'] == 'system-FE'
        p = profile_for(arm, block, 'FE-paper' if fe else 'progressive')
        encoded = codec.encode_relocatable_dialogue(raw, row['english'], p)
        c = cases[row['id']]
        assert encoded.encoded.hex() == row['compiled_hex'] == c['encoded_hex']
        assert semantic_tokens(row['english']) == semantic_tokens(encoded.formatted_markup)
        validate_source_macros(raw, row['english'])
        macro_counts.update(re.findall(rb'FI|FA|FO', raw[1:]))
        assert c['complete_native_independent_plane_equal']
        assert c['all_first_final_internal_glyphs_in_order_and_unique_cells']
        assert c['all_visible_origins_zero_and_native_rows_within4rows']
        assert sha(Path(c['preview']).read_bytes()) == c['preview_sha256']
        assert sum(len(v['cases']) for v in c['current_native_macro_pipelines']) == 8
        if fe:
            assert raw[0] == 254 and c['geometry'] == [228, 64]
            assert c['logical_row_pitch'] == 12 and c['physical_row_pitch'] == 16
            assert c['one_native_page_consumes_complete_target']
            assert c['complete_logical228x48_plane_sha256']
        else:
            assert c['geometry'] == [216, 64] and c['complete_native_independent216x64_plane_equal']
            assert c['logical_row_pitch'] == c['physical_row_pitch'] == 16
        report = codec.audit_relocatable_dialogue_record(raw, row['english'], p)
        assert not [issue for issue in report['issues'] if issue['severity'] in ['warning', 'error']
                    and not (issue['severity'] == 'warning' and issue['code'] == 'line-break-count' and row.get('qa_waiver_reason'))]
        assert row.get('qa_waivers') in [None, ['line-break-count']]
        assert all(row['review'][gate] for gate in ['source', 'context', 'localization', 'naturalness'])
        row['review']['formatting'] = True
        row.update(record_index=row['current_record_index'], current_text_hex=row['current_hex'],
                   native_font_case=c, native_formatting_consumer='FE-paper' if fe else 'progressive',
                   native_plane_verified_not_actual_gameplay=True, current_complete_native_display_pending=False,
                   current_native_voice_macro_entry_and_context_pending=False,
                   status='source-prose-current-native-format-approved;relocation-references-story-representative-release-pending')
        invariants.append(dict(id=row['id'], block=168, source_selector=raw[0],
                               whole_source_English_tokens_and_control_order_preserved=True,
                               encoded_sha256=sha(encoded.encoded)))
        if row['editorial_decision'] == 'retain-wording':
            assert row['english'].split('}', 1)[1] == row['effective_predecessor_paragraph']
            assert row['fresh_retained_wording_justification']
    assert macro_counts == {b'FI': 7, b'FA': 1, b'FO': 1}
    assert Counter(r['editorial_decision'] for r in doc['records']) == {'revise': 28, 'retain-wording': 26}
    assert sum(bool(r.get('qa_waivers')) for r in doc['records']) == 20
    negatives = []
    def reject(label, call):
        try:
            call()
        except (ValueError, AssertionError) as error:
            negatives.append(dict(case=label, rejected=True, error=str(error)))
        else:
            raise AssertionError(label)
    row = doc['records'][0]
    raw = bytes.fromhex(row['source_hex'])
    p = profile_for(arm, block)
    for label, bad in [('width', replace(p, window_width_px=228)), ('rows', replace(p, max_lines=5)),
                       ('glyph', replace(p, default_ascii_width=5)), ('row-spacing', replace(p, line_height_px=12)),
                       ('disabled-LF-guard', replace(p, guard_linebreaks=False)),
                       ('disabled-pair-phase', replace(p, pair_phase_safe_breaks=False)),
                       ('disabled-balancing', replace(p, balanced_wrapping=False)),
                       ('macro-width', replace(p, macro_ascii_lengths={**p.macro_ascii_lengths, 'FA': 6})),
                       ('unscoped-base', get_dialogue_profile('lil-opening-editorial-native-v1'))]:
        reject(label, lambda bad=bad: codec.encode_relocatable_dialogue(raw, row['english'], bad))
    for tag in ['{LB}', '{ALIGN:0}', '{PAD}', '{END}']:
        reject('manual-or-end-' + tag, lambda tag=tag: codec.encode_relocatable_dialogue(raw, row['english'] + tag, p))
    reject('widened-selectors', lambda: codec.encode_relocatable_dialogue(raw, row['english'], replace(p, leading_speaker_bytes=p.leading_speaker_bytes | {149})))
    assert len(negatives) == 14
    macro_negatives = []
    for name, literal in [('FI', 'Lil'), ('FA', 'Argot'), ('FO', 'Argot Co.')]:
        selected = next(r for r in doc['records'] if '{MACRO:' + name + '}' in r['english'])
        bad = selected['english'].replace('{MACRO:' + name + '}', literal, 1)
        try:
            validate_source_macros(bytes.fromhex(selected['source_hex']), bad)
        except ValueError as error:
            macro_negatives.append(dict(case='source-' + name + '-replaced-by-literal', rejected=True, error=str(error)))
        else:
            raise AssertionError(name)
    names_path = Path(doc['source_nameplate_consumer_proof'])
    names = read(names_path)
    assert sha(names_path.read_bytes()) == doc['source_nameplate_consumer_proof_sha256']
    name_rows = names['native_sixteen_consumer_cases']['rows']
    assert len(name_rows) == 16
    assert all(r['all_actor_models_and_unowned4MiB_exact'] and r['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for r in name_rows)
    assert all(not r['original_scratch_rings'] and not r['original_getter_writes'] for r in name_rows if r['actor_ID'] in [87, 165, 166])
    ROOT.mkdir(parents=True)
    merged = ROOT / 'all54_native_progressive_FE_and_source_reconciliation.json'
    save(merged, dict(candidate=doc['current_ROM'], candidate_sha256=doc['current_ROM_sha256'], ARM9_sha256=sha(arm),
        manuscript=str(INPUT), manuscript_sha256=sha(INPUT.read_bytes()), cases=font['cases'],
        current_original_macro_alignment_calls=432, all54_current_native_speech_planes_pass=True,
        progressive_planes=51, FE_planes=3,
        source_FE_null_actor_logical228x48_physical228x64_complete_one_page_proven=True,
        review_sheets=sheets, source_English_macro_control_invariants=invariants,
        source_bound_formatter_negatives=negatives, source_consumer_negative_controls=font['source_consumer_negative_controls'],
        source_macro_preservation_negatives=macro_negatives, scoped_profile=doc['scoped_profile_module'],
        scoped_profile_sha256=doc['scoped_profile_module_sha256'], native_formatter_module=doc['native_formatter_module'],
        native_formatter_module_sha256=doc['native_formatter_module_sha256'],
        all54_source_facts_complete_exchange_and_individual_decisions_reconciled=True,
        source_FI7_FA1_FO1_and_printable_selectors_preserved=True, later_older_record0D_reaudit_stays_open=True,
        evidence={str(path): sha(path.read_bytes()) for path in [INPUT, FONT, names_path, Path(__file__)]},
        no_new_gameplay_or_completion_credit=True, full_goal_complete=False))
    doc.update(previous_manuscript=str(INPUT), previous_manuscript_sha256=sha(INPUT.read_bytes()),
        native_font_proof=str(merged), native_font_proof_sha256=sha(merged.read_bytes()), native_progressive_proof=str(FONT),
        formatting_review_pending=False, all54_five_review_gates_true=True,
        formatter_phrase_flow_findings_resolved_without_waiver=True,
        clean_first_whole_exchange_context_notes_are_historical_and_followed_by_bound_current_contracts=True,
        status='source-prose-current-native-format-approved;relocation-references-story-representative-release-pending')
    validate_natural_dialogue_batch(doc)
    save(OUTPUT, doc)
    save(ROOT / 'approval_receipt.json', dict(manuscripts={str(OUTPUT): sha(OUTPUT.read_bytes())},
        merged_native_proof=str(merged), merged_native_proof_sha256=sha(merged.read_bytes()),
        revised=28, retained=26, progressive_planes=51, FE_planes=3, current_macro_alignment_cases=432,
        source_consumer_negatives=26, source_macro_negatives=3, formatter_negatives=14,
        narrow_row_count_notes=20, review_sheets=sheets, actual_selected_B168_IDs=[], new_emulator_runs=0,
        relocation_references_representative_registered_release_pending=True,
        new_source_prose_reviews=0, new_completed_records=0, producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print('B168: 54 five-gate reviews approved, 28 revisions/26 retentions; 51 progressive/3 FE planes, 432 alignment cases, 26+3+14 rejection controls. Actual scene and integration pending; no credit yet.')
