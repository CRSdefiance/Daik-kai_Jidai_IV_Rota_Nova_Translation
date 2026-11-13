"""Seal the viewed B175 source/prose/native pass; actual scene/release remain pending."""
import re
from collections import Counter
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue import lil_B175_layout_v1 as codec
from dk4tool.dialogue.lil_B175_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B175_native_approval_v4518')
INPUT=Path('translations/lil_B175_editorial_manuscript_v2.json')
OUTPUT=Path('translations/lil_B175_editorial_manuscript_v3.json')
FONT=Path('work/analysis/lil_B175_fonts_v4517/all32_progressive_FE_native_planes_and256_alignment_cases.json')

def validate_source_macros(raw,english):
    if re.findall(rb'FI|FA|FO',raw[1:])!=[v.encode('ascii') for v in re.findall(r'\{MACRO:(FI|FA|FO)\}',english)]:
        raise ValueError('All source FI/FA/FO substitutions and their order are required')

if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    doc,font=deepcopy(read(INPUT)),read(FONT)
    assert font['manuscript_sha256']==sha(INPUT.read_bytes())
    assert len(font['cases'])==32 and font['current_original_macro_alignment_calls']==256
    assert (font['complete_progressive_planes'],font['complete_FE_logical_and_physical_planes'])==(23,9)
    assert len(font['negative_controls'])==24 and all(r['rejected'] for r in font['negative_controls'])
    im=NdsImage.open(doc['current_ROM']);arm=im.read_file('/__arm9__.bin')
    block=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[175]
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==font['candidate_sha256']
    assert sha(arm)==font['ARM9_sha256']==doc['required_runtime_ARM9_sha256']
    sheets=[]
    for sheet in font['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
        sheets.append({**sheet,'viewed_in_full_current_turn':True,
            'review':'Viewed all32 complete progressive/FE panels across four sheets. Recognition builds into encirclement, defiance, pirate-pride rebuke, sea challenge, sword mystery and departure; relief then turns into teasing and concern. All13 retained wordings remain coherent. No clipped leading/internal/final glyph, missing punctuation, overflow, blank page or stranded auxiliary was found. Woman and sword remain unnamed, admiral stays source-bound, and no boss/rank/relationship is added. Offline native rendering; no actual B175 gameplay claim.'})
    assert len(sheets)==4
    cases={r['id']:r for r in font['cases']};invariants=[];macros=Counter()
    for row in doc['records']:
        raw=bytes.fromhex(row['source_hex']);isFE=row['kind']=='system-FE'
        p=profile_for(arm,block,'FE-paper' if isFE else 'progressive');c=cases[row['id']]
        encoded=codec.encode_relocatable_dialogue(raw,row['english'],p)
        assert encoded.encoded.hex()==row['compiled_hex']==c['encoded_hex']
        assert semantic_tokens(row['english'])==semantic_tokens(encoded.formatted_markup)
        validate_source_macros(raw,row['english']);macros.update(re.findall(rb'FI|FA|FO',raw[1:]))
        assert c['complete_native_independent228x48_plane_equal' if isFE else 'complete_native_independent216x64_plane_equal']
        assert c['all_first_final_internal_glyphs_in_order_and_unique_cells'] and c['all_visible_origins_zero_and_within_four_rows']
        assert c['one_native_page_consumes_complete_target'] and sha(Path(c['preview']).read_bytes())==c['preview_sha256']
        assert sum(len(v['cases']) for v in c['current_native_macro_pipelines'])==8
        if isFE:assert all(v['null_source_actor'] for pipeline in c['current_native_macro_pipelines'] for v in pipeline['cases'])
        qa=codec.audit_relocatable_dialogue_record(raw,row['english'],p)
        assert row.get('qa_waivers') in [None,['line-break-count']]
        assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not
                    (i['severity']=='warning' and i['code']=='line-break-count' and row.get('qa_waiver_reason'))]
        assert all(row['review'][g] for g in ['source','context','localization','naturalness'])
        row['review']['formatting']=True
        row.update(record_index=row['current_record_index'],current_text_hex=row['current_hex'],native_font_case=c,
            native_formatting_consumer='FE-paper' if isFE else 'progressive',native_plane_verified_not_actual_gameplay=True,
            current_complete_native_display_pending=False,current_native_voice_macro_entry_and_context_pending=False,
            status='source-prose-current-native-format-approved;relocation-references-story-representative-release-pending')
        invariants.append(dict(id=row['id'],block=175,source_selector=raw[0],whole_source_English_tokens_and_control_order_preserved=True,encoded_sha256=sha(encoded.encoded)))
        if row['editorial_decision']=='retain-wording':
            assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
    assert macros=={b'FI':4,b'FA':1}
    assert Counter(r['editorial_decision'] for r in doc['records'])=={'revise':19,'retain-wording':13}
    assert sum(bool(r.get('qa_waivers')) for r in doc['records'])==13
    negatives=[];macro_negatives=[]
    def reject(bucket,label,fn):
        try:fn()
        except (ValueError,AssertionError) as error:bucket.append(dict(case=label,rejected=True,error=str(error)))
        else:raise AssertionError(label)
    for consumer,selector in [('progressive',2),('FE-paper',254)]:
        p=profile_for(arm,block,consumer);r=next(r for r in doc['records'] if r['source_selector']==selector);raw=bytes.fromhex(r['source_hex'])
        for label,bad in [('width',replace(p,window_width_px=228)),('rows',replace(p,max_lines=5)),
            ('glyph',replace(p,default_ascii_width=5)),('row-spacing',replace(p,line_height_px=12)),
            ('disabled-LF-guard',replace(p,guard_linebreaks=False)),('disabled-pair-phase',replace(p,pair_phase_safe_breaks=False)),
            ('disabled-balancing',replace(p,balanced_wrapping=False)),('macro-length',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FO':10})),
            ('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:
            reject(negatives,consumer+'-'+label,lambda bad=bad,r=r,raw=raw:codec.encode_relocatable_dialogue(raw,r['english'],bad))
        for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:
            reject(negatives,consumer+'-manual-'+tag,lambda tag=tag,r=r,raw=raw,p=p:codec.encode_relocatable_dialogue(raw,r['english']+tag,p))
        reject(negatives,consumer+'-widened-selectors',lambda r=r,raw=raw,p=p:codec.encode_relocatable_dialogue(raw,r['english'],replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{149})))
    assert len(negatives)==28
    for r in doc['records']:
        for macro in re.findall(r'\{MACRO:(FI|FA|FO)\}',r['english']):
            bad=r['english'].replace('{MACRO:'+macro+'}','',1)
            reject(macro_negatives,r['id']+'-missing-'+macro,lambda r=r,bad=bad:validate_source_macros(bytes.fromhex(r['source_hex']),bad))
    r=next(r for r in doc['records'] if r['source_record_index']==73)
    bad=r['english'].replace('{MACRO:FI} {MACRO:FA}','{MACRO:FA} {MACRO:FI}')
    reject(macro_negatives,'full-name-order',lambda:validate_source_macros(bytes.fromhex(r['source_hex']),bad))
    for macro in ['FI','FA','FO']:
        r=doc['records'][0]
        reject(macro_negatives,'invented-'+macro,lambda r=r,m=macro:validate_source_macros(bytes.fromhex(r['source_hex']),r['english']+' {MACRO:'+m+'}'))
    assert len(macro_negatives)==9
    names=read(doc['source_nameplate_consumer_proof'])['native_ten_consumer_cases']['rows']
    assert len(names)==10
    assert sum(bool(r['original_scratch_rings']) and bool(r['original_getter_writes']) and r['actor_ID'] in [2,9] for r in names)==4
    assert sum(not r['original_scratch_rings'] and not r['original_getter_writes'] and r['actor_ID'] in [183,184,185] for r in names)==6
    assert all(r['all_actor_models_and_unowned4MiB_exact'] and r['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for r in names)
    ROOT.mkdir(parents=True);merged=ROOT/'all32_native_progressive_FE_and_source_reconciliation.json'
    save(merged,dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),
        manuscript=str(INPUT),manuscript_sha256=sha(INPUT.read_bytes()),cases=font['cases'],current_original_macro_alignment_calls=256,
        progressive_planes=23,FE_planes=9,review_sheets=sheets,source_English_macro_control_invariants=invariants,
        source_bound_formatter_negatives=negatives,source_consumer_negative_controls=font['negative_controls'],source_macro_preservation_negatives=macro_negatives,
        all32_current_native_speech_planes_pass=True,all32_source_facts_complete_exchange_and_individual_decisions_reconciled=True,
        source_FI4_FA1_order_five_static_selectors_and_null_actor_FE_preserved=True,
        source_three_presentations_one_resource_C200_two_ends_preserved_without_guessed_operands=True,
        scoped_profile=doc['scoped_profile_module'],scoped_profile_sha256=doc['scoped_profile_module_sha256'],
        native_formatter_module=doc['native_formatter_module'],native_formatter_module_sha256=doc['native_formatter_module_sha256'],
        evidence={str(p):sha(p.read_bytes()) for p in [INPUT,FONT,Path(doc['source_nameplate_consumer_proof']),Path(__file__)]},
        no_new_gameplay_or_completion_credit=True,full_goal_complete=False))
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),
        native_font_proof=str(merged),native_font_proof_sha256=sha(merged.read_bytes()),native_progressive_and_FE_proof=str(FONT),
        formatting_review_pending=False,all32_five_review_gates_true=True,formatter_phrase_flow_findings_resolved_without_waiver=True,
        clean_first_whole_exchange_context_notes_are_historical_and_followed_by_bound_current_contracts=True,
        status='source-prose-current-native-format-approved;relocation-references-story-representative-release-pending')
    validate_natural_dialogue_batch(doc);save(OUTPUT,doc)
    save(ROOT/'approval_receipt.json',dict(manuscripts={str(OUTPUT):sha(OUTPUT.read_bytes())},merged_native_proof=str(merged),
        merged_native_proof_sha256=sha(merged.read_bytes()),revised=19,retained=13,progressive_planes=23,FE_planes=9,
        current_macro_alignment_cases=256,source_consumer_negatives=24,source_macro_negatives=9,formatter_negatives=28,
        narrow_row_count_notes=13,review_sheets=sheets,actual_selected_B175_IDs=[],new_emulator_runs=0,
        relocation_references_representative_registered_release_pending=True,new_source_prose_reviews=0,new_completed_records=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B175:32 five-gate reviews,19 revisions/13 retentions;23 progressive+9 FE planes,256 alignments and61 negative controls. Actual scene/release pending;no credit yet.')
