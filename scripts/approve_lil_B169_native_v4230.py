"""Approve all36 source-bound planes after viewing all five complete native sheets."""
import re
from collections import Counter
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue import lil_B169_layout_v2 as codec
from dk4tool.dialogue.lil_B169_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B169_native_approval_v4230')
INPUT = Path('translations/lil_B169_editorial_manuscript_v3.json')
OUTPUT = Path('translations/lil_B169_editorial_manuscript_v4.json')
FONT = Path('work/analysis/lil_B169_fonts_v4229/current_macro_QA_and_progressive_font_proof.json')


def validate_source_macros(raw, english):
    if re.findall(rb'FI|FA|FO', raw[1:]) != [v.encode('ascii') for v in re.findall(r'\{MACRO:(FI|FA|FO)\}', english)]:
        raise ValueError('Complete source FI/FA/FO substitutions and order are required')


if __name__ == '__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    doc, font = deepcopy(read(INPUT)), read(FONT)
    assert font['manuscript_sha256'] == sha(INPUT.read_bytes())
    assert len(font['cases']) == 36 and font['current_original_macro_alignment_calls'] == 288
    assert len(font['negative_controls']) == 21 and font['all36_progressive_full_QA_and_complete_native_fonts_pass']
    image = NdsImage.open(doc['current_ROM'])
    arm = image.read_file('/__arm9__.bin')
    block = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[169]
    assert sha(Path(doc['current_ROM']).read_bytes()) == doc['current_ROM_sha256'] == font['candidate_sha256']
    assert sha(arm) == font['ARM9_sha256'] == doc['required_runtime_ARM9_sha256']
    sheets = []
    for sheet in font['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
        sheets.append({**sheet, 'viewed_in_full_current_turn': True,
                       'review': 'Viewed complete native sheet: all edge/internal glyphs present, complete four-row planes, natural phrase flow, no source-name split. Whole-exchange fluster/flattery, sea-rule legend, clue/ruin distinctions and tavern give-and-take remain complete. Offline native rendering only.'})
    assert len(sheets) == 5
    byid = {row['id']: row for row in font['cases']}
    p = profile_for(arm, block)
    invariants, macros = [], Counter()
    for row in doc['records']:
        raw = bytes.fromhex(row['source_hex'])
        c = byid[row['id']]
        encoded = codec.encode_relocatable_dialogue(raw, row['english'], p)
        assert encoded.encoded.hex() == row['compiled_hex'] == c['encoded_hex']
        assert semantic_tokens(row['english']) == semantic_tokens(encoded.formatted_markup)
        validate_source_macros(raw, row['english'])
        macros.update(re.findall(rb'FI|FA|FO', raw[1:]))
        assert c['complete_native_independent216x64_plane_equal']
        assert c['all_first_final_internal_glyphs_in_order_and_unique_cells']
        assert c['all_visible_origins_zero_and16px_rows_within4rows']
        assert sha(Path(c['preview']).read_bytes()) == c['preview_sha256']
        assert sum(len(v['cases']) for v in c['current_native_macro_pipelines']) == 8
        qa = codec.audit_relocatable_dialogue_record(raw, row['english'], p)
        assert row.get('qa_waivers') in [None, ['line-break-count']]
        assert not [i for i in qa['issues'] if i['severity'] in ['warning', 'error'] and not
                    (i['severity'] == 'warning' and i['code'] == 'line-break-count' and row.get('qa_waiver_reason'))]
        assert all(row['review'][gate] for gate in ['source','context','localization','naturalness'])
        row['review']['formatting'] = True
        row.update(record_index=row['current_record_index'], current_text_hex=row['current_hex'],
                   native_font_case=c, native_formatting_consumer='progressive',
                   native_plane_verified_not_actual_gameplay=True, current_complete_native_display_pending=False,
                   current_native_voice_macro_entry_and_context_pending=False,
                   status='source-prose-current-native-format-approved;relocation-references-story-representative-release-pending')
        invariants.append(dict(id=row['id'], block=169, source_selector=raw[0],
                               whole_source_English_tokens_and_control_order_preserved=True,
                               encoded_sha256=sha(encoded.encoded)))
        if row['editorial_decision'] == 'retain-wording':
            assert row['english'].split('}', 1)[1] == row['effective_predecessor_paragraph']
            assert row['fresh_retained_wording_justification']
    assert macros == {b'FI': 5, b'FO': 2}
    assert Counter(row['editorial_decision'] for row in doc['records']) == {'revise':19, 'retain-wording':17}
    assert sum(bool(row.get('qa_waivers')) for row in doc['records']) == 14
    negatives = []
    def reject(label, fn):
        try:
            fn()
        except (ValueError, AssertionError) as error:
            negatives.append(dict(case=label, rejected=True, error=str(error)))
        else:
            raise AssertionError(label)
    row = doc['records'][0]
    raw = bytes.fromhex(row['source_hex'])
    for label, bad in [('width',replace(p,window_width_px=228)), ('rows',replace(p,max_lines=5)),
                       ('glyph',replace(p,default_ascii_width=5)), ('row-spacing',replace(p,line_height_px=12)),
                       ('disabled-LF-guard',replace(p,guard_linebreaks=False)),
                       ('disabled-pair-phase',replace(p,pair_phase_safe_breaks=False)),
                       ('disabled-balancing',replace(p,balanced_wrapping=False)),
                       ('macro-width',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FO':10})),
                       ('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:
        reject(label,lambda bad=bad:codec.encode_relocatable_dialogue(raw,row['english'],bad))
    for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:
        reject('manual-or-end-'+tag,lambda tag=tag:codec.encode_relocatable_dialogue(raw,row['english']+tag,p))
    reject('widened-selectors',lambda:codec.encode_relocatable_dialogue(raw,row['english'],replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{149})))
    assert len(negatives) == 14
    macro_negatives = []
    for name, literal in [('FI','Lil'),('FO','Argot Co.')]:
        selected = next(r for r in doc['records'] if '{MACRO:'+name+'}' in r['english'])
        try:
            validate_source_macros(bytes.fromhex(selected['source_hex']), selected['english'].replace('{MACRO:'+name+'}',literal,1))
        except ValueError as error:
            macro_negatives.append(dict(case='source-'+name+'-replaced-by-literal',rejected=True,error=str(error)))
        else:
            raise AssertionError(name)
    names_path = Path(doc['source_nameplate_consumer_proof'])
    assert sha(names_path.read_bytes()) == doc['source_nameplate_consumer_proof_sha256']
    names = read(names_path)['native_twelve_consumer_cases']['rows']
    assert len(names) == 12 and all(row['original_scratch_rings'] and row['original_getter_writes'] for row in names)
    assert all(row['all_actor_models_and_unowned4MiB_exact'] and row['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for row in names)
    ROOT.mkdir(parents=True)
    merged = ROOT / 'all36_native_progressive_and_source_reconciliation.json'
    save(merged,dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),
        manuscript=str(INPUT),manuscript_sha256=sha(INPUT.read_bytes()),cases=font['cases'],
        current_original_macro_alignment_calls=288,all36_current_native_speech_planes_pass=True,
        progressive_planes=36,FE_planes=0,review_sheets=sheets,source_English_macro_control_invariants=invariants,
        source_bound_formatter_negatives=negatives,source_consumer_negative_controls=font['negative_controls'],
        source_macro_preservation_negatives=macro_negatives,scoped_profile=doc['scoped_profile_module'],
        scoped_profile_sha256=doc['scoped_profile_module_sha256'],native_formatter_module=doc['native_formatter_module'],
        native_formatter_module_sha256=doc['native_formatter_module_sha256'],
        all36_source_facts_complete_exchange_and_individual_decisions_reconciled=True,
        source_FI5_FO2_and_six_selectors_preserved=True,three_source_predicates_one_later_numeric_A000_and_end_preserved=True,
        no_A000_recruitment_label_or_earned_flag_claim=True,older_Proof_variant_lead_and_later_technical_reaudit_stay_open=True,
        evidence={str(path):sha(path.read_bytes()) for path in [INPUT,FONT,names_path,Path(__file__)]},
        no_new_gameplay_or_completion_credit=True,full_goal_complete=False))
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),
        native_font_proof=str(merged),native_font_proof_sha256=sha(merged.read_bytes()),native_progressive_proof=str(FONT),
        formatting_review_pending=False,all36_five_review_gates_true=True,
        formatter_phrase_flow_findings_resolved_without_waiver=True,
        clean_first_whole_exchange_context_notes_are_historical_and_followed_by_bound_current_contracts=True,
        status='source-prose-current-native-format-approved;relocation-references-story-representative-release-pending')
    validate_natural_dialogue_batch(doc)
    save(OUTPUT,doc)
    save(ROOT/'approval_receipt.json',dict(manuscripts={str(OUTPUT):sha(OUTPUT.read_bytes())},
        merged_native_proof=str(merged),merged_native_proof_sha256=sha(merged.read_bytes()),revised=19,retained=17,
        progressive_planes=36,current_macro_alignment_cases=288,source_consumer_negatives=21,source_macro_negatives=2,
        formatter_negatives=14,narrow_row_count_notes=14,review_sheets=sheets,actual_selected_B169_IDs=[],new_emulator_runs=0,
        relocation_references_representative_registered_release_pending=True,new_source_prose_reviews=0,new_completed_records=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B169:36 five-gate reviews approved,19 revisions/17 retentions;36 native planes/288 cases;21+2+14 rejection controls. Actual scene and integration pending;no credit yet.')
