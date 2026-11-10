"""Keep the full riddle paragraph through two source-owned FE continuation candidates."""
from copy import deepcopy
from pathlib import Path
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

OWNER = 'DK4_MES_B87_R0139'


def main():
    source_path = ROOT/'formatting_v1/formatting_input.json'
    source = load(source_path)
    out = ROOT/'formatting_FE_v1'
    assert not out.exists() and len(source['records']) == 328
    owner = next(r for r in source['records'] if r['id']==OWNER)
    assert owner['kind'] == 'system-FE' and owner['source_complete_preamble_hex'] == '0040ffff00fe'
    assert not any(owner['source_macros'].values())
    marker = ' If there are as many elderly people as babies, how many adults are there?'
    assert owner['english'].count(marker) == 1
    split = owner['english'].index(marker)
    parts = [owner['english'][:split],owner['english'][split+1:]]
    assert ' '.join(parts) == owner['english'] and parts[0].endswith('touch the floor.')
    physical, children = [], []
    for row in source['records']:
        if row['id'] != OWNER:
            physical.append(deepcopy(row))
            continue
        for page, text in enumerate(parts,1):
            child = deepcopy(row)
            child.update(id=OWNER+f'_FE_PAGE_{page}',english=text,planned_English_markup='{SPEAKER:FE}'+text,
                source_editorial_ID=OWNER,native_child_page=page,native_child_page_count=2,
                source_complete_paragraph=row['english'],virtual_formatting_child_not_another_source_editorial_record=True,
                prior_macro_normalized_comparison=None)
            physical.append(child)
            children.append(child)
    pagination = dict(source_ID=OWNER,source_reference=owner['source_reference'],current_reference=owner['current_reference'],
        complete_source_preamble_hex=owner['source_complete_preamble_hex'],source_hex=owner['source_hex'],current_hex=owner['current_hex'],
        unchanged_logical_English=owner['english'],child_IDs=[r['id'] for r in children],page_segments=parts,
        semantic_boundary_reason='First panel gives the ten-person categories and32 floor contacts;the second gives the equality premise andasks for the adult count. Keep every word andnumber. One ordinary paragraph space becomes a native panel boundary,not an authored line break.',
        synthetic_command_count=1,source_control_repeated_exactly_not_a_new_actor_orengine_change=True,
        byte_planner='dk4tool/script/reviewed_FE_pagination_v1.py',
        byte_planner_sha256=digest('dk4tool/script/reviewed_FE_pagination_v1.py'),
        stored_native_branch_inverse_andactual_A_transition_still_required=True)
    target = deepcopy(source)
    target.update(records=physical,physical_speech_objects=314,ordinary_speech_objects=290,
        source_editorial_objects=328,pagination_owners=[pagination],virtual_children_not_extra_source_coverage=True,
        source_owner_manuscript=str(source_path),source_owner_manuscript_sha256=digest(source_path))
    assert len(physical) == 329 and len(children) == 2
    out.mkdir()
    save(out/'physical_manuscript.json',target)
    save(out/'pagination_owners.json',dict(owners=[pagination],new_credit=0))
    preferences = deepcopy(load(ROOT/'formatting_v1/initial_preferences.json'))
    assert preferences['records'] == {}
    for child in children:
        preferences['records'][child['id']] = dict(one_page=True,reason=pagination['semantic_boundary_reason'],
            bindings={k:__import__('hashlib').sha256(child[k].encode()).hexdigest() for k in ['source_hex','current_hex','english']})
    save(out/'preferences.json',preferences)
    save(out/'projection.json',dict(source=str(source_path),source_sha256=digest(source_path),source_objects=328,
        physical_formatting_objects=329,physical_body_candidates=314,choice_captions=15,
        full_riddle_paragraph_andall_other_records_unchanged=True,source_preamble_andconditional_scope_must_be_preserved=True,
        no_authored_line_break_orwidth_font_engine_prose_change=True,new_credit=0,
        evidence={str(p):digest(p) for p in [source_path,Path(__file__)]}))
    print('Prepared full riddle as two FE page candidates;all328 source decisions andevery word preserved.')


if __name__ == '__main__':
    main()
