"""Bind reviewed wound previews and guarded native-consumer successors."""
import ast
from pathlib import Path
from copy import deepcopy
from dk4tool.patch import physical_fatigue_editorial as parent
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_physical_fatigue_native_v961 import rendered
from scripts.prepare_physical_wounds_prose_v966 import MANUSCRIPT,IDS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/physical_wounds_v969')
PRODUCTION=Path('translations/physical_wounds_editorial_manuscript_v2.json')

SOURCE_GATES='''    cases=context['all150_original_direct_main_battle_and_ordinary_wound_selections'];assert len(cases)==150
    assert context['source_condition_IDs']==[2,3] and context['Sera24_special_ID']==1806
    assert context['condition2_3_wound_NPC_IDs']==list(range(1794,1802)) and context['condition2_3_genuine_protagonist_IDs']==list(range(1802,1806))
    assert context['four_genuine_protagonists_and21_NPCs_no_ID_substitution'] and context['job_role_and_mood_getters_not_called']
    assert {r['selected_message_ID'] for r in cases}==set(IDS) and {r['actor_ID'] for r in cases}==set(range(25))
    assert {r['isolated_CPU_condition'] for r in cases}=={2,3}
    for r in cases:
        assert r['source_condition_byte_offset']==6 and r['job_role_and_mood_getters_not_called']
        assert r['original_native_selector_and_callee_saved_ABI_pass'] and r['only_declared_CPU_condition_and_mode_fields_changed']
        assert r['actor_other31_bytes_and_all_other_source_RAM_preserved']
        expected=1806 if r['actor_ID']==24 else 1802+r['actor_ID'] if r['actor_ID']<4 else 1794+r['native_voice_class']
        assert r['selected_message_ID']==expected
        assert r['isolated_CPU_mode_fields8_12']==([0,0] if r['case']=='main_ordinary_status_priority' else [0,1])
    healthy=context['all25_healthy_direct_helper_no_message_controls'];fatigue=context['all25_condition1_prior_fatigue_discriminating_controls']
    assert len(healthy)==len(fatigue)==25 and {r['actor_ID'] for r in healthy}=={r['actor_ID'] for r in fatigue}==set(range(25))
    assert all(r['isolated_CPU_condition']==0 and r['selected_message_ID'] is None and r['original_native_selector_and_callee_saved_ABI_pass'] for r in healthy)
    for r in fatigue:
        expected=1793 if r['actor_ID']==24 else 1789+r['actor_ID'] if r['actor_ID']<4 else 1781+r['native_voice_class']
        assert r['isolated_CPU_condition']==1 and r['selected_message_ID']==expected and r['original_native_selector_and_callee_saved_ABI_pass']
    assert fonts['manuscript_sha256']==sha(draft.read_bytes()) and len(fonts['cases'])==13 and fonts['complete_native_font_cases']==52
    assert visual['native_font_proof_sha256']==sha(Path(doc['native_font_proof']).read_bytes())
    assert visual['all13_previews_visually_reviewed'] and not visual['visual_review_pending']
    assert fonts['all13_source_numeric_selection_complete_ABI_words_and_visible_ink_pass'] and fonts['ordinary_and_battle_both_condition2_3_controls_equal']
    assert fonts['four_original_actual_captain_states_used_no_captain_ID_substitution'] and fonts['Sera24_special1806_included']
    for row,case in zip(doc['records'],fonts['cases'],strict=True):
        assert row['message_id']==case['message_id'] and case['physical_condition_IDs']==row['physical_condition_IDs']==[2,3]
        assert case['all_body_ink_inside_registered216x36_crop'] and case['all_four_original_selectors_full_canvas_and_words_equal']
        variants=case['condition2_3_ordinary_and_battle_font_controls'];assert [v['mode'] for v in variants]==['ordinary_condition2','battle_condition2','ordinary_condition3','battle_condition3']
        for v in variants:
            assert compiled(row).hex()==v['text_hex'] and v['physical_condition_fixture']['CPU_condition'] in (2,3)
            assert v['physical_condition_fixture']['other31_actor_bytes_and_all_other_CPU_RAM_exact']
            for gate in ('complete_native_copy_macro_draw_and_ABI','full252x96_native_and_independent_canvas_equal',
                'independent_authored_words_at_x0_12px_rows_match_every_pixel','bitmap_and_input_guards_exact','original_physical_selector_selected_condition2_3_message'):assert v[gate]
'''

SUPPLEMENT_GATES='''    assert supplement['candidate_sha256']==doc['current_ROM_sha256']
    assert supplement['source_condition2_and3_share_these_dialogue_alternatives'] and supplement['other_condition_effects_not_claimed_identical']
    assert supplement['physical_status_precedes_job_mood_and_battle_work'] and supplement['independent_alternatives_not_consecutive_dialogue']
    assert supplement['no_IC_native_macro_in_selected_Japanese'] and all(r['IC_count']==0 for r in supplement['all13_source_IC_macros'])
    assert supplement['literal_Japanese_first_person_preserved_as_natural_English'] and supplement['source1802_But_I_and1797_unfinished_clause_preserved']
    assert supplement['source1804_personal_pain_and_admiral_responsibility_preserved'] and supplement['source1798_spit_remedy_is_character_speech']
'''


