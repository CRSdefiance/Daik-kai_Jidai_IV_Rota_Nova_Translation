"""Bind26 reviewed native-font previews and condition4/5 consumer guards."""
import ast
from pathlib import Path
from copy import deepcopy
from dk4tool.patch import physical_wounds_editorial as parent
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_physical_fatigue_native_v961 import rendered
from scripts.prepare_illness_critical_prose_v972 import MANUSCRIPT,IDS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/illness_critical_v975')
PRODUCTION=Path('translations/illness_critical_editorial_manuscript_v2.json')

SOURCE_GATES='''    cases=context['all150_original_direct_main_battle_and_ordinary_condition4_5_selections'];assert len(cases)==150
    assert context['source_condition_IDs']==[4,5] and context['condition4_selects_critical_sounding1820_1832_not_illness1807_1819'] and context['condition5_selects_illness1807_1819']
    assert context['four_genuine_protagonists_and21_NPCs_no_ID_substitution'] and context['job_role_and_mood_getters_not_called']
    assert {r['selected_message_ID'] for r in cases}==set(IDS)
    labels=('direct_physical_helper','main_battle_status_priority','main_ordinary_status_priority')
    assert {(r['actor_ID'],r['case'],r['isolated_CPU_condition']) for r in cases}=={(n,label,status) for n in range(25) for label in labels for status in (4,5)}
    for r in cases:
        status=r['isolated_CPU_condition'];nfirst,hfirst,sera=(1820,1828,1832) if status==4 else (1807,1815,1819)
        expected=sera if r['actor_ID']==24 else hfirst+r['actor_ID'] if r['actor_ID']<4 else nfirst+r['native_voice_class']
        assert r['selected_message_ID']==expected and r['source_condition_byte_offset']==6
        assert r['job_role_and_mood_getters_not_called'] and r['original_native_selector_and_callee_saved_ABI_pass']
        assert r['only_declared_CPU_condition_and_mode_fields_changed'] and r['actor_other31_bytes_and_all_other_source_RAM_preserved']
        assert r['isolated_CPU_mode_fields8_12']==([0,0] if r['case']=='main_ordinary_status_priority' else [0,1])
    controls=context['all100_prior_condition0_1_2_3_discriminating_controls'];assert len(controls)==100
    assert {(r['actor_ID'],r['isolated_CPU_condition']) for r in controls}=={(n,status) for n in range(25) for status in (0,1,2,3)}
    for r in controls:
        status=r['isolated_CPU_condition']
        expected=None if status==0 else (1793 if r['actor_ID']==24 else 1789+r['actor_ID'] if r['actor_ID']<4 else 1781+r['native_voice_class']) if status==1 else (1806 if r['actor_ID']==24 else 1802+r['actor_ID'] if r['actor_ID']<4 else 1794+r['native_voice_class'])
        assert r['selected_message_ID']==expected and r['original_native_selector_and_callee_saved_ABI_pass']
        assert r['only_declared_CPU_condition_and_mode_fields_changed'] and r['actor_other31_bytes_and_all_other_source_RAM_preserved']
    assert fonts['manuscript_sha256']==sha(draft.read_bytes()) and len(fonts['cases'])==26 and fonts['complete_native_font_cases']==52
    assert visual['native_font_proof_sha256']==sha(Path(doc['native_font_proof']).read_bytes())
    assert visual['all26_previews_visually_reviewed'] and not visual['visual_review_pending']
    assert fonts['all26_source_numeric_selection_complete_ABI_words_and_visible_ink_pass'] and fonts['ordinary_and_battle_each_condition4_5_control_equal']
    assert fonts['four_original_actual_captain_states_used_no_captain_ID_substitution'] and fonts['Sera24_special1819_1832_included']
    for row,case in zip(doc['records'],fonts['cases'],strict=True):
        assert row['message_id']==case['message_id'] and case['physical_condition_ID']==row['physical_condition_ID']==(5 if row['message_id']<1820 else 4)
        assert case['all_body_ink_inside_registered216x36_crop'] and case['both_original_selectors_full_canvas_and_words_equal']
        variants=case['ordinary_and_battle_font_controls'];assert [v['mode'] for v in variants]==['ordinary','battle']
        for v in variants:
            assert compiled(row).hex()==v['text_hex'] and v['physical_condition_fixture']['CPU_condition']==row['physical_condition_ID']
            assert v['physical_condition_fixture']['other31_actor_bytes_and_all_other_CPU_RAM_exact']
            for gate in ('complete_native_copy_macro_draw_and_ABI','full252x96_native_and_independent_canvas_equal',
                'independent_authored_words_at_x0_12px_rows_match_every_pixel','bitmap_and_input_guards_exact','original_physical_selector_selected_condition4_5_message'):assert v[gate]
'''

