"""Compare previous English only after the complete Japanese exchange and source capture."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B198_comparison_v5716')
SOURCE=Path('work/analysis/lil_B198_source_v5702/all17_clean_current_complete_context.json')
TERMS=Path('work/analysis/lil_B198_context_v5715/clean_first_context_Namahage_dream_and_original_unforced_path.json')
if __name__=='__main__':
    assert not ROOT.exists()
    packet,terms=map(read,[SOURCE,TERMS])
    assert terms['source_context_sha256']==sha(SOURCE.read_bytes())
    assert terms['all_clean_first_glosses_and_original_actual_context_precede_predecessor_speech_comparison']
    glosses={r['source_record_index']:r for r in terms['corrected_contextual_gloss_records']};rows=[]
    for original in sorted(packet['records'],key=lambda r:r['source_reference']['offset']):
        r=deepcopy(original);raw=bytes.fromhex(r['current_hex']);assert raw[0]==r['source_selector']
        body=raw[1:];g=glosses[r['source_record_index']]
        assert all(m not in body and m not in bytes.fromhex(r['source_hex']) for m in [b'FI',b'FA',b'FO'])
        display=body.decode('cp932');paragraph=' '.join(display.split())
        r.update(fresh_source_gloss=g['fresh_source_gloss'],whole_exchange_note=g['whole_exchange_note'],
            actual_source_paths=g['actual_source_paths'],actual_source_fixture_observed=g['actual_source_fixture_observed'],
            previous_display_body=display,previous_paragraph=paragraph,previous_macro_template_paragraph=paragraph,
            previous_bytes_retained_for_exact_comparison=True)
        rows.append(r)
    assert len(rows)==17
    ROOT.mkdir(parents=True)
    save(ROOT/'all17_complete_clean_and_predecessor_exchange.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),terms=str(TERMS),terms_sha256=sha(TERMS.read_bytes()),records=rows,
        clean_first_gloss_names_voices_controls_and_actual_source_context_precede_comparison=True,
        predecessor_is_comparison_material_not_translation_source=True,individual_editorial_decisions_and_native_layout_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,TERMS,Path(packet['whole_exchange_context_notes']),Path(__file__)]},
        new_editorial_credit=0,full_goal_complete=False))
    for r in rows:
        print(r['id'],r['source_selector'],'JP:',r['source_Japanese'].replace('\n',' / '),'CURRENT:',repr(r['previous_paragraph']))
