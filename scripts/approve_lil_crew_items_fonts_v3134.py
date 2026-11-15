"""Seal198 speech andtwo choice reviews; no relocation or completion credit."""
from pathlib import Path
from copy import deepcopy
from dataclasses import replace
from collections import Counter
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.lil_crew_items_profile import profile_for
from dk4tool.dialogue import lil_crew_items_layout_v2 as codec
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens

ROOT=Path('work/analysis/lil_Crew_Items_font_approval_v3134')
OLD=Path('translations/lil_crew_items_editorial_manuscript_v6.json')
DOC=Path('translations/lil_crew_items_editorial_manuscript_v7.json')
MENU=Path('translations/lil_crew_items_choice_manuscript_v1.json')
MENU_OUT=Path('translations/lil_crew_items_choice_manuscript_v2.json')
FONT=Path('work/analysis/lil_Crew_Items_fonts_v3133/current_macro_QA_and_progressive_font_proof.json')
FE=Path('work/analysis/lil_Crew_Items_FE_v3129/current_FE_macro_font_and_typed_paper_proof.json')
CHOICE=Path('work/analysis/lil_Crew_Items_choices_v3130/all1_typed_menu_native_proof.json')

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,DOC,MENU_OUT])
    doc,menu,font,fe,choice=map(read,[OLD,MENU,FONT,FE,CHOICE])
    assert font['manuscript_sha256']==sha(OLD.read_bytes())
    assert len(font['cases'])==191 and len(font['all198_full_QA_reports'])==198
    assert font['current_original_macro_alignment_calls']==1528 and len(font['negative_controls'])==37
    assert font['all191_progressive_full_QA_and_complete_native_fonts_pass'] and all(n['rejected'] for n in font['negative_controls'])
    assert font['newly_executed_font_cases']==3 and font['reused_unchanged_font_cases']==188
    assert font['newly_executed_current_macro_alignment_cases']==24 and font['reused_current_macro_alignment_cases']==1504
    assert sha(Path(font['reused_proof']).read_bytes())==font['reused_proof_sha256'];prior=read(font['reused_proof'])
    changed={i+1 for i,(a,b) in enumerate(zip(prior['review_sheets'],font['review_sheets'],strict=True)) if a['sha256']!=b['sha256']};assert changed=={12,16,19}
    # All24initial ordinary sheets andthe FE/menu sheets were viewed;allthree changed successor sheets were viewed.
    sheets=[dict(**s,review='viewed changed successor sheet' if i in changed else 'hash-identical to viewed3128 sheet') for i,s in enumerate(font['review_sheets'],1)]

    assert len(sheets)==24
    assert len(fe['cases'])==7 and fe['current_original_null_actor_macro_alignment_cases']==56
    assert fe['all7_one_native_page_consumes_complete_target'] and fe['all7_complete_native_independent_planes_all_glyphs_and_canaries_equal']
    assert fe['all7_source_unlabeled_stat_notices_and_monkey_calls_preserved'] and fe['four_distinct_source_Luck_Spirit_notices_and_three_monkey_calls_preserved']
    assert len(fe['source_FI_null_actor_cases'])==2
    assert fe['historical_calibration']['current_calibration_matches_complete_historical_ink_and_blank_mask'] and fe['no_initialized_historical_RAM_ITCM_or_DTCM_overlay_in_painter']
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
    assert len(sheets)==26 and all(sha(Path(s['path']).read_bytes())==s['sha256'] for s in sheets)
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
    assert len(cases)==198 and sum(len(c['macro_cases']) for c in cases)==1584
    assert len(fe_rows)==7 and all(':' not in r['english'].split('}',1)[1].replace('{MACRO:FI}','FI') for r in doc['records'] if r['kind']=='system-FE')
    assert all(c['all8_alignment_cases_Lil_possessive_stat_identity_exact'] for c in fe['source_FI_null_actor_cases'])
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
    assert Counter(r['editorial_decision'] for r in doc['records']+menu['records'])=={'revise':123,'retain-wording':77}
    assert sum(bool(r.get('qa_waivers')) for r in doc['records'])==64 and all(r.get('qa_waivers') in [None,['line-break-count']] for r in doc['records'])
    ROOT.mkdir(parents=True);merged=ROOT/'all198_native_macro_font_reconciliation.json'
    save(merged,dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),manuscript=str(OLD),manuscript_sha256=sha(OLD.read_bytes()),cases=cases,current_original_macro_alignment_calls=1584,all198_current_native_planes_and_complete_glyphs_pass=True,all26_review_sheets=sheets,source_English_macro_control_invariants=invariants,source_bound_formatter_negatives=negatives,effective_planner_sha256=codec.EFFECTIVE_PLANNER_SHA256,global_helpers_unchanged=codec.DEPENDENCIES,evidence={str(p):sha(p.read_bytes()) for p in [FONT,FE,CHOICE,Path(doc['native_formatter_module']),Path(doc['scoped_profile_module'])]},actual_selected_Crew_Items_IDs=[],new_emulator_runs=0,reference_representative_registered_release_pending=True,full_goal_complete=False))
    doc['typed_choice_companion']=str(MENU_OUT)
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),native_font_proof=str(merged),native_font_proof_sha256=sha(merged.read_bytes()),native_progressive_proof=str(FONT),native_FE_proof=str(FE),native_FE_font_proof=str(FE),native_FE_font_proof_sha256=sha(FE.read_bytes()),native_choice_proof=str(CHOICE),choice_companion=str(MENU_OUT),formatting_review_pending=False,all198_native_planes_and1584_current_macro_calls_pass=True,all26_review_sheets_viewed_or_identical=True,formatter_phrase_flow_findings_resolved_without_waiver=True,status='source-prose-current-native-format-approved;reference-representative-release-pending')
    menu.update(previous_manuscript=str(MENU),previous_manuscript_sha256=sha(MENU.read_bytes()),ordinary_FE_companion=str(DOC),formatting_review_pending=False,native_choice_proof=str(CHOICE),native_choice_proof_sha256=sha(CHOICE.read_bytes()),status='source-prose-current-native-choice-format-approved;reference-representative-release-pending')
    validate_natural_dialogue_batch(doc);validate_natural_dialogue_batch({**menu,'encoder':'dialogue-relocatable-v1'})
    save(DOC,doc);save(MENU_OUT,menu)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),choices=str(MENU_OUT),choices_sha256=sha(MENU_OUT.read_bytes()),merged_native_proof=str(merged),merged_native_proof_sha256=sha(merged.read_bytes()),all200_five_review_gates_true=True,progressive_planes=191,FE_planes=7,current_macro_alignment_cases=1584,choice_style_planes=8,VM_selection_cancel_cases=6,formatter_negatives=28,narrow_line_count_notes=64,all26_review_sheets=sheets,review_sheets=sheets,actual_selected_Crew_Items_IDs=[],new_emulator_runs=0,reference_representative_registered_release_pending=True,source_prose_orcompletion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('200formatting gates sealed:198panels/1584macro cases,8choiceplanes/6VMreturns,28formatter rejections;zero completion credit.')
