"""Bind39 complete native previews and exact original mood-consumer guards."""
import ast
from pathlib import Path
from copy import deepcopy
from dk4tool.patch import illness_critical_editorial as parent
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_physical_fatigue_native_v961 import rendered
from scripts.prepare_mood_comments_prose_v978 import MANUSCRIPT,IDS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/mood_comments_v981')
PRODUCTION=Path('translations/mood_comments_editorial_manuscript_v2.json')

SOURCE_GATES='''    cases=context['all225_original_direct_main_battle_and_ordinary_mood_selections'];assert len(cases)==225
    assert context['source_mood_IDs']==[0,4,5] and context['source_physical_condition0_required_for_mood_selection']
    assert context['four_genuine_protagonists_and21_NPCs_no_ID_replacement'] and context['Sera_normal_mood1_2_3_direct_helper_not_executed']
    assert {r['selected_message_ID'] for r in cases}==set(IDS)
    labels=('direct_mood_helper','main_battle_mood_priority','main_ordinary_mood_priority')
    assert {(r['actor_ID'],r['case'],r['isolated_CPU_mood']) for r in cases}=={(n,label,mood) for n in range(25) for label in labels for mood in (0,4,5)}
    for r in cases:
        mood=r['isolated_CPU_mood'];nfirst,hfirst,sera={0:(1833,1841,1845),4:(1846,1854,1858),5:(1859,1867,1871)}[mood]
        expected=sera if r['actor_ID']==24 else hfirst+r['actor_ID'] if r['actor_ID']<4 else nfirst+r['native_voice_class']
        assert r['isolated_CPU_condition']==0 and r['selected_message_ID']==expected
        assert r['source_condition_byte_offset']==6 and r['source_mood_byte_offset']==7 and r['source_mood_getter_calls']>0
        assert r['job_role_getter_not_called'] and r['original_selector_and_callee_saved_ABI_pass']
        assert r['only_declared_condition_mood_and_mode_fields_change'] and r['other30_actor_bytes_and_all_other_source_RAM_exact']
        assert r['isolated_CPU_mode_fields8_12']==([0,0] if r['case']=='main_ordinary_mood_priority' else [0,1])
    priority=context['all75_physical_condition1_priority_controls'];assert len(priority)==75
    assert {(r['actor_ID'],r['isolated_CPU_mood']) for r in priority}=={(n,mood) for n in range(25) for mood in (0,4,5)}
    for r in priority:
        expected=1793 if r['actor_ID']==24 else 1789+r['actor_ID'] if r['actor_ID']<4 else 1781+r['native_voice_class']
        assert r['isolated_CPU_condition']==1 and r['selected_message_ID']==expected and r['source_mood_getter_calls']==0 and r['physical_priority_bypasses_mood_getter']
        assert r['original_selector_and_callee_saved_ABI_pass'] and r['job_role_getter_not_called']
    normal=context['all72_direct_NPC_hero_normal_mood1_2_3_no_message_controls'];assert len(normal)==72
    assert {(r['actor_ID'],r['isolated_CPU_mood']) for r in normal}=={(n,mood) for n in range(24) for mood in (1,2,3)}
    assert all(r['selected_message_ID'] is None and r['isolated_CPU_condition']==0 and r['original_selector_and_callee_saved_ABI_pass'] for r in normal)
    assert fonts['manuscript_sha256']==sha(draft.read_bytes()) and len(fonts['cases'])==39 and fonts['complete_native_font_cases']==78
    assert visual['native_font_proof_sha256']==sha(Path(doc['native_font_proof']).read_bytes()) and visual['all39_previews_visually_reviewed'] and not visual['visual_review_pending']
    assert fonts['all39_source_numeric_selection_complete_ABI_words_and_visible_ink_pass'] and fonts['ordinary_and_battle_each_mood0_4_5_controls_equal']
    assert fonts['four_original_actual_captain_states_used_no_captain_ID_substitution'] and fonts['Sera24_special1845_1858_1871_included']
    prior_path=Path(fonts['prior_native_font_proof']);assert sha(prior_path.read_bytes())==fonts['prior_native_font_proof_sha256']
    prior=read(prior_path);assert prior['candidate_sha256']==doc['current_ROM_sha256'] and prior['manuscript_sha256']==sha(draft.read_bytes())
    assert prior['producer_sha256']==sha(Path('scripts/probe_mood_comments_fonts_v979.py').read_bytes())
    assert fonts['preserved_byte_identical_native_font_cases']==76 and fonts['new_native_font_cases']==2 and fonts['only_changed_compiled_IDs']==[1853]
    for row,case,old in zip(doc['records'],fonts['cases'],prior['cases'],strict=True):
        n=row['message_id'];expected_mood=0 if n<1846 else 4 if n<1859 else 5
        assert n==case['message_id']==old['message_id'] and case['physical_condition_ID']==row['physical_condition_ID']==0 and case['mood_ID']==row['mood_ID']==expected_mood
        assert case['all_body_ink_inside_registered216x36_crop'] and case['both_original_selectors_full_canvas_and_words_equal']
        if n!=1853:
            for key,value in old.items():
                if key!='preview':assert case[key]==value
            assert all(v['text_hex']==compiled(row).hex() for v in old['ordinary_and_battle_font_controls'])
        else:assert case['case_origin']['reexecuted_for_changed_automatic_wrap']
        variants=case['ordinary_and_battle_font_controls'];assert [v['mode'] for v in variants]==['ordinary','battle']
        for v in variants:
            assert compiled(row).hex()==v['text_hex'] and v['mood_fixture']['CPU_mood']==expected_mood and v['mood_fixture']['physical_condition_preserved']==0
            assert v['mood_fixture']['other31_actor_bytes_and_all_other_CPU_RAM_exact']
            for gate in ('complete_native_copy_macro_draw_and_ABI','full252x96_native_and_independent_canvas_equal',
                'independent_authored_words_at_x0_12px_rows_match_every_pixel','bitmap_and_input_guards_exact','original_mood_selector_selected_expected_message'):assert v[gate]
'''

