"""Freeze a B196-scoped profile and unchanged native-metric prose planner."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B196_layout_tools_v5606')
SOURCE='work/analysis/lil_B196_source_v5590/all36_clean_current_complete_context_with_twelve_choice_labels.json'
PROFILE=Path('dk4tool/dialogue/lil_B196_profile.py')
if __name__=='__main__':
    assert not ROOT.exists() and not PROFILE.exists();packet=read(SOURCE)
    doc=read('translations/lil_B196_editorial_manuscript_v1.json')
    dependencies={p:sha(Path(p).read_bytes()) for p in [SOURCE,*[doc[k] for k in ['actor_voice_contract','control_contract','branch_proof',
        'source_entry_proof','source_effect_and_predicate_contract','source6003_and_end_contract','source_nameplate_consumer_proof',
        'source_name_literal_scope_proof','source_financial_context','actor_terminology_reconciliation']]]}
    arm=packet['current_ARM9_sha256'];blocks={packet['blocks'][0]['clean_block_sha256'],packet['blocks'][0]['current_block_sha256']}
    code='''"""Exact B196 runtime,source commands,actors and default-FI contracts."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA=ARM_LITERAL
BLOCKS=BLOCK_LITERAL
SELECTORS=frozenset({2,6,19,20,25,173,254})
DEPENDENCIES=DEPS_LITERAL
CONTROL=CONTROL_LITERAL
TERMS=TERMS_LITERAL
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B196 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B196 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=48 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All24 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':1,'FA':0,'FO':0}:raise ValueError('B196 has exactly one source FI')
    terms=json.loads(Path(TERMS).read_bytes())
    if terms['current_source_FI_expansion']!='Lil' or terms['current_default_captain_ID']!=2:raise ValueError('Exact current default FI name/parity required')
    token=terms['native_FE_macro_pipelines'][1]
    if len(token['cases'])!=4 or any(bytes.fromhex(r['output_hex'])!=b'Lil' for r in token['cases']):raise ValueError('Original FI expansion differs')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B196-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';23 original54020 speeches,six original actor/voice bindings,twelve name consumers. Source119 commands/six menus/52 relative sites/seven predicates/seven ends. No font,width,guard,phase or custom-name claim. Current V5580 font and native guards.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B196-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310 null actor then5473C branch-specific FI Charm-plus-one notice. FI expands to current default Lil in four source alignments.228x48logical/228x64physical,conservative216px planning. No item-effect,custom-player-name or actual scene claim.')
    raise ValueError('Unknown B196 consumer')
'''
    replacements={'ARM_LITERAL':repr(arm),'BLOCK_LITERAL':repr(blocks),'DEPS_LITERAL':repr(dependencies),
        'CONTROL_LITERAL':repr(doc['control_contract']),'TERMS_LITERAL':repr(doc['actor_terminology_reconciliation'])}
    for a,b in replacements.items():assert a in code;code=code.replace(a,b)
    compile(code,str(PROFILE),'exec');PROFILE.write_text(code,encoding='utf-8',newline='\n')
    rows=[derive('dk4tool/dialogue/lil_B195_layout_v1.py','dk4tool/dialogue/lil_B196_layout_v1.py',{'B195':'B196'})]
    rows.append(derive('scripts/plan_lil_B194_layout_v5501.py','scripts/plan_lil_B196_layout_v5607.py',{
        'B194':'B196','Plan11':'Plan24','layout_v5501':'layout_v5607','all11':'all24','len(reports)==11':'len(reports)==24','plans=11':'plans=24'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_source_locked_profile_and_planner.json',dict(tools=rows,profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),
        dependencies=dependencies,unchanged_native_metrics_width_guards_phase_four_row_limit_and_default_FI_width=True,
        no_record_specific_exception_or_prose_shortening_added=True,six_choice_menus_need_separate_native_proof=True,
        new_ROMs=0,new_emulator_runs=0,new_editorial_credit=0,full_goal_complete=False))
