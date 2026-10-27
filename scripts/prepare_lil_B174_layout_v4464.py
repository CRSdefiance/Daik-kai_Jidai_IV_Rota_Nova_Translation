"""Scope B174 to unchanged native geometry and four exact static consumers."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B174_layout_tools_v4464')
if __name__=='__main__':
    assert not ROOT.exists()
    doc=read('translations/lil_B174_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','control_contract','actor_voice_contract','branch_proof',
        'source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']}
    hashes=sorted({g[k] for g in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    profile=Path('dk4tool/dialogue/lil_B174_profile.py');assert not profile.exists()
    text='''"""Exact B174 source/current progressive consumer and four static actors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='''+repr(packet['current_ARM9_sha256'])+'''
BLOCKS=frozenset('''+repr(hashes)+''')
SELECTORS=frozenset({2,14,26,201})
DEPENDENCIES='''+repr(deps)+'''

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B174 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    if consumer!='progressive':raise ValueError('B174 has no FE or typed/dynamic text consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B174-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
        metrics_source=base.metrics_source+';33 original54020 speeches,Lil2/Emilio14/Julian26/Mihwa201,no FI/FA/FO,45 structural commands,eight nonrelative leaves,one resource,two presentations,two A000s,one predicate,four relative sites,C200 andsingle end. Emilio food aside remains conditional. Packed FE0E operand is not a system panel. Six owned scratch-name paths andtwo Mihwa readonly paths preserved. No natural event eligibility claim.')
'''
    compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
    pairs=[('new','employer')]
    tools=[derive('dk4tool/dialogue/lil_B173_layout_v1.py','dk4tool/dialogue/lil_B174_layout_v1.py',{
        'lil-B173-progressive-runtime-bound-v1':'lil-B174-progressive-runtime-bound-v1',
        'frozenset({2,202})':'frozenset({2,14,26,201})','source-bound B173 profile':'source-bound B174 profile',
        '\ndef _word(value):':'\nPROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset('+repr(pairs)+')\n\ndef _word(value):',
    })]
    tools.append(derive('scripts/plan_lil_B173_layout_v4423.py','scripts/plan_lil_B174_layout_v4465.py',{
        'Plan11':'Plan33','lil_B173_layout_v1':'lil_B174_layout_v1','lil_B173_profile':'lil_B174_profile',
        'lil_B173_layout_v4423':'lil_B174_layout_v4465','lil_B173_editorial':'lil_B174_editorial',
        'all11_paragraph_layout':'all33_paragraph_layout','len(reports)==11':'len(reports)==33','plans=11':'plans=33',
    }))
    tools.append(derive('scripts/verify_lil_B173_fonts_v4424.py','scripts/verify_lil_B174_fonts_v4466.py',{
        'Current88 original processor/alignment calls,11 progressive planes and11 complete paragraph QA':'Current264 original processor/alignment calls,33 progressive planes and33 complete paragraph QA',
        'lil_B173_profile':'lil_B174_profile','lil_B173_layout_v1':'lil_B174_layout_v1',
        'lil_B173_fonts_v4424':'lil_B174_fonts_v4466','lil_B173_editorial':'lil_B174_editorial',
        'len(cases)==11 and len(qa_reports)==11 and macro_calls==88':'len(cases)==33 and len(qa_reports)==33 and macro_calls==264',
        'blocks[173]':'blocks[174]','blocks[172]':'blocks[173]','selectors=[2,202]':'selectors=[2,14,26,201]',
        'format(202 if selector==2 else 2':'format(14 if selector==2 else 2','all11':'all33',
        'len(negatives)==13':'len(negatives)==17','current_original_macro_alignment_calls=88':'current_original_macro_alignment_calls=264',
        'actual_selected_B173_IDs':'actual_selected_B174_IDs',
        '11 complete progressive planes,88 original processor/alignment cases,11 QA plans and13 source-consumer negatives pass;two sheets need visual review.':
            '33 complete progressive planes,264 original processor/alignment cases,33 QA plans and17 source-consumer negatives pass;five sheets need visual review.',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),dependencies=deps,tools=tools,
        additional_protected_pairs=pairs,source_actors=[2,14,26,201],source_macros=0,
        native_geometry=dict(width=216,height=64,cell_width=6,row_pitch=16,rows=4),
        no_shared_profile_metrics_or_guard_change=True,native_and_actual_approval_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Exact B174 profile,logical planner and264 original alignment-case producer prepared; source macros0; no credit.')
