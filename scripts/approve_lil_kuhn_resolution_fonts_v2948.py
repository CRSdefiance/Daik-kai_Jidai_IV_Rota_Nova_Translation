"""Seal 358 speech and two choice reviews; no relocation or completion credit."""
from pathlib import Path
from copy import deepcopy
from dataclasses import replace
from collections import Counter
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.lil_kuhn_resolution_profile import profile_for
from dk4tool.dialogue import lil_kuhn_resolution_layout_v3 as codec
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens

ROOT=Path('work/analysis/lil_Kuhn_Resolution_font_approval_v2948')
OLD=Path('translations/lil_kuhn_resolution_editorial_manuscript_v5.json')
DOC=Path('translations/lil_kuhn_resolution_editorial_manuscript_v6.json')
MENU=Path('translations/lil_kuhn_resolution_choice_manuscript_v1.json')
MENU_OUT=Path('translations/lil_kuhn_resolution_choice_manuscript_v2.json')
FONT=Path('work/analysis/lil_Kuhn_Resolution_fonts_v2947/current_macro_QA_and_progressive_font_proof.json')
FE=Path('work/analysis/lil_Kuhn_Resolution_FE_v2942/current_FE_macro_font_and_typed_paper_proof.json')
CHOICE=Path('work/analysis/lil_Kuhn_Resolution_choices_v2940/all1_typed_menu_native_proof.json')

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,DOC,MENU_OUT])
    doc,menu,font,fe,choice=map(read,[OLD,MENU,FONT,FE,CHOICE])
    assert font['manuscript_sha256']==sha(OLD.read_bytes())
    assert len(font['cases'])==342 and len(font['all358_full_QA_reports'])==358
    assert font['current_original_macro_alignment_calls']==2736 and len(font['negative_controls'])==11
    assert font['newly_executed_font_cases']==6 and font['reused_unchanged_font_cases']==336
    assert font['newly_executed_current_macro_alignment_cases']==48 and font['reused_current_macro_alignment_cases']==2688
    prior=read(font['reused_proof']);assert sha(Path(font['reused_proof']).read_bytes())==font['reused_proof_sha256']
    changed={i//8+1 for i,c in enumerate(font['cases']) if not c.get('reused_current_native_case')}
    assert changed=={4,8,14,15,41}
    sheets=[]
    # V2941 sheets1-12 and V2945 sheets4,10,13-43 were viewed. The two changed
    # V2945 sheets4/10 were viewed. All five V2947 changed sheets were viewed.
    older=read(prior['reused_proof'])
    assert sha(Path(prior['reused_proof']).read_bytes())==prior['reused_proof_sha256']
    for i,s in enumerate(prior['review_sheets'],1):
        if i<=12 and i not in {4,10}:assert s['sha256']==older['review_sheets'][i-1]['sha256']
    for i,s in enumerate(font['review_sheets'],1):
        if i not in changed:assert s['sha256']==prior['review_sheets'][i-1]['sha256']
        sheets.append(dict(**s,review='viewed V2947 current sheet' if i in changed else 'hash-identical to viewed V2945 or V2941 predecessor'))
    assert len(fe['cases'])==16 and fe['current_original_null_actor_macro_alignment_cases']==128
    assert fe['all16_one_native_page_consumes_complete_target'] and fe['all16_complete_native_independent_planes_all_glyphs_and_canaries_equal']
    assert fe['all14_distinct_source_theft_notices_preserved'] and fe['source_letter_salutation_and_signature_preserved'] and fe['source_unlabeled_offscreen_FI_has_no_invented_speaker_label']
    assert len(fe['source_FI_null_actor_cases'])==2
    assert fe['historical_calibration']['complete_current_native_ink_and_blank_mask_equal'] and fe['no_initialized_historical_RAM_ITCM_or_DTCM_overlay_in_painter']
    assert sha(Path(fe['manuscript']).read_bytes())==fe['manuscript_sha256']
    fe_rows={r['id']:r for r in read(fe['manuscript'])['records'] if r['kind']=='system-FE'}
    sheets.extend(dict(**s,review='viewed complete FE sheet') for s in fe['review_sheets'])
    assert len(choice['menus'])==1 and choice['native_selection_cancel_cases']==6 and choice['complete_current_and_reviewed_style_label_planes']==8
    assert choice['all2_labels_source_order_pointers_counts_and_original_selection_results_preserved']
    for m in choice['menus']:
        assert sha(Path(m['proof']).read_bytes())==m['sha256'];proof=read(m['proof'])
        assert proof['manuscript_sha256']==sha(MENU.read_bytes()) and proof['stored_option_indices_and_original_selection_return_values_preserved']
        for case in proof['current_and_reviewed_VM_and_font_cases']:
            for plane in case['all_four_style_label_planes']:
                assert plane['storage_padding_all_blank'] and plane['independent_complete_native_pixels_match']
        sheets.append(dict(path=m['review_sheet'],sha256=m['review_sheet_sha256'],review='viewed current and reviewed typed menu'))
    assert len(sheets)==46 and all(sha(Path(s['path']).read_bytes())==s['sha256'] for s in sheets)
    for p in [font,fe]:
        assert p['candidate_sha256']==doc['current_ROM_sha256'] and p['ARM9_sha256']==doc['required_runtime_ARM9_sha256']
        assert sha(Path(p['scoped_profile']).read_bytes())==p['scoped_profile_sha256']
        assert sha(Path(p['native_formatter_module']).read_bytes())==p['native_formatter_module_sha256']
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    assert sha(arm)==doc['required_runtime_ARM9_sha256'] and font['COMMON_sha256']==fe['COMMON_sha256']==sha(image.read_file('/COMMON/MESFILE.DK4'))
    cases=[]
    for c in font['cases']:
        assert c['complete_native_independent216x64_plane_equal'] and c['all_first_final_internal_glyphs_in_order_and_unique_cells']
        cases.append(dict(**c,consumer='progressive',macro_cases=[v for p in c['current_native_macro_pipelines'] for v in p['cases']],native_font_plane_sha256=c['whole_native_plane_sha256'],whole_native_independent_font_plane_exact=True))
    for c in fe['cases']:
        assert c['complete_native_independent_plane_and_all_glyphs_and_canaries_equal'] and c['one_native_page_consumes_complete_target'] and c['all_visible_origins_zero_and4rows']
        assert sha(Path(c['native_plane']).read_bytes())==c['native_plane_sha256']
        cases.append(dict(**c,consumer='FE-paper',macro_cases=[v for p in c['current_native_macro_pipelines'] for v in p['cases']],native_font_plane_sha256=c['native_plane_sha256'],whole_native_independent_font_plane_exact=True,logical_geometry=[228,48],physical_row_advance=16))
    assert len(cases)==358 and sum(len(c['macro_cases']) for c in cases)==2864
    byid={c['id']:c for c in cases};invariants=[]
    for row in doc['records']:
        c=byid[row['id']];consumer='FE-paper' if row['kind']=='system-FE' else 'progressive'
        result=codec.encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile_for(arm,blocks[row['block']],consumer))
        assert result.encoded.hex()==c['encoded_hex'] and semantic_tokens(row['english'])==semantic_tokens(result.formatted_markup)
        assert result.encoded[:1]==bytes.fromhex(row['source_presentation_prefix_hex']) and b'\0' not in result.encoded
        assert sha(Path(c['preview']).read_bytes())==c['preview_sha256']
        if consumer=='FE-paper':assert all(row[k]==fe_rows[row['id']][k] for k in ['english','source_hex','current_hex','source_presentation_prefix_hex','kind'])
        invariants.append(dict(id=row['id'],source_speaker_macro_order_and_complete_English_tokens_exact=True,encoded_sha256=sha(result.encoded),consumer=consumer))
        row['review']['formatting']=True
        row.update(compiled_hex=c['encoded_hex'],native_font_case=c,native_formatting_consumer=consumer,record_index=row['current_record_index'],current_text_hex=row['current_hex'],status='source-prose-current-native-format-approved;reference-representative-release-pending')
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as error:negatives.append(dict(case=label,rejected=True,error=str(error)))
        else:raise AssertionError(label)
    for consumer in ['progressive','FE-paper']:
        row=next(r for r in doc['records'] if (r['kind']=='system-FE')==(consumer=='FE-paper'));raw=bytes.fromhex(row['source_hex']);profile=profile_for(arm,blocks[row['block']],consumer)
        for label,p in [('width',replace(profile,window_width_px=228)),('rows',replace(profile,max_lines=5)),('glyph',replace(profile,default_ascii_width=5)),('row-spacing',replace(profile,line_height_px=12)),('disabled-LF-guard',replace(profile,guard_linebreaks=False)),('disabled-pair-phase',replace(profile,pair_phase_safe_breaks=False)),('disabled-balancing',replace(profile,balanced_wrapping=False)),('macro-width',replace(profile,macro_ascii_lengths={**profile.macro_ascii_lengths,'FO':10})),('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:
            reject(consumer+'-'+label,lambda p=p:codec.encode_relocatable_dialogue(raw,row['english'],p))
        for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:reject(consumer+'-manual-or-end-'+tag,lambda tag=tag:codec.encode_relocatable_dialogue(raw,row['english']+tag,profile))
        reject(consumer+'-widened-source-selectors',lambda:codec.encode_relocatable_dialogue(raw,row['english'],replace(profile,leading_speaker_bytes=profile.leading_speaker_bytes|{148})))
    assert len(negatives)==28
    for path,digest in codec.DEPENDENCIES.items():assert sha(Path(path).read_bytes())==digest
    for row in menu['records']:
        row['review']['formatting']=True;row.update(status='source-prose-current-native-choice-format-approved;reference-representative-release-pending',native_choice_proof=str(CHOICE),native_choice_proof_sha256=sha(CHOICE.read_bytes()),actual_selection_gameplay_claimed=False)
    assert Counter(r['editorial_decision'] for r in doc['records']+menu['records'])=={'revise':214,'retain-wording':146}
    assert sum(bool(r.get('qa_waivers')) for r in doc['records'])==104 and all(r.get('qa_waivers') in [None,['line-break-count']] for r in doc['records'])
    ROOT.mkdir(parents=True);merged=ROOT/'all358_native_macro_font_reconciliation.json'
    save(merged,dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),manuscript=str(OLD),manuscript_sha256=sha(OLD.read_bytes()),cases=cases,current_original_macro_alignment_calls=2864,all358_current_native_planes_and_complete_glyphs_pass=True,all46_review_sheets=sheets,source_English_macro_control_invariants=invariants,source_bound_formatter_negatives=negatives,effective_planner_sha256=codec.EFFECTIVE_PLANNER_SHA256,global_helpers_unchanged=codec.DEPENDENCIES,evidence={str(p):sha(p.read_bytes()) for p in [FONT,FE,CHOICE,Path(doc['native_formatter_module']),Path(doc['scoped_profile_module'])]},actual_selected_Kuhn_Resolution_IDs=[],new_emulator_runs=0,reference_representative_registered_release_pending=True,full_goal_complete=False))
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),native_font_proof=str(merged),native_font_proof_sha256=sha(merged.read_bytes()),native_progressive_proof=str(FONT),native_FE_proof=str(FE),native_FE_font_proof=str(FE),native_FE_font_proof_sha256=sha(FE.read_bytes()),native_choice_proof=str(CHOICE),choice_companion=str(MENU_OUT),formatting_review_pending=False,all358_native_planes_and2864_current_macro_calls_pass=True,all46_review_sheets_viewed_or_identical=True,formatter_phrase_flow_findings_resolved_without_waiver=True,status='source-prose-current-native-format-approved;reference-representative-release-pending')
    menu.update(previous_manuscript=str(MENU),previous_manuscript_sha256=sha(MENU.read_bytes()),ordinary_FE_companion=str(DOC),formatting_review_pending=False,native_choice_proof=str(CHOICE),native_choice_proof_sha256=sha(CHOICE.read_bytes()),status='source-prose-current-native-choice-format-approved;reference-representative-release-pending')
    validate_natural_dialogue_batch(doc);validate_natural_dialogue_batch({**menu,'encoder':'dialogue-relocatable-v1'})
    save(DOC,doc);save(MENU_OUT,menu)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),choices=str(MENU_OUT),choices_sha256=sha(MENU_OUT.read_bytes()),merged_native_proof=str(merged),merged_native_proof_sha256=sha(merged.read_bytes()),all360_five_review_gates_true=True,progressive_planes=342,FE_planes=16,current_macro_alignment_cases=2864,choice_style_planes=8,VM_selection_cancel_cases=6,formatter_negatives=28,narrow_line_count_notes=104,all46_review_sheets=sheets,review_sheets=sheets,actual_selected_Kuhn_Resolution_IDs=[],new_emulator_runs=0,reference_representative_registered_release_pending=True,source_prose_orcompletion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('360 formatting gates sealed:358 panels/2864 macro cases,8 choice planes/6 VM returns,28 formatter rejections;zero completion credit.')
