"""Bind directly viewed six native pages to a preserved manuscript successor; no formatting credit yet."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B47_B48_native_review_v8325')
PAGES=Path('work/analysis/Hodram_B47_B48_pages_v8324/six_complete_native_pages24_compiled_alignments_distinct_FE.json')
OLD=Path('translations/hodram_B47_B48_editorial_manuscript_v1.json')
DOC=Path('translations/hodram_B47_B48_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();pages,old=map(read,[PAGES,OLD]);planpath=Path(pages['plan']);plan=read(planpath)
    assert pages['manuscript_sha256']==plan['manuscript_sha256']==sha(OLD.read_bytes()) and pages['plan_sha256']==sha(planpath.read_bytes())
    sheet=pages['review_sheet'];assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    infos=[];rows=[];reviews=[]
    reasons={
        'DK4_MES_B47_R0006':'Complete one-row surprised/frustrated outburst; found it already stays together and the final Argh! is present. No early wrap or unsupported unfairness accusation.',
        'DK4_MES_B47_R0010':'Complete concise concession and shrug remain on one row, with both the rueful ellipsis and final period intact.',
        'DK4_MES_B47_R0013':'Retain the four-row automatic wrap after comparing subject/verb constraints. Keeping You have and have to indivisible forces a break after the before world and creates a weak-line-ending warning. The selected ordinary complete-word You / have boundary preserves the entire best in the world phrase, the complete final I won\'t settle for less! sentence, all source meaning and one readable four-row page. No glyph or word is split. This is a reviewed paragraph layout choice, not a global rule change, shortened prose or warning waiver.',
        'DK4_MES_B48_R0006':'Complete original FE notice uses two rows at the measured usable width. Lil Argot and appears to have found remain clear; Ullr\'s Bow! stays intact on the second row. Both logical and physical native planes were checked; actual palette/geometry/transition still need a scene capture.',
        'DK4_MES_B48_R0011':'Complete playful taunt remains on one row with the real FI expanded to Hodram, including the final name and exclamation. No invented title for さん or literal singing claim.',
        'DK4_MES_B48_R0014':'Complete conditional instruction stays on one row, with wait in Amsterdam intact and the final period visible. It does not reverse the direction of waiting.',
    }
    for original,p,n in zip(old['records'],plan['records'],pages['records'],strict=True):
        assert original['id']==p['id']==n['id'] and original['english']==n['logical_English']==' '.join(p['lines']) and len(n['pages'])==1 and not original['review']['formatting']
        for page in n['pages']:
            for key in ['native_plane','preview']:
                assert sha(Path(page[key]).read_bytes())==page[key+'_sha256']
            if 'physical_plane' in page:assert sha(Path(page['physical_plane']).read_bytes())==page['physical_plane_sha256']
        for issue in p['base_QA']['issues']:
            assert issue['severity']=='info';infos.append(dict(id=original['id'],issue=issue))
        row=deepcopy(original);row.update(compiled_hex=p['encoded_hex'],compiled_bytes=len(bytes.fromhex(p['encoded_hex'])),formatted_markup=p['formatted_markup'],planned_English_markup=p['planning_record']['english'],generated_lines=p['lines'],expected_native_pages=1,
            qa_waivers=[],qa_waiver_scope=[],native_body_review_reason=reasons[row['id']],native_body_review_proof=str(PAGES),native_body_review_proof_sha256=sha(PAGES.read_bytes()),
            compiled_native_body_review=deepcopy(n),all_stored_controls_actual_effects_headers_FE_geometry_policy_andregistered_release_pending=True)
        assert row['english']==original['english'] and row['review']==original['review'];rows.append(row);reviews.append(dict(id=row['id'],reason=reasons[row['id']],generated_lines=p['lines'],compiled_hex=p['encoded_hex']))
    assert len(rows)==6 and len(infos)==6;ROOT.mkdir(parents=True);doc=deepcopy(old);doc.update(records=rows,native_body_review=str(ROOT/'six_native_pages_directly_viewed_no_warning_waivers.json'),native_body_pages=str(PAGES),native_body_pages_sha256=sha(PAGES.read_bytes()),
        predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),all_six_complete_native_body_pages_directly_viewed=True,all_six_formatting_gates_still_false=True,compiled_plan=str(planpath),compiled_plan_sha256=sha(planpath.read_bytes()),
        status='contextual-prose-andcompiled-native-body-reviewed-stored-effects-actual-policy-release-pending')
    save(DOC,doc)
    save(ROOT/'six_native_pages_directly_viewed_no_warning_waivers.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),pages=str(PAGES),pages_sha256=sha(PAGES.read_bytes()),
        directly_viewed_sheet=sheet,all_six_complete_bodies_visually_read=True,individual_body_reviews=reviews,original_warnings=[],original_infos=infos,original_diagnostics_not_suppressed=True,no_qa_warning_waivers=True,
        read_only_phrase_comparison='scripts/compare_Hodram_outcome_wrap_v8323a.py',subject_verb_andinfinitive_constraint_alternative_would_end_line3_with_the=True,
        no_manual_prose_break_shortening_width_font_or_global_rule_change=True,all_six_formatting_gates_remain_false=True,body_preview_not_actual_names_scene_FE_geometry_palette_orconditional_coverage=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [OLD,PAGES,planpath,Path('scripts/compare_Hodram_outcome_wrap_v8323a.py'),Path(__file__)]}))
    print('Six native bodies directly viewed/no warnings orwaivers/six original infos;manuscriptv2 binds exactcompiled bytes.Fivegate formatting approval still pending actual/stored/effects.')
