"""Derive completion accounting and stage exact document writes for native application."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B167_completion_tools_v4164')
TARGET=Path('scripts/complete_lil_B167_v4164.py')
if __name__=='__main__':
    assert not ROOT.exists() and not TARGET.exists()
    source=Path('scripts/complete_lil_B166_v4114.py');text=source.read_text(encoding='utf-8')
    changes={
        'lil_B166_completion_text_v4114':'lil_B167_completion_text_v4164','lil_B166_completion_v4114':'lil_B167_completion_v4164',
        'lil_B166_contextual_final_review_v1':'lil_B167_contextual_final_review_v1',
        'lil_B166_editorial_manuscript_v6':'lil_B167_editorial_manuscript_v13','lil_B166_choice_manuscript_v3':'lil_B167_choice_manuscript_v3',
        'lil_B166_release_v4111':'lil_B167_release_v4161','lil_B166_startup_v4113':'lil_B167_startup_v4163',
        'lil_B166_actual_v4104/actual_both_choices_conditional_panels_and_single_return':'lil_B167_actual_v4151/actual_both_choices_conditional_panels_and_distinct_returns',
        'lil_B166_transition_review_v4105/both_choices_all7_sheets_Manuel_names_figures_and_paired_returns_review':'lil_B167_transition_review_v4152/both_choices_all5_sheets_static_names_and_distinct_returns_review',
        'lil_B166_checkpoint_v4090':'lil_B167_checkpoint_v4155','lil_B166_registration_v4109':'lil_B167_registration_v4159b',
        'Lil-B166-Manuel-ship-care-recruitment-optional-Workroom-advice44':'Lil-B167-Shipwright-complete-sail-lesson-accept-refuse29',
        "{'DK4_MES_B166_R0087'}":"{'DK4_MES_B167_R0045','DK4_MES_B167_R0131'}",
        'all541':'all543','all44':'all29','all_current_requested_and_final_framebuffers_equal_V4046':'all_current_requested_and_final_framebuffers_equal_V4110',
        'Fernando_remark_not_actual_or_byte_identical_reuse':'both_Cesare_remarks_not_actual_or_byte_identical_reuse',
        'actual_advice_choice_result_observed':'actual_menu_choice_result_observed','source_prose_credit_already_recorded_in_V4090':'source_prose_credit_already_recorded_in_V4136',
        'lil_B166_v4090':'lil_B167_v4136','unfinished_editorial_scope_v4090':'unfinished_editorial_scope_v4136',
        'remaining_B167_B180':'remaining_B168_B180','remaining_B168_B180_physical_speeches=348,remaining_choice_command_leads=1':'remaining_B168_B180_physical_speeches=321,remaining_choice_command_leads=0',
        'source_A000_effect_not_earned':'no_B167_command_omitted_in_content_fixtures',
        '# Current editorial handoff - V4090':'# Current editorial handoff - V4155',
        'Remaining348 physical B167-B180 speech leads,one choice-command lead':'Remaining321 physical B168-B180 speech leads,zero choice-command leads',
        'V4110':'V4160','V4114':'V4164','v4114':'v4164','B166':'B167','event166':'event167'
    }
    # Apply simultaneously so old/target checkpoint and accounting values cannot cascade.
    for old in changes:assert old in text,old
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],text)
    nums={5529:5573,5573:5602,5576:5605,3720:3749,3551:3567,2022:2035,3974:4003,44:29,24:16,20:13,41:25,73:28,72:78,166:167,541:543,348:321}
    text=re.sub(r'\b('+ '|'.join(map(str,nums))+r')\b',lambda m:str(nums[int(m.group(0))]),text)
    old='    save(lp,ledger)';start=text.index(old)
    # The original footer writes files directly. Stage every exact target first;
    # the native application verifies all before/planned hashes before any write.
    footer='''    planned=ROOT/(lp.name+'.planned');save(planned,ledger)
    staged=[dict(target=str(lp),before_sha256=sha(lp.read_bytes()),planned=str(planned),planned_sha256=sha(planned.read_bytes()))]
    section='## V4164: 29 Lil B167 reviews completed in V4160\\n\\n'+summary
    section+='\\n\\nFinal review: '+FINAL.as_posix()+'. Release: '+RELEASE.as_posix()+'. Startup: '+START.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\\n\\n'
    for i,path in enumerate(docsfiles):
        first,rest=path.read_text(encoding='utf-8').split('\\n',1)
        data=(('# Current editorial handoff - V4164' if i==0 else first)+'\\n\\n'+section+rest).encode('utf-8')
        planned=ROOT/(path.name+'.planned');planned.write_bytes(data)
        staged.append(dict(target=str(path),before_sha256=sha(path.read_bytes()),planned=str(planned),planned_sha256=sha(data)))
    receipt=dict(checkpoint='V4164',final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),
        evidence=evidence,updated_files={r['target']:r['planned_sha256'] for r in staged},prior_checkpoint=str(PRIOR),
        new_source_prose_reviews=0,new_completed_records=29,revised=16,retained=13,fresh_reread=5602,fresh_integrated=5602,
        fresh_pending=0,source_prose=5605,completed=5602,historical_revised=3567,historical_retained=2035,
        candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],
        manifest_batches=543,accepted_layers=114,new_actual_emulator_runs=6,new_actual_fixture_runs=4,new_registered_startup_runs=2,
        actual_unique_speech_panels=25,actual_English_speech_observations=28,actual_choice_outcomes=2,
        offline_only_display_IDs=sorted(OFFLINE),remaining_B168_B180_physical_speeches=321,remaining_choice_command_leads=0,
        all_jobs_terminal=True,full_goal_complete=False)
    save(ROOT/'staged_completion_receipt.json',receipt)
    save(ROOT/'staged_completion.json',dict(files=staged,staged_receipt=str(ROOT/'staged_completion_receipt.json'),
        staged_receipt_sha256=sha((ROOT/'staged_completion_receipt.json').read_bytes()),no_current_ledger_or_document_mutation_yet=True))
    print('V4164 completion staged after registered gates; native application and final seal pending. Full goal remains active.')
'''
    text=text[:start]+footer
    assert 'B166' not in text and 'Fernando' not in text
    compile(text,str(TARGET),'exec');TARGET.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(previous=str(source),previous_sha256=sha(source.read_bytes()),successor=str(TARGET),successor_sha256=sha(TARGET.read_bytes()),current_ledger_credit_only_after_all_registered_gates_and_native_application=True,no_source_prose_double_credit=True,no_completion_yet=True))
