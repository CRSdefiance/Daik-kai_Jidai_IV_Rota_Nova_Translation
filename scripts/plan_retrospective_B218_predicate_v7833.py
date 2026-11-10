"""Propose one automatic soft-wrap refinement; every English word stays unchanged."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from types import FunctionType
import inspect
from dk4tool.dialogue import qa
from dk4tool.dialogue.encoder import RelocatableDialogueEncoding
from dk4tool.dialogue.layout import DialogueDiagnostic
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.lil_B218_profile_v1 import contract
from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_lil_B218_layout_v6881c as inherited
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retrospective_B218_predicate_plan_v7833')
GLOSS=Path('work/analysis/retrospective_B218_wrap_gloss_v7832/thirteen_fresh_clean_exchange_glosses_before_full_current_layout_review.json')
LEADS=Path('work/analysis/completed_contraction_wrap_leads_v7831/completed_layout_contraction_andquestion_tag_leads_with_live_storage_refs.json')
FINAL=Path('translations/lil_B218_contextual_final_review_v1.json')
DRAFT=Path('translations/lil_B218_retrospective_layout_manuscript_v1.json')
TARGET='DK4_MES_B218_R0027'
REASONS={
5:"Retain the polite report about town information; it opens the companion's enthusiasm without adding a location.",
8:"Retain Lil's skeptical but interested response and direct question; coming from this companion is her reason to take the description seriously.",
11:"Retain the item name and explicit they-say attribution, including Ares as one of the twelve Olympian gods.",
14:"Retain Lil's unfamiliarity with Ares and practical request for where to obtain the spear.",
17:"Retain may and rumor attribution for nearby armor; neither a guaranteed reward nor a precise place is asserted.",
20:"Retain the short impatient question, which contrasts with the companion's indirect explanation.",
23:"Retain suspect/nearby and the townspeople source, followed by the companion's strong wish to find it; whatever it takes reflects his determination.",
27:"Retain the complete parenthetical and its two short sentences: Lil privately finds Ian's interest surprising. Keep That's a surprise together automatically so the short predicate reads as a thought.",
30:"Retain his noticing Lil's expression and asking whether his interest in legends surprises her; it follows her aside naturally.",
34:"Retain Lil's personal impression that weapons do not suit him, without inventing incompetence or a new profession.",
37:"Retain his concession and reflective explanation about the mystery of mythic gods roaming the land; this is his fascination, not a demonstrated game effect.",
40:"Retain the imaginative response, may-have-used uncertainty and thoughts returning to antiquity.",
43:"Retain Lil's hesitant lack of understanding; the exchange closes without giving her his enthusiasm.",
}
if __name__=='__main__':
    assert not ROOT.exists() and not DRAFT.exists()
    gloss,leads,final=map(read,[GLOSS,LEADS,FINAL]);bindings=contract()['record_bindings']
    source={r['id']:r for r in gloss['records']}
    assert len(source)==len(final['records'])==13 and gloss['whole_exchange_read']
    selected=next(r for r in leads['leads'] if r['id']==TARGET and r['file_path']=='/data/SC2.DK4')
    assert selected['current_raw_body_has_no_catalogue_override'] and selected['compiled_equals_current_body_except_possible_one_zero_ink_storage_space']
    # Restrict this ordinary boundary preference to one source-bound paragraph.
    pairs=inherited.PAIRS|{("that's","a")}
    bound=FunctionType(inherited.plan.__code__,{**inherited.plan.__globals__,'PAIRS':pairs},argdefs=inherited.plan.__defaults__)
    rows=[];plans=[];changed=[]
    for old in final['records']:
        ident=old['id'];b=bindings[ident];planning=deepcopy(b['planning_record'])
        assert planning['english']==old['english'] and planning['source_hex']==source[ident]['source_hex']
        previous=inherited.plan(planning);assert previous['encoded_hex']==b['compiled_hex']==old['compiled_hex']
        current=bound(planning) if ident==TARGET else previous
        assert ' '.join(previous['lines'])==' '.join(current['lines'])
        assert current['expected_native_pages']==1 and current['max_total_rows']==4
        if previous['encoded_hex']!=current['encoded_hex']:changed.append(ident)
        profile=replace(get_dialogue_profile('lil-opening-editorial-native-v1'),name='B218-retrospective-predicate-research:'+ident,
            max_lines=4,leading_speaker_bytes=frozenset([2,21]))
        def encoded(raw,text,prof):
            assert raw.hex()==planning['source_hex'] and text==planning['english'] and prof==profile
            return RelocatableDialogueEncoding(current['formatted_markup'],bytes.fromhex(current['encoded_hex']),
                tuple(DialogueDiagnostic(**d) for d in current['diagnostics']))
        audit=FunctionType(qa.audit_relocatable_dialogue_record.__code__,{**qa.audit_relocatable_dialogue_record.__globals__,
            'encode_relocatable_dialogue':encoded},argdefs=qa.audit_relocatable_dialogue_record.__defaults__)
        report=audit(bytes.fromhex(planning['source_hex']),planning['english'],profile)
        assert not any(i['severity'] in ['warning','error'] for i in report['issues'])
        row=deepcopy(old)
        row.update(fresh_retrospective_source_context=deepcopy(source[ident]),
            retrospective_wording_decision='retain-wording',retrospective_wording_reason=REASONS[old['source_record_index']],
            retrospective_layout_decision='revise-automatic-soft-wrap' if ident==TARGET else 'retain-exact-compiled-plan',
            previous_final_review=str(FINAL),previous_final_review_sha256=sha(FINAL.read_bytes()),
            previous_approved_compiled_hex=old['compiled_hex'],proposed_compiled_hex=current['encoded_hex'],
            proposed_formatted_markup=current['formatted_markup'],proposed_automatic_lines=current['lines'],
            proposed_base_QA=report,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=ident!=TARGET),
            proposed_changed_native_storage_actual_policy_andregistered_release_pending=ident==TARGET,
            no_new_source_prose_orcompletion_credit=True)
        rows.append(row);plans.append(dict(id=ident,previous=previous,proposed=current,base_QA=report,
            exact_previous_compiled_plan_reused=ident!=TARGET,
            independent_new_native_font_storage_actual_andrelease_approval_not_claimed=ident==TARGET))
    assert changed==[TARGET]
    target=next(p for p in plans if p['id']==TARGET)
    assert target['proposed']['lines']==["(Ian's interested?","That's a surprise.)"]
    ROOT.mkdir(parents=True)
    save(DRAFT,dict(format='dk4-retrospective-dialogue-layout-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        file_path='/data/SC2.DK4',block=218,current_ROM=leads['candidate'],current_ROM_sha256=leads['candidate_sha256'],
        records=rows,all13_complete_clean_andcurrent_exchanges_read=True,
        complete_exchange_cadence_andemotional_progression_preserved=True,
        wording_retentions=13,proposed_automatic_layout_revisions=1,unchanged_exact_compiled_plans=12,
        source_controls_selectors_andzero_macros_preserved=True,
        no_authored_line_breaks_padding_alignment_shortening_width_orfont_change=True,
        proposed_formatting_native_storage_actual_policy_release_pending=True,
        no_new_completion_orintegrated_revision_counter_credit=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [GLOSS,LEADS,FINAL,Path(inherited.__file__),Path(__file__)]},full_goal_complete=False))
    save(ROOT/'one_changed_automatic_plan12_exact_reuses_all13_unmodified_base_QA.json',dict(
        manuscript=str(DRAFT),manuscript_sha256=sha(DRAFT.read_bytes()),records=plans,changed_IDs=changed,
        source_owned_original_planner=inspect.getsource(inherited.plan),
        original_pairs=sorted(inherited.PAIRS),scoped_target_pair=["that's","a"],
        preference_applied_only_to_exact_target_ID=True,all13_base_QA_without_warning_removal_orwaivers=True,
        no_new_native_oractual_display_checks_claimed=True,new_credit=0,full_goal_complete=False))
    print('B218 R27 proposed:',target['previous']['lines'],'->',target['proposed']['lines'])
    print('All13 words/meanings retained;one automatic wrap change/12exact compiled reuses.All13 baseQA pass.Native/storage/actual/policy/release pending.No credit.')
