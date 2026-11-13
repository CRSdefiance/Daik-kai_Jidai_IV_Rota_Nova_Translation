"""Freeze source-scoped B198 profiles and unchanged native metrics with CP932 pause checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B198_layout_tools_v5719')
PROFILE=Path('dk4tool/dialogue/lil_B198_profile.py')
if __name__=='__main__':
    assert not ROOT.exists() and not PROFILE.exists()
    doc=read('translations/lil_B198_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    keys=['source_context','actor_voice_contract','control_contract','branch_proof','source_entry_proof',
        'source_effect_and_predicate_contract','source_nameplate_consumer_proof','source_name_literal_scope_proof',
        'actor_terminology_reconciliation','actual_original_response_paths']
    deps={doc[k]:doc[k+'_sha256'] for k in keys}
    code='''"""Exact B198 eleven progressive speeches and six unattributed FE voice panels."""
import json
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA=ARM_LITERAL
BLOCKS=BLOCK_LITERAL
SELECTORS=frozenset({12,15})
DEPENDENCIES=DEPS_LITERAL
CONTROL=CONTROL_LITERAL
TERMS=TERMS_LITERAL

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B198 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B198 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=34 or sum(r['source_selector']==254 for r in cases)!=12:raise ValueError('All17 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B198 has no source name macros')
    terms=json.loads(Path(TERMS).read_bytes())
    if not terms['source_FE_is_unattributed_speaking_voice_not_impersonal_notice']:raise ValueError('Complete encounter context required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B198-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';11 original54020 speeches,Yukihisa12 voice1/Angelo15 voice4,four name consumers.37 source commands/eight relative sites/two predicates/one end. No source macros. V5692 unchanged font,width,guard and pair phase.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B198-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';six original24310 null actor then5473C unattributed voice panels,no FI.228x48logical/228x64physical,conservative216px planning.15 source speeches observed,two conditional Angelo lines offline only;no English scene or full effect-body claim.')
    raise ValueError('Unknown B198 consumer')
'''
    changes={'ARM_LITERAL':repr(packet['current_ARM9_sha256']),
        'BLOCK_LITERAL':repr({packet['blocks'][0][k] for k in ['clean_block_sha256','current_block_sha256']}),
        'DEPS_LITERAL':repr(deps),'CONTROL_LITERAL':repr(doc['control_contract']),'TERMS_LITERAL':repr(doc['actor_terminology_reconciliation'])}
    for a,b in changes.items():assert a in code;code=code.replace(a,b)
    compile(code,str(PROFILE),'exec');PROFILE.write_text(code,encoding='utf-8',newline='\n')
    rows=[derive('dk4tool/dialogue/lil_B197_layout_v1.py','dk4tool/dialogue/lil_B198_layout_v1.py',{
        'B197':'B198','frozenset({21,169})':'frozenset({12,15})'})]
    rows.append(derive('scripts/plan_lil_B197_layout_v5667.py','scripts/plan_lil_B198_layout_v5720.py',{
        'B197':'B198','layout_v5667':'layout_v5720','all21':'all17','Plan21':'Plan17',
        'len(reports)==21':'len(reports)==17','plans=21':'plans=17'}))
    rows.append(derive('scripts/verify_lil_B197_fonts_v5668.py','scripts/verify_lil_B198_fonts_v5721.py',{
        'B197':'B198','fonts_v5668':'fonts_v5721','voices_v5648':'voices_v5703',
        'blocks[197]':'blocks[198]','blocks[196]':'blocks[197]',
        "logical=logical.encode('ascii')":"logical=logical.encode('cp932')",
        "assert [e['code'] for e in visible]==[v for v in expected if v not in [32,10]]":
        "semantic=[('ascii',ord(c)) if len(c.encode('cp932'))==1 else ('cp932',int.from_bytes(c.encode('cp932'),'big')) for c in expected.decode('cp932') if c not in ' \\n']\n        assert [(e['kind'],e['code']) for e in visible]==semantic",
        "assert all(0<=e['x']<=maxx and 0<=e['y']<=maxy and e['y']%pitch==0 for e in visible)":
        "assert all(0<=e['x']<=maxx-(6 if e['kind']=='cp932' else 0) and 0<=e['y']<=maxy and e['y']%pitch==0 for e in visible)",
        'len(qa_reports)==21 and macro_calls==168':'len(qa_reports)==17 and macro_calls==136',
        "sum(c['kind']=='system-FE' for c in cases)==1":"sum(c['kind']=='system-FE' for c in cases)==6",
        'for selector in [21,169,254]:':'for selector in [12,15,254]:',
        "format(21 if selector==169 else 169,":"format(12 if selector==15 else 15,",
        "r['source_selector']==169":"r['source_selector']==15",
        'all21':'all17','and168':'and136','current_original_macro_alignment_calls=168':'current_original_macro_alignment_calls=136',
        'progressive_alignment_calls=160':'progressive_alignment_calls=88','FE_null_actor_alignment_calls=8':'FE_null_actor_alignment_calls=48',
        'complete_progressive_planes=20':'complete_progressive_planes=11','complete_FE_logical_and_physical_planes=1':'complete_FE_logical_and_physical_planes=6',
        'All21 current-font native planes,168 alignment cases':'All17 current-font native planes,136 alignment cases'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'prepared_profile_planner_and_native_fonts.json',dict(profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),
        dependencies=deps,tools=rows,unchanged_current_metrics_width_guards_pair_phase_four_rows_and_runtime=True,
        CP932_pause_glyphs_checked_by_kind_and_big_endian_code_with_original_independent_font_oracle=True,
        no_new_prose_shortening_authored_break_or_weak_boundary_waiver=True,
        new_ROMs=0,new_emulator_runs=0,new_editorial_credit=0,full_goal_complete=False))
    print('B198 source-scoped profile/planner/native adapters prepared:17planes,136alignments,18negatives. Original CP932 pauses retained;no runtime or global metrics change.')
