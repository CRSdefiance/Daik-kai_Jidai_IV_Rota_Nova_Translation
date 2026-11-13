"""Prepare B200-only native display planning without changing prose or earlier profiles."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B200_layout_tools_v5843')
PROFILE=Path('dk4tool/dialogue/lil_B200_profile.py')
if __name__=='__main__':
    assert not ROOT.exists() and not PROFILE.exists()
    doc=read('translations/lil_B200_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    keys=['source_context','actor_voice_contract','control_contract','branch_proof','source_entry_proof',
        'source_effect_and_predicate_contract','source_nameplate_consumer_proof','source_name_literal_scope_proof',
        'actor_terminology_reconciliation','actual_original_response_paths']
    deps={doc[k]:doc[k+'_sha256'] for k in keys}
    code='''"""Exact B20017 progressive speeches and two distinct original null-actor FE objects."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA=ARM_LITERAL
BLOCKS=BLOCK_LITERAL
SELECTORS=frozenset({19,172})
DEPENDENCIES=DEPS_LITERAL
CONTROL=CONTROL_LITERAL
TERMS=TERMS_LITERAL

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B200 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B200 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=38 or sum(r['source_selector']==254 for r in cases)!=4:raise ValueError('All19 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B200 has no original runtime name macro')
    terms=json.loads(Path(TERMS).read_bytes())
    if not terms['explicit_not_a_doctor_denial_preserved']:raise ValueError('Complete rescue and profession-denial context required')
    if terms['source_FE_impact_index']!=5 or terms['source_FE_stat_notice_index']!=72:raise ValueError('Distinct collapse sound and stat FE objects required')
    if terms['source_actual_speeches']!=19 or terms['offline_only_speeches']:raise ValueError('Complete19-source-panel fixture evidence required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B200-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';17 original54020 speeches,Carlo19 voice7/anonymous172 voice0,four name consumers.31 source commands/no choices,relatives,predicates or macros.One original end with two tailzeros.V5816 unchanged font,width,guard and pair phase.Stranger label is a separate unimplemented target.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B200-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';two original24310 null-actor then5473C objects:collapse sound and Carlo Charm+1 notice.No FE macros.228x48logical/228x64physical,conservative216px planning.All19 source panels observed;English scene and complete effect-body semantics unapproved.')
    raise ValueError('Unknown B200 consumer')
'''
    changes={'ARM_LITERAL':repr(packet['current_ARM9_sha256']),
        'BLOCK_LITERAL':repr({packet['blocks'][0][k] for k in ['clean_block_sha256','current_block_sha256']}),
        'DEPS_LITERAL':repr(deps),'CONTROL_LITERAL':repr(doc['control_contract']),'TERMS_LITERAL':repr(doc['actor_terminology_reconciliation'])}
    for a,b in changes.items():assert a in code;code=code.replace(a,b)
    compile(code,str(PROFILE),'exec');PROFILE.write_text(code,encoding='utf-8',newline='\n')
    rows=[derive('dk4tool/dialogue/lil_B199_layout_v3.py','dk4tool/dialogue/lil_B200_layout_v1.py',{
        'B199':'B200','frozenset({2,9,22})':'frozenset({19,172})',
        'The exact B199 successor recognizes complete locative over there as a valid boundary. There remains weak elsewhere. No global helper orprevious profile is modified.':
        'This exact B200 successor uses no source-specific locative or Samwell idiom exception. No global helper or previous profile is modified.',
        '# Complete source70 predicate: the contraction is Samwell is, and quick on his feet is one idiom.\nPROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({("samwell\'s",\'quick\'),(\'quick\',\'on\'),(\'on\',\'his\'),(\'his\',\'feet\')})':
        '# No B199-only Samwell idiom rule is inherited into this source exchange.',
        "    # In this exchange over there completes the preceding noun phrase.\n    # It is not the existential there of a stranded there is.\n    return index>=1 and tuple(_word(v) for v in labels[index-1:index+1])==('over','there')":
        '    # This source-bound batch needs no locative boundary exception.\n    return False'})]
    plan=Path('scripts/plan_lil_B199_layout_v5791.py').read_text(encoding='utf-8')
    rows.append(derive('scripts/plan_lil_B199_layout_v5791.py','scripts/plan_lil_B200_layout_v5844.py',{
        'B199':'B200','layout_v5791':'layout_v5844','lil_B199_layout_v3':'lil_B200_layout_v1',
        'all31':'all19','Plan31':'Plan19','len(reports)==31':'len(reports)==19','plans=31':'plans=19',
        'manuscript_v3.json':'manuscript_v1.json','manuscript_v4.json':'manuscript_v2.json',
        "doc=deepcopy(read(INPUT));image=":"doc=deepcopy(read(INPUT));doc['actor172_Stranger_draft_not_applied_no_new_name_localization_completion_credit']=doc.pop('actor172_Strander_draft_not_applied_no_new_name_localization_completion_credit');image="}))
    source=Path('scripts/verify_lil_B199_fonts_v5792.py').read_text(encoding='utf-8')
    a=source.index("    required=next(r for r in doc['records'] if r['source_record_index']==37)");b=source.index('    sheets=[]',a)
    rows.append(derive('scripts/verify_lil_B199_fonts_v5792.py','scripts/verify_lil_B200_fonts_v5845.py',{
        source[a:b]:'    assert len(negatives)==18\n',
        'B199':'B200','fonts_v5792':'fonts_v5845','voices_v5768':'voices_v5827','layout_v3':'layout_v1',
        'manuscript_v4.json':'manuscript_v2.json','blocks[199]':'blocks[200]','blocks[198]':'blocks[199]',
        'len(qa_reports)==31 and macro_calls==248':'len(qa_reports)==19 and macro_calls==152',
        'for selector in [2,9,22,254]:':'for selector in [19,172,254]:',
        "format(2 if selector==9 else 9,":"format(19 if selector==172 else 172,",
        "r['source_selector']==22":"r['source_selector']==19",
        'all31':'all19','and248':'and152','current_original_macro_alignment_calls=248':'current_original_macro_alignment_calls=152',
        'progressive_alignment_calls=240':'progressive_alignment_calls=136','FE_null_actor_alignment_calls=8':'FE_null_actor_alignment_calls=16',
        'complete_progressive_planes=30':'complete_progressive_planes=17','complete_FE_logical_and_physical_planes=1':'complete_FE_logical_and_physical_planes=2',
        'native_source_FI1_FA0_FO0_and_all_four_selectors_preserved':'native_source_FI0_FA0_FO0_and_all_three_selectors_preserved',
        'All31 current-font native planes,248 alignment cases and22 source-consumer negatives pass;four sheets need visual review.':
        'All19 current-font native planes,152 alignment cases and18 source-consumer negatives pass;three sheets need visual review.',
        'and248 native alignment cases':'and152 native alignment cases'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_profile_planner_and_native_fonts.json',dict(profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),
        dependencies=deps,tools=rows,source_current_prose_no_macros_and19_source_actual_panels_bound=True,
        unchanged_current_metrics_width_guards_pair_phase_four_rows_and_runtime=True,
        no_new_prose_shortening_authored_break_or_weak_boundary_waiver=True,
        prior_v1_metadata_Strander_typo_corrected_only_in_successor=True,
        native_name_target_Stranger_not_implicitly_applied=True,new_ROMs=0,new_emulator_runs=0,new_editorial_credit=0,full_goal_complete=False))
    print('B200 scoped profile/planner/native tests prepared:19 planes,152 alignments,18 negatives. No shared metric,runtime or prose changes.')
