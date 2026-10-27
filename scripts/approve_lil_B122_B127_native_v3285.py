"""Seal all159 contextual formatting reviews; release gates remain pending."""
from collections import Counter
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue import lil_B122_B127_layout_v2 as codec
from dk4tool.dialogue.lil_B122_B127_profile_v2 import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B122_B127_native_approval_v3285')
INPUTS=[Path('translations/lil_B122_B127_editorial_manuscript_v4.json'),Path('translations/lil_B122_B127_choice_manuscript_v3.json')]
OUTPUTS=[Path('translations/lil_B122_B127_editorial_manuscript_v5.json'),Path('translations/lil_B122_B127_choice_manuscript_v4.json')]
FONT=Path('work/analysis/lil_B122_B127_fonts_v3283/current_macro_QA_and_progressive_font_proof.json')
FE=Path('work/analysis/lil_B122_B127_FE_v3284/current_FE_macro_font_and_typed_paper_proof.json')
MENU=Path('work/analysis/lil_B122_B127_choices_v3279/all2_typed_menu_native_proof.json')
VISUAL=Path('work/analysis/lil_B122_B127_visual_refinement_v3280/all23_viewed_native_sheets_and_phrase_findings.json')

if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in OUTPUTS)
    doc,menu=map(lambda p:deepcopy(read(p)),INPUTS);font,fe,menus,visual=map(read,[FONT,FE,MENU,VISUAL])
    assert font['manuscript_sha256']==fe['manuscript_sha256']==sha(INPUTS[0].read_bytes())
    assert len(font['cases'])==145 and len(font['all155_full_QA_reports'])==155 and font['current_original_macro_alignment_calls']==1160
    assert len(font['negative_controls'])==23 and all(r['rejected'] for r in font['negative_controls'])
    assert (font['newly_executed_font_cases'],font['reused_unchanged_font_cases'])==(5,140)
    assert font['changed_IDs']==['DK4_MES_B124_R0005','DK4_MES_B124_R0016','DK4_MES_B126_R0061','DK4_MES_B127_R0089','DK4_MES_B127_R0107']
    assert sha(Path(font['reused_proof']).read_bytes())==font['reused_proof_sha256']
    prior=read(font['reused_proof']);oldfe=read('work/analysis/lil_B122_B127_FE_v3278/current_FE_macro_font_and_typed_paper_proof.json')
    assert visual['all19_progressive_two_FE_and_two_choice_sheets_viewed']
    sheets=[]
    for kind,current,old,viewed in [('progressive',font,prior,{4,5,13,17}),('FE-paper',fe,oldfe,{1})]:
        changed={i for i,(a,b) in enumerate(zip(old['review_sheets'],current['review_sheets'],strict=True),1) if a['sha256']!=b['sha256']}
        assert changed==viewed,(kind,changed)
        for i,s in enumerate(current['review_sheets'],1):
            assert sha(Path(s['path']).read_bytes())==s['sha256']
            if i not in changed:assert any(v['sha256']==s['sha256'] for v in visual['sheets'])
            sheets.append({**s,'review':'viewed final successor; phrase finding resolved' if i in changed else 'hash-identical to viewed predecessor'})
    assert len(fe['cases'])==10 and fe['current_original_null_actor_macro_alignment_cases']==80
    assert len(fe['source_leading_vertical_staging_cases'])==7 and len(fe['source_FI_null_actor_cases'])==3
    assert fe['all10_one_native_page_consumes_complete_target'] and fe['all10_complete_native_independent_planes_all_glyphs_and_canaries_equal']
    assert fe['historical_calibration']['current_calibration_matches_complete_historical_ink_and_blank_mask'] and fe['no_initialized_historical_RAM_ITCM_or_DTCM_overlay_in_painter']
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    assert sha(arm)==doc['required_runtime_ARM9_sha256']
    for proof in [font,fe]:
        assert proof['candidate_sha256']==doc['current_ROM_sha256'] and proof['ARM9_sha256']==sha(arm) and proof['COMMON_sha256']==sha(common)
        assert Path(proof['native_formatter_module'])==Path(doc['native_formatter_module']) and sha(Path(proof['native_formatter_module']).read_bytes())==proof['native_formatter_module_sha256']==doc['native_formatter_module_sha256']
    assert sha(Path(font['scoped_profile']).read_bytes())==font['scoped_profile_sha256']==doc['scoped_profile_module_sha256']
    cases=[];invariants=[]
    for c in font['cases']:
        assert c['complete_native_independent216x64_plane_equal'] and c['all_first_final_internal_glyphs_in_order_and_unique_cells']
        cases.append({**c,'consumer':'progressive','macro_cases':[v for p in c['current_native_macro_pipelines'] for v in p['cases']],'native_font_plane_sha256':c['whole_native_plane_sha256'],'whole_native_independent_font_plane_exact':True})
    for c in fe['cases']:
        assert c['one_native_page_consumes_complete_target'] and c['complete_native_independent_plane_and_all_glyphs_and_canaries_equal']
        assert sha(Path(c['native_plane']).read_bytes())==c['native_plane_sha256']
        cases.append({**c,'consumer':'FE-paper','macro_cases':[v for p in c['current_native_macro_pipelines'] for v in p['cases']],'native_font_plane_sha256':c['native_plane_sha256'],'whole_native_independent_font_plane_exact':True,'logical_geometry':[228,48],'physical_row_advance':16})
    assert len(cases)==155 and sum(len(c['macro_cases']) for c in cases)==1240
    byid={c['id']:c for c in cases}
    for row in doc['records']:
        raw=bytes.fromhex(row['source_hex']);c=byid[row['id']]
        result=codec.encode_relocatable_dialogue(raw,row['english'],profile_for(arm,blocks[row['block']],c['consumer']))
        assert result.encoded.hex()==row['compiled_hex']==c['encoded_hex'] and result.encoded[0]==row['source_selector']
        assert semantic_tokens(row['english'])==semantic_tokens(result.formatted_markup) and b'\0' not in result.encoded
        assert sha(Path(c['preview']).read_bytes())==c['preview_sha256']
        row['review']['formatting']=True
        row.update(record_index=row['current_record_index'],current_text_hex=row['current_hex'],native_font_case=c,native_formatting_consumer=c['consumer'],current_complete_native_display_pending=False,status='source-prose-current-native-format-approved;relocation-representative-release-pending')
        invariants.append(dict(id=row['id'],source_speaker_macro_order_and_complete_English_tokens_exact=True,encoded_sha256=sha(result.encoded),consumer=c['consumer']))
    menu_targets={}
    assert len(menus['menus'])==2 and menus['native_selection_cancel_cases']==12 and menus['complete_current_and_reviewed_style_label_planes']==16
    for m in menus['menus']:
        assert sha(Path(m['proof']).read_bytes())==m['sha256'];proof=read(m['proof'])
        assert proof['candidate_sha256']==doc['current_ROM_sha256'] and proof['source_context_sha256']==doc['source_context_sha256']
        assert proof['source_count2_results0_1_and_cancel_explicit'] and proof['six_original_VM_selection_and_cancel_cases_pass'] and proof['eight_complete_native_style_label_planes_pass']
        for d in proof['clean_current_reviewed_native_decoder_cases']:assert d['native_count']==2 and [r['stored_index'] for r in d['labels']]==[0,1]
        for c in proof['current_and_reviewed_VM_and_font_cases']:
            vm=c['native_VM_getters_geometry_and_selection'];assert [v['modal_selection'] for v in vm['VM_cases']]==[0,1,-1]
            assert len(c['all_four_style_label_planes'])==4 and all(p['storage_padding_all_blank'] and p['independent_complete_native_pixels_match'] for p in c['all_four_style_label_planes'])
            if c['version']=='reviewed-research':menu_targets[proof['block'],proof['original_command_offset']]=dict(object_hex=proof['typed_target_object_hex'],labels=vm['labels'],native_geometry=vm['native_menu_rectangle'])
        assert sha(Path(m['review_sheet']).read_bytes())==m['review_sheet_sha256'] and any(v['sha256']==m['review_sheet_sha256'] for v in visual['sheets'])
        sheets.append(dict(path=m['review_sheet'],sha256=m['review_sheet_sha256'],review='viewed current/reviewed two-option menu; final labels unchanged'))
    for row in menu['records']:
        target=menu_targets[row['block'],row['command_offset']];assert row['english']==target['labels'][row['option_index']] and row['compiled_hex']==row['english'].encode('ascii').hex()
        row['review']['formatting']=True
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
    assert len(negatives)==28 and len(sheets)==23
    rows=doc['records']+menu['records'];assert len(rows)==159 and Counter(r['editorial_decision'] for r in rows)=={'revise':55,'retain-wording':104}
    assert sum(bool(r.get('qa_waivers')) for r in rows)==68 and all(r.get('qa_waivers') in [None,['line-break-count']] for r in rows)
    ROOT.mkdir(parents=True);merged=ROOT/'all159_native_macro_font_choice_reconciliation.json'
    save(merged,dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),manuscripts={str(p):sha(p.read_bytes()) for p in INPUTS},cases=cases,menu_targets=[dict(block=k[0],command_offset=k[1],**v) for k,v in menu_targets.items()],current_original_macro_alignment_calls=1240,all155_current_native_speech_planes_and_four_menu_labels_pass=True,review_sheets=sheets,source_English_macro_control_invariants=invariants,source_bound_formatter_negatives=negatives,source_consumer_negative_controls=font['negative_controls'],no_new_gameplay_or_completion_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    for d,old,new in zip([doc,menu],INPUTS,OUTPUTS,strict=True):
        d.update(previous_manuscript=str(old),previous_manuscript_sha256=sha(old.read_bytes()),prose_companions=[str(p) for p in OUTPUTS if p!=new],native_font_proof=str(merged),native_font_proof_sha256=sha(merged.read_bytes()),native_progressive_proof=str(FONT),native_FE_proof=str(FE),native_choice_proof=str(MENU),formatting_review_pending=False,all159_five_review_gates_true=True,formatter_phrase_flow_findings_resolved_without_waiver=True,status='source-prose-current-native-format-approved;relocation-representative-release-pending')
        validate_natural_dialogue_batch(d);save(new,d)
    save(ROOT/'approval_receipt.json',dict(manuscripts={str(p):sha(p.read_bytes()) for p in OUTPUTS},manuscript=str(OUTPUTS[0]),manuscript_sha256=sha(OUTPUTS[0].read_bytes()),choices=str(OUTPUTS[1]),choices_sha256=sha(OUTPUTS[1].read_bytes()),merged_native_proof=str(merged),merged_native_proof_sha256=sha(merged.read_bytes()),all159_five_review_gates_true=True,progressive_planes=145,FE_planes=10,choice_labels=4,two_option_menus=2,current_macro_alignment_cases=1240,source_consumer_negatives=23,formatter_negatives=28,narrow_row_count_notes=68,review_sheets=sheets,revised=55,retained=104,actual_selected_B122_B127_IDs=[],new_emulator_runs=0,relocation_representative_registered_release_pending=True,source_prose_orcompletion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('All159 five review gates pass:55 revisions/104 retentions,145 progressive/10 FE planes,4 labels,1240 macro cases,23 consumer/28 formatter negatives,23 viewed or hash-exact sheets. Release remains pending.')
