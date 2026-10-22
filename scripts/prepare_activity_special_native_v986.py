"""Bind17 native previews and strict mixed-consumer guards to production prose."""
import ast
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/activity_special_v987')
PRODUCTION=Path('translations/activity_special_editorial_manuscript_v2.json')

GATES='''def apply_release(common,arm,path):
    config=read(path);assert config['format']=='dk4-activity-special-editorial-v1'
    assert sha(common)==config['source_common_sha256']==SOURCE_COMMON and sha(arm)==config['source_arm9_sha256']==SOURCE_ARM
    for name,digest in config['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    manuscript=Path(config['manuscript']);assert sha(manuscript.read_bytes())==config['manuscript_sha256']
    doc=read(manuscript);draft=Path(doc['reviewed_research_manuscript'])
    assert sha(draft.read_bytes())==doc['reviewed_research_manuscript_sha256']
    assert [(r['message_id'],r['english'],r['source_meaning']) for r in doc['records']]==[(r['message_id'],r['english'],r['source_meaning']) for r in read(draft)['records']]
    for key in ('native_context_proof','native_font_proof','visual_review_proof','source_context_supplement'):
        assert sha(Path(doc[key]).read_bytes())==doc[key+'_sha256']
    context=read(doc['native_context_proof']);fonts=read(doc['native_font_proof']);visual=read(doc['visual_review_proof'])
    assert context['candidate_sha256']==doc['current_ROM_sha256']
    assert len(context['all52_activity2_direct_and_main_priority_cases'])==52
    assert len(context['all16_special_ordinary_battle_direct_and_main_bit2_controls'])==16
    assert len(context['all12_original_actor_role_legality_controls'])==12
    refusals=context['all3_original_Chapel_assignment_refusal_owner_and_speaker_calls'];assert len(refusals)==3
    for r in refusals:
        assert r['all28_actor_records_and31_room_occupants_preserved_no_assignment_performed'] and r['original_ABI_and_stack_pass']
        assert r['requested_role']==18 and r['dialogue_dispatcher']==0x02053FE4
    assert {(r['actor_ID'],r['original_legality_and_actor_specific_refusal_calls'][0]['message_ID']) for r in refusals}=={(17,1878),(25,1879),(12,1880)}
    assert fonts['manuscript_sha256']==sha(draft.read_bytes()) and len(fonts['cases'])==17
    assert fonts['complete_Deck_native_font_cases']==20 and fonts['complete_modal_native_font_cases']==3
    assert fonts['all17_complete_words_leading_trailing_letters_and_native_bounds_pass']
    assert fonts['modal3_use_existing_native_balanced_formatter_as_offline_compiler_no_runtime_code_or_membership_changes']
    assert visual['native_font_proof_sha256']==sha(Path(doc['native_font_proof']).read_bytes()) and visual['all17_previews_visually_reviewed'] and not visual['visual_review_pending']
    for row,case in zip(doc['records'],fonts['cases'],strict=True):
        n=row['message_id'];assert n==case['message_id'] and row['actor_ID']==case['actor_ID']==context['actor_by_message_ID'][str(n)]
        assert compiled(row).hex()==case['compiled_hex'] and case['consumer']==row['consumer']
        assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
        if case['consumer']=='Deck-CabinInfoView':
            assert case['complete_words_and216x36_body_bounds_pass']
            assert len(case['native_controls'])==(2 if n<1878 else 1)
            for v in case['native_controls']:
                assert v['text_hex']==case['compiled_hex'] and v['original_numeric_selector_selected_expected_message']
                for gate in ('complete_native_copy_macro_draw_and_ABI','full252x96_native_and_independent_canvas_equal','independent_authored_words_at_x0_12px_rows_match_every_pixel','bitmap_and_input_guards_exact'):
                    assert v[gate]
        else:
            assert n in (1878,1879,1880) and case['original_54014_COMMON_dispatch_keeps_compiled_bytes_exact']
            assert case['whole228x64_native_and_independent_font_canvas_equal'] and case['all_leading_trailing_glyphs_and_uniform_visible_left_margin_pass']
    c,a,proof=plan(common,arm,doc)
    assert sha(c)==config['target_common_sha256'] and sha(a)==config['target_arm9_sha256'] and proof['directory_sha256']==config['directory_sha256']
    copies=read(config['native_copy_proof'])
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==178
    assert copies['COMMON_sha256']==sha(c) and copies['ARM9_sha256']==sha(a)
    assert copies['all_full_span_plus_NUL_and_entire8192_input_bytes_and_output_guard_pass'] and copies['callee_saved_ABI_and_stack_pass']
    supplement=read(doc['source_context_supplement'])
    assert supplement['candidate_sha256']==doc['current_ROM_sha256'] and supplement['all17_source_IC_and_printf_counts_zero']
    assert supplement['Yifa1879_personal_training_not_universal_Taoist_ban'] and supplement['Al1878_Arab_pride_without_invented_religion']
    assert supplement['Yukihisa1880_explicit_Christian_refusal_with_formal_voice'] and supplement['Aziza1884_1888_addressee_identity_gender_kinship_and_bit2_meaning_not_invented']
    assert supplement['activity2_after_original_event_no_invented_Scold_button']
    for name,digest in supplement['established_term_documents'].items():assert sha(Path(name).read_bytes())==digest
    audit=read(config['native_consumer_audit']);assert audit['batch_sha256']==sha(manuscript.read_bytes())
    assert audit['blocking_errors']==audit['unwaived_warnings']==0 and len(audit['records'])==17
    assert audit['target_COMMON_sha256']==sha(c) and audit['target_ARM9_sha256']==sha(a)
    return c,a,proof
'''

