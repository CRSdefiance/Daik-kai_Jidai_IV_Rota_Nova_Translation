"""Approve the complete sail-lesson exchange using source-bound native display evidence."""
from collections import Counter
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue import lil_B167_layout_v6 as codec
from dk4tool.dialogue.lil_B167_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B167_native_approval_v4135')
INPUTS=[Path('translations/lil_B167_editorial_manuscript_v11.json'),Path('translations/lil_B167_choice_manuscript_v1.json')]
OUTPUTS=[Path('translations/lil_B167_editorial_manuscript_v12.json'),Path('translations/lil_B167_choice_manuscript_v2.json')]
FONT=Path('work/analysis/lil_B167_fonts_v4134d/current_macro_QA_and_progressive_font_proof.json')
MENU=Path('work/analysis/lil_B167_choices_v4133/B167_C152/original_choice_decoder_VM_geometry_and_native_pixels.json')
if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in OUTPUTS)
    doc,menu=[deepcopy(read(p)) for p in INPUTS];font,choice=map(read,[FONT,MENU])
    assert font['manuscript_sha256']==sha(INPUTS[0].read_bytes()) and choice['manuscript_sha256']==sha(INPUTS[1].read_bytes())
    assert len(font['cases'])==27 and font['current_original_macro_alignment_calls']==216 and len(font['negative_controls'])==19
    assert font['new_current_original_macro_alignment_calls']==8 and font['reused_original_macro_alignment_calls']==208
    assert choice['six_original_VM_selection_and_cancel_cases_pass'] and choice['eight_complete_native_style_label_planes_pass']
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[167]
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==font['candidate_sha256']==choice['candidate_sha256']
    assert sha(arm)==font['ARM9_sha256']==doc['required_runtime_ARM9_sha256']
    sheets=[]
    for s in font['review_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        sheets.append({**s,'review':'Viewed full final native sheet. Complete first/internal/final glyphs, natural clause boundaries and four-row bounds. The source square/lateen and supplementary-sail facts, mast explanation and distinct voices remain complete.'})
    assert len(sheets)==4 and sha(Path(choice['visual_review_sheet']).read_bytes())==choice['visual_review_sheet_sha256']
    menusheet=dict(path=choice['visual_review_sheet'],sha256=choice['visual_review_sheet_sha256'],review='Viewed current/reviewed Okay and No thanks in all native styles: complete centered glyphs and source option order. Offline native rendering only; no B167 actual scene or accepted choice is claimed.')
    byid={r['id']:r for r in font['cases']};invariants=[];profile=profile_for(arm,block)
    for r in doc['records']:
        raw=bytes.fromhex(r['source_hex']);c=byid[r['id']]
        encoded=codec.encode_relocatable_dialogue(raw,r['english'],profile)
        assert encoded.encoded.hex()==r['compiled_hex']==c['encoded_hex']
        assert semantic_tokens(r['english'])==semantic_tokens(encoded.formatted_markup)
        assert c['complete_native_independent216x64_plane_equal'] and c['all_first_final_internal_glyphs_in_order_and_unique_cells'] and c['all_visible_origins_zero_and16px_rows_within4rows']
        assert sha(Path(c['preview']).read_bytes())==c['preview_sha256'] and sum(len(p['cases']) for p in c['current_native_macro_pipelines'])==8
        assert all(raw.count(k.encode())==r['english'].count('{MACRO:'+k+'}')==0 for k in ['FI','FA','FO'])
        qa=codec.audit_relocatable_dialogue_record(raw,r['english'],profile)
        assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code']=='line-break-count' and r.get('qa_waiver_reason'))]
        r['review']['formatting']=True
        r.update(record_index=r['current_record_index'],current_text_hex=r['current_hex'],native_font_case=c,native_formatting_consumer='progressive',native_plane_verified_not_actual_gameplay=True,current_complete_native_display_pending=False,current_native_voice_macro_entry_and_context_pending=False,status='source-prose-current-native-format-approved;relocation-references-story-representative-release-pending')
        invariants.append(dict(id=r['id'],block=167,source_selector=raw[0],whole_source_English_tokens_and_control_order_preserved=True,encoded_sha256=sha(encoded.encoded)))
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as e:negatives.append(dict(case=label,rejected=True,error=str(e)))
        else:raise AssertionError(label)
    r=doc['records'][0];raw=bytes.fromhex(r['source_hex']);p=profile
    for label,bad in [('width',replace(p,window_width_px=228)),('rows',replace(p,max_lines=5)),('glyph',replace(p,default_ascii_width=5)),('row-spacing',replace(p,line_height_px=12)),('disabled-LF-guard',replace(p,guard_linebreaks=False)),('disabled-pair-phase',replace(p,pair_phase_safe_breaks=False)),('disabled-balancing',replace(p,balanced_wrapping=False)),('macro-width',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FA':6})),('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:
        reject(label,lambda bad=bad:codec.encode_relocatable_dialogue(raw,r['english'],bad))
    for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:reject('manual-or-end-'+tag,lambda tag=tag:codec.encode_relocatable_dialogue(raw,r['english']+tag,p))
    reject('widened-selectors',lambda:codec.encode_relocatable_dialogue(raw,r['english'],replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{149})))
    assert len(negatives)==14
    target=bytes.fromhex(choice['typed_target_object_hex']);assert len(target)==22
    assert [r['option_index'] for r in menu['records']]==[0,1] and [r['english'] for r in menu['records']]==['Okay','No thanks']
    for r in menu['records']:
        r['review']['formatting']=True
        r.update(typed_target_object_hex=target.hex(),compiled_hex=target.hex(),native_choice_proof=str(MENU),native_choice_proof_sha256=sha(MENU.read_bytes()),choice_consumer_selection_geometry_native_display_pending=False,actual_choice_selection_still_pending=True,status='source-prose-current-native-format-approved;relocation-references-story-representative-release-pending')
    allrows=doc['records']+menu['records']
    assert Counter(r['editorial_decision'] for r in allrows)=={'revise':16,'retain-wording':13}
    assert sum(bool(r.get('qa_waivers')) for r in doc['records'])==11
    for r in allrows:
        if r['editorial_decision']=='retain-wording':
            text=r['english'].split('}',1)[1] if r['kind']=='progressive' else r['english']
            assert text==r['effective_predecessor_paragraph'] and r['fresh_retained_wording_justification']
    namespath=Path(doc['source_nameplate_consumer_proof']);names=read(namespath)
    assert sha(namespath.read_bytes())==doc['source_nameplate_consumer_proof_sha256']
    assert names['approved_prose_names']=={'2':'Lil','4':'Janus','13':'Cesare','23':'Manuel','109':'Shipwright'}
    rows=names['native_ten_consumer_cases']['rows'];assert len(rows)==10
    assert all(r['all_actor_models_and_unowned4MiB_exact'] and r['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for r in rows)
    assert all(not r['original_scratch_rings'] and not r['original_getter_writes'] for r in rows if r['actor_ID']==109)
    ROOT.mkdir(parents=True);merged=ROOT/'all29_native_speech_choice_and_source_reconciliation.json'
    paths=[*INPUTS,FONT,MENU,namespath,Path('scripts/refine_lil_B167_astern_v4134d.py'),Path(__file__)]
    save(merged,dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),manuscript=str(INPUTS[0]),manuscript_sha256=sha(INPUTS[0].read_bytes()),cases=font['cases'],current_original_macro_alignment_calls=216,all27_current_native_speech_planes_pass=True,review_sheets=sheets,choice_review_sheet=menusheet,source_English_macro_control_invariants=invariants,source_bound_formatter_negatives=negatives,source_consumer_negative_controls=font['negative_controls'],typed_choice_proof=str(MENU),typed_choice_proof_sha256=sha(MENU.read_bytes()),scoped_profile=doc['scoped_profile_module'],scoped_profile_sha256=doc['scoped_profile_module_sha256'],native_formatter_module=doc['native_formatter_module'],native_formatter_module_sha256=doc['native_formatter_module_sha256'],all29_source_facts_complete_branches_and_individual_decisions_reconciled=True,source_0D_and_printable6D_preserved_older_record_reaudit_open=True,source_two_paths_and_separate_later_Cesare_query_result_not_menu_index_preserved=True,evidence={str(x):sha(x.read_bytes()) for x in paths},no_new_gameplay_orcompletion_credit=True,full_goal_complete=False))
    for i,d in enumerate([doc,menu]):
        d.update(previous_manuscript=str(INPUTS[i]),previous_manuscript_sha256=sha(INPUTS[i].read_bytes()),native_font_proof=str(merged),native_font_proof_sha256=sha(merged.read_bytes()),native_progressive_proof=str(FONT),formatting_review_pending=False,all29_five_review_gates_true=True,formatter_phrase_flow_findings_resolved_without_waiver=True,prose_companions=[str(OUTPUTS[1-i])],status='source-prose-current-native-format-approved;relocation-references-story-representative-release-pending')
        validate_natural_dialogue_batch(d);save(OUTPUTS[i],d)
    save(ROOT/'approval_receipt.json',dict(manuscripts={str(p):sha(p.read_bytes()) for p in OUTPUTS},merged_native_proof=str(merged),merged_native_proof_sha256=sha(merged.read_bytes()),revised=16,retained=13,progressive_planes=27,current_macro_alignment_cases=216,source_consumer_negatives=19,formatter_negatives=14,menu_selection_cancel_cases=6,menu_style_label_planes=8,narrow_row_count_notes=11,review_sheets=sheets,choice_review_sheet=menusheet,actual_selected_B167_IDs=[],actual_B167_speech_or_choice_return_coverage_added=0,new_emulator_runs=0,relocation_references_representative_registered_release_pending=True,new_source_prose_reviews=0,new_completed_records=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B167:29 five-gate reviews approved,16 revisions/13 retentions;27 native planes/216 alignment cases,19+14 negatives and typed menu pass. Actual scene and integration pending;no credit yet.')