SUPPLEMENT_GATES='''    assert supplement['candidate_sha256']==doc['current_ROM_sha256'] and supplement['source_mood0_positive4_dejected5_panic']
    assert supplement['physical_condition0_required_and_condition1_preempts_mood'] and supplement['independent_alternatives_not_consecutive_dialogue']
    assert supplement['no_IC_native_macro_in_selected_Japanese'] and len(supplement['all39_source_IC_macros'])==39 and all(r['IC_count']==0 for r in supplement['all39_source_IC_macros'])
    assert supplement['literal_Japanese_first_person_preserved_as_natural_English'] and supplement['independent1843_1844_and1855_1856_not_split_words']
    assert supplement['obsolete_full_width_I_entries']==[1845,1846,1858] and supplement['nonverbal_English_equivalents']=={'1855':'...','1871':'@#$*!!'}
    assert supplement['no_spoken_words_added_to_silence_or_comic_symbols'] and supplement['source1868_and1870_are_personal_self_calming']
    assert supplement['Sera_direct_normal_moods_not_used_outside_original_contract']
'''


def main():
    packet=read('work/analysis/mood_comments_v977/source_context_packet.json')
    s,t,b,text=rendered('dk4tool/patch/illness_critical_editorial.py','dk4tool/patch/mood_comments_editorial.py',[
        ('Complete26 physical-condition4/5 illness and near-death','Complete39 mood0/4/5'),('illness_critical','mood_comments'),
        ('from dk4tool.patch.physical_wounds_editorial import current_entries as previous_entries','from dk4tool.patch.illness_critical_editorial import current_entries as previous_entries'),
        ('mood_comments_layout_v974','mood_comments_layout_v980'),('range(1807,1833)','range(1833,1872)'),
        (parent.SOURCE_COMMON,packet['COMMON_sha256']),(parent.SOURCE_ARM,packet['ARM9_sha256']),('deck-illness-critical-visible-v1','deck-mood-comments-visible-v1'),
        ('dk4-illness-critical-editorial-v1','dk4-mood-comments-editorial-v1'),("row['physical_condition_ID'] in (4,5)","row['physical_condition_ID']==0 and row['mood_ID'] in (0,4,5)"),
        ('all3642_other_message_strings_exact','all3629_other_message_strings_exact')])
    start=text.index("    cases=context[");end=text.index('    c,a,proof=plan',start);text=text[:start]+SOURCE_GATES+text[end:]
    start=text.index("    assert supplement['candidate_sha256']");end=text.index('    for name,digest in supplement',start);text=text[:start]+SUPPLEMENT_GATES+text[end:]
    text=text.replace("len(audit['records'])==26","len(audit['records'])==39");ast.parse(text);module=(s,t,b,text)
    audit=rendered('scripts/audit_illness_critical_native_v975.py','scripts/audit_mood_comments_native_v981.py',[
        ('illness_critical','mood_comments'),('mood_comments_layout_v974','mood_comments_layout_v980'),('probe_mood_comments_fonts_v974','probe_mood_comments_fonts_v980'),
        ('deck-illness-critical-visible-v1','deck-mood-comments-visible-v1'),('all150_original_direct_main_battle_and_ordinary_condition4_5_selections','all225_original_direct_main_battle_and_ordinary_mood_selections'),('==150','==225'),
        ("len(context['all100_prior_condition0_1_2_3_discriminating_controls'])==100 and context['job_role_and_mood_getters_not_called']","len(context['all75_physical_condition1_priority_controls'])==75 and len(context['all72_direct_NPC_hero_normal_mood1_2_3_no_message_controls'])==72"),
        ('all26_previews_visually_reviewed','all39_previews_visually_reviewed'),('all26_native_previews_visually_reviewed','all39_native_previews_visually_reviewed'),('==26','==39'),
        ("case['physical_condition_ID']==row['physical_condition_ID']","case['physical_condition_ID']==row['physical_condition_ID']==0 and case['mood_ID']==row['mood_ID']"),
        ('original_physical_selector_selected_condition4_5_message','original_mood_selector_selected_expected_message'),('Illness and near-death native-consumer audit','Mood and panic native-consumer audit'),
        ('26 records;zero','39 records;zero'),('Native illness/near-death audit:all26','Native mood/panic audit:all39')])
    ROOT.mkdir(parents=True,exist_ok=True);font_path=Path('work/analysis/mood_comments_v980/native_font_proof.json');fonts=read(font_path)
    assert fonts['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and tuple(c['message_id'] for c in fonts['cases'])==IDS
    for case in fonts['cases']:assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
    visual=font_path.parent/'visual_review.json';assert not visual.exists() and not PRODUCTION.exists()
    save(visual,{'native_font_proof':str(font_path),'native_font_proof_sha256':sha(font_path.read_bytes()),'review_sheet':fonts['review_sheet'],'review_sheet_sha256':fonts['review_sheet_sha256'],
        'all39_previews_visually_reviewed':True,'native_IDs':list(IDS),'visual_review_pending':False,
        'findings':'All39 complete original-font previews reviewed. Independent Lil1843/Maria1844 and silence1855/Ugh1856 have no borrowed word fragments. Complete ASCII I1845/1846/1858 survives. Silent1855 contains only three periods;1871 remains six comic symbols. Self-talk1853 now has a19cell quoted first row and35cell complete reply starting Oh;two fresh native cases verify the change and76 byte-identical cases retain their original proof. All visible rows start at x0 with no authored padding,missing edge glyphs,gaps,word splits,overflow or extra pages. Actual RGB scenes and returns remain required.',
        'CPU_only_font_scope_no_actual_gameplay_credit':True,'full_goal_complete':False})
    doc=deepcopy(read(MANUSCRIPT));doc.update(reviewed_research_manuscript=str(MANUSCRIPT),reviewed_research_manuscript_sha256=sha(MANUSCRIPT.read_bytes()),formatting_review_pending=False,
        review_gates=['source','context','localization','naturalness','formatting'],status='39-source-prose-native-font-and-visual-reviewed-registered-release-and-actual-pending')
    for key,path in [('native_font_proof',font_path),('visual_review_proof',visual)]:doc[key]=str(path);doc[key+'_sha256']=sha(path.read_bytes())
    for row in doc['records']:row['review']['formatting']=True
    save(PRODUCTION,doc);provenance=[]
    for source,target,raw,text in (module,audit):
        with target.open('x',encoding='utf-8') as f:f.write(text)
        assert source.read_bytes()==raw
        provenance.append({'source':str(source),'source_before_sha256':sha(raw),'source_after_sha256':sha(source.read_bytes()),'source_unchanged':True,'successor':str(target),'successor_sha256':sha(target.read_bytes())})
    save(ROOT/'native_successor_provenance.json',{'files':provenance,'all_source_hashes_unchanged':True,'all_successor_replacements_preflighted_before_output':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('39 original-font previews reviewed;production manuscript and guarded mood-consumer module/auditor created.',flush=True)


if __name__=='__main__':main()
