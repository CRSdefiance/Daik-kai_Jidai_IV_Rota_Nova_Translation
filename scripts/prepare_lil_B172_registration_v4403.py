"""Derive B172 registration with explicit no-macro and read-only ownership negatives."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B172_registration_tools_v4403')
SOURCE=Path('scripts/register_lil_B171_v4352.py')
TARGET=Path('scripts/register_lil_B172_v4403.py')
if __name__=='__main__':
    assert not ROOT.exists() and not TARGET.exists()
    text=SOURCE.read_text(encoding='utf-8')
    a=text.index('    profile.update(status=');b=text.index("    registry['profiles'][PROFILE]",a)
    text=text[:a]+'''    profile.update(status='experimental',lil_B172_editorial=owned.CONFIG,
        description='Full V4353 stack plus27 complete B172 Julian/Mihwa Silla crown reviews:19 revisions/eight retentions,27 progressive speeches,38 commands,11 leaves,five presentations,three resources,C200 before source A000/6240 and single end;zero substitutions,pause,predicates or relative sites. Two complete-content boots cover every panel and original departure/effects/town return;two focused repeats bind post-effect persistent state and later PRNG/timing scope. Two transient and99 later nontext differences remain disclosed. No natural eligibility,earned progress,full-route or hardware claim.',
        note='B172 source/native/reference/representative approved;registered build,exact patch and fresh startup pending.')
''' + text[b:]
    a=text.index("    for macro in ['FI']:");b=text.index('    def changed_actual',a)
    text=text[:a]+'''    for macro in ['FI','FA','FO']:
        def invent_macro(value,macro=macro):
            value['records'][0]['english']+=' {MACRO:'+macro+'}'
        mutations.append(('invented_'+macro,'manuscript',invent_macro))
    mutations.extend([
        ('invented_Mihwa_scratch_write','source_nameplate_consumer_proof',lambda value:next(r for r in value['native_six_consumer_cases']['rows'] if r['actor_ID']==201).update(original_getter_writes=[{}])),
        ('invented_Mihwa_scratch_ring','source_nameplate_consumer_proof',lambda value:next(r for r in value['native_six_consumer_cases']['rows'] if r['actor_ID']==201).update(original_scratch_rings=[{}])),
    ])
''' + text[b:]
    text=text.replace("        elif label == 'wrong_actual_resource':", "        elif label == 'wrong_actual_A000':\n            actual['versions'][0]['source_A000_hex']='00a0ffff00000000'\n        elif label == 'wrong_actual_resource':")
    text=text.replace("'wrong_actual_resource', 'missing_actual_version'", "'wrong_actual_resource', 'wrong_actual_A000', 'missing_actual_version'")
    changes={
        'B171':'B172','v4352':'v4403','all-routes-unified-v4353':'all-routes-unified-v4404',
        'all-routes-unified-v4303':'all-routes-unified-v4353','all_routes_combined_v4303':'all_routes_combined_v4353',
        'editorial_manuscript_v5':'editorial_manuscript_v4','reference_checkpoint_v4347':'reference_checkpoint_v4400',
        'reference_approval_v4346':'reference_approval_v4399','loader_v4336':'loader_v4385',
        "        'work/analysis/lil_B171_timing_count_amendment_v4349/amendment_receipt.json',\n":'',
        'editorial_handoff_verification_v4350':'editorial_handoff_verification_v4401b',
        'transition_review_v4345/all7_sheets_dream_morning_C200_and_paired_return_review':'transition_review_v4398/all5_sheets_departure_C200_A000_and_paired_return_review',
        "deps.update(row['path'] for row in visual['later_sailing_views'])":"deps.update(row['path'] for row in visual['all4_paired_full_screen_sheets_viewed'])",
        "value['source_macro_preservation_negatives'].pop()":"value['source_macro_absence_negatives'].pop()",
        'source_resource10_boundary_cases_reused_only_by_exact_word_and_runtime':'source_resource30_boundary_cases_reused_only_by_exact_words_and_runtime',
        'all8_source_current_target_nonrelative_nonspeech_leaves':'all11_source_current_target_nonrelative_nonspeech_leaves',
        'all4_declared_end_decodes_return_type0_extent4_without_post_payload_read':'all2_declared_end_decodes_return_type0_extent4_without_post_payload_read',
        'first_end2112_actual_second2116_native_decoder_only':'single_end1880_actual',
        'later59_sailing_differences_preserved_with_explicit_inference_and_state_scope':'two_transient_and99_later_nontext_differences_preserved_with_explicit_state_scope',
        'paired_town11770_whole1A04_actor_models_and_captain2_equal':'paired_town9370_whole1A04_actor_models_and_captain2_equal',
        'actual_all37_dream_morning_presentations_resource_C200_and_first_end':'actual_all27_presentations_resources_C200_A000_and_end',
        "['source_first_end_offset'] = 2116":"['single_source_end_offset'] = 1884",
        'Sanghyeon_selector_as_text':'Mihwa_selector_as_text','wrong_4500_extent':'wrong_45FF_extent',
        'false_actual_second_end':'lost_actual_single_end','invented_A000':'extra_A000',
        'V4303':'V4353','expected_batches=547':'expected_batches=548',
    }
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m[0]],text)
    text=re.sub(r'(?<!\d)37(?!\d)','27',text)
    assert not re.search(r'B171|v4352|all37|2116|source_first_end|later59',text)
    compile(text,str(TARGET),'exec');TARGET.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'derivation.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),
        target=str(TARGET),target_sha256=sha(TARGET.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),
        no_source_macro_deletion_cases_invented=True,three_invented_macro_and_two_readonly_name_ownership_negatives_added=True,
        source_A000_raw_negative_added=True,full_goal_complete=False))
    print('Prepared atomic B172 registration after full V4353;positive reconstruction and all negatives precede registry/builder writes.')
