"""Seal 235 editorial format reviews; relocation and release remain pending."""
from collections import Counter
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue import lil_shrines_temples_layout_v2 as codec
from dk4tool.dialogue.lil_shrines_temples_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_Shrines_Temples_font_approval_v3189')
INPUTS=[Path('translations/lil_shrines_temples_editorial_manuscript_v5.json'),
        Path('translations/lil_shrines_temples_actor_style_manuscript_v3.json'),
        Path('translations/lil_shrines_temples_choice_manuscript_v2.json')]
OUTPUTS=[Path('translations/lil_shrines_temples_editorial_manuscript_v6.json'),
         Path('translations/lil_shrines_temples_actor_style_manuscript_v4.json'),
         Path('translations/lil_shrines_temples_choice_manuscript_v3.json')]
FONT=Path('work/analysis/lil_Shrines_Temples_fonts_v3183b/current_macro_QA_and_progressive_font_proof.json')
FE=Path('work/analysis/lil_Shrines_Temples_FE_v3184/current_FE_macro_font_and_typed_paper_proof.json')
MENU=Path('work/analysis/lil_Shrines_Temples_choices_v3188/all5_typed_menu_native_proof.json')
VISUAL=Path('work/analysis/lil_Shrines_Temples_refinement_v3181/native_visual_findings_and_successor_receipt.json')

