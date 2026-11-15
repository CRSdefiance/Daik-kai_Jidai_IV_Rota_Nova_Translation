"""Prepare exact B199 profiles and native display tests without changing shared metrics."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B199_layout_tools_v5787')
PROFILE=Path('dk4tool/dialogue/lil_B199_profile.py')
if __name__=='__main__':
    assert not ROOT.exists() and not PROFILE.exists()
    doc=read('translations/lil_B199_editorial_manuscript_v2.json');packet=read(doc['source_context'])
    keys=['source_context','actor_voice_contract','control_contract','branch_proof','source_entry_proof',
        'source_effect_and_predicate_contract','source_nameplate_consumer_proof','source_name_literal_scope_proof',
        'actor_terminology_reconciliation','actual_original_response_paths']
    deps={doc[k]:doc[k+'_sha256'] for k in keys}
    code='''"""Exact B19930 progressive speeches and one four-impact null-actor FE object."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA=ARM_LITERAL
BLOCKS=BLOCK_LITERAL
SELECTORS=frozenset({2,9,22})
DEPENDENCIES=DEPS_LITERAL
CONTROL=CONTROL_LITERAL
TERMS=TERMS_LITERAL

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B199 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B199 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=62 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All31 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':1,'FA':0,'FO':0}:raise ValueError('Exactly one original FI macro required')
    terms=json.loads(Path(TERMS).read_bytes())
    if not terms['source_FE_four_impacts_not_stat_notice_or_named_speaker']:raise ValueError('Four-impact scene context required')
    if terms['source_actual_speeches']!=31 or terms['offline_only_speeches']:raise ValueError('Complete31-source-panel fixture evidence required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B199-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';30 original54020 speeches,Lil2 voice3/Camille9 voice2/Samwell22 voice2,six name consumers.47 source commands/no choices or relatives/one2000/one end with two tailzeros.One source FI.V5756 unchanged font,width,guard and pair phase.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B199-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310 null actor then5473C four-impact sound-effect panel,no FE macros.228x48logical/228x64physical,conservative216px planning.All31 Japanese source panels observed;English scene and complete effect-body semantics unapproved.')
    raise ValueError('Unknown B199 consumer')
'''
    changes={'ARM_LITERAL':repr(packet['current_ARM9_sha256']),
        'BLOCK_LITERAL':repr({packet['blocks'][0][k] for k in ['clean_block_sha256','current_block_sha256']}),
        'DEPS_LITERAL':repr(deps),'CONTROL_LITERAL':repr(doc['control_contract']),'TERMS_LITERAL':repr(doc['actor_terminology_reconciliation'])}
    for a,b in changes.items():assert a in code;code=code.replace(a,b)
    compile(code,str(PROFILE),'exec');PROFILE.write_text(code,encoding='utf-8',newline='\n')
    rows=[derive('dk4tool/dialogue/lil_B197_layout_v1.py','dk4tool/dialogue/lil_B199_layout_v1.py',{
        'B197':'B199','frozenset({21,169})':'frozenset({2,9,22})'})]
    rows.append(derive('scripts/plan_lil_B197_layout_v5667.py','scripts/plan_lil_B199_layout_v5788.py',{
        'B197':'B199','layout_v5667':'layout_v5788','all21':'all31','Plan21':'Plan31',
        'len(reports)==21':'len(reports)==31','plans=21':'plans=31',
        'manuscript_v1.json':'manuscript_v2.json','manuscript_v2.json':'manuscript_v3.json'}))
    rows.append(derive('scripts/verify_lil_B197_fonts_v5668.py','scripts/verify_lil_B199_fonts_v5789.py',{
        'B197':'B199','fonts_v5668':'fonts_v5789','voices_v5648':'voices_v5768',
        'manuscript_v2.json':'manuscript_v3.json','blocks[197]':'blocks[199]','blocks[196]':'blocks[198]',
        'len(qa_reports)==21 and macro_calls==168':'len(qa_reports)==31 and macro_calls==248',
        'for selector in [21,169,254]:':'for selector in [2,9,22,254]:',
        'format(21 if selector==169 else 169,':'format(2 if selector==9 else 9,',
        "r['source_selector']==169":"r['source_selector']==22",
        '    assert len(negatives)==18':
        """    required=next(r for r in doc['records'] if r['source_record_index']==37)
    raw_required=bytes.fromhex(required['source_hex'])
    reject('missing-required-FI',lambda:encode_relocatable_dialogue(raw_required,required['english'].replace('{MACRO:FI}','Lil'),prog))
    reject('duplicated-required-FI',lambda:encode_relocatable_dialogue(raw_required,required['english']+' {MACRO:FI}',prog))
    assert len(negatives)==22""",
        'all21':'all31','and168':'and248','current_original_macro_alignment_calls=168':'current_original_macro_alignment_calls=248',
        'progressive_alignment_calls=160':'progressive_alignment_calls=240','complete_progressive_planes=20':'complete_progressive_planes=30',
        'native_source_FI0_FA0_FO0_and_all_three_selectors_preserved':'native_source_FI1_FA0_FO0_and_all_four_selectors_preserved',
        'All21 current-font native planes,168 alignment cases and18 source-consumer negatives pass;three sheets need visual review.':
        'All31 current-font native planes,248 alignment cases and22 source-consumer negatives pass;four sheets need visual review.',
        'and168 native alignment cases':'and248 native alignment cases'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'prepared_profile_planner_and_native_fonts.json',dict(profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),
        dependencies=deps,tools=rows,source_current_prose_macro_and_31_source_actual_panels_bound=True,
        unchanged_current_metrics_width_guards_pair_phase_four_rows_and_runtime=True,
        no_new_prose_shortening_authored_break_or_weak_boundary_waiver=True,
        all_English_targets_ASCII_after_original_FI_expansion_no_CP932_pause_transfer=True,
        new_ROMs=0,new_emulator_runs=0,new_editorial_credit=0,full_goal_complete=False))
    print('B199 scoped profile/planner/native tests prepared:31 planes,248 alignments,22 negatives. No shared metric or runtime changes.')
