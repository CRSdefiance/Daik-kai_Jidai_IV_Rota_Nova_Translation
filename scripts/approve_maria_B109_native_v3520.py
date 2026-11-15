"""Seal source/context/prose/display gates after the explicitly scoped actual test."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.dialogue import maria_B109_layout_v2 as codec
from dk4tool.dialogue.maria_B109_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/maria_B109_native_approval_v3520')
INPUT=Path('translations/maria_B109_editorial_manuscript_v8.json')
OUTPUT=Path('translations/maria_B109_editorial_manuscript_v9.json')
FONT=Path('work/analysis/maria_B109_fonts_v3515/current_macro_QA_and_progressive_font_proof.json')
STORED=Path('work/analysis/maria_B109_stored_target_v3518/all26_stored_objects104_macro_cases14_formatter_guards_and_viewed_sheets.json')
ACTUAL=Path('work/analysis/maria_B109_B33_actual_v3519/terminal_B33_fixture_commands_and_actual_native_planes.json')
PLAN=Path('work/analysis/maria_B109_B33_fixture_v3516/B109_source_owned_relocation_and_B33_entry_fixture.json')
ROM=ROOT/'Maria_B109_only_full_V3487_derived_RESEARCH_ONLY.nds'

if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=deepcopy(read(INPUT));font,stored,actual,plan=map(read,[FONT,STORED,ACTUAL,PLAN])
    assert font['manuscript_sha256']==stored['manuscript_sha256']==plan['manuscript_sha256']==sha(INPUT.read_bytes())
    assert len(font['cases'])==26 and font['current_original_macro_alignment_calls']==208 and stored['stored_target_macro_alignment_cases']==104
    assert len(stored['source_bound_formatter_negatives'])==14 and len(font['negative_controls'])==17
    assert all(r['rejected'] for r in stored['source_bound_formatter_negatives']+font['negative_controls'])
    assert actual['complete_matching_panels']==actual['complete_matching_holds']==26 and not actual['unmatched_capture_planes']
    assert actual['source_event109_not_selected_or_earned'] and actual['B109_content_in_B33_entry_fixture_only']
    assert len(actual['representative_contact_sheets'])==6
    for s in actual['representative_contact_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    source_return=[];photos=[]
    for v in actual['versions']:
        assert v['all34_source_command_shapes_and_normal_exit'] and v['all26_speeches_observed'] and v['source_UI_prefix_4500_4684_pause_and_C200_executed']
        report=read(v['capture_report']);p=next(p for p in report['frames_captured'] if p['frame']==20200);assert sha(Path(p['path']).read_bytes())==p['PNG_sha256']
        pic=Image.open(p['path']).convert('RGB');photos.append(pic)
        pairs=[r for r in v['original_commands'] if r['block']==33];assert pairs[-2]['word']==0xC200 and pairs[-2]['start']==19619 and pairs[-2]['returned']==19620 and pairs[-1]['word']==0 and pairs[-1]['returned']==19620
        source_return.append(dict(case=v['case'],normal_Hangzhou_frame=20200,capture=p['path'],capture_sha256=p['PNG_sha256'],C200=pairs[-2],normal_exit=pairs[-1],viewed=True))
    assert photos[0].tobytes()==photos[1].tobytes(),'Immediate post-C200 source/English town frame must match.'
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC3.DK4')).blocks
    assert sha(Path(doc['current_ROM']).read_bytes())==font['candidate_sha256']==doc['current_ROM_sha256']
    assert sha(arm)==font['ARM9_sha256']==doc['required_runtime_ARM9_sha256']
    cases=[]
    for c in font['cases']:
        assert c['complete_native_independent216x64_plane_equal'] and c['all_first_final_internal_glyphs_in_order_and_unique_cells'] and c['all_visible_origins_zero_and16px_rows_within4rows']
        cases.append({**c,'consumer':'progressive','macro_cases':[x for p in c['current_native_macro_pipelines'] for x in p['cases']],'native_font_plane_sha256':c['whole_native_plane_sha256'],'whole_native_independent_font_plane_exact':True})
    byid={c['id']:c for c in cases};obsolete=[];invariants=[]
    for r in doc['records']:
        encoded=codec.encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'],profile_for(arm,blocks[109]));c=byid[r['id']]
        assert encoded.encoded.hex()==r['compiled_hex']==c['encoded_hex'] and semantic_tokens(r['english'])==semantic_tokens(encoded.formatted_markup)
        if r.get('qa_waivers') and not any(d.code=='line-break-count' for d in encoded.diagnostics):
            assert r['qa_waivers']==['line-break-count'];reason=r['qa_waiver_reason'];obsolete.append(dict(id=r['id'],old_reason=reason));r['localization_note']=r['localization_note'].replace(reason,'').rstrip();r.pop('qa_waivers');r.pop('qa_waiver_reason')
        r['review']['formatting']=True
        r.update(record_index=r['current_record_index'],current_text_hex=r['current_hex'],native_font_case=c,native_formatting_consumer='progressive',current_complete_native_display_pending=False,current_voice_macro_entry_conditional_and_whole_exchange_gloss_comparison_pending=False,current_macro_dispatch_consumer_and_complete_native_display_pending=False,status='all-five-editorial-gates-approved;registered-integration-pending',focused_actual_display_proof=str(ACTUAL),focused_actual_B33_entry_content_fixture=True,source_event109_natural_activation_not_claimed=True)
        invariants.append(dict(id=r['id'],source_speaker_macro_order_and_complete_English_tokens_exact=True,encoded_sha256=sha(encoded.encoded)))
    assert Counter(r['editorial_decision'] for r in doc['records'])=={'revise':16,'retain-wording':10}
    assert all(r.get('qa_waivers') in [None,['line-break-count']] for r in doc['records']);notes=sum(bool(r.get('qa_waivers')) for r in doc['records']);assert notes==5
    ROOT.mkdir(parents=True);sheet=Image.new('RGB',(1024,768),'#263238');draw=ImageDraw.Draw(sheet)
    for x,v in enumerate(actual['versions']):
        report=read(v['capture_report'])
        for y,frame in enumerate([4000,20200]):
            p=next(p for p in report['frames_captured'] if p['frame']==frame);pic=Image.open(p['path']).convert('RGB');sheet.paste(pic.resize((512,384)),(x*512,y*384));draw.text((x*512+3,y*384+3),v['case']+' / '+str(frame),fill='red')
    sheetpath=ROOT/'viewed_setup_and_immediate_normal_Hangzhou_return.png';sheet.save(sheetpath)
    merged=ROOT/'all26_native_macro_font_and_source_reconciliation.json'
    evidence={str(p):sha(p.read_bytes()) for p in [FONT,STORED,ACTUAL,PLAN,Path(font['reused_proof'])]}
    save(merged,dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),manuscript=str(INPUT),manuscript_sha256=sha(INPUT.read_bytes()),cases=cases,current_original_macro_alignment_calls=208,macro_count_includes_hash_bound_prior_cases=True,all26_current_native_speech_planes_pass=True,source_bound_formatter_negatives=stored['source_bound_formatter_negatives'],source_consumer_negative_controls=font['negative_controls'],source_English_macro_control_invariants=invariants,review_sheets=stored['review_sheets'],obsolete_row_count_notes_removed=obsolete,evidence=evidence,all5_actual_English_panel_sheets_and_setup_transition_sheet_viewed=True,actual_panels26_complete=True,source_restored_4500_config8_0_0_and_4684_pause_C200_actual_executed=True,source_and_English_immediate_normal_Hangzhou_return_exact=source_return,incidental_later_sailing_frames_not_scene_return_evidence=True,B109_content_tested_in_B33_entry_only=True,event109_eligibility_natural_activation_and_earned_progression_unclaimed=True,wordless_three_periods_complete_at_origin=True,no_new_ledger_review_or_completion_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),native_font_proof=str(merged),native_font_proof_sha256=sha(merged.read_bytes()),native_progressive_proof=str(FONT),formatting_review_pending=False,all26_five_review_gates_true=True,focused_actual_display_proof=str(ACTUAL),focused_actual_display_proof_sha256=sha(ACTUAL.read_bytes()),source_restored_control_prefix_actual_display_and_transition_approved=True,status='source-prose-current-native-format-approved;registered-integration-pending')
    validate_natural_dialogue_batch(doc);save(OUTPUT,doc)
    target=Path(plan['target_block']).read_bytes();assert sha(target)==plan['target_block_sha256'];container=IlnkContainer.parse(image.read_file('/data/SC3.DK4'));container.blocks[109]=target;image.replace_file('/data/SC3.DK4',container.to_bytes());image.save(ROM)
    parent=NdsImage.open(doc['current_ROM']);result=NdsImage.open(ROM)
    assert [p for _,p,v in parent.iter_files() if result.read_file(p)!=v]==['/data/SC3.DK4'] and all(result.read_file(p)==v for p,v in parent.iter_components())
    a,b=[IlnkContainer.parse(im.read_file('/data/SC3.DK4')).blocks for im in [parent,result]];assert len(a)==len(b)==303 and [n for n,(x,y) in enumerate(zip(a,b,strict=True)) if x!=y]==[109]
    save(ROOT/'approval_and_production_scope_research_receipt.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),parent=doc['current_ROM'],parent_sha256=doc['current_ROM_sha256'],research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),merged_native_proof=str(merged),merged_native_proof_sha256=sha(merged.read_bytes()),plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),all26_five_review_gates_true=True,revised=16,retained=10,narrow_row_count_notes=notes,source_consumer_negatives=17,formatter_negatives=14,stored_target_macro_cases=104,complete_actual_content_panels=26,source_event109_not_selected=True,all302_other_SC3_blocks_every_other_file_component_exact=True,only_SC3_B109_differs_from_full_V3487=True,existing_promotion_unchanged=True,registration_loader_references_and_release_pending=True,no_ledger_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(approved=26,revised=16,retained=10,row_count_notes=notes,actual_fixture_panels=26,only_B109_research_ROM=True,credit=0))
