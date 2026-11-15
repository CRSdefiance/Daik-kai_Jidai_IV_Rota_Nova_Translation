"""Seal67 five-gate reviews after viewed native planes and source-specific negatives."""
from collections import Counter
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue import lil_B139_B140_layout_v2 as codec
from dk4tool.dialogue.lil_B139_B140_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B139_B140_native_approval_v3475')
INPUT=Path('translations/lil_B139_B140_editorial_manuscript_v5.json')
OUTPUT=Path('translations/lil_B139_B140_editorial_manuscript_v6.json')
FONT=Path('work/analysis/lil_B139_B140_fonts_v3474/current_macro_QA_and_progressive_font_proof.json')
VISUAL=Path('work/analysis/lil_B139_B140_visual_flow_v3473/all9_viewed_native_sheets_and_phrase_findings.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=deepcopy(read(INPUT));font,visual=map(read,[FONT,VISUAL])
    assert font['manuscript_sha256']==sha(INPUT.read_bytes()) and len(font['cases'])==67 and font['current_original_macro_alignment_calls']==536
    assert len(font['negative_controls'])==23 and all(c['rejected'] for c in font['negative_controls'])
    assert (font['newly_executed_font_cases'],font['reused_unchanged_font_cases'])==(8,59) and sha(Path(font['reused_proof']).read_bytes())==font['reused_proof_sha256']
    assert visual['all9_progressive_sheets_viewed'] and len(visual['findings'])==8
    old=read(font['reused_proof']);changed={i for i,(a,b) in enumerate(zip(old['review_sheets'],font['review_sheets'],strict=True),1) if a['sha256']!=b['sha256']};assert changed=={2,4,5,7}
    sheets=[]
    for i,s in enumerate(font['review_sheets'],1):
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        if i not in changed:assert any(v['sha256']==s['sha256'] for v in visual['sheets'])
        sheets.append({**s,'review':'viewed current successor; phrase findings resolved' if i in changed else 'hash-identical to viewed predecessor'})
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    assert font['candidate_sha256']==doc['current_ROM_sha256'] and font['ARM9_sha256']==sha(arm)==doc['required_runtime_ARM9_sha256'] and font['COMMON_sha256']==sha(image.read_file('/COMMON/MESFILE.DK4'))
    assert font['native_formatter_module_sha256']==doc['native_formatter_module_sha256']==sha(Path(doc['native_formatter_module']).read_bytes())
    cases=[];invariants=[]
    for c in font['cases']:
        assert c['complete_native_independent216x64_plane_equal'] and c['all_first_final_internal_glyphs_in_order_and_unique_cells'] and c['all_visible_origins_zero_and16px_rows_within4rows']
        cases.append({**c,'consumer':'progressive','macro_cases':[v for p in c['current_native_macro_pipelines'] for v in p['cases']],'native_font_plane_sha256':c['whole_native_plane_sha256'],'whole_native_independent_font_plane_exact':True})
    byid={c['id']:c for c in cases};obsolete=[]
    for r in doc['records']:
        raw=bytes.fromhex(r['source_hex']);c=byid[r['id']];encoded=codec.encode_relocatable_dialogue(raw,r['english'],profile_for(arm,blocks[r['block']]))
        assert encoded.encoded.hex()==r['compiled_hex']==c['encoded_hex'] and encoded.encoded[0]==raw[0]==r['source_selector'] and b'\0' not in encoded.encoded
        assert semantic_tokens(r['english'])==semantic_tokens(encoded.formatted_markup) and sha(Path(c['preview']).read_bytes())==c['preview_sha256']
        if r.get('qa_waivers') and not any(d.code=='line-break-count' for d in encoded.diagnostics):
            assert r['qa_waivers']==['line-break-count'];reason=r['qa_waiver_reason'];item=dict(id=r['id'],old_waivers=r['qa_waivers'],old_reason=reason,reason='Final encoder has no row-count difference.');obsolete.append(item);r['obsolete_row_count_note_removed']=item
            r['localization_note']=r['localization_note'].replace(reason,'').rstrip();r.pop('qa_waivers');r.pop('qa_waiver_reason')
        r['review']['formatting']=True;r.update(record_index=r['current_record_index'],current_text_hex=r['current_hex'],native_font_case=c,native_formatting_consumer='progressive',current_complete_native_display_pending=False,status='source-prose-current-native-format-approved;relocation-representative-release-pending')
        invariants.append(dict(id=r['id'],source_speaker_macro_order_and_complete_English_tokens_exact=True,encoded_sha256=sha(encoded.encoded),consumer='progressive'))
    questions=[]
    for ident,prefix,count in [('DK4_MES_B140_R0071',2,3),('DK4_MES_B140_R0130',2,6),('DK4_MES_B140_R0274',9,6)]:
        c=byid[ident];events=[(e['code'],e['x'],e['y']) for e in c['complete_glyph_events'] if e['code']!=32]
        assert bytes.fromhex(c['encoded_hex'])==bytes([prefix])+b'.'*count and events==[(46,6*n,0) for n in range(count)]
        assert len(c['current_native_macro_pipelines'])==2 and all(len(p['cases'])==4 for p in c['current_native_macro_pipelines'])
        questions.append(dict(id=ident,encoded_hex=c['encoded_hex'],complete_visible_glyphs=events,source_wordless_reaction_not_placeholder=True,wording_retained_storage_normalized=True))
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as e:negatives.append(dict(case=label,rejected=True,error=str(e)))
        else:raise AssertionError(label)
    r=doc['records'][0];raw=bytes.fromhex(r['source_hex']);profile=profile_for(arm,blocks[139])
    for label,p in [('width',replace(profile,window_width_px=228)),('rows',replace(profile,max_lines=5)),('glyph',replace(profile,default_ascii_width=5)),('row-spacing',replace(profile,line_height_px=12)),('disabled-LF-guard',replace(profile,guard_linebreaks=False)),('disabled-pair-phase',replace(profile,pair_phase_safe_breaks=False)),('disabled-balancing',replace(profile,balanced_wrapping=False)),('macro-width',replace(profile,macro_ascii_lengths={**profile.macro_ascii_lengths,'FO':10})),('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:reject(label,lambda p=p:codec.encode_relocatable_dialogue(raw,r['english'],p))
    for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:reject('manual-or-end-'+tag,lambda tag=tag:codec.encode_relocatable_dialogue(raw,r['english']+tag,profile))
    reject('widened-selectors',lambda:codec.encode_relocatable_dialogue(raw,r['english'],replace(profile,leading_speaker_bytes=profile.leading_speaker_bytes|{148})))
    assert len(negatives)==14 and len(sheets)==9 and Counter(r['editorial_decision'] for r in doc['records'])=={'revise':29,'retain-wording':38}
    assert all(r.get('qa_waivers') in [None,['line-break-count']] for r in doc['records']);notes=sum(bool(r.get('qa_waivers')) for r in doc['records'])
    ROOT.mkdir(parents=True);merged=ROOT/'all67_native_macro_font_and_source_reconciliation.json'
    evidence={str(p):sha(p.read_bytes()) for p in [FONT,VISUAL,Path(font['reused_proof']),Path('work/analysis/lil_B139_B140_world_happiness_v3471/finding_and_successors.json')]}
    save(merged,dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),manuscript=str(INPUT),manuscript_sha256=sha(INPUT.read_bytes()),cases=cases,current_original_macro_alignment_calls=536,all67_current_native_speech_planes_pass=True,three_source_wordless_ellipses_complete_at_origin=questions,review_sheets=sheets,source_English_macro_control_invariants=invariants,obsolete_row_count_notes_removed=obsolete,source_bound_formatter_negatives=negatives,source_consumer_negative_controls=font['negative_controls'],evidence=evidence,one_Camille_registered_catalogue_replacement_raw_effective_provenance_preserved=True,leaf_platter_joke_Indian_Ocean_India_polder_personal_motive_and_conditional_replies_reviewed=True,no_new_gameplay_orcompletion_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),native_font_proof=str(merged),native_font_proof_sha256=sha(merged.read_bytes()),native_progressive_proof=str(FONT),formatting_review_pending=False,all67_five_review_gates_true=True,formatter_phrase_flow_findings_resolved_without_waiver=True,status='source-prose-current-native-format-approved;relocation-representative-release-pending');validate_natural_dialogue_batch(doc);save(OUTPUT,doc)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),merged_native_proof=str(merged),merged_native_proof_sha256=sha(merged.read_bytes()),all67_five_review_gates_true=True,progressive_planes=67,current_macro_alignment_cases=536,source_consumer_negatives=23,formatter_negatives=14,narrow_row_count_notes=notes,obsolete_notes_removed=len(obsolete),review_sheets=sheets,revised=29,retained=38,actual_selected_B139_B140_IDs=[],new_emulator_runs=0,relocation_representative_registered_release_pending=True,new_source_prose_reviews=0,new_completed_records=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(approved_speeches=67,revisions=29,retentions=38,planes=67,macro_cases=536,source_consumer_negatives=23,formatter_negatives=14,row_count_notes=notes,obsolete_notes_removed=len(obsolete),ellipses=3,credit=0))
