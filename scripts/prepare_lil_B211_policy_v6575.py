"""Freeze twelve source/prose/native bindings without widening either original consumer."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B211_policy_tools_v6575');DOC=Path('translations/lil_B211_editorial_manuscript_v1.json');PLAN=Path('work/analysis/lil_B211_layout_v6559c/twelve_whole_paragraph_research_plans.json');CONTRACT=Path('translations/lil_B211_native_contract_v1.json');PROFILE=Path('dk4tool/dialogue/lil_B211_profile_v1.py');FORMATTER=Path('dk4tool/dialogue/lil_B211_layout_v1.py')
REASONS={
17:'All three drawn-out calls and two softer clucks,including the final emphatic call and pause,fit two complete English rows instead of three Japanese rows. No sound sequence is omitted andthe original FE null-actor modal consumer is unchanged. Four actual complete FE body/absence holds pass. Exact source/prose only.',
28:'The complete wondering question andsurprised carrying-something discovery use two natural English rows instead of three Japanese rows. Wait stays with its complete discovery clause;there is no added source pause,shortening or invented object identity. All actual complete glyph holds pass. Exact source/prose only.',
36:'The retained familiar call andquestion fit one complete English row. The Japanese break after the drawn-out given name supplies no essential dramatic pause. Current Cristina name identity andall words remain;actual full leading/internal/final glyphs andnameplate pass. Exact source/prose only.',
42:'The complete natural singular first-person wish,including too,uses one English row instead of two Japanese rows. Restoring I removes the old unsupported we without shortening for fit. Lil remains spontaneously disappointed at missing the birds. All native andactual complete glyphs pass. Exact source/prose only.',
45:'The full126-character observation,uncertain somewhere-near-Amsterdam report andinvitation require four original guarded English rows rather than three Japanese rows. All words,punctuation,uncertainty andquestion are retained;the physical page remains four rows. The long/and andwere/headed complete-word soft boundaries keep the full destination phrase andfinal invitation coherent without widening or shortening. Native andactual complete page holds pass. Exact source/prose only.',
}
PROFILE_CODE='''"""Exact B211 two-consumer/source/FI contract; no shared formatter or runtime mutation."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path('translations/lil_B211_native_contract_v1.json')
CONTRACT_SHA=@HASH@
ARM9_SHA='aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05'
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError('B211 frozen native contract changed')
    d=json.loads(raw)
    for p,h in d['dependencies'].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('B211 native dependency changed:'+p)
    if len(d['record_bindings'])!=12 or d['physical_native_rows_per_page']!=4 or d['complete_native_pages']!=12 or d['FE_pages']!=3 or d['FI_objects']!=1:raise ValueError('Complete B211 twelve-object/two-consumer contract required')
    return d
def expected_profile(ident):
    d=contract()
    if ident not in d['record_bindings']:raise ValueError('Unreviewed B211 record')
    r=d['record_bindings'][ident];base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B211-source-bound-v1:'+ident,max_lines=4,leading_speaker_bytes=frozenset({r['source_selector']}),metrics_source=base.metrics_source+';exact B211 record '+ident+'. Nine original216x64 progressive objects,two static actors/voice3,three original null-actor FE228x48 logical/228x64 physical objects with measured216px text capacity,and one original FI expansion toLil. Every paragraph occupies one original four-row page. Fonts,guards,pair phase andnative metrics unchanged;full glyphs/pages/actual holds independently proved.')
def profile_for(arm,source_block,ident):
    d=contract()
    if sha(arm)!=ARM9_SHA or sha(source_block) not in d['source_block_hashes']:raise ValueError('Exact B211 clean/current block andV6541 runtime required')
    return expected_profile(ident)
