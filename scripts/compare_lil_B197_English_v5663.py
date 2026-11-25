"""Compare all older English only after the clean exchange and actual source paths."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B197_comparison_v5663')
SOURCE=Path('work/analysis/lil_B197_source_v5647/all24_clean_current_complete_context_with_three_choice_labels.json')
TERMS=Path('work/analysis/lil_B197_context_v5662/clean_first_context_original_three_paths_gold_and_Charm.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,terms=map(read,[SOURCE,TERMS])
    assert terms['source_context_sha256']==sha(SOURCE.read_bytes())
    assert terms['all_clean_first_glosses_and_original_actual_context_precede_predecessor_speech_comparison']
    glosses={r['source_record_index']:r for r in terms['corrected_contextual_gloss_records']};rows=[]
    for original in sorted(packet['records']+packet['typed_choice_records'],key=lambda r:r['source_reference']['offset']):
        r=deepcopy(original);choice=r['kind']=='typed-choice-label';raw=bytes.fromhex(r['current_hex'])
        body=raw if choice else raw[1:]
        if not choice:
            assert raw[0]==r['source_selector']
            g=glosses[r['source_record_index']]
            r.update(fresh_source_gloss=g['fresh_source_gloss'],whole_exchange_note=g['whole_exchange_note'],actual_source_paths=g['actual_source_paths'])
        assert all(m not in body and m not in bytes.fromhex(r['source_hex']) for m in [b'FI',b'FA',b'FO'])
        display=body.decode('cp932');paragraph=' '.join(display.split())
        r.update(previous_display_body=display,previous_paragraph=paragraph,previous_macro_template_paragraph=paragraph,
                 previous_bytes_retained_for_exact_comparison=True)
        rows.append(r)
    assert len(rows)==24 and sum(r['kind']=='typed-choice-label' for r in rows)==3
    ROOT.mkdir(parents=True)
    save(ROOT/'all24_complete_clean_and_predecessor_exchange_with_three_choices.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),terms=str(TERMS),terms_sha256=sha(TERMS.read_bytes()),records=rows,
        clean_first_whole_exchange_gloss_names_voices_control_payment_terms_and_actual_original_paths_precede_comparison=True,
        predecessor_is_comparison_material_not_translation_source=True,individual_contextual_decisions_and_native_layout_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,TERMS,Path(packet['whole_exchange_context_notes']),Path(__file__)]},
        new_editorial_credit=0,full_goal_complete=False))
    for r in rows:
        print(r['id'],r.get('source_selector','choice'))
        print('JP:',r['source_Japanese'].replace('\n',' / '));print('CURRENT:',repr(r['previous_paragraph']))