def main():
    assert not PRODUCTION.exists();ROOT.mkdir(parents=True,exist_ok=True)
    s=Path('dk4tool/patch/mood_comments_editorial_v981b.py');raw=s.read_bytes();text=s.read_text(encoding='utf-8')
    t=Path('dk4tool/patch/activity_special_editorial.py');assert not t.exists()
    text=text[:text.index('def apply_release(')]
    pairs=[('Complete39 mood0/4/5','Complete17 activity,Chapel-refusal and special-character'),
        ('from dk4tool.patch.illness_critical_editorial import current_entries as previous_entries','from dk4tool.patch.mood_comments_editorial_v981b import current_entries as previous_entries'),
        ('from scripts.mood_comments_layout_v980 import compiled','from scripts.activity_special_layout_v986 import compiled'),
        ('range(1833,1872)','range(1872,1889)'),
        ('97e35ed3e2ea00ea1f46cf5d9e40eb22093956df9b4785d36b6e9b9bade73251','eb50d15cdc33306b2c321795719e7f03a58a4867fedafcaa59b1695d0fa8258d'),
        ('ae387dd92e66ee580a5a48f5b7196fcbcdaefc3d40112338106e6ebe35f753db','a446afb0ea754456351b9257b34edc8526d9c437bd2af7fe0f9cb2fe3e0ddadb'),
        ('translations/mood_comments_editorial_release_v1.json','translations/activity_special_editorial_release_v1.json'),
        ('deck-mood-comments-visible-v1','activity-special-mixed-consumers-v1'),
        ("row['physical_condition_ID']==0 and row['mood_ID'] in (0,4,5) and row['role_ID_is_CPU_layout_fixture_only_not_source_semantics']","row['actor_ID'] in (6,11,12,14,15,17,20,22,25,26,27) and row['consumer'] in ('Deck-CabinInfoView','assignment-refusal-modal')"),
        ('all3629_other_message_strings_exact','all3651_other_message_strings_exact')]
    for old,new in pairs:assert old in text,old;text=text.replace(old,new)
    text+=GATES;ast.parse(text)
    font_path=Path('work/analysis/activity_special_v986/native_font_proof.json');fonts=read(font_path)
    assert len(fonts['cases'])==17 and fonts['complete_Deck_native_font_cases']==20 and fonts['complete_modal_native_font_cases']==3
    visual=Path('work/analysis/activity_special_v986/visual_review.json');assert not visual.exists()
    save(visual,{'native_font_proof_sha256':sha(font_path.read_bytes()),'all17_previews_visually_reviewed':True,'visual_review_pending':False,
        'findings':'All14 Deck texts and3 modal texts show complete natural words,uniform cell origins and complete edge glyphs.36cell Emilio promise,Fernando continuation and Yifa training are intact. Two original Aziza bit outcomes are independent texts. The3 popup compilations keep the complete original paragraph and native guards;first-row narrow-I bearing is glyph shape,not a different cell indent. No actual RGB,modal geometry or dismissal claim.',
        'actual_RGB_and_registered_integration_pending':True,'full_goal_complete':False})
    research=Path('translations/activity_special_editorial_manuscript_v1.json');doc=deepcopy(read(research))
    doc.update(reviewed_research_manuscript=str(research),reviewed_research_manuscript_sha256=sha(research.read_bytes()),
        formatting_review_pending=False,review_gates=['source','context','localization','naturalness','formatting'],
        status='17-source-prose-native-font-visually-reviewed-registered-release-and-actual-pending')
    for key,path in (('native_font_proof',font_path),('visual_review_proof',visual)):
        doc[key]=str(path);doc[key+'_sha256']=sha(path.read_bytes())
    for row in doc['records']:row['review']['formatting']=True
    save(PRODUCTION,doc)
    with t.open('x',encoding='utf-8') as f:f.write(text)
    assert s.read_bytes()==raw
    save(ROOT/'native_module_provenance.json',{'source':str(s),'source_sha256':sha(raw),'source_after_sha256':sha(s.read_bytes()),
        'successor':str(t),'successor_sha256':sha(t.read_bytes()),'source_unchanged':True,
        'all_replacements_and_syntax_preflighted_before_output':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('17 native/visual reviews bound to production and exact source/consumer guards;actual samples remain.')

if __name__=='__main__':main()
