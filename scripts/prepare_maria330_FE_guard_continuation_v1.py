"""Preserve B116R41 under a second exact source-owned FE continuation after a native guard failure."""
from copy import deepcopy
from pathlib import Path
import hashlib
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

OWNER='DK4_MES_B116_R0041'
def main():
    path=ROOT/'formatting_FE_v1/physical_manuscript.json';source=load(path)
    pref_path=ROOT/'continuity_preferences_v4.json';prefs=deepcopy(load(pref_path));out=ROOT/'formatting_FE_v2'
    assert not out.exists() and len(source['records'])==331 and source['physical_speech_objects']==329
    owner=next(r for r in source['records'] if r['id']==OWNER)
    assert owner['kind']=='system-FE' and owner['source_complete_preamble_hex']=='0040ffff00fe' and not any(owner['source_macros'].values())
    marker=' He left our ships fighting, surrounded by the enemy.';assert owner['english'].count(marker)==1
    split=owner['english'].index(marker);parts=[owner['english'][:split],owner['english'][split+1:]]
    assert ' '.join(parts)==owner['english'] and parts[0].endswith('save himself.')
    rows=[];children=[]
    for row in source['records']:
        if row['id']!=OWNER:rows.append(deepcopy(row));continue
        for i,text in enumerate(parts,1):
            child=deepcopy(row);child.update(id=OWNER+f'_FE_PAGE_{i}',english=text,planned_English_markup='{SPEAKER:FE}'+text,
                source_editorial_ID=OWNER,native_child_page=i,native_child_page_count=2,source_complete_paragraph=row['english'],
                virtual_formatting_child_not_another_source_editorial_record=True,prior_macro_normalized_comparison=None)
            rows.append(child);children.append(child)
    reason=('Native painter stopped before the terminator on the original four-row plan with a37-cell guarded first row. '
        'Reuse the validated source-scoped36-cell planning reserve at unchanged228-pixel physical width. The complete first sentence narrates desertion; '
        'the second narrates abandoning the surrounded allies. Preserve every word and the original FE control, with one explicit additional A transition still to test.')
    pagination=dict(source_ID=OWNER,source_reference=owner['source_reference'],current_reference=owner['current_reference'],
        complete_source_preamble_hex=owner['source_complete_preamble_hex'],source_hex=owner['source_hex'],current_hex=owner['current_hex'],
        unchanged_logical_English=owner['english'],child_IDs=[r['id'] for r in children],page_segments=parts,semantic_boundary_reason=reason,
        synthetic_command_count=1,source_control_repeated_exactly_not_a_new_actor_orengine_change=True,
        byte_planner='dk4tool/script/reviewed_FE_pagination_v1.py',byte_planner_sha256=digest('dk4tool/script/reviewed_FE_pagination_v1.py'),
        stored_native_branch_inverse_andactual_A_transition_still_required=True)
    target=deepcopy(source);target.update(records=rows,physical_speech_objects=330,ordinary_speech_objects=295,
        source_editorial_objects=330,pagination_owners=sorted([*source['pagination_owners'],pagination],key=lambda r:r['source_reference']['offset']))
    assert len(rows)==332 and len(target['pagination_owners'])==2 and len({r['id'] for r in rows})==332
    for child in children:
        prefs['records'][child['id']]=dict(one_page=True,FE_planning_cells=36,reason=reason,
            bindings={k:hashlib.sha256(child[k].encode()).hexdigest() for k in ['source_hex','current_hex','english']})
    prefs['evidence'].update({str(p):digest(p) for p in [path,pref_path,ROOT/'native_pages_v1/native_run_inputs.json',Path(__file__)]})
    out.mkdir();save(out/'physical_manuscript.json',target);save(out/'preferences.json',prefs)
    save(out/'pagination_owners.json',dict(owners=target['pagination_owners'],new_credit=0))
    save(out/'projection.json',dict(source=str(path),source_sha256=digest(path),source_editorial_objects=330,physical_formatting_objects=332,
        physical_body_candidates=330,choice_captions=2,full_source_paragraphs_andall_other_records_unchanged=True,
        native_failure_owner=OWNER,validated_guard_reserve_source_scoped_only=True,physical_FE_width_228_unchanged=True,
        no_shortened_prose_no_authored_ordinary_breaks_no_new_source_credit=True,new_credit=0,producer_sha256=digest(__file__)))
    print('Prepared two source-owned FE owners/four children:330 bodies/two captions; all330 source objects unchanged.')

if __name__=='__main__':main()