SUPPLEMENT_GATES='''    assert supplement['candidate_sha256']==doc['current_ROM_sha256'] and supplement['source_condition4_is_critical_dialogue_and5_is_illness']
    assert supplement['physical_status_precedes_job_mood_and_battle_work'] and supplement['independent_alternatives_not_consecutive_dialogue']
    assert supplement['no_IC_native_macro_in_selected_Japanese'] and len(supplement['all26_source_IC_macros'])==26 and all(r['IC_count']==0 for r in supplement['all26_source_IC_macros'])
    assert supplement['literal_Japanese_first_person_preserved_as_natural_English'] and supplement['independent1821_and1822_no_cross_message_contraction']
    assert supplement['obsolete_full_width_I_entries']==[1810,1824,1830] and supplement['approved_Camille_decision']['localized_first_name']=='Camille'
    assert supplement['source1816_personal_admiral_responsibility_preserved'] and supplement['source1828_dream1829_strongest_fleet1830_Camille1832_personal_wish_preserved']
    assert supplement['cure_boasts_and_death_fears_are_character_speech_not_measured_game_outcomes']
'''


def main():
    packet=read('work/analysis/illness_critical_v971/source_context_packet.json')
    s,t,b,text=rendered('dk4tool/patch/physical_wounds_editorial.py','dk4tool/patch/illness_critical_editorial.py',[
        ('Complete13 physical-condition2/3 wound','Complete26 physical-condition4/5 illness and near-death'),('physical_wounds','illness_critical'),
        ('from dk4tool.patch.physical_fatigue_editorial import current_entries as previous_entries','from dk4tool.patch.physical_wounds_editorial import current_entries as previous_entries'),
        ('illness_critical_layout_v968b','illness_critical_layout_v974'),('range(1794,1807)','range(1807,1833)'),
        (parent.SOURCE_COMMON,packet['COMMON_sha256']),(parent.SOURCE_ARM,packet['ARM9_sha256']),
        ('deck-physical-wounds-visible-v1','deck-illness-critical-visible-v1'),('dk4-physical-wounds-editorial-v1','dk4-illness-critical-editorial-v1'),
        ("row['physical_condition_IDs']==[2,3]","row['physical_condition_ID'] in (4,5)"),('all3655_other_message_strings_exact','all3642_other_message_strings_exact')])
    start=text.index("    cases=context[");end=text.index('    c,a,proof=plan',start);text=text[:start]+SOURCE_GATES+text[end:]
    start=text.index("    assert supplement['candidate_sha256']");end=text.index('    for name,digest in supplement',start);text=text[:start]+SUPPLEMENT_GATES+text[end:]
    text=text.replace("len(audit['records'])==13","len(audit['records'])==26");ast.parse(text);module=(s,t,b,text)
    audit=rendered('scripts/audit_physical_fatigue_native_v962.py','scripts/audit_illness_critical_native_v975.py',[
        ('physical_fatigue','illness_critical'),('illness_critical_layout_v960','illness_critical_layout_v974'),('probe_illness_critical_fonts_v960','probe_illness_critical_fonts_v974'),
        ('deck-physical-fatigue-visible-v1','deck-illness-critical-visible-v1'),('all75_original_direct_main_battle_and_ordinary_fatigue_selections','all150_original_direct_main_battle_and_ordinary_condition4_5_selections'),('==75','==150'),
        ("len(context['all25_healthy_direct_helper_no_message_controls'])==25 and context['job_role_and_mood_not_queried_in_physical_status_branch']","len(context['all100_prior_condition0_1_2_3_discriminating_controls'])==100 and context['job_role_and_mood_getters_not_called']"),
        ('all13_previews_visually_reviewed','all26_previews_visually_reviewed'),('all13_native_previews_visually_reviewed','all26_native_previews_visually_reviewed'),('==13','==26'),
        ("case['physical_condition_ID']==1","case['physical_condition_ID']==row['physical_condition_ID']"),('original_physical_selector_selected_condition1_message','original_physical_selector_selected_condition4_5_message'),
        ('Physical fatigue native-consumer audit','Illness and near-death native-consumer audit'),('13 records;zero','26 records;zero'),('Native fatigue audit:all13','Native illness/near-death audit:all26')])
    ROOT.mkdir(parents=True,exist_ok=True);font_path=Path('work/analysis/illness_critical_v974/native_font_proof.json');fonts=read(font_path)
    assert fonts['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and tuple(c['message_id'] for c in fonts['cases'])==IDS
    for case in fonts['cases']:assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
    visual=font_path.parent/'visual_review.json';assert not visual.exists() and not PRODUCTION.exists()
    save(visual,{'native_font_proof':str(font_path),'native_font_proof_sha256':sha(font_path.read_bytes()),'review_sheet':fonts['review_sheet'],'review_sheet_sha256':fonts['review_sheet_sha256'],
        'all26_previews_visually_reviewed':True,'native_IDs':list(IDS),'visual_review_pending':False,
        'findings':'All26 original-font previews reviewed in both ordinary/battle controls. Complete ASCII I1810/1824/1830,independent Here1821 and I cant die yet1822,all of Camille1830,and Seras opening hesitation1832 are intact. Long1811 uses three rows with Well attached to the answer and a full36cell last row. Personal admiral1816 uses three rows. Appetite1813,retained1818 and Rafael1828 continuation fill36cells. All rows start at x0,with complete punctuation and no manual alignment,stray words,gaps,or overflow. The prior soft clause layout is retained. Actual RGB panels and normal returns remain required.',
        'CPU_only_font_scope_no_actual_gameplay_credit':True,'full_goal_complete':False})
    doc=deepcopy(read(MANUSCRIPT));doc.update(reviewed_research_manuscript=str(MANUSCRIPT),reviewed_research_manuscript_sha256=sha(MANUSCRIPT.read_bytes()),formatting_review_pending=False,
        review_gates=['source','context','localization','naturalness','formatting'],status='26-source-prose-native-font-and-visual-reviewed-registered-release-and-actual-pending')
    for key,path in [('native_font_proof',font_path),('visual_review_proof',visual)]:doc[key]=str(path);doc[key+'_sha256']=sha(path.read_bytes())
    for row in doc['records']:row['review']['formatting']=True
    save(PRODUCTION,doc);provenance=[]
    for source,target,raw,text in (module,audit):
        with target.open('x',encoding='utf-8') as f:f.write(text)
        assert source.read_bytes()==raw
        provenance.append({'source':str(source),'source_before_sha256':sha(raw),'source_after_sha256':sha(source.read_bytes()),'source_unchanged':True,'successor':str(target),'successor_sha256':sha(target.read_bytes())})
    save(ROOT/'native_successor_provenance.json',{'files':provenance,'all_source_hashes_unchanged':True,'all_successor_replacements_preflighted_before_output':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('26 original-font previews reviewed;production manuscript and guarded condition4/5 module/auditor created.',flush=True)


if __name__=='__main__':main()
