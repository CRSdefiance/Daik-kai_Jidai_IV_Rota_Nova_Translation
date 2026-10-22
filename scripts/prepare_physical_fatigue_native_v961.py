"""Bind13 visually reviewed native previews and fatigue-specific guarded successors."""
import ast
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch import battle_gunnery_deck_editorial as parent
from scripts.prepare_physical_fatigue_prose_v959 import MANUSCRIPT,IDS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/physical_fatigue_v962')
PRODUCTION=Path('translations/physical_fatigue_editorial_manuscript_v2.json')


def rendered(source,target,pairs):
    source,target=Path(source),Path(target);before=source.read_bytes();text=source.read_text(encoding='utf-8');assert not target.exists()
    for old,new in pairs:
        assert old in text,(source,old)
        text=text.replace(old,new)
    ast.parse(text)
    return source,target,before,text


FATIGUE_GATE='''def apply_release(common,arm,path):
    config=read(path);assert config['format']=='dk4-physical-fatigue-editorial-v1'
    assert sha(common)==config['source_common_sha256']==SOURCE_COMMON and sha(arm)==config['source_arm9_sha256']==SOURCE_ARM
    for name,digest in config['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    manuscript=Path(config['manuscript']);assert sha(manuscript.read_bytes())==config['manuscript_sha256']
    doc=read(manuscript);draft=Path(doc['reviewed_research_manuscript'])
    assert sha(draft.read_bytes())==doc['reviewed_research_manuscript_sha256']
    assert [(r['message_id'],r['english'],r['source_meaning']) for r in doc['records']]==[(r['message_id'],r['english'],r['source_meaning']) for r in read(draft)['records']]
    for key in ('native_context_proof','native_font_proof','visual_review_proof','source_context_supplement'):
        assert sha(Path(doc[key]).read_bytes())==doc[key+'_sha256']
    context=read(doc['native_context_proof']);fonts=read(doc['native_font_proof']);visual=read(doc['visual_review_proof'])
    cases=context['all75_original_direct_main_battle_and_ordinary_fatigue_selections'];assert len(cases)==75
    assert context['source_condition_ID']==1 and context['Sera24_special_ID']==1793
    assert context['condition1_fatigue_NPC_IDs']==list(range(1781,1789)) and context['condition1_genuine_protagonist_IDs']==list(range(1789,1793))
    assert context['four_genuine_captains_and21_NPCs_no_actor_ID_replacement'] and context['job_role_and_mood_not_queried_in_physical_status_branch']
    assert {r['selected_message_ID'] for r in cases}==set(IDS) and {r['actor_ID'] for r in cases}==set(range(25))
    for r in cases:
        assert r['isolated_CPU_condition']==1 and r['source_condition_byte_offset']==6
        assert r['job_role_and_mood_getters_not_called'] and r['original_native_selector_and_callee_saved_ABI_pass']
        assert r['only_declared_CPU_condition_and_mode_fields_changed'] and r['actor_other31_bytes_and_all_other_source_RAM_preserved']
        expected=1793 if r['actor_ID']==24 else 1789+r['actor_ID'] if r['actor_ID']<4 else 1781+r['native_voice_class']
        assert r['selected_message_ID']==expected
        if r['case']=='main_ordinary_status_priority':assert r['isolated_CPU_mode_fields8_12']==[0,0]
        else:assert r['isolated_CPU_mode_fields8_12']==[0,1]
    healthy=context['all25_healthy_direct_helper_no_message_controls'];assert len(healthy)==25
    assert {r['actor_ID'] for r in healthy}==set(range(25))
    assert all(r['isolated_CPU_condition']==0 and r['selected_message_ID'] is None and r['original_native_selector_and_callee_saved_ABI_pass'] for r in healthy)
    assert fonts['manuscript_sha256']==sha(draft.read_bytes()) and len(fonts['cases'])==13 and fonts['complete_native_font_cases']==26
    assert visual['native_font_proof_sha256']==sha(Path(doc['native_font_proof']).read_bytes())
    assert visual['all13_previews_visually_reviewed'] and not visual['visual_review_pending']
    assert fonts['all13_source_numeric_selection_complete_ABI_words_and_visible_ink_pass'] and fonts['ordinary_and_battle_condition1_controls_equal']
    assert fonts['four_original_actual_captain_states_used_no_captain_ID_substitution'] and fonts['Sera24_special1793_included']
    for row,case in zip(doc['records'],fonts['cases'],strict=True):
        assert row['message_id']==case['message_id'] and case['physical_condition_ID']==row['physical_condition_ID']==1
        assert case['all_body_ink_inside_registered216x36_crop'] and case['both_original_selectors_full_canvas_and_words_equal']
        variants=case['ordinary_and_battle_font_controls'];assert [v['mode'] for v in variants]==['ordinary','battle']
        for variant in variants:
            assert compiled(row).hex()==variant['text_hex']
            for gate in ('complete_native_copy_macro_draw_and_ABI','full252x96_native_and_independent_canvas_equal',
                'independent_authored_words_at_x0_12px_rows_match_every_pixel','bitmap_and_input_guards_exact','original_physical_selector_selected_condition1_message'):assert variant[gate]
            assert variant['physical_condition_fixture']['CPU_condition']==1 and variant['physical_condition_fixture']['other31_actor_bytes_and_all_other_CPU_RAM_exact']
    c,a,proof=plan(common,arm,doc)
    assert sha(c)==config['target_common_sha256'] and sha(a)==config['target_arm9_sha256'] and proof['directory_sha256']==config['directory_sha256']
    copies=read(config['native_copy_proof'])
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==178
    assert copies['COMMON_sha256']==sha(c) and copies['ARM9_sha256']==sha(a)
    assert copies['all_full_span_plus_NUL_and_entire8192_input_bytes_and_output_guard_pass'] and copies['callee_saved_ABI_and_stack_pass']
    supplement=read(doc['source_context_supplement'])
    assert supplement['candidate_sha256']==doc['current_ROM_sha256'] and supplement['physical_condition1_precedes_mood_and_work_roles']
    assert supplement['reference_help112']['heading']=='Recreation Room' and supplement['storage_neighbors_are_independent_selections_not_consecutive_speech']
    assert [(r['message_id'],r['IC_count']) for r in supplement['all13_source_IC_macros']]==[(n,int(n==1783)) for n in IDS]
    pronoun_path=Path(supplement['source_pronoun_proof']);assert sha(pronoun_path.read_bytes())==supplement['source_pronoun_proof_sha256']
    pronoun=read(pronoun_path);assert pronoun['candidate_sha256']==doc['current_ROM_sha256'] and pronoun['IC_is_first_person_not_actor_name']
    assert len(pronoun['all25_current_and_clean_parser_control_cases'])==25 and pronoun['four_genuine_captain_states_no_actor_ID_replacement']
    assert all(len(r['variants'])==2 and all(v['source_output_guards_and_ABI_pass'] for v in r['variants']) for r in pronoun['all25_current_and_clean_parser_control_cases'])
    for name,digest in supplement['established_term_documents'].items():assert sha(Path(name).read_bytes())==digest
    audit=read(config['native_consumer_audit']);assert audit['batch_sha256']==sha(manuscript.read_bytes())
    assert audit['blocking_errors']==audit['unwaived_warnings']==0 and len(audit['records'])==13
    assert audit['target_COMMON_sha256']==sha(c) and audit['target_ARM9_sha256']==sha(a)
    return c,a,proof
'''


