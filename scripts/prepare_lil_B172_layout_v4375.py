"""Bind B172 actors and exact runtime to unchanged native progressive display rules."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B172_layout_tools_v4375')
if __name__=='__main__':
    assert not ROOT.exists()
    doc=read('translations/lil_B172_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof',
        'source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']}
    hashes=sorted({g[k] for g in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    profile=Path('dk4tool/dialogue/lil_B172_profile.py');assert not profile.exists()
    text='''"""Exact B172 source/current progressive consumer and three static actors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='''+repr(packet['current_ARM9_sha256'])+'''
BLOCKS=frozenset('''+repr(hashes)+''')
SELECTORS=frozenset({2,26,201})
DEPENDENCIES='''+repr(deps)+'''

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B172 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    if consumer!='progressive':raise ValueError('B172 has no FE or typed/dynamic text consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B172-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';27 original54020 speeches,Lil2/Julian26/Mihwa201,no FI/FA/FO,38 commands,11 leaves,three resources,five presentations,C200 then later A000 and one tail end. Source1A/C9 are actor26/201,not literal prose. Mihwa original name pointer is readonly;Lil/Julian owned scratch paths are preserved. No natural event eligibility claim.')
'''
    compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
    pairs=[('ahead','of'),('of','yourself'),('think','about'),('go','on'),('a','date'),('date','with'),
        ('as','soon'),('soon','as'),('counting','on'),('day','and'),('and','night'),('get','there'),('ask','around')]
    tools=[derive('dk4tool/dialogue/lil_B171_layout_v1.py','dk4tool/dialogue/lil_B172_layout_v1.py',{
        'lil-B171-progressive-runtime-bound-v1':'lil-B172-progressive-runtime-bound-v1',
        'frozenset({2,25,81})':'frozenset({2,26,201})','source-bound B171 profile':'source-bound B172 profile',
        '\ndef _word(value):':'\nPROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset('+repr(pairs)+')\n\ndef _word(value):',
    })]
    tools.append(derive('scripts/plan_lil_B171_layout_v4326.py','scripts/plan_lil_B172_layout_v4376.py',{
        'Plan37':'Plan27','lil_B171_layout_v1':'lil_B172_layout_v1','lil_B171_profile':'lil_B172_profile',
        'lil_B171_layout_v4326':'lil_B172_layout_v4376',
        'lil_B171_editorial_manuscript_v2':'lil_B172_editorial_manuscript_v1',
        'lil_B171_editorial_manuscript_v3':'lil_B172_editorial_manuscript_v2',
        'all37_paragraph_layout':'all27_paragraph_layout','len(reports)==37':'len(reports)==27','plans=37':'plans=27',
    }))
    tools.append(derive('scripts/verify_lil_B171_fonts_v4327.py','scripts/verify_lil_B172_fonts_v4377.py',{
        'Current296 macro calls,37 progressive planes and37 complete paragraph QA.':'Current216 original processor/alignment calls,27 progressive planes and27 complete paragraph QA;zero source macros.',
        'lil_B171_profile':'lil_B172_profile','lil_B171_layout_v1':'lil_B172_layout_v1',
        'lil_B171_fonts_v4327':'lil_B172_fonts_v4377','lil_B171_editorial_manuscript_v3':'lil_B172_editorial_manuscript_v2',
        'len(cases)==37 and len(qa_reports)==37 and macro_calls==296':'len(cases)==27 and len(qa_reports)==27 and macro_calls==216',
        'blocks[171]':'blocks[172]','blocks[170]':'blocks[171]','selectors=[2,25,81]':'selectors=[2,26,201]',
        'format(25 if selector==2 else 2':'format(26 if selector==2 else 2','all37':'all27',
        'current_original_macro_alignment_calls=296':'current_original_macro_alignment_calls=216','actual_selected_B171_IDs':'actual_selected_B172_IDs',
        '37 complete progressive planes,296 macro cases,37 QA plans and15 source-consumer negatives pass;five sheets need visual review.':'27 complete progressive planes,216 original processor/alignment cases,27 QA plans and15 source-consumer negatives pass;four sheets need visual review. Source macros0.',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),dependencies=deps,tools=tools,
        additional_protected_pairs=pairs,source_actors=[2,26,201],source_macros=0,Mihwa_readonly_name_path_distinguished=True,
        no_shared_profile_metrics_or_guard_change=True,wrong_legal_actor_negative_uses_in_profile_selector26_for_Lil=True,
        native_and_actual_approval_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Exact B172 profile,logical planner and216 original alignment-case producer prepared;source macros0;no credit.')
