"""Seal38 five-gate source/prose reviews after viewed native planes;integration remains pending."""
from collections import Counter
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue import lil_B142_B145_layout_v2 as codec
from dk4tool.dialogue.lil_B142_B145_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B142_B145_native_approval_v3590')
INPUT=Path('translations/lil_B142_B145_editorial_manuscript_v3.json')
OUTPUT=Path('translations/lil_B142_B145_editorial_manuscript_v4.json')
FONT=Path('work/analysis/lil_B142_B145_fonts_v3589/all38_native_planes304_macros_and28_consumer_negatives.json')
REUSE=Path('work/analysis/lil_B142_B145_fonts_v3589/selective_native_recheck_and_viewed_sheet_reuse.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=deepcopy(read(INPUT));font,reuse=map(read,[FONT,REUSE]);assert font['manuscript_sha256']==sha(INPUT.read_bytes()) and len(font['cases'])==38 and font['current_original_macro_alignment_calls']==304 and font['new_current_original_macro_alignment_calls']==8 and len(font['source_consumer_negative_controls'])==28 and len(reuse['first_four_sheets_equal_viewed_predecessors'])==4
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==font['candidate_sha256'] and sha(arm)==font['ARM9_sha256']==doc['required_runtime_ARM9_sha256'];sheets=[]
    for i,s in enumerate(font['review_sheets']):assert sha(Path(s['path']).read_bytes())==s['sha256'];sheets.append({**s,'review':'Viewed final fifth sheet;Come on stays together.' if i==4 else 'Viewed original sheet;final successor hash exactly matches the viewed predecessor.'})
    assert len(sheets)==5;byid={c['id']:c for c in font['cases']};invariants=[]
    for r in doc['records']:
        fe=r['kind']=='system-FE';profile=profile_for(arm,blocks[r['block']],'FE-paper' if fe else 'progressive');raw=bytes.fromhex(r['source_hex']);c=byid[r['id']];encoded=codec.encode_relocatable_dialogue(raw,r['english'],profile);assert encoded.encoded.hex()==r['compiled_hex']==c['encoded_hex'] and semantic_tokens(r['english'])==semantic_tokens(encoded.formatted_markup) and c['all_first_final_internal_glyphs_in_order_and_unique_cells'] and c['all_visible_origins_zero_and_native_rows_within4rows'] and c['complete_native_independent_plane_equal'];assert sha(Path(c['preview']).read_bytes())==c['preview_sha256']
        assert all(raw.count(k.encode())==r['english'].count('{MACRO:'+k+'}') for k in ['FI','FA','FO']);r['review']['formatting']=True;r.update(record_index=r['current_record_index'],current_text_hex=r['current_hex'],native_font_case=c,native_formatting_consumer='FE-paper' if fe else 'progressive',current_complete_native_display_pending=False,current_macro_dispatch_consumer_and_complete_native_display_pending=False,current_native_voice_macro_entry_and_context_pending=False,status='source-prose-current-native-format-approved;relocation-references-representative-release-pending');invariants.append(dict(id=r['id'],source_selector=raw[0],complete_English_tokens_and_FI_macro_order_preserved=True,encoded_sha256=sha(encoded.encoded)))
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as e:negatives.append(dict(case=label,rejected=True,error=str(e)))
        else:raise AssertionError(label)
    for kind in ['progressive','FE-paper']:
        r=next(r for r in doc['records'] if (r['kind']=='system-FE')==(kind=='FE-paper'));raw=bytes.fromhex(r['source_hex']);profile=profile_for(arm,blocks[r['block']],kind)
        for label,p in [('width',replace(profile,window_width_px=228)),('rows',replace(profile,max_lines=5)),('glyph',replace(profile,default_ascii_width=5)),('row-spacing',replace(profile,line_height_px=12)),('disabled-LF-guard',replace(profile,guard_linebreaks=False)),('disabled-pair-phase',replace(profile,pair_phase_safe_breaks=False)),('disabled-balancing',replace(profile,balanced_wrapping=False)),('macro-width',replace(profile,macro_ascii_lengths={**profile.macro_ascii_lengths,'FO':10})),('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:reject(kind+'-'+label,lambda p=p:codec.encode_relocatable_dialogue(raw,r['english'],p))
        for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:reject(kind+'-manual-or-end-'+tag,lambda tag=tag:codec.encode_relocatable_dialogue(raw,r['english']+tag,profile))
        reject(kind+'-widened-selectors',lambda:codec.encode_relocatable_dialogue(raw,r['english'],replace(profile,leading_speaker_bytes=profile.leading_speaker_bytes|{148})))
    assert len(negatives)==28 and Counter(r['editorial_decision'] for r in doc['records'])=={'revise':22,'retain-wording':16};assert all(r.get('qa_waivers') in [None,['line-break-count']] for r in doc['records']);notes=sum(bool(r.get('qa_waivers')) for r in doc['records']);assert notes==18
    ROOT.mkdir(parents=True);merged=ROOT/'all38_native_macro_font_and_source_reconciliation.json';evidence={str(p):sha(p.read_bytes()) for p in [INPUT,FONT,REUSE,Path('work/analysis/lil_B142_B145_visual_refinement_v3588/observed_wrap_finding_and_scoped_successors.json'),Path('work/analysis/lil_B145_picture_controls_v3587/three_original_item_picture_descriptors_and_hide_eight_cases.json')]}
    save(merged,dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),manuscript=str(INPUT),manuscript_sha256=sha(INPUT.read_bytes()),cases=font['cases'],current_original_macro_alignment_calls=304,new_latest_macro_cases=8,exact_reused_macro_cases=296,progressive_planes=37,FE_planes=1,all38_current_native_speech_planes_pass=True,review_sheets=sheets,source_English_macro_control_invariants=invariants,source_bound_formatter_negatives=negatives,source_consumer_negative_controls=font['source_consumer_negative_controls'],evidence=evidence,scoped_profile=doc['scoped_profile_module'],scoped_profile_sha256=doc['scoped_profile_module_sha256'],native_formatter_module=doc['native_formatter_module'],native_formatter_module_sha256=doc['native_formatter_module_sha256'],source_FI2_native_default_Lil_and_logical_template_distinguished=True,source_Cesare0D_Shipwright6D_and_FE_nullactor_preserved=True,FE_logical228x48_and_physical228x64_rules_distinguished=True,prior_FE_logical_row_harness_assumption_corrected_without_production_change=True,no_new_gameplay_orcompletion_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),native_font_proof=str(merged),native_font_proof_sha256=sha(merged.read_bytes()),native_progressive_and_FE_proof=str(FONT),formatting_review_pending=False,all38_five_review_gates_true=True,formatter_phrase_flow_finding_resolved_without_waiver=True,status='source-prose-current-native-format-approved;relocation-references-representative-release-pending');validate_natural_dialogue_batch(doc);save(OUTPUT,doc)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),merged_native_proof=str(merged),merged_native_proof_sha256=sha(merged.read_bytes()),all38_five_review_gates_true=True,revised=22,retained=16,progressive_planes=37,FE_planes=1,current_macro_alignment_cases=304,source_consumer_negatives=28,formatter_negatives=28,narrow_row_count_notes=notes,review_sheets=sheets,actual_selected_B142_B145_IDs=[],new_emulator_runs=0,relocation_references_representative_registered_release_pending=True,new_source_prose_reviews=0,new_completed_records=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('38 five-gate reviews approved:22 revisions/16 justified retentions;37 progressive+one FE planes,304 macro cases,56 negatives,18 row notes. Integration pending.')
