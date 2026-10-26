"""Seal218 source/prose/native reviews, retaining separate runtime consumers."""
from pathlib import Path
from copy import deepcopy
from dataclasses import replace
from collections import Counter
from dk4tool.dialogue.codec import parse_markup
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.lil_kuhn_china_profile import profile_for
from dk4tool.dialogue import lil_kuhn_china_layout_v1 as codec
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Kuhn_China_font_approval_v2905')
OLD=Path('translations/lil_kuhn_china_editorial_manuscript_v5.json')
DOC=Path('translations/lil_kuhn_china_editorial_manuscript_v6.json')
FONT=Path('work/analysis/lil_Kuhn_China_fonts_v2904/current_macro_QA_and_progressive_font_proof.json')
FE=Path('work/analysis/lil_Kuhn_China_FE_v2901b/current_FE_macro_font_and_typed_paper_proof.json')


def semantic_tokens(markup):
    tokens=parse_markup(markup)
    controls=[(t.kind,t.value) for t in tokens if t.kind not in ['text','line_break','align']]
    words=' '.join(''.join(t.value if t.kind=='text' else (' ' if t.kind=='line_break' else '{'+t.kind+':'+t.value+'}') for t in tokens).split())
    return controls,words


if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();doc=deepcopy(read(OLD));font=read(FONT);fe=read(FE)
    assert font['manuscript_sha256']==sha(OLD.read_bytes()) and font['all196_progressive_full_QA_and_complete_native_fonts_pass']
    assert len(font['cases'])==196 and len(font['all218_full_QA_reports'])==218 and font['current_original_macro_alignment_calls']==1568
    assert len(font['negative_controls'])==11 and len(font['review_sheets'])==25
    prior=read(font['reused_proof']);assert sha(Path(font['reused_proof']).read_bytes())==font['reused_proof_sha256']
    assert font['newly_executed_font_cases']==1 and font['reused_unchanged_font_cases']==195
    assert font['newly_executed_current_macro_alignment_cases']==8 and font['reused_current_macro_alignment_cases']==1560
    changed={i//8 for i,c in enumerate(font['cases']) if not c.get('reused_current_native_case')};assert changed=={6}
    for i,sheet in enumerate(font['review_sheets']):
        if i not in changed:assert sheet['sha256']==prior['review_sheets'][i]['sha256']
    assert len(fe['cases'])==22 and fe['current_original_null_actor_macro_alignment_cases']==176
    assert fe['all22_one_native_page_consumes_complete_target'] and fe['all22_complete_native_independent_planes_all_glyphs_and_canaries_equal']
    assert len(fe['all21_source_literal_speaker_labels_preserved'])==21 and len(fe['source_FI_null_actor_cases'])==1 and len(fe['review_sheets'])==3
    assert sha(Path(fe['manuscript']).read_bytes())==fe['manuscript_sha256']
    fe_rows={r['id']:r for r in read(fe['manuscript'])['records'] if r['kind']=='system-FE'}
    sheets=font['review_sheets']+fe['review_sheets']
    # All25 initial normal sheets and3 FE sheets were viewed, then changed normal sheet7.
    # The24 unchanged successor normal sheets are byte-identical to viewed predecessors.
    assert all(sha(Path(s['path']).read_bytes())==s['sha256'] for s in sheets)
    for proof in [font,fe]:
        assert proof['candidate_sha256']==doc['current_ROM_sha256'] and proof['ARM9_sha256']==doc['required_runtime_ARM9_sha256']
        assert sha(Path(proof['scoped_profile']).read_bytes())==proof['scoped_profile_sha256']
        assert sha(Path(proof['native_formatter_module']).read_bytes())==proof['native_formatter_module_sha256']
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    cases={c['id']:c for c in font['cases']+fe['cases']};reports={c['id']:c for c in font['all218_full_QA_reports']};invariants=[]
    for row in doc['records']:
        isfe=row['kind']=='system-FE';case=cases[row['id']];profile=profile_for(arm,blocks[row['block']],'FE-paper' if isfe else 'progressive')
        compiled=codec.encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile)
        assert compiled.encoded.hex()==case['encoded_hex']==reports[row['id']]['encoded_hex']
        assert semantic_tokens(row['english'])==semantic_tokens(compiled.formatted_markup) and compiled.encoded[:1]==bytes.fromhex(row['source_presentation_prefix_hex'])
        assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
        if isfe:
            old=fe_rows[row['id']]
            assert all(row[k]==old[k] for k in ['source_hex','current_hex','english','source_presentation_prefix_hex','kind'])
            assert case['complete_native_independent_plane_and_all_glyphs_and_canaries_equal'] and case['one_native_page_consumes_complete_target'] and case['all_visible_origins_zero_and4rows']
            assert sha(Path(case['native_plane']).read_bytes())==case['native_plane_sha256']
        else:
            assert case['complete_native_independent216x64_plane_equal'] and case['all_first_final_internal_glyphs_in_order_and_unique_cells'] and case['all_visible_origins_zero_and16px_rows_within4rows']
        invariants.append(dict(id=row['id'],complete_reviewed_English_and_control_macro_order_preserved=True,encoded_sha256=sha(compiled.encoded),consumer='FE-paper' if isfe else 'progressive',FE_unchanged_from_executed_proof=isfe))
        row['review']['formatting']=True
        row.update(compiled_hex=case['encoded_hex'],native_font_case=case,record_index=row['current_record_index'],current_text_hex=row['current_hex'],
            native_display_consumer='original_FE_5473C_mode1_paper' if isfe else 'original_progressive_54020',status='source-prose-current-native-format-approved;reference-representative-release-pending')
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
    assert len(negatives)==28 and len(invariants)==218
    for path,digest in codec.DEPENDENCIES.items():assert sha(Path(path).read_bytes())==digest
    assert Counter(r['editorial_decision'] for r in doc['records'])=={'revise':152,'retain-wording':66}
    assert sum(bool(r.get('qa_waivers')) for r in doc['records'])==89 and all(r.get('qa_waivers') in [None,['line-break-count']] for r in doc['records'])
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),
        native_FE_font_proof=str(FE),native_FE_font_proof_sha256=sha(FE.read_bytes()),formatting_review_pending=False,all218_current_native_planes_and1744_macro_cases_bound=True,all28_review_sheets_viewed=True,
        phrase_flow_refinement_preserves_complete_source_meaning=True,status='source-prose-current-native-format-approved;reference-representative-release-pending')
    validate_natural_dialogue_batch(doc);ROOT.mkdir(parents=True);save(DOC,doc)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),native_FE_font_proof=str(FE),native_FE_font_proof_sha256=sha(FE.read_bytes()),
        all218_five_per_record_review_gates_true=True,current_complete_native_panels=218,current_macro_alignment_cases=1744,ordinary_macro_alignment_cases=1568,FE_null_actor_alignment_cases=176,
        all28_review_sheets_viewed=True,changed_successor_sheet7_viewed=True,unchanged_successor_sheets24_exact=True,review_sheets=sheets,source_English_control_macro_invariants=invariants,source_bound_formatter_negatives=negatives,
        effective_planner_sha256=codec.EFFECTIVE_PLANNER_SHA256,global_helpers_unchanged=codec.DEPENDENCIES,narrow_line_count_notes=89,no_weak_orphan_predicate_control_overflow_glyph_or_blank_page_waivers=True,
        phrase_flow_refinements=doc['phrase_flow_refinements'],actual_selected_Kuhn_China_IDs=[],new_emulator_runs=0,reference_representative_registered_release_pending=True,source_prose_orcompletion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('218source/prose/native reviews sealed:196normal+22FE complete planes/1744macro cases,28metric-layout rejections,89line-count-only notes. Reference/representative/release pending;zero credit.')
