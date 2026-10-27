"""Bind existing role7/portrait and capture samples to focused source tests."""
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/admiral_shot_sampling_v2663')
DOC = Path('translations/admiral_shot_contextual_editorial_manuscript_v2.json')
SEARCH = Path('work/analysis/search_reports_history_v2632b/historical_search_current_binding.json')
CAPTURE = Path('work/analysis/flagship_capture_history_v2583b/historical_flagship_capture_current_binding.json')
RETURN = Path('work/analysis/admiral_shot_return_v2662b/original_post_report_cleanup_and_dispatch.json')
FONT = Path('work/analysis/admiral_shot_fonts_v2658/native_font_proof.json')
BASE = 0x02000000

if __name__ == '__main__':
    assert not ROOT.exists()
    doc=read(DOC);rom=NdsImage.open(doc['current_ROM']);arm=rom.read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds');source=clean.read_file('/__arm9__.bin')
    search,capture,returned,font=map(read,[SEARCH,CAPTURE,RETURN,FONT])
    assert all(p['candidate_sha256']==doc['current_ROM_sha256'] for p in [search,capture,returned,font])
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,SEARCH,CAPTURE,RETURN,FONT,Path('docs/editorial_testing_scope_v1870.md')]}
    for path in [Path('translations/search_reports_contextual_final_review_v1.json'),Path('translations/flagship_capture_contextual_final_review_v1.json')]:
        final=read(path);evidence[str(path)]=sha(path.read_bytes())
        for p in [str(SEARCH),str(CAPTURE)]:
            for k,v in final['evidence'].items():
                if Path(k)==Path(p):assert sha(Path(p).read_bytes())==v
    assert search['no_new_current_emulator_runs_or_visits']
    assert all(r['normal_Sea_View_after_original_dismissal'] for r in search['historical_normal_returns'])
    for bound in search['historical_proof_bindings']:
        for pk,dk in [('proof','proof_sha256'),('report','report_sha256')]:
            p=Path(bound[pk]);assert sha(p.read_bytes())==bound[dk];evidence[str(p)]=bound[dk]
    for pk,dk in [('historical_proof','historical_proof_sha256'),('historical_report','historical_report_sha256')]:
        p=Path(capture[pk]);assert sha(p.read_bytes())==capture[dk];evidence[str(p)]=capture[dk]
    spans=[(0x53D44,0x53DCC),(0x54058,0x54144),(0x54164,0x54240),
           (0x73B8C,0x73C10),(0x72368,0x72474),(0x71D54,0x71EFC),(0x1096F8,0x1097DC)]
    olds=[NdsImage.open(p).read_file('/__arm9__.bin') for p in ['out/all_routes_combined_v1676_candidate.nds','out/all_routes_combined_v1364_candidate.nds']]
    for a,b in spans:assert arm[a:b]==source[a:b] and all(arm[a:b]==old[a:b] for old in olds)
    assert [p['source_voice'] for p in font['all8_original_role7_speech_pipelines']]==list(range(8))
    assert len(returned['main4MiB_changes'])==1 and returned['main4MiB_changes'][0]==dict(address=returned['original_enemy_mobile']+13,before=4,after=0)
    assert returned['native_experience_dispatch_2_250_0_executed_without_substitution']
    assert returned['original_post_message_calls_capture_mode0_for_regular_commander']
    assert all(r['no_outcome_callee_executed'] and r['all_main4MiB_unchanged'] for r in returned['isolated_original_regular_and_B5_dispatch_tests'])
    assert len(capture['historical_holds'])==2
    regular=read(capture['historical_proof'])
    assert regular['normal_A_dialogue_X_cargo_finish_touch_Yes_and_reward_dismissal_return_to_sailing']
    assert capture['no_fixtures_after4800'] and capture['all_accepted_input_events_reconstructed_at_pause_frame_plus1']
    # This additionally exposed five neighboring outcome reports whose full
    # editorial status is separate. Read their clean/current context now,
    # preserve exact references,and give them no completion credit here.
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
    en=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)
    table=0x021183C0;members=list(struct.unpack_from('<8i',arm,table-BASE))
    assert members==[2187,2188,-1,-1,2189,2190,2191,-1]
    def ref(r):return dict(block=r.block,offset=r.block_offset,copy_end=r.copy_end,bytes=len(r.text),record_index=r.record_index,table_offset=r.table_offset,start_in_record=r.start)
    context_rows=[dict(message_ID=n,source_reference=ref(jp[n]),source_hex=jp[n].text.hex(),source_Japanese=jp[n].text.decode('cp932'),
        current_reference=ref(en[n]),current_hex=en[n].text.hex(),current_English=en[n].text.decode('ascii'),
        contextual_read_only_no_editorial_completion_credit=True) for n in range(2187,2192)]
    labels=[]
    for row,label in [(next(r for r in search['historical_holds'] if r['message_id']==2229),'Historical role7 Search hold;not a shot'),
                      (next(r for r in search['historical_normal_returns'] if r['run']=='forage'),'Historical normal portrait dismissal/sea'),
                      (capture['historical_holds'][1],'Historical original regular capture handler'),
                      (capture['scoped_historical_cancellation_and_battle_transitions_freshly_rechecked'][-1],'Historical rewards/cargo return;same callee')]:
        path=Path(row['capture']);assert sha(path.read_bytes())==row['capture_sha256'];evidence[str(path)]=row['capture_sha256']
        labels.append(dict(path=str(path),sha256=row['capture_sha256'],label=label))
    ROOT.mkdir(parents=True)
    sheet=Image.new('RGB',(512,820),'#263238');draw=ImageDraw.Draw(sheet)
    for i,r in enumerate(labels):
        x,y=i%2*256,i//2*410;draw.text((x+2,y+3),r['label'][:40],fill='white');sheet.paste(Image.open(r['path']).convert('RGB'),(x,y+24))
    sheetpath=ROOT/'historical_representative_scope.png';sheet.save(sheetpath)
    save(ROOT/'representative_family_and_transition_reconciliation.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),evidence=evidence,
        exact_source_current_and_two_historical_control_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],
        historical_actual_role7_ID=2229,historical_actual_regular_outcome_ID=2011,
        actual_admiral_shot_IDs=[],new_emulator_runs=0,
        current_native_shot_IDs=list(range(1924,1931)),current_original_role7_voice_pipelines=8,
        focused_post_report_cleanup_and_regular_special_dispatch_proof=str(RETURN),
        preceding_call_1096F8_unchanged_and_before_text_not_a_new_text_consumer=True,
        original_UI_construction_dismissal_and_return_code_exact_to_clean_and_both_representative_builds=True,
        regular_capture_reward_cargo_return_reuses_original_72368_mode0=True,
        special_B5_handler_dispatch_tested_offline_no_individual_activation_claim=True,
        special_handler_context=dict(table=table,members=members,records=context_rows,
            original_argument='Virtual method+4 on the original enemy mobile returns its ship name;the original53D44 role1 call passes that pointer as%s.',
            context='Named-target defeat reports,not a named human admiral or assertion of death. The original handler continues into its existing result/reward flow.',
            separate_full_editorial_native_and_actual_scope_pending=True,completion_credit_added=0),
        risk_resolution='The seven translations introduce no new display/control behavior. All seven complete current native paragraphs and all eight original role7 selector/loader/printf/formatter paths pass. Existing actual role7 portrait holds/dismissal and actual regular capture/rewards/cargo/sailing establish the shared presentation and callee behavior;their UI/caller code is clean/current/historical exact. Focused copied-state execution verifies the only distinct post-report cleanup and original outcome dispatch,with synthetic header tests disclosed separately. The original pre-report call is unchanged and precedes text. No current or historical individual shot activation is claimed. Under the user representative-sampling policy,an additional conditional shot visit is not required to complete these seven unchanged paragraphs. Generic chance eligibility is source-bound and tested separately;offline comparison inputs are not earned qualifications or original RNG draws.',
        no_open_translation_specific_display_or_transition_finding=True,
        no_claim_that_two_outcome_branches_were_both_individually_activated=True,
        completed_prior_fixture_input_and_pixel_audits_hash_bound_without_repeating_them=True,
        new_companion_prose_lead_IDs=list(range(2187,2192)),companion_context_credit_added=0,
        review_sheet=str(sheetpath),review_sheet_sha256=sha(sheetpath.read_bytes()),visual_review_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Representative role7/portrait and original capture-return evidence bound to current cleanup/dispatch tests;shot7 has no remaining translation-specific transition finding. Zero individually activated shot claims;five companion context leads remain separate.')
