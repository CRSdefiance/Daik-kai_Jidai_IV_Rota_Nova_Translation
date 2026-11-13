"""Seal14 complete-context reviews after both viewed final native sheets."""
from collections import Counter
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue import lil_B141_layout_v2 as codec
from dk4tool.dialogue.lil_B141_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B141_native_approval_v3550')
INPUT=Path('translations/lil_B141_editorial_manuscript_v5.json')
OUTPUT=Path('translations/lil_B141_editorial_manuscript_v6.json')
FONT=Path('work/analysis/lil_B141_fonts_v3549/current_macro_QA_and_progressive_font_proof.json')
VISUAL=Path('work/analysis/lil_B141_visual_flow_v3547/both_viewed_sheets_and_phrase_flow_successors.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=deepcopy(read(INPUT));font=read(FONT);assert font['manuscript_sha256']==sha(INPUT.read_bytes()) and len(font['cases'])==14 and font['current_original_macro_alignment_calls']==112 and len(font['negative_controls'])==17
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[141];profile=profile_for(arm,block);cases=[]
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==font['candidate_sha256'] and sha(arm)==font['ARM9_sha256']==doc['required_runtime_ARM9_sha256']
    assert sha(Path(doc['native_formatter_module']).read_bytes())==doc['native_formatter_module_sha256']==font['native_formatter_module_sha256']
    sheets=[]
    for s in font['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256'];sheets.append({**s,'review':'Viewed final current successor;all five phrase-flow findings resolved.'})
    assert len(sheets)==2
    for c in font['cases']:
        assert c['complete_native_independent216x64_plane_equal'] and c['all_first_final_internal_glyphs_in_order_and_unique_cells'] and c['all_visible_origins_zero_and16px_rows_within4rows']
        cases.append({**c,'consumer':'progressive','macro_cases':[v for p in c['current_native_macro_pipelines'] for v in p['cases']],'native_font_plane_sha256':c['whole_native_plane_sha256'],'whole_native_independent_font_plane_exact':True})
    byid={c['id']:c for c in cases};obsolete=[];invariants=[]
    for r in doc['records']:
        raw=bytes.fromhex(r['source_hex']);encoded=codec.encode_relocatable_dialogue(raw,r['english'],profile);assert encoded.encoded.hex()==r['compiled_hex']==byid[r['id']]['encoded_hex'] and semantic_tokens(r['english'])==semantic_tokens(encoded.formatted_markup)
        if r.get('qa_waivers') and not any(d.code=='line-break-count' for d in encoded.diagnostics):
            reason=r['qa_waiver_reason'];assert r['qa_waivers']==['line-break-count'];obsolete.append(dict(id=r['id'],old_reason=reason));r['localization_note']=r['localization_note'].replace(reason,'').rstrip();r.pop('qa_waivers');r.pop('qa_waiver_reason')
        r['review']['formatting']=True;r.update(record_index=r['current_record_index'],current_text_hex=r['current_hex'],native_font_case=byid[r['id']],native_formatting_consumer='progressive',current_complete_native_display_pending=False,current_macro_dispatch_consumer_and_complete_native_display_pending=False,current_voice_macro_entry_conditional_and_whole_exchange_gloss_comparison_pending=False,status='source-prose-current-native-format-approved;relocation-references-representative-release-pending')
        invariants.append(dict(id=r['id'],source_static_selector_and_FI_macro_order_exact=True,complete_English_tokens_preserved=True,encoded_sha256=sha(encoded.encoded)))
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as e:negatives.append(dict(case=label,rejected=True,error=str(e)))
        else:raise AssertionError(label)
    r=doc['records'][0];raw=bytes.fromhex(r['source_hex'])
    for label,p in [('width',replace(profile,window_width_px=228)),('rows',replace(profile,max_lines=5)),('glyph',replace(profile,default_ascii_width=5)),('row-spacing',replace(profile,line_height_px=12)),('disabled-LF-guard',replace(profile,guard_linebreaks=False)),('disabled-pair-phase',replace(profile,pair_phase_safe_breaks=False)),('disabled-balancing',replace(profile,balanced_wrapping=False)),('macro-width',replace(profile,macro_ascii_lengths={**profile.macro_ascii_lengths,'FO':10})),('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:reject(label,lambda p=p:codec.encode_relocatable_dialogue(raw,r['english'],p))
    for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:reject('manual-or-end-'+tag,lambda tag=tag:codec.encode_relocatable_dialogue(raw,r['english']+tag,profile))
    reject('widened-selectors',lambda:codec.encode_relocatable_dialogue(raw,r['english'],replace(profile,leading_speaker_bytes=profile.leading_speaker_bytes|{148})))
    assert len(negatives)==14 and Counter(r['editorial_decision'] for r in doc['records'])=={'revise':7,'retain-wording':7}
    assert all(r.get('qa_waivers') in [None,['line-break-count']] for r in doc['records']);notes=sum(bool(r.get('qa_waivers')) for r in doc['records']);assert notes==9
    ROOT.mkdir(parents=True);merged=ROOT/'all14_native_macro_font_and_source_reconciliation.json';evidence={str(p):sha(p.read_bytes()) for p in [INPUT,FONT,VISUAL,Path('work/analysis/lil_B141_promise_v3545/finding_and_faithful_successors.json')]}
    save(merged,dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),manuscript=str(INPUT),manuscript_sha256=sha(INPUT.read_bytes()),cases=cases,current_original_macro_alignment_calls=112,all14_current_native_speech_planes_pass=True,review_sheets=sheets,source_English_macro_control_invariants=invariants,obsolete_row_count_notes_removed=obsolete,source_bound_formatter_negatives=negatives,source_consumer_negative_controls=font['negative_controls'],evidence=evidence,source_FI1_native_default_Lil_preserved=True,source_macro_template_retention_separate_from_current_expansion=True,no_new_gameplay_orcompletion_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),native_font_proof=str(merged),native_font_proof_sha256=sha(merged.read_bytes()),native_progressive_proof=str(FONT),formatting_review_pending=False,all14_five_review_gates_true=True,formatter_phrase_flow_findings_resolved_without_waiver=True,status='source-prose-current-native-format-approved;relocation-references-representative-release-pending');validate_natural_dialogue_batch(doc);save(OUTPUT,doc)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),merged_native_proof=str(merged),merged_native_proof_sha256=sha(merged.read_bytes()),all14_five_review_gates_true=True,revised=7,retained=7,progressive_planes=14,current_macro_alignment_cases=112,source_consumer_negatives=17,formatter_negatives=14,narrow_row_count_notes=notes,obsolete_notes_removed=len(obsolete),review_sheets=sheets,actual_selected_B141_IDs=[],new_emulator_runs=0,relocation_references_representative_registered_release_pending=True,new_source_prose_reviews=0,new_completed_records=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(approved_speeches=14,revisions=7,retentions=7,planes=14,macro_cases=112,consumer_negatives=17,formatter_negatives=14,row_count_notes=notes,credit=0))
