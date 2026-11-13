"""Freeze the reviewed20-record native contract without changing shared formatters or runtime code."""
import json
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B209_policy_tools_v6478')
DOC=Path('translations/lil_B209_editorial_manuscript_v1.json')
SOURCE=Path('work/analysis/lil_B209_source_v6450d/all20_clean_current_letter_and_voice_alternative_context.json')
PLAN=Path('work/analysis/lil_B209_layout_research_v6462e/all20_research_plans_no_word_changes_or_approval.json')
CONTRACT=Path('translations/lil_B209_native_contract_v1.json')
PROFILE=Path('dk4tool/dialogue/lil_B209_profile_v1.py')
FORMATTER=Path('dk4tool/dialogue/lil_B209_layout_v1.py')
ROW_REASONS={
'DK4_MES_B209_R0027':'The complete182-character heard-rumor paragraph preserves the legendary/cursed Muramasa blades,their craftsmanship,reported bane of Tokugawa as ruler of Japan and agentless eradication effort. It uses six ordinary English rows across two original four-row native pages. The core reported-bane assertion ends at Tokugawa on page1;the entire ruler of Japan appositive and following clause remain on page2. Actual normal A continuation,complete glyphs/names and return are verified. Four Japanese rows need not force shortening,clipping or an invented opcode. Only this exact source/prose row-count difference is approved.',
'DK4_MES_B209_R0030':'The full135-character paragraph preserves apparent concealment,an unnamed grudge-bearing clan,one blade,East Asia and provisional communication. Its first complete report uses four native rows;the For now news-passing sentence takes two rows on the original continuation page. All words remain. Actual original A continuation and all glyphs are complete,without a blank page or added source command. Only this exact source/prose row-count difference is approved.',
'DK4_MES_B209_R0033':'The Japanese four rows include a blank row and indented signature. English retains the complete personal long-search statement and full Yukihisa Genjo Shiraki signature as a separate automatic footer row,using three native rows. Japanese alignment spaces and blank staging are not authored into English. Actual complete footer/name and one-page return pass. Only this exact source/prose row-count difference is approved.',
'DK4_VOICE_B209_C8_T20':'The already-good concise arrival announcement fits one complete native English row;the Japanese two-row physical wrap is not a dramatic pause. Every word remains and original D0/style0 body ownership is preserved. No artificial early break or extra page. Only this exact source/prose row-count difference is approved.',
'DK4_VOICE_B209_C8_T264':'The already-good excited announcement fits one complete native English row while preserving both exclamations and sender. Japanese two-row physical wrapping does not require English staging. Original D0/style6 ownership and all words remain. Only this exact source/prose row-count difference is approved.',
'DK4_VOICE_B209_C702_T246':'The already-good simple-voice reaction fits one complete native English row and retains inability to understand this letter without adding the other styles callback. Japanese two-row physical wrapping supplies no dramatic pause. Original unique style6 body and complete glyphs remain. Only this exact source/prose row-count difference is approved.'}
PROFILE_CODE='''"""Exact B209 source/name/control/native-page contract; no global formatter or runtime changes."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path('translations/lil_B209_native_contract_v1.json')
CONTRACT_SHA='@HASH@'
ARM9_SHA='4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351'
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError('B209 frozen native contract changed')
    d=json.loads(raw)
    for p,digest in d['dependencies'].items():
        if sha(Path(p).read_bytes())!=digest:raise ValueError('B209 native dependency changed:'+p)
    if len(d['record_bindings'])!=20 or d['physical_native_rows_per_page']!=4 or d['complete_native_pages']!=22:raise ValueError('Complete B20920-object/two native continuation contract required')
    return d
def expected_profile(record_id):
    d=contract()
    if record_id not in d['record_bindings']:raise ValueError('Unreviewed B209 record')
    r=d['record_bindings'][record_id];base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B209-source-bound-v1:'+record_id,max_lines=r['maximum_total_rows'],leading_speaker_bytes=frozenset({r['source_selector']}),metrics_source=base.metrics_source+';exact B209 record '+record_id+'. Native viewport216x64,6px ASCII/16px pitch,original guards/pair phase. Only two exact letter paragraphs allow six reviewed rows across two original four-row pages;other18 objects remain one page. All source aliases,voices and full signatures bound;no runtime/font change.')
def profile_for(arm,source_block,record_id):
    d=contract()
    if sha(arm)!=ARM9_SHA or sha(source_block) not in d['source_block_hashes']:raise ValueError('Exact B209 clean/current source block and V6439 runtime required')
    return expected_profile(record_id)
'''
FORMATTER_CODE='''"""Source-locked whole-paragraph compiler for B209 and its two validated native continuations."""
from copy import deepcopy
from types import FunctionType
from dk4tool.dialogue import qa
from dk4tool.dialogue.encoder import RelocatableDialogueEncoding
from dk4tool.dialogue.layout import DialogueDiagnostic
from dk4tool.dialogue.lil_B209_profile_v1 import contract,expected_profile
from scripts.plan_lil_B209_research_v6462e import plan as frozen_plan
def binding(source_raw,target_markup,profile):
    prefix='lil-B209-source-bound-v1:'
    if not profile.name.startswith(prefix):raise ValueError('Exact per-record B209 profile required')
    ident=profile.name[len(prefix):];d=contract()
    if ident not in d['record_bindings'] or profile!=expected_profile(ident):raise ValueError('B209 font,viewport,page,selector,guard or substitution profile changed')
    r=d['record_bindings'][ident]
    if source_raw.hex()!=r['compiler_source_hex']:raise ValueError('B209 exact source/kind/virtual-selector contract required')
    if target_markup!=r['planning_record']['english'] or any(v in target_markup for v in ['{LB','{ALIGN','{PAD','\\n','\\r']):raise ValueError('B209 reviewed logical paragraph and complete selector required')
    return ident,r
def encode_relocatable_dialogue(source_raw,target_markup,profile):
    ident,r=binding(source_raw,target_markup,profile);p=frozen_plan(deepcopy(r['planning_record']))
    if p['encoded_hex']!=r['compiled_hex'] or p['lines']!=r['lines']:raise ValueError('Frozen B209 source/prose/native layout changed')
    return RelocatableDialogueEncoding(p['formatted_markup'],bytes.fromhex(p['encoded_hex']),tuple(DialogueDiagnostic(**d) for d in p['diagnostics']))
_audit=FunctionType(qa.audit_relocatable_dialogue_record.__code__,{**qa.audit_relocatable_dialogue_record.__globals__,'encode_relocatable_dialogue':encode_relocatable_dialogue},argdefs=qa.audit_relocatable_dialogue_record.__defaults__)
def audit_relocatable_dialogue_record(source_raw,target_markup,profile):
    ident,r=binding(source_raw,target_markup,profile);report=_audit(source_raw,target_markup,profile);removed=[]
    for issue in list(report['issues']):
        if issue['code']=='weak-line-ending' and issue['message'] in r['approved_base_weak_messages']:
            report['issues'].remove(issue);removed.append(issue)
    if len(removed)!=len(r['approved_base_weak_messages']):raise ValueError('Exact reviewed B209 ordinary boundary no longer present')
    report['reviewed_ordinary_boundaries']=r['ordinary_wrap_reasons'];report['native_rows_per_page']=4;report['native_page_count']=r['native_page_count'];report['row_count_reason']=r['row_count_reason']
    return report
'''
if __name__=='__main__':
    assert not ROOT.exists() and all(not p.exists() for p in [CONTRACT,PROFILE,FORMATTER]);doc,source,plan=map(read,[DOC,SOURCE,PLAN]);assert len(doc['records'])==20 and not plan['failures'] and plan['manuscript_sha256']==sha(DOC.read_bytes())
    actualview=Path('work/analysis/lil_B209_actual_view_v6477/eight_actual_pages25_complete_holds_names_returns_and_later_scope_viewed.json');v=read(actualview);assert not v['upper_scene_and_portrait_differences'] and v['all25_complete_body_and_style11_name_holds_match_independent_native_models']
    deps=[DOC,SOURCE,PLAN,actualview,Path('scripts/plan_lil_B209_research_v6462e.py'),Path('scripts/research_lil_B209_native_pages_v6461.py'),Path('scripts/current_build_native_context_v6261b.py'),Path('scripts/shady_man_font_oracles_v6263.py'),Path('dk4tool/dialogue/encoder.py'),Path('dk4tool/dialogue/layout.py'),Path('dk4tool/dialogue/qa.py'),Path('work/analysis/lil_B209_controls_v6460/two_predicates40_relative_cases10_staging_structural_cases_and10_complete_ends.json'),Path('work/analysis/lil_B209_research_fonts_v6463/all20_bodies22_complete_native_pages_and160_alignments_RESEARCH.json'),Path('work/analysis/lil_B209_name_planes_v6464/four_name_planes112_alignments_actual_headers_and_two_source_style4_masks.json'),Path('work/analysis/lil_B209_stored_v6467/all20_final_stored_targets80_alignment_cases_and22_complete_pages.json'),Path('work/analysis/lil_B209_reference_v6468/research_image_receipt.json'),Path('work/analysis/lil_B209_entry_v6471/source_EV2_B209_action_dependency_and_native_getter_binding.json'),Path('work/analysis/lil_B209_loader_v6472/whole_SC2_and_B209_initial_entry_proof.json'),Path('work/analysis/lil_B209_reference_census_v6473/all18_commands_four_relative_sites_and_shipped_entry_census.json'),Path('work/analysis/lil_B209_actual_v6474/six_English_objects_eight_native_pages24_commands_and_source_differences.json'),Path('work/analysis/lil_B209_later_v6475/all187_later_differences_original_final_getters_and_honest_scope.json'),Path('work/analysis/lil_B209_relocated_controls_v6476/all20_dispatches_two_whole_styles414_slots_predicate_staging_and_complete_ends.json')]
    plans={p['id']:p for p in plan['records']};bindings={}
    for row in doc['records']:
        ident=row['id'];p=plans[ident];kind=row['kind'];raw=bytes.fromhex(row['source_hex']);virtual=kind!='progressive';reasons=[];messages=[]
        if ident=='DK4_MES_B209_R0027':
            messages=["line 1 ends with weak wrap word 'the'"]
            reasons=[dict(line=1,after_word='the',before_word='legendary',reason='Ordinary complete-word article boundary keeps the whole legendary cursed Muramasa blades noun phrase on the next33-character row. Appending legendary to the first row would require36 pre-LF characters,which the unchanged guarded phase contract rejects. The existing native width stays216px. Exact source/prose only.'),dict(line=3,after_word='said',before_word='to',reason='Normal reporting verb followed by an intact to-infinitive complement;complete words and hearsay remain. Exact paragraph only,no global auxiliary exemption.'),dict(line=5,after_word='are',before_word='afoot',reason='Normal complete-word copula/complement wrap keeps the whole final eradication clause on two readable continuation rows. Exact paragraph only,no global auxiliary exemption.'),dict(line=4,after_word='Tokugawa,',before_word='ruler',reason='Original native continuation follows the complete reported-bane core assertion;the full ruler of Japan appositive remains together on page2. Actual ordinary A transition and complete glyphs are verified;no command or authored page marker is added.')]
        if ident=='DK4_VOICE_B209_C8_T188':
            messages=["line 1 ends with weak wrap word 'in'"];reasons=[dict(line=1,after_word='in',before_word='from',reason='In come in,the final in is a phrasal-verb particle completing the arrival clause;from Yukihisa is its sender adjunct. This keeps come in intact without narrowing the window. Only this exact source/style4 prose is approved,no global preposition waiver.')]
        for reason in reasons:reason.update(exact_source_hex=raw.hex(),exact_English=row['english'])
        bindings[ident]=dict(source_selector=row['source_selector'],source_kind=kind,compiler_source_hex=((bytes([208])+raw) if virtual else raw).hex(),virtual_selector_not_stored_in_4100_body=virtual,planning_record={k:row[k] for k in ['id','english','kind','source_hex','source_selector']},compiled_hex=p['encoded_hex'],lines=p['lines'],maximum_total_rows=8 if ident in ['DK4_MES_B209_R0027','DK4_MES_B209_R0030'] else 4,native_page_count=2 if ident in ['DK4_MES_B209_R0027','DK4_MES_B209_R0030'] else 1,row_count_reason=ROW_REASONS.get(ident),approved_base_weak_messages=messages,ordinary_wrap_reasons=reasons)
    data=dict(format='B209-current-native-source-contract-v1',source_block_hashes=[source['blocks'][0]['clean_block_sha256'],source['blocks'][0]['current_block_sha256']],physical_native_rows_per_page=4,physical_viewport=[216,64],complete_native_pages=22,record_bindings=bindings,dependencies={str(p):sha(p.read_bytes()) for p in deps},two_native_continuations_not_a_taller_viewport=True,all_actual_and_later_scope_limits_preserved=True,source_prose_or_completion_credit_added=0,full_goal_complete=False)
    save(CONTRACT,data);PROFILE.write_text(PROFILE_CODE.replace('@HASH@',sha(CONTRACT.read_bytes())),encoding='utf-8');FORMATTER.write_text(FORMATTER_CODE,encoding='utf-8')
    for p in [PROFILE,FORMATTER]:compile(p.read_text('utf-8'),str(p),'exec')
    ROOT.mkdir(parents=True);save(ROOT/'prepared_policy.json',dict(contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),formatter=str(FORMATTER),formatter_sha256=sha(FORMATTER.read_bytes()),twenty_positive_checks_and_source_metric_page_control_rejections_pending=True,no_shared_global_formatter_runtime_font_or_viewport_change=True,no_ROM_registry_ledger_orcredit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('B209 per-record native policy prepared:two exact native continuations,18 single-page objects,source-bound normal boundaries/six rowcount reasons. Validation pending.')
