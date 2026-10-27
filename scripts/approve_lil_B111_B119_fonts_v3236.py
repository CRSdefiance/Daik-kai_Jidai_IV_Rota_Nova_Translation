"""Seal all 150 contextual format gates; relocation and release remain pending."""
from collections import Counter
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue import lil_B111_B119_layout_v2 as codec
from dk4tool.dialogue.lil_B111_B119_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B111_B119_font_approval_v3236')
INPUTS=[Path('translations/lil_B111_B119_editorial_manuscript_v4.json'),Path('translations/lil_B111_B119_actor_style_manuscript_v3.json')]
OUTPUTS=[Path('translations/lil_B111_B119_editorial_manuscript_v5.json'),Path('translations/lil_B111_B119_actor_style_manuscript_v4.json')]
FONT=Path('work/analysis/lil_B111_B119_fonts_v3234c/current_macro_QA_and_progressive_font_proof.json')
FE=Path('work/analysis/lil_B111_B119_FE_v3235/current_FE_macro_font_and_typed_paper_proof.json')
VISUAL=Path('work/analysis/lil_B111_B119_refinement_v3232/native_visual_findings_and_successor_receipt.json')

if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in OUTPUTS)
    doc,voice=[deepcopy(read(p)) for p in INPUTS];font,fe=map(read,[FONT,FE])
    assert font['manuscript_sha256']==fe['manuscript_sha256']==sha(INPUTS[0].read_bytes())
    assert font['actor_style_manuscript_sha256']==sha(INPUTS[1].read_bytes())
    assert len(font['cases'])==149 and len(font['all150_full_QA_reports'])==150
    assert font['current_original_macro_alignment_calls']==1192
    assert len(font['negative_controls'])==43 and all(n['rejected'] for n in font['negative_controls'])
    assert (font['newly_executed_font_cases'],font['reused_unchanged_font_cases'])==(1,148)
    assert (font['newly_executed_current_macro_alignment_cases'],font['reused_current_macro_alignment_cases'])==(8,1184)
    assert sha(Path(font['reused_proof']).read_bytes())==font['reused_proof_sha256']
    prior=read(font['reused_proof']);visual=read(VISUAL)
    assert visual['all19_progressive_and1_FE_sheets_viewed']
    changed={i for i,(a,b) in enumerate(zip(prior['review_sheets'],font['review_sheets'],strict=True),1) if a['sha256']!=b['sha256']}
    assert changed=={4}
    sheets=[{**s,'review':'viewed successor sheet4 with intact sharp tongue idiom' if i in changed else 'hash-identical to viewed3230b sheet'} for i,s in enumerate(font['review_sheets'],1)]
    assert len(fe['cases'])==1 and fe['current_original_null_actor_macro_alignment_cases']==8
    for k in ['all1_one_native_page_consumes_complete_target','all1_complete_native_independent_planes_all_glyphs_and_canaries_equal','one_source_unlabeled24000_gold_notice_preserved_without_invented_names_or_macros','no_source_leading_vertical_staging_in_gold_notice','all1_successor_source_prose_runtime_and_encoded_outputs_exact','all1_FE_sheets_viewed_and_hash_unchanged']:
        assert fe[k],k
    assert not fe['source_leading_vertical_staging_cases']
    assert fe['historical_calibration']['current_calibration_matches_complete_historical_ink_and_blank_mask']
    assert fe['no_initialized_historical_RAM_ITCM_or_DTCM_overlay_in_painter']
    sheets.extend({**s,'review':'viewed3231 FE sheet; exact3235 output rebind'} for s in fe['review_sheets'])
    assert len(sheets)==20 and all(sha(Path(s['path']).read_bytes())==s['sha256'] for s in sheets)
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    assert sha(arm)==doc['required_runtime_ARM9_sha256']
    for p in [font,fe]:
        assert p['candidate_sha256']==doc['current_ROM_sha256'] and p['ARM9_sha256']==sha(arm) and p['COMMON_sha256']==sha(common)
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
            'native_font_plane_sha256':c['native_plane_sha256'],'whole_native_independent_font_plane_exact':True,'logical_geometry':[228,48],'physical_row_advance':16})
    assert len(cases)==150 and sum(len(c['macro_cases']) for c in cases)==1200
    byid={c['id']:c for c in cases};invariants=[]
    for d in [doc,voice]:
        for row in d['records']:
            isvoice=row['kind']=='typed-4100-actor-style-alternative';raw=bytes.fromhex(row['source_hex'])
            if isvoice:raw=bytes.fromhex(row['virtual_formatter_prefix_hex'])+raw
            c=byid[row['id']];encoded=codec.encode_relocatable_dialogue(raw,row['english'],profile_for(arm,blocks[row['block']],c['consumer']))
            assert encoded.encoded.hex()==row['compiled_hex']==c['encoded_hex']
            assert semantic_tokens(row['english'])==semantic_tokens(encoded.formatted_markup) and b'\0' not in encoded.encoded
            if isvoice:
                assert encoded.encoded[0]==row['source_selector']
                assert encoded.encoded[1:].hex()==row['compiled_stored_alternative_hex']
                assert row['virtual_formatter_prefix_is_not_part_of_stored_alternative_text']
            else:
                assert encoded.encoded[:1]==bytes.fromhex(row['source_presentation_prefix_hex'])
                row.update(record_index=row['current_record_index'],current_text_hex=row['current_hex'])
            assert sha(Path(c['preview']).read_bytes())==c['preview_sha256']
            row['review']['formatting']=True
            row.update(native_font_case=c,native_formatting_consumer=c['consumer'],status='source-prose-current-native-format-approved;relocation-representative-release-pending')
            if isvoice:row['actor_style_consumer_and_full_native_display_approval_pending']=False
            invariants.append(dict(id=row['id'],source_speaker_macro_order_and_complete_English_tokens_exact=True,encoded_sha256=sha(encoded.encoded),consumer=c['consumer'],actual_virtual_prefix_excluded_from_stored_body=isvoice))
    assert len(voice['records'])==34 and sum(len(r['style_indices']) for r in voice['records'])==48
    assert len({(r['block'],r['command_offset']) for r in voice['records']})==6
    assert {r['virtual_formatter_prefix_hex'] for r in voice['records']}=={'d0','d1','d6','d7','dc'}
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
    rows=doc['records']+voice['records']
    assert len(rows)==150 and Counter(r['editorial_decision'] for r in rows)=={'revise':47,'retain-wording':103}
    assert sum(bool(r.get('qa_waivers')) for r in rows)==46
    assert all(r.get('qa_waivers') in [None,['line-break-count']] for r in rows)
    ROOT.mkdir(parents=True);merged=ROOT/'all150_native_macro_font_reconciliation.json'
    save(merged,dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),manuscripts={str(p):sha(p.read_bytes()) for p in INPUTS},cases=cases,current_original_macro_alignment_calls=1200,all150_current_native_planes_and_complete_glyphs_pass=True,all20_review_sheets=sheets,source_English_macro_control_invariants=invariants,source_bound_formatter_negatives=negatives,source_consumer_negative_controls=font['negative_controls'],effective_planner_sha256=codec.EFFECTIVE_PLANNER_SHA256,global_helpers_unchanged=codec.DEPENDENCIES,evidence={str(p):sha(p.read_bytes()) for p in [FONT,FE,VISUAL]},actual_selected_B111_B119_IDs=[],new_emulator_runs=0,relocation_representative_registered_release_pending=True,source_prose_or_completion_credit_added=0,full_goal_complete=False))
    for d,old,new in zip([doc,voice],INPUTS,OUTPUTS,strict=True):
        d.update(previous_manuscript=str(old),previous_manuscript_sha256=sha(old.read_bytes()),review_gates=['source','context','localization','naturalness','formatting'],encoder='dialogue-relocatable-v1',prose_companions=[str(p) for p in OUTPUTS if p!=new],native_font_proof=str(merged),native_font_proof_sha256=sha(merged.read_bytes()),native_progressive_proof=str(FONT),native_FE_proof=str(FE),formatting_review_pending=False,all150_five_review_gates_true=True,formatter_phrase_flow_findings_resolved_without_waiver=True,status='source-prose-current-native-format-approved;relocation-representative-release-pending')
        validate_natural_dialogue_batch(d);save(new,d)
    save(ROOT/'approval_receipt.json',dict(manuscripts={str(p):sha(p.read_bytes()) for p in OUTPUTS},manuscript=str(OUTPUTS[0]),manuscript_sha256=sha(OUTPUTS[0].read_bytes()),actor_styles=str(OUTPUTS[1]),actor_styles_sha256=sha(OUTPUTS[1].read_bytes()),merged_native_proof=str(merged),merged_native_proof_sha256=sha(merged.read_bytes()),all150_five_review_gates_true=True,progressive_planes=149,FE_planes=1,current_macro_alignment_cases=1200,formatter_negatives=28,source_consumer_negatives=43,narrow_line_count_notes=46,all20_review_sheets=sheets,review_sheets=sheets,canonical_Maria32_pending_uncredited=True,unowned_appended_current_copy_bytes_must_remain_exact=True,actual_selected_B111_B119_IDs=[],new_emulator_runs=0,relocation_representative_registered_release_pending=True,source_prose_orcompletion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('All150 five gates sealed:149progressive/1FE planes,1200macro cases,43source-consumer/28formatter negatives,20viewed orhash-exact sheets;47revisions/103retentions. No integration credit.')
