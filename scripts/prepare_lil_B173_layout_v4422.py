"""Bind B173 to validated original progressive geometry without changing shared rules."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B173_layout_tools_v4422')
if __name__=='__main__':
    assert not ROOT.exists()
    doc=read('translations/lil_B173_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','control_contract','actor_voice_contract','branch_proof',
        'source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']}
    hashes=sorted({g[k] for g in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    profile=Path('dk4tool/dialogue/lil_B173_profile.py');assert not profile.exists()
    text='''"""Exact B173 source/current progressive consumer and two static actors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='''+repr(packet['current_ARM9_sha256'])+'''
BLOCKS=frozenset('''+repr(hashes)+''')
SELECTORS=frozenset({2,202})
DEPENDENCIES='''+repr(deps)+'''

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B173 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    if consumer!='progressive':raise ValueError('B173 has no FE or typed/dynamic text consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B173-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
        metrics_source=base.metrics_source+';11 original54020 speeches,Lil2/Reika202,no FI/FA/FO,23 structural commands,eight nonrelative leaves,two resources,two presentations,two A000s,one predicate,four relative sites andsingle tail end. All speech precedes the conditional suffix. CA is actor202,not literal prose. Reika original name pointer is readonly;Lil owned scratch paths remain intact. No natural event eligibility claim.')
'''
    compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
    pairs=[('tomb','of'),('of','king'),('king','muryeong'),('smooth','talker'),('historic','site')]
    tools=[derive('dk4tool/dialogue/lil_B172_layout_v1.py','dk4tool/dialogue/lil_B173_layout_v1.py',{
        'lil-B172-progressive-runtime-bound-v1':'lil-B173-progressive-runtime-bound-v1',
        'frozenset({2,26,201})':'frozenset({2,202})','source-bound B172 profile':'source-bound B173 profile',
        '\ndef _word(value):':'\nPROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset('+repr(pairs)+')\n\ndef _word(value):',
    })]
    tools.append(derive('scripts/plan_lil_B172_layout_v4376.py','scripts/plan_lil_B173_layout_v4423.py',{
        'Plan27':'Plan11','lil_B172_layout_v1':'lil_B173_layout_v1','lil_B172_profile':'lil_B173_profile',
        'lil_B172_layout_v4376':'lil_B173_layout_v4423','lil_B172_editorial':'lil_B173_editorial',
        'all27_paragraph_layout':'all11_paragraph_layout','len(reports)==27':'len(reports)==11','plans=27':'plans=11',
    }))
    tools.append(derive('scripts/verify_lil_B172_fonts_v4377.py','scripts/verify_lil_B173_fonts_v4424.py',{
        'Current216 original processor/alignment calls,27 progressive planes and27 complete paragraph QA;zero source macros.':'Current88 original processor/alignment calls,11 progressive planes and11 complete paragraph QA;zero source macros.',
        'lil_B172_profile':'lil_B173_profile','lil_B172_layout_v1':'lil_B173_layout_v1',
        'lil_B172_fonts_v4377':'lil_B173_fonts_v4424','lil_B172_editorial':'lil_B173_editorial',
        'len(cases)==27 and len(qa_reports)==27 and macro_calls==216':'len(cases)==11 and len(qa_reports)==11 and macro_calls==88',
        'blocks[172]':'blocks[173]','blocks[171]':'blocks[172]','selectors=[2,26,201]':'selectors=[2,202]',
        'format(26 if selector==2 else 2':'format(202 if selector==2 else 2','all27':'all11',
        'len(negatives)==15':'len(negatives)==13','current_original_macro_alignment_calls=216':'current_original_macro_alignment_calls=88',
        'actual_selected_B172_IDs':'actual_selected_B173_IDs',
        '27 complete progressive planes,216 original processor/alignment cases,27 QA plans and15 source-consumer negatives pass;four sheets need visual review.':'11 complete progressive planes,88 original processor/alignment cases,11 QA plans and13 source-consumer negatives pass;two sheets need visual review.',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),dependencies=deps,tools=tools,
        additional_protected_pairs=pairs,source_actors=[2,202],source_macros=0,Reika_readonly_path_distinguished=True,
        native_geometry=dict(width=216,height=64,cell_width=6,row_pitch=16,rows=4),
        no_shared_profile_metrics_or_guard_change=True,wrong_legal_actor_negative_uses_in_profile_selector202_for_Lil=True,
        native_and_actual_approval_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Exact B173 profile,logical planner and88 original alignment-case producer prepared;source macros0;no credit.')