def main():
    packet=read('work/analysis/physical_wounds_v965/source_context_packet.json')
    s,t,b,text=rendered('dk4tool/patch/physical_fatigue_editorial.py','dk4tool/patch/physical_wounds_editorial.py',[
        ('physical-condition1 fatigue','physical-condition2/3 wound'),('physical_fatigue','physical_wounds'),
        ('from dk4tool.patch.battle_gunnery_deck_editorial import current_entries as previous_entries','from dk4tool.patch.physical_fatigue_editorial import current_entries as previous_entries'),
        ('physical_wounds_layout_v960','physical_wounds_layout_v968b'),('range(1781,1794)','range(1794,1807)'),
        (parent.SOURCE_COMMON,packet['COMMON_sha256']),(parent.SOURCE_ARM,packet['ARM9_sha256']),
        ('deck-physical-fatigue-visible-v1','deck-physical-wounds-visible-v1'),('dk4-physical-fatigue-editorial-v1','dk4-physical-wounds-editorial-v1'),
        ("row['source_native_macros']==(['IC'] if n==1783 else [])","row['source_native_macros']==[]"),
        ("row['physical_condition_ID']==1","row['physical_condition_IDs']==[2,3]")])
    start=text.index("    cases=context[");end=text.index('    c,a,proof=plan',start);text=text[:start]+SOURCE_GATES+text[end:]
    start=text.index("    assert supplement['candidate_sha256']");end=text.index("    for name,digest in supplement",start);text=text[:start]+SUPPLEMENT_GATES+text[end:]
    ast.parse(text);module=(s,t,b,text)
    audit=rendered('scripts/audit_physical_fatigue_native_v962.py','scripts/audit_physical_wounds_native_v969.py',[
        ('physical_fatigue','physical_wounds'),('physical_wounds_layout_v960','physical_wounds_layout_v968b'),('probe_physical_wounds_fonts_v960','probe_physical_wounds_fonts_v968b'),
        ('deck-physical-fatigue-visible-v1','deck-physical-wounds-visible-v1'),('all75_original_direct_main_battle_and_ordinary_fatigue_selections','all150_original_direct_main_battle_and_ordinary_wound_selections'),('==75','==150'),
        ("context['job_role_and_mood_not_queried_in_physical_status_branch']","context['job_role_and_mood_getters_not_called'] and len(context['all25_condition1_prior_fatigue_discriminating_controls'])==25"),
        ("case['physical_condition_ID']==1","case['physical_condition_IDs']==[2,3]"),('both_original_selectors_full_canvas_and_words_equal','all_four_original_selectors_full_canvas_and_words_equal'),
        ('ordinary_and_battle_font_controls','condition2_3_ordinary_and_battle_font_controls'),('original_physical_selector_selected_condition1_message','original_physical_selector_selected_condition2_3_message'),('Physical fatigue native-consumer audit','Physical wound native-consumer audit'),('Native fatigue audit','Native wound audit')])
    ROOT.mkdir(parents=True,exist_ok=True);font_path=Path('work/analysis/physical_wounds_v968b/native_font_proof.json');fonts=read(font_path)
    assert fonts['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and tuple(c['message_id'] for c in fonts['cases'])==IDS
    for case in fonts['cases']:assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
    visual=font_path.parent/'visual_review.json';assert not visual.exists() and not PRODUCTION.exists()
    save(visual,{'native_font_proof':str(font_path),'native_font_proof_sha256':sha(font_path.read_bytes()),'review_sheet':fonts['review_sheet'],'review_sheet_sha256':fonts['review_sheet_sha256'],
        'all13_previews_visually_reviewed':True,'native_IDs':list(IDS),'visual_review_pending':False,
        'findings':'All13 complete original-font previews and four condition/mode variants reviewed. Initial I1796/1799/1800,Lils personal admiral1804,Rafaels full35cell But I1802,and brief Sera1806 are intact. Maria1805 wraps after Dont worry,keeping about a little wound like this together;the prior soft-hint versions are retained without claiming improved layout. Complete native rows start at x0 with no manual padding,gaps,word splits,missing edge glyphs,overflow or extra pages. Actual RGB scenes and normal returns remain required.',
        'CPU_only_font_scope_no_actual_gameplay_credit':True,'full_goal_complete':False})
    doc=deepcopy(read(MANUSCRIPT));doc.update(reviewed_research_manuscript=str(MANUSCRIPT),reviewed_research_manuscript_sha256=sha(MANUSCRIPT.read_bytes()),formatting_review_pending=False,
        review_gates=['source','context','localization','naturalness','formatting'],status='13-source-prose-native-font-and-visual-reviewed-registered-release-and-actual-pending')
    for key,path in [('native_font_proof',font_path),('visual_review_proof',visual)]:doc[key]=str(path);doc[key+'_sha256']=sha(path.read_bytes())
    for row in doc['records']:row['review']['formatting']=True
    save(PRODUCTION,doc);provenance=[]
    for source,target,raw,text in (module,audit):
        with target.open('x',encoding='utf-8') as f:f.write(text)
        assert source.read_bytes()==raw
        provenance.append({'source':str(source),'source_before_sha256':sha(raw),'source_after_sha256':sha(source.read_bytes()),'source_unchanged':True,'successor':str(target),'successor_sha256':sha(target.read_bytes())})
    save(ROOT/'native_successor_provenance.json',{'files':provenance,'all_source_hashes_unchanged':True,'all_successor_replacements_preflighted_before_output':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('13 wound previews reviewed;production manuscript and strict wound module/auditor created.',flush=True)


if __name__=='__main__':main()
