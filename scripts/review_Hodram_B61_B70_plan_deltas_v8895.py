"""Record actual wrap defects found, corrections, and passing checks separately."""
from pathlib import Path
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B61_B70_boundary_review_v8895')
OLD=Path('work/analysis/Hodram_B61_B70_layout_v8892/automatic_plans.json')
NEW=Path('work/analysis/Hodram_B61_B70_layout_v8893/automatic_plans.json')
DOC=Path('translations/hodram_B61_B70_editorial_manuscript_v1.json')

if __name__=='__main__':
    assert not ROOT.exists();old,new,doc=map(read,[OLD,NEW,DOC])
    assert not old['failures'] and not new['failures'] and old['manuscript_sha256']==new['manuscript_sha256']==sha(DOC.read_bytes())
    assert len(old['records'])==len(new['records'])==len(doc['records'])==224
    changes=[];by_id={r['id']:r for r in doc['records']};pairs={}
    for a,b in zip(old['records'],new['records'],strict=True):
        assert a['id']==b['id'];row=by_id[a['id']];assert ' '.join(a['lines'])==' '.join(b['lines'])==row['english']
        assert a['original_consumer_usable_text_width_px']==b['original_consumer_usable_text_width_px']==216
        assert not any(i['severity'] in ['warning','error'] for r in [a,b] for i in r['base_QA']['issues'])
        pairs[a['id']]=(a,b)
        if a['lines']!=b['lines']:
            changes.append(dict(id=a['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],
                source_hex=row['source_hex'],current_hex=row['current_hex'],logical_English=row['english'],
                before_lines=a['lines'],after_lines=b['lines'],before_encoded_hex=a['encoded_hex'],after_encoded_hex=b['encoded_hex'],
                before_cost=a['planning_cost'],after_cost=b['planning_cost'],
                original_before_QA_issues=a['base_QA']['issues'],original_after_QA_issues=b['base_QA']['issues'],
                native_English_pages_anddirect_view_still_pending=True))
    a,b=pairs['DK4_MES_B64_R0011'];assert a['lines'][0]=='You truly' and b['lines'][0]=='You truly are the king'
    a,b=pairs['DK4_MES_B63_R0022'];assert a['lines'][0].endswith("don't") and b['lines'][1].startswith("don't you?")
    a,b=pairs['DK4_MES_B67_R0238'];assert a['lines'][3].endswith("won't") and b['lines'][4].startswith("He won't be")
    assert pairs['DK4_MES_B62_R0039'][1]['lines']==['Tell me...','what is your homeland like?']
    assert len(changes)>0 and sum(r['expected_native_pages'] for r in new['records'])==229
    issues=Counter(i['severity'] for r in new['records'] for i in r['base_QA']['issues'])
    ROOT.mkdir(parents=True)
    save(ROOT/'actual_boundary_findings_andprose_preserving_corrections.json',dict(
        first_plans=str(OLD),first_plans_sha256=sha(OLD.read_bytes()),corrected_plans=str(NEW),corrected_plans_sha256=sha(NEW.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),changed_plans=changes,changed_record_count=len(changes),
        actual_readability_findings=[
            dict(id='DK4_MES_B64_R0011',finding='Incomplete You truly was left alone on the first row.',correction='The first row now contains the complete predicate You truly are the king; the geographic complement continues naturally.'),
            dict(id='DK4_MES_B63_R0022',finding='The short tag don\'t you? was split between rows.',correction='The complete tag remains together through automatic phrase preferences.'),
            dict(id='DK4_MES_B67_R0238',finding='The auxiliary He won\'t was separated from be easy by a page boundary.',correction='The complete final sentence begins on page2.'),
            dict(id='DK4_MES_B62_R0039',finding='The question was split after what.',correction='The complete question remains together after the opening Tell me... pause; short complete clauses are valid.')],
        all224_words_punctuation_names_macros_andprose_values_unchanged=True,
        full216_width_font_page_height_encoder_macro_guards_andbase_QA_preserved=True,
        original_QA_severity_counts=dict(issues),no_QA_warnings_errors_removed_orwaived=True,
        ordinary_complete_word_wraps_still_require_contextual_native_review=True,
        B64R63_iron_ship_word_boundary_remains_reviewable_complete_words_not_dropped_glyph_oridentity_error=True,
        automatic_plan_findings_not_actual_gameplay_corruption=True,
        controls_source_native_andlogical_checks_passed_without_new_runtime_defect=True,
        independent_native_English_page_glyph_bounds_pagination_direct_view_andstored_actual_release_gates_pending=True,
        new_credit=0,new_emulator_runs=0,no_ROM_registry_orledger_change=True,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [OLD,NEW,DOC,Path(__file__)]}))
    print(dict(changed_plans=len(changes),QA=dict(issues),pages=229,actual_wrap_findings=4,no_words_orprose_changed=True,native_page_review_pending=True))
