"""Seal90 current-native formatting reviews; keep integration gates pending."""
from pathlib import Path
from copy import deepcopy
from dataclasses import replace
from collections import Counter
from dk4tool.dialogue.codec import parse_markup
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.lil_goods_mediterranean_profile import profile_for
from dk4tool.dialogue import lil_goods_mediterranean_layout_v2 as codec
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Goods_Mediterranean_font_approval_v2830')
OLD=Path('translations/lil_goods_mediterranean_editorial_manuscript_v4.json')
DOC=Path('translations/lil_goods_mediterranean_editorial_manuscript_v5.json')
FONT=Path('work/analysis/lil_Goods_Mediterranean_fonts_v2829/current_macro_QA_and_progressive_font_proof.json')

def semantic_tokens(markup):
    tokens=parse_markup(markup)
    controls=[(t.kind,t.value) for t in tokens if t.kind not in ['text','line_break','align']]
    words=' '.join(''.join(t.value if t.kind=='text' else (' ' if t.kind=='line_break' else '{'+t.kind+':'+t.value+'}') for t in tokens).split())
    return controls,words

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();doc=deepcopy(read(OLD));font=read(FONT)
    assert font['manuscript_sha256']==sha(OLD.read_bytes()) and font['all90_progressive_full_QA_and_complete_native_fonts_pass']
    assert len(font['cases'])==len(font['all90_full_QA_reports'])==90 and font['current_original_macro_alignment_calls']==720
    assert len(font['negative_controls'])==7 and len(font['review_sheets'])==12
    assert all(sha(Path(s['path']).read_bytes())==s['sha256'] for s in font['review_sheets'])
    prior=read(font['reused_proof']);assert sha(Path(font['reused_proof']).read_bytes())==font['reused_proof_sha256']
    assert font['newly_executed_font_cases']==4 and font['reused_unchanged_font_cases']==86
    assert font['newly_executed_current_macro_alignment_cases']==32 and font['reused_current_macro_alignment_cases']==688
    changed={i//8 for i,c in enumerate(font['cases']) if not c.get('reused_current_native_case')};assert changed=={7,8,9}
    for i,sheet in enumerate(font['review_sheets']):
        if i not in changed:assert sheet['sha256']==prior['review_sheets'][i]['sha256']
    # All12 original2827 sheets and changed2829 sheets8/9/10 were viewed.

    assert font['candidate_sha256']==doc['current_ROM_sha256'] and font['ARM9_sha256']==doc['required_runtime_ARM9_sha256']
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    cases={c['id']:c for c in font['cases']};reports={c['id']:c for c in font['all90_full_QA_reports']};invariants=[]
    # Every one of the12 full native contact sheets is viewed before this producer runs.
    for row in doc['records']:
        case=cases[row['id']];profile=profile_for(arm,blocks[row['block']]);compiled=codec.encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile)
        assert compiled.encoded.hex()==case['encoded_hex']==reports[row['id']]['encoded_hex']
        assert semantic_tokens(row['english'])==semantic_tokens(compiled.formatted_markup) and compiled.encoded[:1]==bytes.fromhex(row['source_presentation_prefix_hex'])
        assert case['complete_native_independent216x64_plane_equal'] and case['all_first_final_internal_glyphs_in_order_and_unique_cells'] and case['all_visible_origins_zero_and16px_rows_within4rows']
        invariants.append(dict(id=row['id'],complete_reviewed_English_and_control_macro_order_preserved=True,encoded_sha256=sha(compiled.encoded)))
        row['review']['formatting']=True
        row.update(compiled_hex=case['encoded_hex'],native_font_case=case,record_index=row['current_record_index'],current_text_hex=row['current_hex'],native_display_consumer='original_progressive_54020',status='source-prose-current-native-format-approved;reference-representative-release-pending')
    row=doc['records'][0];raw=bytes.fromhex(row['source_hex']);profile=profile_for(arm,blocks[row['block']]);negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as error:negatives.append(dict(case=label,rejected=True,error=str(error)))
        else:raise AssertionError(label)
    for label,p in [('width',replace(profile,window_width_px=228)),('rows',replace(profile,max_lines=5)),('glyph',replace(profile,default_ascii_width=5)),('row-spacing',replace(profile,line_height_px=12)),('disabled-LF-guard',replace(profile,guard_linebreaks=False)),('disabled-pair-phase',replace(profile,pair_phase_safe_breaks=False)),('disabled-balancing',replace(profile,balanced_wrapping=False)),('macro-width',replace(profile,macro_ascii_lengths={**profile.macro_ascii_lengths,'FO':10})),('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:
        reject(label,lambda p=p:codec.encode_relocatable_dialogue(raw,row['english'],p))
    for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:reject('manual-or-end-'+tag,lambda tag=tag:codec.encode_relocatable_dialogue(raw,row['english']+tag,profile))
    reject('widened-source-selectors',lambda:codec.encode_relocatable_dialogue(raw,row['english'],replace(profile,leading_speaker_bytes=profile.leading_speaker_bytes|{148})))
    assert len(negatives)==14 and len(invariants)==90
    for path,digest in codec.DEPENDENCIES.items():assert sha(Path(path).read_bytes())==digest
    assert Counter(r['editorial_decision'] for r in doc['records'])=={'revise':67,'retain-wording':23}
    assert sum(bool(r.get('qa_waivers')) for r in doc['records'])==42 and all(r.get('qa_waivers') in [None,['line-break-count']] for r in doc['records'])
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),formatting_review_pending=False,all90_current_native_planes_and720_macro_cases_bound=True,all12_review_sheets_viewed=True,phrase_flow_refinement_preserves_complete_source_meaning=True,status='source-prose-current-native-format-approved;reference-representative-release-pending')
    validate_natural_dialogue_batch(doc);ROOT.mkdir(parents=True);save(DOC,doc)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),all90_five_per_record_review_gates_true=True,current_complete_native_panels=90,current_macro_alignment_cases=720,all12_review_sheets_viewed=True,review_sheets=font['review_sheets'],source_English_control_macro_invariants=invariants,source_bound_formatter_negatives=negatives,effective_planner_sha256=codec.EFFECTIVE_PLANNER_SHA256,global_helpers_unchanged=codec.DEPENDENCIES,narrow_line_count_notes=42,no_weak_orphan_predicate_control_overflow_glyph_or_blank_page_waivers=True,phrase_flow_refinements=doc['phrase_flow_refinements'],actual_selected_Goods_Mediterranean_IDs=[],new_emulator_runs=0,reference_representative_registered_release_pending=True,source_prose_orcompletion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('90source/prose/native reviews sealed:90complete fontplanes/720macro cases,14formatter rejections,42line-count-only notes. References/representative/release pending;zero credit.')