if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in OUTPUTS)
    doc,voice,menu=[deepcopy(read(p)) for p in INPUTS]
    font,fe,choices=map(read,[FONT,FE,MENU])
    assert font['manuscript_sha256']==sha(INPUTS[0].read_bytes())
    assert font['actor_style_manuscript_sha256']==sha(INPUTS[1].read_bytes())
    assert fe['manuscript_sha256']==sha(INPUTS[0].read_bytes())
    assert len(font['cases'])==190 and len(font['all220_full_QA_reports'])==220
    assert font['current_original_macro_alignment_calls']==1520 and len(font['negative_controls'])==31
    assert all(n['rejected'] for n in font['negative_controls'])
    assert font['newly_executed_font_cases']==3 and font['reused_unchanged_font_cases']==187
    assert font['newly_executed_current_macro_alignment_cases']==24 and font['reused_current_macro_alignment_cases']==1496
    assert sha(Path(font['reused_proof']).read_bytes())==font['reused_proof_sha256']
    prior=read(font['reused_proof'])
    visual=read(VISUAL)
    assert visual['all24_progressive_and4_FE_sheets_viewed']
    changed={i+1 for i,(a,b) in enumerate(zip(prior['review_sheets'],font['review_sheets'],strict=True)) if a['sha256']!=b['sha256']}
    assert changed=={2,13,16}
    sheets=[{**s,'review':'viewed changed successor sheet' if i in changed else 'hash-identical to viewed3179 sheet'} for i,s in enumerate(font['review_sheets'],1)]
    assert len(fe['cases'])==30 and fe['current_original_null_actor_macro_alignment_cases']==240
    assert fe['all30_one_native_page_consumes_complete_target']
    assert fe['all30_complete_native_independent_planes_all_glyphs_and_canaries_equal']
    assert fe['all30_source_unlabeled_panels_preserved_without_invented_names_or_macros']
    assert fe['all30_successor_source_prose_runtime_and_encoded_outputs_exact']
    assert fe['all4_FE_sheets_viewed_and_hash_unchanged']
    assert len(fe['source_leading_vertical_staging_cases'])==2
    assert fe['historical_calibration']['current_calibration_matches_complete_historical_ink_and_blank_mask']
    assert fe['no_initialized_historical_RAM_ITCM_or_DTCM_overlay_in_painter']
    sheets.extend({**s,'review':'viewed3180 FE sheet;exact3184 output rebind'} for s in fe['review_sheets'])
    assert len(choices['menus'])==5 and choices['native_selection_cancel_cases']==40
    assert choices['complete_current_and_reviewed_style_label_planes']==60
    assert choices['all15_labels_source_order_pointers_counts_and_original_selection_results_preserved']
    menu_targets={}
    for m in choices['menus']:
        assert sha(Path(m['proof']).read_bytes())==m['sha256']
        proof=read(m['proof'])
        assert proof['manuscript_sha256']==sha(INPUTS[2].read_bytes())
        assert proof['stored_option_indices_and_original_selection_return_values_preserved']
        assert proof['source_count3_and_result2_and_cancel_explicit']
        for decode in proof['clean_current_reviewed_native_decoder_cases']:
            assert decode['native_count']==3 and [r['stored_index'] for r in decode['labels']]==[0,1,2]
        for case in proof['current_and_reviewed_VM_and_font_cases']:
            vm=case['native_VM_getters_geometry_and_selection']
            assert [c['modal_selection'] for c in vm['VM_cases']]==[0,1,2,-1]
            assert len(case['all_six_style_label_planes'])==6
            assert all(p['storage_padding_all_blank'] and p['independent_complete_native_pixels_match'] for p in case['all_six_style_label_planes'])
            if case['version']=='reviewed-research':
                menu_targets[(proof['block'],proof['original_command_offset'])]=dict(
                    object_hex=proof['typed_target_object_hex'],labels=vm['labels'],native_geometry=vm['native_menu_rectangle'])
        sheets.append(dict(path=m['review_sheet'],sha256=m['review_sheet_sha256'],review='viewed current and reviewed three-option labels'))
    assert len(sheets)==33
    assert all(sha(Path(s['path']).read_bytes())==s['sha256'] for s in sheets)
    image=NdsImage.open(doc['current_ROM'])
    arm=image.read_file('/__arm9__.bin')
    blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    assert sha(arm)==doc['required_runtime_ARM9_sha256']
    assert font['candidate_sha256']==fe['candidate_sha256']==doc['current_ROM_sha256']
    assert font['COMMON_sha256']==fe['COMMON_sha256']==sha(image.read_file('/COMMON/MESFILE.DK4'))
    for p in [font,fe]:
        assert p['ARM9_sha256']==sha(arm)
        assert sha(Path(p['native_formatter_module']).read_bytes())==p['native_formatter_module_sha256']
    assert sha(Path(font['scoped_profile']).read_bytes())==font['scoped_profile_sha256']
    cases=[]
    for c in font['cases']:
        assert c['complete_native_independent216x64_plane_equal'] and c['all_first_final_internal_glyphs_in_order_and_unique_cells']
        cases.append({**c,'consumer':'progressive','macro_cases':[v for p in c['current_native_macro_pipelines'] for v in p['cases']],
            'native_font_plane_sha256':c['whole_native_plane_sha256'],'whole_native_independent_font_plane_exact':True})
    for c in fe['cases']:
        assert c['one_native_page_consumes_complete_target'] and c['complete_native_independent_plane_and_all_glyphs_and_canaries_equal']
        assert sha(Path(c['native_plane']).read_bytes())==c['native_plane_sha256']
        cases.append({**c,'consumer':'FE-paper','macro_cases':[v for p in c['current_native_macro_pipelines'] for v in p['cases']],
            'native_font_plane_sha256':c['native_plane_sha256'],'whole_native_independent_font_plane_exact':True,
            'logical_geometry':[228,48],'physical_row_advance':16})
    assert len(cases)==220 and sum(len(c['macro_cases']) for c in cases)==1760
    byid={c['id']:c for c in cases};invariants=[]
    for paragraph_doc in [doc,voice]:
        for row in paragraph_doc['records']:
            isvoice=row['kind']=='typed-4100-actor-style-alternative'
            raw=bytes.fromhex(row['source_hex'])
            if isvoice:raw=b'\xd0'+raw
            c=byid[row['id']];consumer=c['consumer']
            encoded=codec.encode_relocatable_dialogue(raw,row['english'],profile_for(arm,blocks[row['block']],consumer))
            assert encoded.encoded.hex()==row['compiled_hex']==c['encoded_hex']
            assert semantic_tokens(row['english'])==semantic_tokens(encoded.formatted_markup)
            assert b'\0' not in encoded.encoded
            if isvoice:
                assert encoded.encoded[0]==208 and encoded.encoded[1:].hex()==row['compiled_stored_alternative_hex']
                assert row['virtual_formatter_prefix_is_not_part_of_stored_alternative_text']
            else:
                assert encoded.encoded[:1]==bytes.fromhex(row['source_presentation_prefix_hex'])
                row.update(record_index=row['current_record_index'],current_text_hex=row['current_hex'])
            assert sha(Path(c['preview']).read_bytes())==c['preview_sha256']
            row['review']['formatting']=True
            row.update(native_font_case=c,native_formatting_consumer=consumer,
                status='source-prose-current-native-format-approved;relocation-representative-release-pending')
            if isvoice:row['actor_style_consumer_and_full_native_display_approval_pending']=False
            invariants.append(dict(id=row['id'],source_speaker_macro_order_and_complete_English_tokens_exact=True,
                encoded_sha256=sha(encoded.encoded),consumer=consumer,virtual_D0_excluded_from_stored_body=isvoice))
    assert len(voice['records'])==56 and sum(len(r['style_indices']) for r in voice['records'])==64
    assert len({(r['block'],r['command_offset']) for r in voice['records']})==8
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as error:negatives.append(dict(case=label,rejected=True,error=str(error)))
        else:raise AssertionError(label)
    for consumer in ['progressive','FE-paper']:
        row=next(r for r in doc['records'] if (r['kind']=='system-FE')==(consumer=='FE-paper'))
        raw=bytes.fromhex(row['source_hex']);profile=profile_for(arm,blocks[row['block']],consumer)
        for label,p in [('width',replace(profile,window_width_px=228)),('rows',replace(profile,max_lines=5)),('glyph',replace(profile,default_ascii_width=5)),('row-spacing',replace(profile,line_height_px=12)),('disabled-LF-guard',replace(profile,guard_linebreaks=False)),('disabled-pair-phase',replace(profile,pair_phase_safe_breaks=False)),('disabled-balancing',replace(profile,balanced_wrapping=False)),('macro-width',replace(profile,macro_ascii_lengths={**profile.macro_ascii_lengths,'FO':10})),('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:
            reject(consumer+'-'+label,lambda p=p:codec.encode_relocatable_dialogue(raw,row['english'],p))
        for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:
            reject(consumer+'-manual-or-end-'+tag,lambda tag=tag:codec.encode_relocatable_dialogue(raw,row['english']+tag,profile))
        reject(consumer+'-widened-source-selectors',lambda:codec.encode_relocatable_dialogue(raw,row['english'],replace(profile,leading_speaker_bytes=profile.leading_speaker_bytes|{148})))
    assert len(negatives)==28
    for path,digest in codec.DEPENDENCIES.items():assert sha(Path(path).read_bytes())==digest
    for row in menu['records']:
        target=menu_targets[(row['block'],row['command_offset'])]
        assert row['english']==target['labels'][row['option_index']]
        row['review']['formatting']=True
        row.update(status='source-prose-current-native-three-option-format-approved;relocation-representative-release-pending',
            native_choice_proof=str(MENU),native_choice_proof_sha256=sha(MENU.read_bytes()),
            typed_target_object_hex=target['object_hex'],native_menu_rectangle=target['native_geometry'],
            selection_cancel_VM_and_complete_native_menu_display_pending=False,actual_selection_gameplay_claimed=False)
    allrows=doc['records']+voice['records']+menu['records']
    assert len(allrows)==235 and Counter(r['editorial_decision'] for r in allrows)=={'revise':117,'retain-wording':118}
    assert sum(bool(r.get('qa_waivers')) for r in allrows)==54
    assert all(r.get('qa_waivers') in [None,['line-break-count']] for r in allrows)
    ROOT.mkdir(parents=True)
    merged=ROOT/'all220_native_macro_font_reconciliation.json'
    save(merged,dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),
        manuscripts={str(p):sha(p.read_bytes()) for p in INPUTS},cases=cases,current_original_macro_alignment_calls=1760,
        all220_current_native_planes_and_complete_glyphs_pass=True,all33_review_sheets=sheets,
        source_English_macro_control_invariants=invariants,source_bound_formatter_negatives=negatives,
        effective_planner_sha256=codec.EFFECTIVE_PLANNER_SHA256,global_helpers_unchanged=codec.DEPENDENCIES,
        evidence={str(p):sha(p.read_bytes()) for p in [FONT,FE,MENU,VISUAL]},
        actual_selected_Shrines_Temples_IDs=[],new_emulator_runs=0,relocation_representative_registered_release_pending=True,
        source_prose_or_completion_credit_added=0,full_goal_complete=False))
    for paragraph_doc,old,new in zip([doc,voice,menu],INPUTS,OUTPUTS,strict=True):
        paragraph_doc.update(previous_manuscript=str(old),previous_manuscript_sha256=sha(old.read_bytes()),
            encoder='dialogue-relocatable-v1',prose_companions=[str(p) for p in OUTPUTS if p!=new],
            native_font_proof=str(merged),native_font_proof_sha256=sha(merged.read_bytes()),
            native_progressive_proof=str(FONT),native_FE_proof=str(FE),native_choice_proof=str(MENU),
            formatting_review_pending=False,all235_five_review_gates_true=True,
            formatter_phrase_flow_findings_resolved_without_waiver=True,
            status='source-prose-current-native-format-approved;relocation-representative-release-pending')
        validate_natural_dialogue_batch(paragraph_doc)
        save(new,paragraph_doc)
    save(ROOT/'approval_receipt.json',dict(manuscripts={str(p):sha(p.read_bytes()) for p in OUTPUTS},
        manuscript=str(OUTPUTS[0]),manuscript_sha256=sha(OUTPUTS[0].read_bytes()),
        actor_styles=str(OUTPUTS[1]),actor_styles_sha256=sha(OUTPUTS[1].read_bytes()),
        choices=str(OUTPUTS[2]),choices_sha256=sha(OUTPUTS[2].read_bytes()),
        merged_native_proof=str(merged),merged_native_proof_sha256=sha(merged.read_bytes()),
        all235_five_review_gates_true=True,progressive_planes=190,FE_planes=30,current_macro_alignment_cases=1760,
        choice_style_planes=60,VM_selection_cancel_cases=40,formatter_negatives=28,narrow_line_count_notes=54,
        all33_review_sheets=sheets,review_sheets=sheets,actual_selected_Shrines_Temples_IDs=[],new_emulator_runs=0,
        relocation_representative_registered_release_pending=True,source_prose_orcompletion_credit_added=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('235five review gates sealed:220panels/1760macro cases,60choiceplanes/40VMreturns,28formatter negatives,33viewed orhash-exact sheets. No integration/completion credit.')
