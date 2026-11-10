"""Seal viewed exact native/actual prose evidence and retain the incidental unreviewed sailing lead."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B97_actual_approval_v5018')
INPUT=Path('translations/maria_B97_editorial_manuscript_v4.json')
OUTPUT=Path('translations/maria_B97_editorial_manuscript_v5.json')
ACTUAL=Path('work/analysis/maria_B97_actual_v5017b/terminal40_commands32_speeches_and_actual_two_page_continuation.json')
NATIVE=Path('work/analysis/maria_B97_native_review_v5016/all32_viewed_matrices_42_formatter_negatives_and_one_actual_page_gate.json')
CAPBASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc,actual,native=deepcopy(read(INPUT)),read(ACTUAL),read(NATIVE)
    assert native['manuscript_sha256']==sha(INPUT.read_bytes()) and actual['complete_actual_panel_pages']==33 and not actual['failures'] and not actual['nontext_differences']
    assert len(actual['paired_nontext_samples'])==327 and sum(len(r['holds']) for r in actual['actual_panels'])==327
    assert [v['normal_end_frame'] for v in actual['versions']]==[23222,23822] and [v['frames'] for v in actual['versions']]==[31000,31000]
    assert actual['source72_page_boundary']['original_A_event']==dict(start=15401,duration=8,buttons=['A']) and actual['source72_page_boundary']['original_continuation_first_row_indent_px']==6
    assert len(actual['representative_contact_sheets'])==6
    for p in actual['representative_contact_sheets']:assert sha(Path(p['path']).read_bytes())==p['sha256']
    pairs=[]
    for case,frame in [('clean_Japanese',22920),('reviewed_English',23520),('clean_Japanese',31000),('reviewed_English',31000)]:
        p=CAPBASE/('maria_B97_B33_fixture_v5015b_'+case)/f'frame_{frame:06d}_cold_boot.png';assert p.exists();pairs.append(dict(case=case,frame=frame,path=str(p),sha256=sha(p.read_bytes()),viewed_full256x384=True))
    assert Image.open(pairs[0]['path']).convert('RGB').tobytes()==Image.open(pairs[1]['path']).convert('RGB').tobytes()
    assert Image.open(pairs[2]['path']).convert('RGB').tobytes()!=Image.open(pairs[3]['path']).convert('RGB').tobytes()
    timing=[]
    for index,(a,b) in enumerate(zip(actual['versions'][0]['command_pairs'],actual['versions'][1]['command_pairs'],strict=True)):
        if (a['start'],a['returned'])!=(b['start'],b['returned']):timing.append(dict(command_index=index,source_offset=a['offset'],source_start=a['start'],source_return=a['returned'],English_start=b['start'],English_return=b['returned']))
    assert len(timing)==34
    for row in doc['records']:
        observed=[r for r in actual['actual_panels'] if r['id']==row['id']];assert len(observed)==(2 if row['source_record_index']==72 else 1) and all(r['holds'] for r in observed)
        row['review']['formatting']=True
        row.update(current_complete_native_display_pending=False,current_actual_page_advance_pending=False,actual_content_fixture_proof=str(ACTUAL),actual_content_fixture_proof_sha256=sha(ACTUAL.read_bytes()),actual_panel_pages=observed,actual_source97_eligibility_not_claimed=True,status='source-prose-native-format-and-focused-actual-approved;reference-loader-atomic-registered-release-pending')
        if row['source_record_index']==72:
            row.update(source72_actual_A_continuation_proof=actual['source72_page_boundary'],source72_historical_zero_indent_projection_is_not_actual_page_geometry=True)
        if 'reviewed_ordinary_soft_wrap' in row:row['reviewed_ordinary_soft_wrap']['native_and_actual_approval_still_pending']=False
    doc.update(formatting_review_pending=False,status='source-prose-native-format-and-focused-actual-approved;reference-loader-atomic-registered-release-pending',actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),native_review_proof=str(NATIVE),native_review_proof_sha256=sha(NATIVE.read_bytes()),all32_records_33_actual_pages_and_six_actual_sheets_viewed=True,source72_two_pages_are_offline_projection_until_fresh_A_advance=False,source72_actual_two_pages_complete_original_guard_indent6_verified=True,actual_source_entry_is_disclosed_B33_content_fixture=True,source97_natural_eligibility_earned_recruitment_or_earned_tablet_not_claimed=True,source_prose_or_completion_credit_added=0,full_goal_complete=False)
    validate_natural_dialogue_batch(doc)
    # The final source run incidentally shows a sailing exchange. Preserve its
    # unique visible-string match as a lead,not a live global-ID trace or review.
    parent=NdsImage.open(doc['current_ROM']);clean=NdsImage.open('work/clean.nds');arm=parent.read_file('/__arm9__.bin');common=parent.read_file('/COMMON/MESFILE.DK4')
    context=read('work/analysis/maria_B97_voices_v5000/current_capture_context.json');current=owned_entries(common,arm,context['directory_sha256']);original=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    expected="Admiral, rats are everywhere! Is the food safe?!";hits=[r for r in current if ' '.join(r.text.decode('cp932').split())==expected];assert len(hits)==1 and hits[0].message_id==405
    refs=[]
    for ident in [401,404,405]:
        row={}
        for label,entries,rawfile in [('clean',original,clean.read_file('/COMMON/MESFILE.DK4')),('current',current,common)]:
            e=entries[ident];blocks=IlnkContainer.parse(rawfile).blocks;assert blocks[e.block][e.block_offset:e.block_offset+len(e.text)]==e.text
            row[label]={**asdict(e),'text':e.text.decode('cp932'),'text_hex':e.text.hex()}
        refs.append(dict(message_id=ident,**row))
    ROOT.mkdir(parents=True);lead=ROOT/'incidental_COMMON405_rats_scene_unreviewed_lead.json'
    save(lead,dict(actual_capture=pairs[2],visible_role='Sailor',visible_text=expected,unique_current_visible_string_match=405,actual_global_message_ID_and_role_dispatch_not_traced=True,clean_current_related_message_references=refs,next='Read the complete clean rat-outbreak exchange and its alternative voices/responses before comparing older English. Bind exact COMMON405 caller,source preamble,shared dynamic wrapping and role/substitution consumer. This visible capture adds practical sailing-scene evidence only;no fresh contextual review or automatic wrapping correction.',no_claim_that_source_B97_has_a_rats_scene=True,source97_content_fixture_has_ended_before_this_incidental_scene=True,no_new_review_credit=True,full_goal_complete=False))
    save(OUTPUT,doc)
    save(ROOT/'all32_native_actual_approval_and_remaining_release_gates.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),source_native_actual_records=32,revised=23,retained=9,actual_panel_pages=33,complete_actual_matching_holds=327,paired_nontext_samples=327,paired_nontext_differences=0,all_six_actual_sheets_viewed=[dict(p,viewed_in_full_current_turn=True) for p in actual['representative_contact_sheets']],four_full_resource_and_final_screens_viewed=pairs,original_item_presentation_pair_whole_RGB_equal=True,no_earned_inventory_claim_from_original_acquisition_caption=True,source72_current_original_A_continuation_complete_with_one_cell_indent=True,all_words_controls_compiled_payloads_and_native_metrics_preserved=True,first_page_full_four_rows_and_second_page_full_final_sentence_verified=True,original_subsequent_Bandit_speech_and_normal_end_observed=True,measured_timing_differences=timing,source_exit=23222,English_exit=23822,final31000_whole_RGB_not_equal_and_different_incidental_sailing_UI_observed=True,final_actor_and_PRNG_differences=actual['final_state_observations'],no_PRNG_causality_future_state_or_full_RAM_equivalence_claim=True,new_practical_unreviewed_scene_lead=str(lead),new_practical_unreviewed_scene_lead_sha256=sha(lead.read_bytes()),remaining_gates=['whole-SC3 loader/cache and entry/reference census','source and relocated guarded end/control checks','production-scope B97-only reference image and exact other-file preservation','source-locked atomic compiler and meaningful rejection controls','registered cumulative build after V4987','exact clean-input patch reconstruction','fresh current cumulative startup and scoped regressions','final exact source/current/compiled/integrated ledger credit once'],evidence={str(p):sha(p.read_bytes()) for p in [INPUT,ACTUAL,NATIVE,Path(doc['source_context']),Path(__file__)]},new_emulator_runs=2,new_emulator_frames=62000,new_review_credit=0,all_jobs_terminal_and_sessions_reaped=True,full_goal_complete=False))
    print('32 native/actual reviews sealed,23 revisions/9 retentions;327 full holds and paired nontext samples. Source72 A continuation verified at6px indent. Registered integration remains pending;zero credit.')
