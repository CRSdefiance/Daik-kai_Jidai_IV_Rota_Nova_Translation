"""Freeze B197-only source contracts and unchanged native display adapters."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B197_layout_tools_v5666')
PROFILE=Path('dk4tool/dialogue/lil_B197_profile.py')
if __name__=='__main__':
    assert not ROOT.exists() and not PROFILE.exists()
    doc=read('translations/lil_B197_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    keys=['source_context','actor_voice_contract','control_contract','branch_proof','source_entry_proof',
        'source_effect_and_predicate_contract','source_nameplate_consumer_proof','source_name_literal_scope_proof',
        'source_financial_context','actor_terminology_reconciliation','actual_original_response_paths']
    deps={doc[k]:doc[k+'_sha256'] for k in keys}
    code='''"""Exact B19720 progressive speeches and one common-tail null-actor FE."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA=ARM_LITERAL
BLOCKS=BLOCK_LITERAL
SELECTORS=frozenset({21,169})
DEPENDENCIES=DEPS_LITERAL
CONTROL=CONTROL_LITERAL
TERMS=TERMS_LITERAL

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B197 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B197 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=42 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All21 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B197 has no source name macros')
    terms=json.loads(Path(TERMS).read_bytes())
    if not terms['source_FE_R109_common_tail_observed_after_all_three_choices']:raise ValueError('Common-tail notice context required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B197-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';20 original54020 speeches,Ian21 voice1 and woman169 voice0,four name consumers.39 source commands/one2200/six relative sites/one end. No source macros. V5637 unchanged font,width,guard and pair phase.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B197-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310 null actor then5473C common-tail Ian Charm-plus-one notice,no FI.228x48logical/228x64physical,conservative216px planning. Actual Japanese paths bound;no English scene or effect-body claim.')
    raise ValueError('Unknown B197 consumer')
'''
    replacements={'ARM_LITERAL':repr(packet['current_ARM9_sha256']),
        'BLOCK_LITERAL':repr({packet['blocks'][0][k] for k in ['clean_block_sha256','current_block_sha256']}),
        'DEPS_LITERAL':repr(deps),'CONTROL_LITERAL':repr(doc['control_contract']),'TERMS_LITERAL':repr(doc['actor_terminology_reconciliation'])}
    for a,b in replacements.items():assert a in code;code=code.replace(a,b)
    compile(code,str(PROFILE),'exec');PROFILE.write_text(code,encoding='utf-8',newline='\n')
    rows=[derive('dk4tool/dialogue/lil_B195_layout_v1.py','dk4tool/dialogue/lil_B197_layout_v1.py',{
        'B195':'B197','frozenset({92,103,119})':'frozenset({21,169})'})]
    rows.append(derive('scripts/plan_lil_B196_layout_v5607.py','scripts/plan_lil_B197_layout_v5667.py',{
        'B196':'B197','layout_v5607':'layout_v5667','all24':'all21','Plan24':'Plan21','len(reports)==24':'len(reports)==21','plans=24':'plans=21'}))
    source=Path('scripts/verify_lil_B196_fonts_v5609b.py').read_text(encoding='utf-8')
    obsolete=source[source.index("    active=next(r for r in doc['records'] if '{MACRO:FI}'"):source.index('    assert len(negatives)==30')]
    rows.append(derive('scripts/verify_lil_B196_fonts_v5609b.py','scripts/verify_lil_B197_fonts_v5668.py',{
        'B196':'B197','lil_B196_profile_v2':'lil_B197_profile','lil_B196_layout_v3':'lil_B197_layout_v1',
        'fonts_v5609b':'fonts_v5668','voices_v5591':'voices_v5648','blocks[196]':'blocks[197]','blocks[195]':'blocks[196]',
        'len(qa_reports)==24 and macro_calls==192':'len(qa_reports)==21 and macro_calls==168',
        'for selector in [2,6,19,20,25,173,254]:':'for selector in [21,169,254]:',
        'format(2 if selector==6 else 6,':'format(21 if selector==169 else 169,',
        "r['source_selector']==173":"r['source_selector']==169",obsolete:'',
        'len(negatives)==30':'len(negatives)==18',
        'all24':'all21','and192':'and168','current_original_macro_alignment_calls=192':'current_original_macro_alignment_calls=168',
        'progressive_alignment_calls=184':'progressive_alignment_calls=160','complete_progressive_planes=23':'complete_progressive_planes=20',
        'native_source_FI1_FA0_FO0_and_all_seven_selectors_preserved':'native_source_FI0_FA0_FO0_and_all_three_selectors_preserved',
        'All24 current-font native planes,192 alignment cases and30':'All21 current-font native planes,168 alignment cases and18',
        'and88 native alignment cases':'and168 native alignment cases'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_profile_planner_and_native_fonts.json',dict(profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),dependencies=deps,tools=rows,
        unchanged_current_native_metrics_width_guards_phase_and_four_row_limit=True,
        no_B196_R74_exception_transferred_no_prose_shortening_or_authored_breaks=True,
        inherited_locative_over_there_helper_unused_by_this_manuscript=True,
        three_choice_font_and_geometry_need_separate_proof=True,new_ROMs=0,new_emulator_runs=0,new_editorial_credit=0,full_goal_complete=False))
