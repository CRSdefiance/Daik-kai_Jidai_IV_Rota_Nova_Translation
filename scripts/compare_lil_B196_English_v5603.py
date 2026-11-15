"""Read all older B196 speech/choice prose only after the clean exchange and terms."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B196_comparison_v5603')
SOURCE=Path('work/analysis/lil_B196_source_v5590/all36_clean_current_complete_context_with_twelve_choice_labels.json')
TERMS=Path('work/analysis/lil_B196_terms_v5602/six_roles_gold_Charm_FI_and_six_prices_without_invented_item_identity.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,terms=read(SOURCE),read(TERMS)
    assert terms['source_context_sha256']==sha(SOURCE.read_bytes())
    assert terms['all24_clean_first_glosses_and12_choice_glosses_precede_predecessor_prose_comparison']
    rows=[]
    for original in sorted(packet['records']+packet['typed_choice_records'],key=lambda r:r['source_reference']['offset']):
        r=deepcopy(original);value=bytes.fromhex(r['current_hex'])
        body=value if r['kind']=='typed-choice-label' else value[1:]
        if r['kind']!='typed-choice-label':assert value[0]==r['source_selector']
        display=body.decode('cp932');paragraph=' '.join(display.split());template=paragraph
        for m in ['FI','FA','FO']:
            assert bytes.fromhex(r['source_hex']).count(m.encode())==body.count(m.encode())
            template=template.replace(m,'{MACRO:'+m+'}')
        r.update(previous_display_body=display,previous_paragraph=paragraph,previous_macro_template_paragraph=template,
            previous_bytes_retained_for_exact_comparison=True)
        rows.append(r)
    assert len(rows)==36 and sum(r['kind']=='typed-choice-label' for r in rows)==12
    ROOT.mkdir(parents=True)
    save(ROOT/'all36_complete_clean_and_predecessor_exchange_with_six_choices.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),terms=str(TERMS),terms_sha256=sha(TERMS.read_bytes()),records=rows,
        clean_first_whole_exchange_gloss_names_voices_control_boundaries_payment_amounts_and_terms_precede_comparison=True,
        predecessor_is_comparison_material_not_translation_source=True,individual_contextual_decisions_and_native_layout_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,TERMS,Path(packet['whole_exchange_context_notes']),Path(__file__)]},new_editorial_credit=0,full_goal_complete=False))
    for r in rows:
        print(r['id'],r.get('source_selector','choice'))
        print('JP:',r['source_Japanese'].replace('\n',' / '));print('CURRENT:',repr(r['previous_macro_template_paragraph']))
