"""Seal63 contextual format gates,including the narrowly proven source00 prefix."""
from collections import Counter
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue import lil_B131_B133_layout_v2 as codec
from dk4tool.dialogue.lil_B131_B133_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B131_B133_native_approval_v3326')
INPUTS=[Path('translations/lil_B131_B133_editorial_manuscript_v3.json'),Path('translations/lil_B131_B133_choice_manuscript_v4.json')]
OUTPUTS=[Path('translations/lil_B131_B133_editorial_manuscript_v4.json'),Path('translations/lil_B131_B133_choice_manuscript_v5.json')]
FONT=Path('work/analysis/lil_B131_B133_fonts_v3324b/current_macro_QA_and_progressive_font_proof.json')
FE=Path('work/analysis/lil_B131_B133_FE_v3325/current_FE_macro_font_and_typed_paper_proof.json')
MENU=Path('work/analysis/lil_B131_B133_choices_v3321c/all1_typed_menu_native_proof.json')
TYPED=Path('work/analysis/lil_B131_B133_typed_speech_v3323/all366_whole4000_commands_and108_source00_cases.json')
VISUAL=Path('work/analysis/lil_B131_B133_visual_refinement_v3322/all10_viewed_native_sheets_and_phrase_findings.json')
if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in OUTPUTS);doc,menu=[deepcopy(read(p)) for p in INPUTS];font,fe,menus,typed,visual=map(read,[FONT,FE,MENU,TYPED,VISUAL])
    assert font['manuscript_sha256']==fe['manuscript_sha256']==typed['manuscript_sha256']==sha(INPUTS[0].read_bytes())
    assert len(font['cases'])==60 and len(font['all61_full_QA_reports'])==61 and font['current_original_macro_alignment_calls']==480 and len(font['negative_controls'])==22 and all(r['rejected'] for r in font['negative_controls'])
    assert (font['newly_executed_font_cases'],font['reused_unchanged_font_cases'])==(3,57) and font['changed_IDs']==['DK4_MES_B133_R0008','DK4_MES_B133_R0129','DK4_MES_B133_R0178']
    assert sha(Path(font['reused_proof']).read_bytes())==font['reused_proof_sha256'];prior=read(font['reused_proof']);oldfe=read('work/analysis/lil_B131_B133_FE_v3320/current_FE_macro_font_and_typed_paper_proof.json');assert visual['all8_progressive_one_FE_one_choice_sheets_viewed'];sheets=[]
    for kind,current,old,viewed in [('progressive',font,prior,{2,6,7}),('FE-paper',fe,oldfe,set())]:
        changed={i for i,(a,b) in enumerate(zip(old['review_sheets'],current['review_sheets'],strict=True),1) if a['sha256']!=b['sha256']};assert changed==viewed,(kind,changed)
        for i,s in enumerate(current['review_sheets'],1):
            assert sha(Path(s['path']).read_bytes())==s['sha256']
            if i not in changed:assert any(v['sha256']==s['sha256'] for v in visual['sheets'])
            sheets.append({**s,'review':'viewed final successor with phrase finding resolved' if i in changed else 'hash-identical to viewed predecessor'})
    assert len(fe['cases'])==1 and fe['current_original_null_actor_macro_alignment_cases']==8 and not fe['source_leading_vertical_staging_cases'] and not fe['source_FI_null_actor_cases'] and fe['all1_one_native_page_consumes_complete_target'] and fe['all1_complete_native_independent_planes_all_glyphs_and_canaries_equal'] and fe['historical_calibration']['current_calibration_matches_complete_historical_ink_and_blank_mask']
    assert len(typed['cases'])==366 and sum(c['source_selector']==0 for c in typed['cases'])==108 and typed['all108_source00_cases_forward_nonempty_body_after_selector_to_original_display']
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;assert sha(arm)==doc['required_runtime_ARM9_sha256']
    for proof in [font,fe]:
        assert proof['candidate_sha256']==doc['current_ROM_sha256'] and proof['ARM9_sha256']==sha(arm) and proof['COMMON_sha256']==sha(common) and Path(proof['native_formatter_module'])==Path(doc['native_formatter_module']) and sha(Path(proof['native_formatter_module']).read_bytes())==proof['native_formatter_module_sha256']==doc['native_formatter_module_sha256']
    assert sha(Path(font['scoped_profile']).read_bytes())==font['scoped_profile_sha256']==doc['scoped_profile_module_sha256']
    cases=[];invariants=[]
    for c in font['cases']:
        assert c['complete_native_independent216x64_plane_equal'] and c['all_first_final_internal_glyphs_in_order_and_unique_cells']
        cases.append({**c,'consumer':'progressive','macro_cases':[v for p in c['current_native_macro_pipelines'] for v in p['cases']],'native_font_plane_sha256':c['whole_native_plane_sha256'],'whole_native_independent_font_plane_exact':True})
    for c in fe['cases']:
        assert c['one_native_page_consumes_complete_target'] and c['complete_native_independent_plane_and_all_glyphs_and_canaries_equal'] and sha(Path(c['native_plane']).read_bytes())==c['native_plane_sha256']
        cases.append({**c,'consumer':'FE-paper','macro_cases':[v for p in c['current_native_macro_pipelines'] for v in p['cases']],'native_font_plane_sha256':c['native_plane_sha256'],'whole_native_independent_font_plane_exact':True,'logical_geometry':[228,48],'physical_row_advance':16})
    assert len(cases)==61 and sum(len(c['macro_cases']) for c in cases)==488;byid={c['id']:c for c in cases}
    for row in doc['records']:
        raw=bytes.fromhex(row['source_hex']);c=byid[row['id']];encoded=codec.encode_relocatable_dialogue(raw,row['english'],profile_for(arm,blocks[row['block']],c['consumer']))
        assert encoded.encoded.hex()==row['compiled_hex']==c['encoded_hex'] and encoded.encoded[0]==row['source_selector'] and b'\0' not in encoded.encoded[1:]
        assert (b'\0' in encoded.encoded)==(row['source_selector']==0) and semantic_tokens(row['english'])==semantic_tokens(encoded.formatted_markup) and sha(Path(c['preview']).read_bytes())==c['preview_sha256']
        row['review']['formatting']=True;row.update(record_index=row['current_record_index'],current_text_hex=row['current_hex'],native_font_case=c,native_formatting_consumer=c['consumer'],current_complete_native_display_pending=False,status='source-prose-current-native-format-approved;relocation-representative-release-pending')
        invariants.append(dict(id=row['id'],source_speaker_macro_order_and_complete_English_tokens_exact=True,encoded_sha256=sha(encoded.encoded),consumer=c['consumer'],only_proven_source00_prefix_can_be_NUL=row['source_selector']==0))
    menu_targets={};assert len(menus['menus'])==1 and menus['native_selection_cancel_cases']==6 and menus['complete_current_and_reviewed_style_label_planes']==8
    for m in menus['menus']:
        assert sha(Path(m['proof']).read_bytes())==m['sha256'];proof=read(m['proof']);assert proof['candidate_sha256']==doc['current_ROM_sha256'] and proof['source_context_sha256']==doc['source_context_sha256'] and proof['source_count2_results0_1_and_cancel_explicit'] and proof['six_original_VM_selection_and_cancel_cases_pass'] and proof['eight_complete_native_style_label_planes_pass']
        for c in proof['current_and_reviewed_VM_and_font_cases']:
            vm=c['native_VM_getters_geometry_and_selection'];assert [v['modal_selection'] for v in vm['VM_cases']]==[0,1,-1] and len(c['all_four_style_label_planes'])==4 and all(p['storage_padding_all_blank'] and p['independent_complete_native_pixels_match'] for p in c['all_four_style_label_planes'])
            if c['version']=='reviewed-research':
                assert c['source_derived_text_canvas_width']==108;menu_targets[proof['block'],proof['original_command_offset']]=dict(object_hex=proof['typed_target_object_hex'],labels=vm['labels'],native_geometry=vm['native_menu_rectangle'])
        assert sha(Path(m['review_sheet']).read_bytes())==m['review_sheet_sha256'] and any(v['sha256']==m['review_sheet_sha256'] for v in visual['sheets']);sheets.append(dict(path=m['review_sheet'],sha256=m['review_sheet_sha256'],review='viewed complete current/reviewed labels;18-cell acceptance preserves all leading H pixels'))
    for row in menu['records']:
        target=menu_targets[row['block'],row['command_offset']];assert row['english']==target['labels'][row['option_index']] and row['compiled_hex']==row['english'].encode('ascii').hex();row['review']['formatting']=True
        row.update(native_choice_proof=str(MENU),native_choice_proof_sha256=sha(MENU.read_bytes()),typed_target_object_hex=target['object_hex'],native_menu_rectangle=target['native_geometry'],choice_consumer_selection_geometry_native_display_pending=False,current_complete_native_display_pending=False,actual_selection_gameplay_claimed=False,status='source-prose-current-native-two-option-format-approved;relocation-representative-release-pending')
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as error:negatives.append(dict(case=label,rejected=True,error=str(error)))
        else:raise AssertionError(label)
    for consumer in ['progressive','FE-paper']:
        row=next(r for r in doc['records'] if (r['kind']=='system-FE')==(consumer=='FE-paper'));raw=bytes.fromhex(row['source_hex']);profile=profile_for(arm,blocks[row['block']],consumer)
        for label,p in [('width',replace(profile,window_width_px=228)),('rows',replace(profile,max_lines=5)),('glyph',replace(profile,default_ascii_width=5)),('row-spacing',replace(profile,line_height_px=12)),('disabled-LF-guard',replace(profile,guard_linebreaks=False)),('disabled-pair-phase',replace(profile,pair_phase_safe_breaks=False)),('disabled-balancing',replace(profile,balanced_wrapping=False)),('macro-width',replace(profile,macro_ascii_lengths={**profile.macro_ascii_lengths,'FO':10})),('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:reject(consumer+'-'+label,lambda p=p:codec.encode_relocatable_dialogue(raw,row['english'],p))
        for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:reject(consumer+'-manual-or-end-'+tag,lambda tag=tag:codec.encode_relocatable_dialogue(raw,row['english']+tag,profile))
        reject(consumer+'-widened-selectors',lambda:codec.encode_relocatable_dialogue(raw,row['english'],replace(profile,leading_speaker_bytes=profile.leading_speaker_bytes|{148})))
    rows=doc['records']+menu['records'];assert len(negatives)==28 and len(sheets)==10 and len(rows)==63 and Counter(r['editorial_decision'] for r in rows)=={'revise':27,'retain-wording':36} and sum(bool(r.get('qa_waivers')) for r in rows)==19 and all(r.get('qa_waivers') in [None,['line-break-count']] for r in rows)
    ROOT.mkdir(parents=True);merged=ROOT/'all63_native_macro_font_choice_and_source00_reconciliation.json'
    save(merged,dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),manuscripts={str(p):sha(p.read_bytes()) for p in INPUTS},cases=cases,menu_targets=[dict(block=k[0],command_offset=k[1],**v) for k,v in menu_targets.items()],current_original_macro_alignment_calls=488,all61_current_native_speech_planes_and_two_menu_labels_pass=True,review_sheets=sheets,source_English_macro_control_invariants=invariants,source_bound_formatter_negatives=negatives,source_consumer_negative_controls=font['negative_controls'],whole_typed_command_proof=str(TYPED),whole_typed_command_proof_sha256=sha(TYPED.read_bytes()),all366_whole4000_commands_and108_source00_cases_pass=True,shared_encoder_still_rejects_NUL_and_only_exact_source00_profile_allows_one_prefix=True,native_leading_H_menu_finding_resolved_without_padding_or_waiver=True,no_new_gameplay_orcompletion_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    for d,old,new in zip([doc,menu],INPUTS,OUTPUTS,strict=True):
        d.update(previous_manuscript=str(old),previous_manuscript_sha256=sha(old.read_bytes()),prose_companions=[str(p) for p in OUTPUTS if p!=new],native_font_proof=str(merged),native_font_proof_sha256=sha(merged.read_bytes()),native_progressive_proof=str(FONT),native_FE_proof=str(FE),native_choice_proof=str(MENU),whole_typed_speech_proof=str(TYPED),whole_typed_speech_proof_sha256=sha(TYPED.read_bytes()),formatting_review_pending=False,all63_five_review_gates_true=True,formatter_phrase_flow_findings_resolved_without_waiver=True,status='source-prose-current-native-format-approved;relocation-representative-release-pending')
        validate_natural_dialogue_batch(d);save(new,d)
    save(ROOT/'approval_receipt.json',dict(manuscripts={str(p):sha(p.read_bytes()) for p in OUTPUTS},manuscript=str(OUTPUTS[0]),manuscript_sha256=sha(OUTPUTS[0].read_bytes()),choices=str(OUTPUTS[1]),choices_sha256=sha(OUTPUTS[1].read_bytes()),merged_native_proof=str(merged),merged_native_proof_sha256=sha(merged.read_bytes()),all63_five_review_gates_true=True,progressive_planes=60,FE_planes=1,choice_labels=2,two_option_menus=1,current_macro_alignment_cases=488,source_consumer_negatives=22,formatter_negatives=28,narrow_row_count_notes=19,review_sheets=sheets,revised=27,retained=36,source00_speeches=18,whole_typed_command_cases=366,whole_source00_cases=108,native_leading_H_choice_finding_resolved=True,actual_selected_B131_B133_IDs=[],new_emulator_runs=0,relocation_representative_registered_release_pending=True,source_prose_orcompletion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('All63 five review gates pass:27 revisions/36retentions,60 progressive/one FE/two labels,488macro cases,366 typedcommands/108source00cases,22consumer/28formatter negatives,10viewed/hash-exact sheets. Relocation/release pending.')