'''
if __name__=='__main__':
    assert not ROOT.exists() and all(not p.exists() for p in [CONTRACT,PROFILE,FORMATTER]);doc,plan=map(read,[DOC,PLAN]);SOURCE=Path(doc['source_context']);source=read(SOURCE);VIEW=Path('work/analysis/lil_B211_actual_view_v6573/all12_English_panels47_body35_name12_FE_holds_and_honest_later_limits_viewed.json');view=read(VIEW);assert not view['visual_review_pending'] and view['all12_objects12_native_pages47_complete_body_holds_viewed'];assert len(doc['records'])==12 and not plan['failures'] and plan['manuscript_sha256']==sha(DOC.read_bytes());planned={r['id']:r for r in plan['records']};bindings={};rowcounts=[]
    for row in doc['records']:
        ident=row['id'];p=planned[ident];index=row['source_record_index'];different=bytes.fromhex(row['source_hex']).count(b'\n')!=len(p['lines'])-1;assert different==(index in REASONS);rowcounts.append(index) if different else None;ordinary=[]
        if index==13:ordinary.append(dict(line=2,after_word='me,',before_word='are',reason='The complete introductory Tell me comma phrase ends on row2 andthe entire question follows on row3. This keeps all words andthe gentle address,avoids an unnecessary fourth row,andadds no dramatic pause or source opcode. Exact source/prose only.'))
        if index==45:
            ordinary.extend([dict(line=1,after_word='long',before_word='and',reason='Complete-word adjective continuation preserves long andshiny in the full126-character report;the complete observed object andits qualities stay unchanged. Four rows are required at the original guarded capacity. Exact source/prose only.'),dict(line=2,after_word='were',before_word='headed',reason='Normal complete-word auxiliary/participle wrapping keeps the entire headed somewhere near Amsterdam phrase on row3 andthe full invitation on row4. Uncertainty,nearby area andquestion remain;no widening or shortening. Exact source/prose only.')])
        for item in ordinary:item.update(exact_source_hex=row['source_hex'],exact_English=row['english'])
        bindings[ident]=dict(source_selector=row['source_selector'],source_kind=row['kind'],compiler_source_hex=row['source_hex'],planning_record={k:row[k] for k in ['id','english','kind','source_hex','source_selector']},compiled_hex=p['encoded_hex'],lines=p['lines'],maximum_total_rows=4,native_page_count=1,row_count_reason=REASONS.get(index),approved_base_weak_messages=[],ordinary_wrap_reasons=ordinary)
    assert rowcounts==[17,28,36,42,45]
    deps=[DOC,SOURCE,PLAN,VIEW,Path('translations/lil_B211_speaker_name_review_v3.json'),Path('work/analysis/lil_B211_research_fonts_v6560/all12_bodies12_complete_native_pages_and96_alignments_RESEARCH.json'),Path('work/analysis/lil_B211_stored_v6565/all12_final_stored_targets48_alignments_and12_complete_pages.json'),Path('work/analysis/lil_B211_source_native_view_v6563/twelve_source_objects_twelve_English_native_pages_names_and_scope_viewed.json'),Path('work/analysis/lil_B211_relocated_controls_v6572/twelve_target_dispatches_original_A000_and_five_guarded_ends.json'),Path('work/analysis/lil_B211_loader_v6570/whole_SC2_and_B211_initial_entry_proof.json'),Path('work/analysis/lil_B211_reference_census_v6571/all14_commands_no_relative_sites_and_shipped_entry_census.json'),Path('work/analysis/lil_B211_entry_v6558/source_EV2_B211_action_dependency_and_native_getter_binding.json'),Path('work/analysis/lil_B211_controls_v6557/one_source_current_structural_pair_and_ten_guarded_complete_end_cases.json'),Path('scripts/plan_lil_B211_layout_v6559c.py'),Path('scripts/Al_Ferid_exact_native_context_v6520.py'),Path('scripts/Al_Ferid_font_oracles_v6520.py'),Path('scripts/Al_Ferid_name_style_v6520.py'),Path(__file__),*[Path('dk4tool/dialogue')/(n+'.py') for n in ['profiles','codec','encoder','layout','qa','review']]]
    data=dict(format='B211-current-native-source-contract-v1',source_block_hashes=[source['blocks'][0]['clean_block_sha256'],source['blocks'][0]['current_block_sha256']],physical_native_rows_per_page=4,progressive_physical_viewport=[216,64],FE_original_logical_descriptor=[228,48],FE_physical_viewport=[228,64],FE_measured_text_capacity=216,complete_native_pages=12,progressive_pages=9,FE_pages=3,FI_objects=1,record_bindings=bindings,dependencies={str(p):sha(p.read_bytes()) for p in deps},all12_original_single_pages_and_all14_source_commands_bound=True,no_base_weak_ending_glyph_bounds_or_page_waiver=True,all10_timing6_RNG4_duration110_RGB18_prompt92_broader_and_final_state_limits_preserved=True,full207_name_role_alias_scope_and_88_Christina23_Cristina_consumers_open=True,source_prose_or_completion_credit_added=0,full_goal_complete=False);save(CONTRACT,data)
    profile=PROFILE_CODE.replace('@HASH@',repr(sha(CONTRACT.read_bytes())));formatter=checked_text(Path('dk4tool/dialogue/lil_B210_layout_v1.py').read_text('utf-8'),{'B210':'B211','scripts.plan_lil_B210_layout_v6507c':'scripts.plan_lil_B211_layout_v6559c','ten complete single-page paragraphs':'twelve complete progressive/FE single-page paragraphs'});compile(profile,str(PROFILE),'exec');compile(formatter,str(FORMATTER),'exec');PROFILE.write_text(profile,'utf-8');FORMATTER.write_text(formatter,'utf-8');ROOT.mkdir(parents=True);save(ROOT/'prepared_policy.json',dict(contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),formatter=str(FORMATTER),formatter_sha256=sha(FORMATTER.read_bytes()),twelve_positive_QA_and_meaningful_native_source_macro_FE_control_negatives_pending=True,five_individual_rowcount_reasons_three_ordinary_boundaries_bound=True,all12_native_actual_pages47_body35_name12_FE_holds_bound=True,no_shared_formatter_runtime_font_viewport_guard_or_registry_mutation=True,new_review_credit=0,full_goal_complete=False));print('B211 exact contract/profile/compiler frozen:12 single pages,nine progressive/three FE,oneFI,five rowcount reasons andthree ordinary boundaries. Positive/negative QA next.')
