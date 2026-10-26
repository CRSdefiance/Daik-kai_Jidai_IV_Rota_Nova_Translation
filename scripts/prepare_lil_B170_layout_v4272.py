"""Bind B170's two original progressive actors to the validated native geometry."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B170_layout_tools_v4272')
if __name__=='__main__':
    assert not ROOT.exists()
    doc=read('translations/lil_B170_editorial_manuscript_v1.json')
    packet=read(doc['source_context'])
    deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof',
        'source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']}
    hashes=sorted({g[k] for g in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    profile=Path('dk4tool/dialogue/lil_B170_profile.py')
    assert not profile.exists()
    text='''"""Exact B170 source/current progressive consumer and two static actors."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA='''+repr(packet['current_ARM9_sha256'])+'''
BLOCKS=frozenset('''+repr(hashes)+''')
SELECTORS=frozenset({2,25})
DEPENDENCIES='''+repr(deps)+'''

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B170 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    if consumer!='progressive':raise ValueError('B170 has no FE or typed/dynamic text consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B170-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';33 original54020 speeches,Lil2/Yifa25,FI1/FO1,45 commands,one pause,C200,two resources andtwo endwords bound. Source19 is Yifa25,not removable text. No natural event eligibility claim.')
'''
    compile(text,str(profile),'exec')
    profile.write_text(text,encoding='utf-8',newline='\n')
    pairs=[('taoist','arts'),('my','teacher'),('your','teacher'),('keep','training'),('whole','lot'),('lot','stronger'),
        ('some','nerve'),('come','aboard'),('in','command'),('a','fleet'),('fleet','called'),('called',''),('what','you'),('you','can'),('can','do'),
        ('real','bind'),('all','about'),('about','it'),('after','all'),('in','a'),('a','hurry'),('already','said'),('said','i'),('i','was'),('was','sorry'),
        ('i','told'),('told','you'),('run','away'),('first','place'),('quit','training'),('prove','my'),('prove','your'),('teacher','wrong'),
        ('no','time'),('time','to'),('to','argue'),('tough','training'),('been','through'),('seem','pretty'),('pretty','determined'),('work','hard'),
        ('never','to'),('to','let'),('let','anyone'),('anyone','beat'),('beat','you')]
    tools=[derive('dk4tool/dialogue/lil_B169_layout_v2.py','dk4tool/dialogue/lil_B170_layout_v1.py',{
        'lil-B169-progressive-runtime-bound-v1':'lil-B170-progressive-runtime-bound-v1',
        'frozenset({2,6,9,20,21,76})':'frozenset({2,25})',
        'source-bound B169 profile':'source-bound B170 profile',
        '\ndef _word(value):':'\nPROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset('+repr(pairs)+')\n\ndef _word(value):',
    })]
    tools.append(derive('scripts/plan_lil_B169_layout_v4228.py','scripts/plan_lil_B170_layout_v4273.py',{
        'Plan36':'Plan33','lil_B169_layout_v2':'lil_B170_layout_v1','lil_B169_profile':'lil_B170_profile',
        'lil_B169_layout_v4228':'lil_B170_layout_v4273',
        'lil_B169_editorial_manuscript_v2':'lil_B170_editorial_manuscript_v1',
        'lil_B169_editorial_manuscript_v3':'lil_B170_editorial_manuscript_v2',
        'all36_paragraph_layout':'all33_paragraph_layout','len(reports)==36':'len(reports)==33','plans=36':'plans=33',
    }))
    tools.append(derive('scripts/verify_lil_B169_fonts_v4229.py','scripts/verify_lil_B170_fonts_v4274.py',{
        'Current288 macro calls,36 progressive planes and36 complete paragraph QA.':'Current264 macro calls,33 progressive planes and33 complete paragraph QA.',
        'lil_B169_profile':'lil_B170_profile','lil_B169_layout_v2':'lil_B170_layout_v1',
        'lil_B169_fonts_v4229':'lil_B170_fonts_v4274',
        'lil_B169_editorial_manuscript_v3':'lil_B170_editorial_manuscript_v2',
        'len(cases)==36 and len(qa_reports)==36 and macro_calls==288':'len(cases)==33 and len(qa_reports)==33 and macro_calls==264',
        'blocks[169]':'blocks[170]','blocks[168]':'blocks[169]',
        'selectors=[2,6,9,20,21,76]':'selectors=[2,25]','len(negatives)==21':'len(negatives)==13',
        'all36':'all33','current_original_macro_alignment_calls=288':'current_original_macro_alignment_calls=264',
        'actual_selected_B169_IDs':'actual_selected_B170_IDs',
        '36 complete progressive planes,288 macro cases,36 QA plans and21 source-consumer negatives pass':'33 complete progressive planes,264 macro cases,33 QA plans and13 source-consumer negatives pass',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),dependencies=deps,tools=tools,
        additional_protected_pairs=pairs,source_actor19_hex_is_Yifa25=True,no_shared_profile_metrics_or_guard_change=True,
        native_and_actual_approval_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Exact B170 profile,logical planner and264-case native proof prepared;no credit.')
