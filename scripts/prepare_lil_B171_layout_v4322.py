"""Bind B171's three static actors to the validated native progressive geometry."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B171_layout_tools_v4322')

if __name__ == '__main__':
    assert not ROOT.exists()
    doc = read('translations/lil_B171_editorial_manuscript_v1.json')
    packet = read(doc['source_context'])
    deps = {doc[k]: doc[k + '_sha256'] for k in ['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof',
        'source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']}
    hashes = sorted({g[k] for g in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    profile = Path('dk4tool/dialogue/lil_B171_profile.py')
    assert not profile.exists()
    text = '''"""Exact B171 source/current progressive consumer and three static actors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA=''' + repr(packet['current_ARM9_sha256']) + '''
BLOCKS=frozenset(''' + repr(hashes) + ''')
SELECTORS=frozenset({2,25,81})
DEPENDENCIES=''' + repr(deps) + '''

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B171 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    if consumer!='progressive':raise ValueError('B171 has no FE or typed/dynamic text consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B171-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';37 original54020 speeches,Lil2/Yifa25/Sanghyeon81,FI1,45 commands,eight leaves,four presentations,one resource,C200 andtwo endwords bound. Source51 is actor81,not literal Q. No natural event eligibility claim.')
'''
    compile(text, str(profile), 'exec')
    profile.write_text(text, encoding='utf-8', newline='\n')
    pairs = [('fellow','disciple'),('share','a'),('a','teacher'),('her','senior'),('poor','guidance'),('sudden','intrusion'),
        ('mean','no'),('no','harm'),('brief','greeting'),('unruly','ways'),('teacher\'s','permission'),('teacher\'s','instructions'),
        ('grave','offense'),('our','school'),('right','path'),('if','possible'),('keep','training'),('strangely','real'),
        ('come','down'),('the','mountain'),('taoist','arts'),('to','visit'),('come','visit'),('so','immature'),
        ('stop','worrying'),('behave','badly'),('before','you'),('you','did'),('set','sail'),('hee','hee'),('let','sanghyeon'),
        ('sanghyeon','down'),('work','on'),('comes','first'),('comes','second'),('no','way'),('go','abroad'),('went','abroad')]
    tools = [derive('dk4tool/dialogue/lil_B170_layout_v2.py', 'dk4tool/dialogue/lil_B171_layout_v1.py', {
        'lil-B170-progressive-runtime-bound-v1': 'lil-B171-progressive-runtime-bound-v1',
        'frozenset({2,25})': 'frozenset({2,25,81})', 'source-bound B170 profile': 'source-bound B171 profile',
        '\ndef _word(value):': '\nPROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset(' + repr(pairs) + ')\n\ndef _word(value):',
    })]
    tools.append(derive('scripts/plan_lil_B170_layout_v4273.py', 'scripts/plan_lil_B171_layout_v4323.py', {
        'Plan33': 'Plan37', 'lil_B170_layout_v1': 'lil_B171_layout_v1', 'lil_B170_profile': 'lil_B171_profile',
        'lil_B170_layout_v4273': 'lil_B171_layout_v4323', 'lil_B170_editorial': 'lil_B171_editorial',
        'all33_paragraph_layout': 'all37_paragraph_layout', 'len(reports)==33': 'len(reports)==37', 'plans=33': 'plans=37',
    }))
    tools.append(derive('scripts/verify_lil_B170_fonts_v4274.py', 'scripts/verify_lil_B171_fonts_v4324.py', {
        'Current264 macro calls,33 progressive planes and33 complete paragraph QA.': 'Current296 macro calls,37 progressive planes and37 complete paragraph QA.',
        'lil_B170_profile': 'lil_B171_profile', 'lil_B170_layout_v1': 'lil_B171_layout_v1',
        'lil_B170_fonts_v4274': 'lil_B171_fonts_v4324', 'lil_B170_editorial': 'lil_B171_editorial',
        'len(cases)==33 and len(qa_reports)==33 and macro_calls==264': 'len(cases)==37 and len(qa_reports)==37 and macro_calls==296',
        'blocks[170]': 'blocks[171]', 'blocks[169]': 'blocks[170]',
        'selectors=[2,25]': 'selectors=[2,25,81]', 'len(negatives)==13': 'len(negatives)==15',
        'format(9 if selector==2 else 2': 'format(25 if selector==2 else 2',
        'all33': 'all37', 'current_original_macro_alignment_calls=264': 'current_original_macro_alignment_calls=296',
        'actual_selected_B170_IDs': 'actual_selected_B171_IDs',
        '33 complete progressive planes,264 macro cases,33 QA plans and13 source-consumer negatives pass': '37 complete progressive planes,296 macro cases,37 QA plans and15 source-consumer negatives pass',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(profile=str(profile), profile_sha256=sha(profile.read_bytes()), dependencies=deps, tools=tools,
        additional_protected_pairs=pairs, source_actor51_hex_is_Sanghyeon81=True, no_shared_profile_metrics_or_guard_change=True,
        wrong_legal_actor_negative_uses_in_profile_selector25_for_Lil=True,
        native_and_actual_approval_pending=True, producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print('Exact B171 profile,logical planner and296-case native proof prepared;no credit.')
