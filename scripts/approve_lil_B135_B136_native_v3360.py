"""Seal35 per-record format gates withcomplete native planes andnegative tests."""
from collections import Counter
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue import lil_B135_B136_layout_v2 as codec
from dk4tool.dialogue.lil_B135_B136_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B135_B136_native_approval_v3360')
INPUT=Path('translations/lil_B135_B136_editorial_manuscript_v4.json')
OUTPUT=Path('translations/lil_B135_B136_editorial_manuscript_v5.json')
FONT=Path('work/analysis/lil_B135_B136_fonts_v3359/current_macro_QA_and_progressive_font_proof.json')
VISUAL=Path('work/analysis/lil_B135_B136_visual_refinement_v3358/all5_viewed_native_sheets_and_phrase_findings.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=deepcopy(read(INPUT));font,visual=map(read,[FONT,VISUAL]);assert font['manuscript_sha256']==sha(INPUT.read_bytes()) and len(font['cases'])==35 and font['current_original_macro_alignment_calls']==280 and len(font['negative_controls'])==21 and all(c['rejected'] for c in font['negative_controls'])
    assert (font['newly_executed_font_cases'],font['reused_unchanged_font_cases'])==(5,30) and sha(Path(font['reused_proof']).read_bytes())==font['reused_proof_sha256'];old=read(font['reused_proof']);assert visual['all5_progressive_sheets_viewed'];sheets=[]
    changed={i for i,(a,b) in enumerate(zip(old['review_sheets'],font['review_sheets'],strict=True),1) if a['sha256']!=b['sha256']};assert changed=={2,3,4,5}
    for i,s in enumerate(font['review_sheets'],1):
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        if i not in changed:assert any(v['sha256']==s['sha256'] for v in visual['sheets'])
        sheets.append({**s,'review':'viewed final successor with phrase findings resolved' if i in changed else 'hash-identical to viewed predecessor'})
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    assert font['candidate_sha256']==doc['current_ROM_sha256'] and font['ARM9_sha256']==sha(arm)==doc['required_runtime_ARM9_sha256'] and font['COMMON_sha256']==sha(image.read_file('/COMMON/MESFILE.DK4'))
    assert font['native_formatter_module_sha256']==doc['native_formatter_module_sha256']==sha(Path(doc['native_formatter_module']).read_bytes())
    cases=[];invariants=[]
    for c in font['cases']:
        assert c['complete_native_independent216x64_plane_equal'] and c['all_first_final_internal_glyphs_in_order_and_unique_cells'] and c['all_visible_origins_zero_and16px_rows_within4rows']
        cases.append({**c,'consumer':'progressive','macro_cases':[v for p in c['current_native_macro_pipelines'] for v in p['cases']],'native_font_plane_sha256':c['whole_native_plane_sha256'],'whole_native_independent_font_plane_exact':True})
    byid={c['id']:c for c in cases}
    for row in doc['records']:
        raw=bytes.fromhex(row['source_hex']);c=byid[row['id']];encoded=codec.encode_relocatable_dialogue(raw,row['english'],profile_for(arm,blocks[row['block']]))
        assert encoded.encoded.hex()==row['compiled_hex']==c['encoded_hex'] and encoded.encoded[0]==raw[0]==row['source_selector'] and b'\0' not in encoded.encoded
        assert semantic_tokens(row['english'])==semantic_tokens(encoded.formatted_markup) and sha(Path(c['preview']).read_bytes())==c['preview_sha256']
        row['review']['formatting']=True;row.update(record_index=row['current_record_index'],current_text_hex=row['current_hex'],native_font_case=c,native_formatting_consumer='progressive',current_complete_native_display_pending=False,status='source-prose-current-native-format-approved;relocation-representative-release-pending')
        invariants.append(dict(id=row['id'],source_speaker_macro_order_and_complete_English_tokens_exact=True,encoded_sha256=sha(encoded.encoded),consumer='progressive'))
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as e:negatives.append(dict(case=label,rejected=True,error=str(e)))
        else:raise AssertionError(label)
    row=doc['records'][0];raw=bytes.fromhex(row['source_hex']);profile=profile_for(arm,blocks[row['block']])
    for label,p in [('width',replace(profile,window_width_px=228)),('rows',replace(profile,max_lines=5)),('glyph',replace(profile,default_ascii_width=5)),('row-spacing',replace(profile,line_height_px=12)),('disabled-LF-guard',replace(profile,guard_linebreaks=False)),('disabled-pair-phase',replace(profile,pair_phase_safe_breaks=False)),('disabled-balancing',replace(profile,balanced_wrapping=False)),('macro-width',replace(profile,macro_ascii_lengths={**profile.macro_ascii_lengths,'FO':10})),('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:reject(label,lambda p=p:codec.encode_relocatable_dialogue(raw,row['english'],p))
    for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:reject('manual-or-end-'+tag,lambda tag=tag:codec.encode_relocatable_dialogue(raw,row['english']+tag,profile))
    reject('widened-selectors',lambda:codec.encode_relocatable_dialogue(raw,row['english'],replace(profile,leading_speaker_bytes=profile.leading_speaker_bytes|{148})))
    assert len(negatives)==14 and len(sheets)==5 and Counter(r['editorial_decision'] for r in doc['records'])=={'revise':16,'retain-wording':19} and sum(bool(r.get('qa_waivers')) for r in doc['records'])==15 and all(r.get('qa_waivers') in [None,['line-break-count']] for r in doc['records'])
    ROOT.mkdir(parents=True);merged=ROOT/'all35_native_macro_font_and_source_reconciliation.json'
    save(merged,dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),manuscript=str(INPUT),manuscript_sha256=sha(INPUT.read_bytes()),cases=cases,current_original_macro_alignment_calls=280,all35_current_native_speech_planes_pass=True,review_sheets=sheets,source_English_macro_control_invariants=invariants,source_bound_formatter_negatives=negatives,source_consumer_negative_controls=font['negative_controls'],evidence={str(p):sha(p.read_bytes()) for p in [FONT,VISUAL,Path(font['reused_proof']),Path('work/analysis/lil_B135_conditional_refinement_v3358c/finding_and_successors.json')]},one_registered_Camille_effective_current_wording_retained=True,chart_cheese_tart_joke_reviewed_as_complete_exchange=True,no_new_gameplay_orcompletion_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),native_font_proof=str(merged),native_font_proof_sha256=sha(merged.read_bytes()),native_progressive_proof=str(FONT),formatting_review_pending=False,all35_five_review_gates_true=True,formatter_phrase_flow_findings_resolved_without_waiver=True,status='source-prose-current-native-format-approved;relocation-representative-release-pending');validate_natural_dialogue_batch(doc);save(OUTPUT,doc)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),merged_native_proof=str(merged),merged_native_proof_sha256=sha(merged.read_bytes()),all35_five_review_gates_true=True,progressive_planes=35,current_macro_alignment_cases=280,source_consumer_negatives=21,formatter_negatives=14,narrow_row_count_notes=15,review_sheets=sheets,revised=16,retained=19,actual_selected_B135_B136_IDs=[],new_emulator_runs=0,relocation_representative_registered_release_pending=True,new_source_prose_reviews=0,new_completed_records=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('All35 five review gates pass:16revisions/19retentions,35nativeplanes/280macro cases,21consumer/14formatter negatives,fiveviewed/hash-exact sheets. Relocation/release pending.')
