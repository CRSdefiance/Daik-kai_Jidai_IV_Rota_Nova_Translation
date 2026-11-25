"""Seal44 source/context/localization/naturalness/formatting reviews with exact speech andmenu evidence."""
from collections import Counter
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue import lil_B166_layout_v4 as codec
from dk4tool.dialogue.lil_B166_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B166_native_approval_v4082')
INPUTS=[Path('translations/lil_B166_editorial_manuscript_v4.json'),Path('translations/lil_B166_choice_manuscript_v1.json')]
OUTPUTS=[Path('translations/lil_B166_editorial_manuscript_v5.json'),Path('translations/lil_B166_choice_manuscript_v2.json')]
FONT=Path('work/analysis/lil_B166_fonts_v4081b/current_macro_QA_and_progressive_font_proof.json')
MENU=Path('work/analysis/lil_B166_choices_v4080/B166_C2152/original_choice_decoder_VM_geometry_and_native_pixels.json')
ACTUAL=Path('work/analysis/lil_B166_actual_menu_v4079/complete_current_reviewed_caption_masks_and_native_backing.json')
OWNER=Path('work/analysis/lil_B166_menu_owner_trace_v4086/actual_caption_context_view_and_backing.json')
if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in OUTPUTS);doc,menu=map(lambda p:deepcopy(read(p)),INPUTS);font,choice,actual,owner=map(read,[FONT,MENU,ACTUAL,OWNER]);assert font['manuscript_sha256']==sha(INPUTS[0].read_bytes()) and choice['manuscript_sha256']==sha(INPUTS[1].read_bytes())
    assert len(font['cases'])==42 and font['current_original_macro_alignment_calls']==336 and font['new_current_original_macro_alignment_calls']==4 and font['reused_original_macro_alignment_calls']==332 and len(font['negative_controls'])==17
    assert choice['six_original_VM_selection_and_cancel_cases_pass'] and choice['eight_complete_native_style_label_planes_pass'] and len(bytes.fromhex(choice['typed_target_object_hex']))==24
    assert actual['actual_four_full_frames_and_eight_complete_caption_masks_pass'] and actual['captured_actual_native_caption_bitmap_256x36_backing_and54x12_views_bound'] and not owner['errors'] and len(owner['rows'])==5
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==font['candidate_sha256']==choice['candidate_sha256'] and sha(arm)==doc['required_runtime_ARM9_sha256']==font['ARM9_sha256']
    prior=read('work/analysis/lil_B166_fonts_v4081/current_macro_QA_and_progressive_font_proof.json');sheets=[]
    for i,s in enumerate(font['review_sheets']):
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        if i<5:assert s['sha256']==prior['review_sheets'][i]['sha256']
        sheets.append({**s,'review':'Viewed complete final native sheet;all reviewed words andglyphs intact. Phrase boundaries preserve complete care object,active-crew comparison,room names,food/water group andfinal care-it-deserves instruction.' if i==5 else 'Viewed complete predecessor sheet;final sheet hash is identical. Phrase-flow refinements andall leading/internal/final glyphs remain intact.'})
    assert len(sheets)==6;assert sha(Path(choice['visual_review_sheet']).read_bytes())==choice['visual_review_sheet_sha256'] and sha(Path(actual['review_sheet']).read_bytes())==actual['review_sheet_sha256']
    menusheet=dict(path=choice['visual_review_sheet'],sha256=choice['visual_review_sheet_sha256'],review='Viewed complete current/reviewed native Please do andDecline labels. Reviewed labels preserve first/final/internal glyphs andsource option order,centered in unchanged logical widths onobserved backing. Actual matching masks/highlights are separately bound.')
    actualsheet=dict(path=actual['review_sheet'],sha256=actual['review_sheet_sha256'],review='Viewed allfour actual current/reviewed full screens atframes3000/3500. Initial P andcomplete labels are intact;ordinary DOWN moves highlight0 to1. No actual menu return orB166 story branch is claimed.')
    original={r['id']:r for r in read('translations/lil_B166_editorial_manuscript_v1.json')['records']};byid={r['id']:r for r in font['cases']};invariants=[]
    for r in doc['records']:
        assert all(r[k]==original[r['id']][k] for k in ['english','source_meaning','editorial_decision','source_hex','current_hex','source_complete_preamble_hex'])
        raw=bytes.fromhex(r['source_hex']);p=profile_for(arm,blocks[166]);c=byid[r['id']];encoded=codec.encode_relocatable_dialogue(raw,r['english'],p)
        assert encoded.encoded.hex()==r['compiled_hex']==c['encoded_hex'] and semantic_tokens(r['english'])==semantic_tokens(encoded.formatted_markup)
        assert c['complete_native_independent216x64_plane_equal'] and c['all_first_final_internal_glyphs_in_order_and_unique_cells'] and c['all_visible_origins_zero_and16px_rows_within4rows'] and sha(Path(c['preview']).read_bytes())==c['preview_sha256'] and sum(len(x['cases']) for x in c['current_native_macro_pipelines'])==8
        for macro in ['FI','FA','FO']:assert raw.count(macro.encode())==r['english'].count('{MACRO:'+macro+'}')
        qa=codec.audit_relocatable_dialogue_record(raw,r['english'],p);assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code']=='line-break-count' and r.get('qa_waiver_reason'))]
        r['review']['formatting']=True;r.update(record_index=r['current_record_index'],current_text_hex=r['current_hex'],native_font_case=c,native_formatting_consumer='progressive',native_plane_verified_not_actual_gameplay=True,current_complete_native_display_pending=False,current_native_voice_macro_entry_and_context_pending=False,status='source-prose-current-native-format-approved;relocation-references-story-representative-release-pending');invariants.append(dict(id=r['id'],block=166,source_selector=raw[0],whole_source_English_tokens_and_control_order_preserved=True,encoded_sha256=sha(encoded.encoded)))
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as e:negatives.append(dict(case=label,rejected=True,error=str(e)))
        else:raise AssertionError(label)
    r=doc['records'][0];raw=bytes.fromhex(r['source_hex']);p=profile_for(arm,blocks[166])
    for label,bad in [('width',replace(p,window_width_px=228)),('rows',replace(p,max_lines=5)),('glyph',replace(p,default_ascii_width=5)),('row-spacing',replace(p,line_height_px=12)),('disabled-LF-guard',replace(p,guard_linebreaks=False)),('disabled-pair-phase',replace(p,pair_phase_safe_breaks=False)),('disabled-balancing',replace(p,balanced_wrapping=False)),('macro-width',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FA':6})),('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:reject(label,lambda bad=bad:codec.encode_relocatable_dialogue(raw,r['english'],bad))
    for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:reject('manual-or-end-'+tag,lambda tag=tag:codec.encode_relocatable_dialogue(raw,r['english']+tag,p))
    reject('widened-selectors',lambda:codec.encode_relocatable_dialogue(raw,r['english'],replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{149})));assert len(negatives)==14
    target=bytes.fromhex(choice['typed_target_object_hex']);assert [r['option_index'] for r in menu['records']]==[0,1] and [r['english'] for r in menu['records']]==['Please do','Decline']
    for r in menu['records']:r['review']['formatting']=True;r.update(typed_target_object_hex=target.hex(),compiled_hex=target.hex(),native_choice_proof=str(MENU),native_choice_proof_sha256=sha(MENU.read_bytes()),choice_consumer_selection_geometry_native_display_pending=False,actual_highlight_association_in_menu_only_fixture_verified=True,actual_choice_selection_still_pending=True,status='source-prose-current-native-format-approved;relocation-references-story-representative-release-pending')
    allrows=doc['records']+menu['records'];assert Counter(r['editorial_decision'] for r in allrows)=={'revise':24,'retain-wording':20} and sum(bool(r.get('qa_waivers')) for r in doc['records'])==15
    for r in allrows:
        if r['editorial_decision']=='retain-wording':assert r['english'].removeprefix('{SPEAKER:'+format(r.get('source_selector',0),'02X')+'}')==r['effective_predecessor_paragraph'] and r['fresh_retained_wording_justification']
    namespath=Path(doc['source_nameplate_consumer_proof']);names=read(namespath);assert len(names['native_six_consumer_cases']['rows'])==6 and names['approved_prose_names']['23']=='Manuel Almeida' and names['later_older_record0D_reaudit_stays_open']
    assert all(r['all_actor_models_and_unowned4MiB_exact'] and r['source_owned_scratch_restoration_recovers_all4MiB'] for r in names['native_six_consumer_cases']['rows'])
    ROOT.mkdir(parents=True);merged=ROOT/'all44_native_speech_choice_source_and_actual_menu_reconciliation.json';evidencepaths=[*INPUTS,FONT,MENU,ACTUAL,OWNER,namespath,Path('work/analysis/lil_B166_menu_owner_trace_v4086/terminal.json'),Path('scripts/refine_lil_B166_viewed_flow_v4078.py'),Path('scripts/refine_lil_B166_viewed_flow_v4078b.py'),Path('scripts/refine_lil_B166_final_flow_v4078c.py'),Path(__file__)]
    save(merged,dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),manuscript=str(INPUTS[0]),manuscript_sha256=sha(INPUTS[0].read_bytes()),cases=font['cases'],current_original_macro_alignment_calls=336,new_latest_macro_cases=4,exact_reused_latest_macro_cases=332,all42_current_native_speech_planes_pass=True,review_sheets=sheets,choice_review_sheet=menusheet,actual_menu_review_sheet=actualsheet,source_English_macro_control_invariants=invariants,source_bound_formatter_negatives=negatives,source_consumer_negative_controls=font['negative_controls'],typed_choice_proof=str(MENU),typed_choice_proof_sha256=sha(MENU.read_bytes()),actual_menu_proof=str(ACTUAL),actual_menu_proof_sha256=sha(ACTUAL.read_bytes()),actual_menu_owner_proof=str(OWNER),actual_menu_owner_proof_sha256=sha(OWNER.read_bytes()),actual_menu_only_new_cold_boot_runs=3,actual_B166_speeches_or_choice_returns_or_natural_source_event_claimed=False,all44_source_facts_complete_branches_and_individual_decisions_reconciled=True,source_FI3_and_all_four_static_actor_controls_preserved=True,no_ROM_label_padding_or_renderer_change_for_synthetic_menu_failure=True,later_older_record0D_reaudit_open=True,scoped_profile=doc['scoped_profile_module'],scoped_profile_sha256=doc['scoped_profile_module_sha256'],native_formatter_module=doc['native_formatter_module'],native_formatter_module_sha256=doc['native_formatter_module_sha256'],evidence={str(x):sha(x.read_bytes()) for x in evidencepaths},no_new_source_prose_or_completion_credit=True,full_goal_complete=False))
    for i,d in enumerate([doc,menu]):
        d.update(previous_manuscript=str(INPUTS[i]),previous_manuscript_sha256=sha(INPUTS[i].read_bytes()),native_font_proof=str(merged),native_font_proof_sha256=sha(merged.read_bytes()),native_progressive_proof=str(FONT),formatting_review_pending=False,all44_five_review_gates_true=True,formatter_phrase_flow_findings_resolved_without_waiver=True,prose_companions=[str(OUTPUTS[1-i])],status='source-prose-current-native-format-approved;relocation-references-story-representative-release-pending');validate_natural_dialogue_batch(d);save(OUTPUTS[i],d)
    save(ROOT/'approval_receipt.json',dict(manuscripts={str(p):sha(p.read_bytes()) for p in OUTPUTS},merged_native_proof=str(merged),merged_native_proof_sha256=sha(merged.read_bytes()),revised=24,retained=20,progressive_planes=42,current_macro_alignment_cases=336,source_consumer_negatives=17,formatter_negatives=14,menu_selection_cancel_cases=6,menu_style_label_planes=8,narrow_row_count_notes=15,review_sheets=sheets,choice_review_sheet=menusheet,actual_menu_review_sheet=actualsheet,actual_menu_only_cold_boot_runs=3,actual_selected_B166_IDs=[],actual_B166_speech_or_choice_return_coverage_added=0,new_emulator_runs_added_by_approval=0,relocation_references_story_representative_registered_release_pending=True,new_source_prose_reviews=0,new_completed_records=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('44 five-gate reviews approved:24 revisions/20 retentions;42planes/336cases,17+14negatives,menu6returns/8planes andactual focused menu backing resolved. Story/release pending;no credit yet.')
