"""Seal172 speech formatting gates after complete native visual review."""
from pathlib import Path
from copy import deepcopy
from dataclasses import replace
from collections import Counter
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.lil_homecoming_ian_profile import profile_for
from dk4tool.dialogue import lil_homecoming_ian_layout_v2 as codec
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens

ROOT=Path('work/analysis/lil_Homecoming_Ian_font_approval_v3018')
OLD=Path('translations/lil_homecoming_ian_editorial_manuscript_v4.json')
DOC=Path('translations/lil_homecoming_ian_editorial_manuscript_v5.json')
FONT=Path('work/analysis/lil_Homecoming_Ian_fonts_v3013/current_macro_QA_and_progressive_font_proof.json')
FE=Path('work/analysis/lil_Homecoming_Ian_FE_v3017/current_FE_macro_font_and_typed_paper_proof.json')

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();doc,font,fe=map(read,[OLD,FONT,FE])
    assert font['manuscript_sha256']==sha(OLD.read_bytes()) and len(font['cases'])==158 and len(font['all172_full_QA_reports'])==172
    assert font['current_original_macro_alignment_calls']==1264 and font['all158_progressive_full_QA_and_complete_native_fonts_pass'] and len(font['negative_controls'])==13
    assert all(n['rejected'] for n in font['negative_controls'])
    assert len(fe['cases'])==14 and fe['current_original_null_actor_macro_alignment_cases']==112 and fe['all14_one_native_page_consumes_complete_target'] and fe['all14_complete_native_independent_planes_all_glyphs_and_canaries_equal']
    assert len(fe['source_FI_null_actor_cases'])==1 and fe['all14_source_panels_remain_distinct_and_unlabeled']
    assert fe['historical_calibration']['current_calibration_matches_complete_historical_ink_and_blank_mask'] and fe['no_initialized_historical_RAM_ITCM_or_DTCM_overlay_in_painter']
    assert fe['manuscript_sha256']==sha(OLD.read_bytes())
    fe_rows={r['id']:r for r in read(fe['manuscript'])['records'] if r['kind']=='system-FE'}
    sheets=font['review_sheets']+fe['review_sheets']
    # All20ordinary andboth FE sheets were viewed completely in this pass.
    assert len(font['review_sheets'])==20 and len(fe['review_sheets'])==2 and len(sheets)==22
    assert all(sha(Path(s['path']).read_bytes())==s['sha256'] for s in sheets)
    for p in [font,fe]:
        assert p['candidate_sha256']==doc['current_ROM_sha256'] and p['ARM9_sha256']==doc['required_runtime_ARM9_sha256']
        assert sha(Path(p['scoped_profile']).read_bytes())==p['scoped_profile_sha256']
        assert sha(Path(p['native_formatter_module']).read_bytes())==p['native_formatter_module_sha256']
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    assert font['COMMON_sha256']==fe['COMMON_sha256']==sha(image.read_file('/COMMON/MESFILE.DK4'))
    cases=[]
    for c in font['cases']:
        assert c['complete_native_independent216x64_plane_equal'] and c['all_first_final_internal_glyphs_in_order_and_unique_cells']
        cases.append(dict(**c,consumer='progressive',macro_cases=[v for p in c['current_native_macro_pipelines'] for v in p['cases']],native_font_plane_sha256=c['whole_native_plane_sha256'],whole_native_independent_font_plane_exact=True))
    for c in fe['cases']:
        assert c['complete_native_independent_plane_and_all_glyphs_and_canaries_equal'] and c['one_native_page_consumes_complete_target'] and c['all_visible_origins_zero_and4rows']
        assert sha(Path(c['native_plane']).read_bytes())==c['native_plane_sha256']
        cases.append(dict(**c,consumer='FE-paper',macro_cases=[v for p in c['current_native_macro_pipelines'] for v in p['cases']],native_font_plane_sha256=c['native_plane_sha256'],whole_native_independent_font_plane_exact=True,logical_geometry=[228,48],physical_row_advance=16))
    assert len(cases)==172 and sum(len(c['macro_cases']) for c in cases)==1376
    byid={c['id']:c for c in cases};invariants=[]
    for row in doc['records']:
        c=byid[row['id']];consumer='FE-paper' if row['kind']=='system-FE' else 'progressive';raw=bytes.fromhex(row['source_hex'])
        result=codec.encode_relocatable_dialogue(raw,row['english'],profile_for(arm,blocks[row['block']],consumer))
        assert result.encoded.hex()==c['encoded_hex'] and semantic_tokens(row['english'])==semantic_tokens(result.formatted_markup)
        assert result.encoded[:1]==bytes.fromhex(row['source_presentation_prefix_hex']) and b'\0' not in result.encoded
        assert sha(Path(c['preview']).read_bytes())==c['preview_sha256']
        if consumer=='FE-paper':assert all(row[k]==fe_rows[row['id']][k] for k in ['english','source_hex','current_hex','source_presentation_prefix_hex','kind'])
        invariants.append(dict(id=row['id'],source_speaker_macro_order_and_complete_English_tokens_exact=True,encoded_sha256=sha(result.encoded),consumer=consumer,FE_native_case_freshly_executed=consumer=='FE-paper'))
        row['review']['formatting']=True
        row.update(compiled_hex=c['encoded_hex'],native_font_case=c,native_formatting_consumer=consumer,record_index=row['current_record_index'],current_text_hex=row['current_hex'],native_display_consumer='original_FE_5473C_mode1_paper' if consumer=='FE-paper' else 'original_progressive_54020',status='source-prose-current-native-format-approved;reference-representative-release-pending')
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
    assert Counter(r['editorial_decision'] for r in doc['records'])=={'revise':120,'retain-wording':52}
    assert sum(bool(r.get('qa_waivers')) for r in doc['records'])==63 and all(r.get('qa_waivers') in [None,['line-break-count']] for r in doc['records'])
    ROOT.mkdir(parents=True);merged=ROOT/'all172_native_macro_font_reconciliation.json'
    save(merged,dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),manuscript=str(OLD),manuscript_sha256=sha(OLD.read_bytes()),cases=cases,current_original_macro_alignment_calls=1376,all172_current_native_planes_and_complete_glyphs_pass=True,all22_review_sheets=sheets,source_English_macro_control_invariants=invariants,source_bound_formatter_negatives=negatives,effective_planner_sha256=codec.EFFECTIVE_PLANNER_SHA256,global_helpers_unchanged=codec.DEPENDENCIES,evidence={str(p):sha(p.read_bytes()) for p in [FONT,FE,Path(doc['native_formatter_module']),Path(doc['scoped_profile_module'])]},actual_selected_Homecoming_Ian_IDs=[],new_emulator_runs=0,reference_representative_registered_release_pending=True,full_goal_complete=False))
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),native_font_proof=str(merged),native_font_proof_sha256=sha(merged.read_bytes()),native_progressive_proof=str(FONT),native_FE_proof=str(FE),native_FE_font_proof=str(FE),native_FE_font_proof_sha256=sha(FE.read_bytes()),formatting_review_pending=False,all172_native_planes_and1376_current_macro_calls_pass=True,all22_review_sheets_viewed=True,formatter_phrase_flow_findings_resolved_without_waiver=True,source_0D_cross_consumer_and_missing_selector_negatives_pass=True,status='source-prose-current-native-format-approved;reference-representative-release-pending')
    validate_natural_dialogue_batch(doc);save(DOC,doc)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),merged_native_proof=str(merged),merged_native_proof_sha256=sha(merged.read_bytes()),all172_five_review_gates_true=True,progressive_planes=158,FE_planes=14,current_macro_alignment_cases=1376,formatter_negatives=28,narrow_line_count_notes=63,all22_review_sheets=sheets,review_sheets=sheets,actual_selected_Homecoming_Ian_IDs=[],new_emulator_runs=0,reference_representative_registered_release_pending=True,source_prose_orcompletion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('172formatting gates sealed:158ordinary/14FE completeplanes,1376macro cases/28metric-layout rejections;zero completion credit.')