def main():
    packet=read('work/analysis/physical_fatigue_v957/source_context_packet.json')
    module=rendered('dk4tool/patch/battle_gunnery_deck_editorial.py','dk4tool/patch/physical_fatigue_editorial.py',[
        ('Complete24 battle Gunnery/DeckCleaning','Complete13 physical-condition1 fatigue'),('battle_gunnery_deck','physical_fatigue'),
        ('from dk4tool.patch.battle_sails_boarding_editorial import current_entries as previous_entries','from dk4tool.patch.battle_gunnery_deck_editorial import current_entries as previous_entries'),
        ('physical_fatigue_layout_v952','physical_fatigue_layout_v960'),('range(1757,1781)','range(1781,1794)'),
        (parent.SOURCE_COMMON,packet['COMMON_sha256']),(parent.SOURCE_ARM,packet['ARM9_sha256']),
        ('deck-battle-gunnery-deck-visible-v1','deck-physical-fatigue-visible-v1'),('all3644_other_message_strings_exact','all3655_other_message_strings_exact'),
        ("row['source_native_macros']==[]","row['source_native_macros']==(['IC'] if n==1783 else [])"),
        ("        authored[n]=compiled(row)","        assert row['physical_condition_ID']==1 and row['role_ID_is_CPU_layout_fixture_only_not_source_semantics']\n        authored[n]=compiled(row)")])
    s,t,b,text=module;text=text[:text.index('def apply_release(')]+FATIGUE_GATE;ast.parse(text);module=(s,t,b,text)
    source=Path('scripts/audit_battle_gunnery_deck_native_v954.py').read_text(encoding='utf-8')
    start=source.index("        assert n==case['message_id']");end=source.index("        path=Path(case['preview'])",start)
    audit=rendered('scripts/audit_battle_gunnery_deck_native_v954.py','scripts/audit_physical_fatigue_native_v962.py',[
        ('battle_gunnery_deck','physical_fatigue'),('physical_fatigue_layout_v952','physical_fatigue_layout_v960'),('probe_physical_fatigue_fonts_v952','probe_physical_fatigue_fonts_v960'),
        ('deck-battle-gunnery-deck-visible-v1','deck-physical-fatigue-visible-v1'),
        ("assert len(context['all150_original_battle_helper_main_and_ordinary_control_selections'])==150","assert len(context['all75_original_direct_main_battle_and_ordinary_fatigue_selections'])==75\n    assert len(context['all25_healthy_direct_helper_no_message_controls'])==25 and context['job_role_and_mood_not_queried_in_physical_status_branch']"),
        ('all24_previews_visually_reviewed','all13_previews_visually_reviewed'),('all24_native_previews_visually_reviewed','all13_native_previews_visually_reviewed'),('==24','==13'),
        (source[start:end],"""        assert n==case['message_id'] and case['physical_condition_ID']==1
        assert lines==case['generated_native_lines'] and ' '.join(lines)==row['english']
        assert len(lines)<=3 and max(map(len,lines))<=36
        assert case['all_body_ink_inside_registered216x36_crop'] and case['both_original_selectors_full_canvas_and_words_equal']
        for variant in case['ordinary_and_battle_font_controls']:
            assert compiled(row).hex()==variant['text_hex']
            for gate in ('complete_native_copy_macro_draw_and_ABI','full252x96_native_and_independent_canvas_equal',
                'bitmap_and_input_guards_exact','independent_authored_words_at_x0_12px_rows_match_every_pixel','original_physical_selector_selected_condition1_message'):
                assert variant[gate]
"""),
        ('Battle Gunnery/DeckCleaning native-consumer audit','Physical fatigue native-consumer audit'),('24 records;zero','13 records;zero'),('Native work audit:all24','Native fatigue audit:all13')])
    ROOT.mkdir(parents=True,exist_ok=True);font_path=Path('work/analysis/physical_fatigue_v960/native_font_proof.json');fonts=read(font_path)
    assert fonts['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and tuple(c['message_id'] for c in fonts['cases'])==IDS
    for case in fonts['cases']:assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
    visual=Path('work/analysis/physical_fatigue_v960/visual_review.json');assert not visual.exists() and not PRODUCTION.exists()
    save(visual,{'native_font_proof':str(font_path),'native_font_proof_sha256':sha(font_path.read_bytes()),'review_sheet':fonts['review_sheet'],'review_sheet_sha256':fonts['review_sheet_sha256'],
        'all13_previews_visually_reviewed':True,'native_IDs':list(IDS),'visual_review_pending':False,
        'findings':'All13 native body previews reviewed. Complete initial ASCII I1783 and the stammer1792 are intact. Recreation Room1784 stays together on row2. Fatigue1788 wraps at a natural clause. Sera1793 deliberately remains ... I... on the first row;this is faithful hesitation,not an accidental incomplete line. All visible rows start at x0 with no large internal spacing,manual padding,missing leading/trailing glyphs,overflow,word splits or extra pages. Ordinary and battle font planes match. Actual RGB panels and returns still required.',
        'CPU_only_font_scope_no_actual_gameplay_credit':True,'full_goal_complete':False})
    doc=deepcopy(read(MANUSCRIPT));doc.update(reviewed_research_manuscript=str(MANUSCRIPT),reviewed_research_manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
        formatting_review_pending=False,review_gates=['source','context','localization','naturalness','formatting'],status='13-source-prose-native-font-and-visual-reviewed-registered-release-and-actual-pending')
    for key,path in [('native_font_proof',font_path),('visual_review_proof',visual)]:doc[key]=str(path);doc[key+'_sha256']=sha(path.read_bytes())
    for row in doc['records']:row['review']['formatting']=True
    save(PRODUCTION,doc);provenance=[]
    for source,target,before,text in (module,audit):
        with target.open('x',encoding='utf-8') as f:f.write(text)
        assert source.read_bytes()==before
        provenance.append({'source':str(source),'source_before_sha256':sha(before),'source_after_sha256':sha(source.read_bytes()),'source_unchanged':True,'successor':str(target),'successor_sha256':sha(target.read_bytes())})
    save(ROOT/'native_successor_provenance.json',{'files':provenance,'all_source_hashes_unchanged':True,'all_successor_replacements_preflighted_before_output':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('13 native previews reviewed;production manuscript and fatigue-specific strict module/auditor created.',flush=True)


if __name__=='__main__':main()
