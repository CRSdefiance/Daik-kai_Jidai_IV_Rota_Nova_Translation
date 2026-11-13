"""Scope the unchanged native metrics and automatic paragraph planner to B169."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/lil_B169_layout_tools_v4223')
if __name__ == '__main__':
    assert not ROOT.exists()
    doc = read('translations/lil_B169_editorial_manuscript_v1.json')
    packet = read(doc['source_context'])
    deps = {doc[key]:doc[key + '_sha256'] for key in ['source_context','control_contract','actor_voice_contract','branch_proof',
        'source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']}
    hashes = {block[key] for block in packet['blocks'] for key in ['clean_block_sha256','current_block_sha256']}
    profile = Path('dk4tool/dialogue/lil_B169_profile.py')
    assert not profile.exists()
    text = '''"""Exact B169 source consumers:36 progressive speeches,six static actors,FI5/FO2."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA=''' + repr(packet['current_ARM9_sha256']) + '''
BLOCKS=frozenset(''' + repr(sorted(hashes)) + ''')
SELECTORS=frozenset({2,6,9,20,21,76})
DEPENDENCIES=''' + repr(deps) + '''

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B169 clean/current source and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    if consumer!='progressive':raise ValueError('B169 has no FE or other speech consumer')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B169-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';36 original54020 speeches/six source static actors,FI5/FO2,twelve relative sites,three predicates,five opaque leaves and one tail end;15 is Ian21 and4C is Mikhail76. No natural eligibility claim.')
'''
    compile(text,str(profile),'exec')
    profile.write_text(text,encoding='utf-8',newline='\n')
    pairs = [('of','conquest'),('seven','sages'),('seven','treasures'),('their','locations'),('different','shapes'),
        ('that','sea'),('the','strongest'),('strongest','power'),('influential','people'),('evil','person'),('sealed','proofs'),
        ('nearby','ruins'),('mikhail','letzel'),('the','great'),('great','naturalist'),('train','of'),('of','thought'),
        ('go','about'),('collecting','these'),('those','proofs'),('different','regions')]
    tools = [derive('dk4tool/dialogue/lil_B168_layout_v3.py','dk4tool/dialogue/lil_B169_layout_v1.py',{
        "expected={'lil-B168-progressive-runtime-bound-v1':frozenset({2,6,9,20,76,87,165,166}),'lil-B168-FE-runtime-bound-v1':frozenset({254})}":
            "expected={'lil-B169-progressive-runtime-bound-v1':frozenset({2,6,9,20,21,76})}",
        'source-bound B168 profile':'source-bound B169 profile',
        'def _word(value):':'PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset(' + repr(pairs) + ')\n\ndef _word(value):',
    })]
    tools.append(derive('scripts/plan_lil_B168_layout_v4184.py','scripts/plan_lil_B169_layout_v4224.py',{
        'lil_B168_layout_v3':'lil_B169_layout_v1','lil_B168_profile':'lil_B169_profile',
        'lil_B168_layout_v4184':'lil_B169_layout_v4224','lil_B168_editorial_manuscript_v4':'lil_B169_editorial_manuscript_v1',
        'lil_B168_editorial_manuscript_v5':'lil_B169_editorial_manuscript_v2',
        'all54_paragraph':'all36_paragraph','len(reports)==54':'len(reports)==36','plans=54':'plans=36','Plan54':'Plan36',
    }))
    tools.append(derive('scripts/verify_lil_B167_fonts_v4132.py','scripts/verify_lil_B169_fonts_v4225.py',{
        'Current216 macro calls,27 progressive planes and27 complete paragraph QA.':'Current288 macro calls,36 progressive planes and36 complete paragraph QA.',
        'lil_B167_profile':'lil_B169_profile','lil_B167_layout_v1':'lil_B169_layout_v1',
        'lil_B167_fonts_v4132':'lil_B169_fonts_v4225','lil_B167_editorial_manuscript_v2':'lil_B169_editorial_manuscript_v2',
        'len(cases)==27 and len(qa_reports)==27 and macro_calls==216':'len(cases)==36 and len(qa_reports)==36 and macro_calls==288',
        'blocks[167]':'blocks[169]','blocks[168]':'blocks[168]','[2,4,13,23,109]':'[2,6,9,20,21,76]',
        'len(negatives)==19':'len(negatives)==21','all27_':'all36_',
        'current_original_macro_alignment_calls=216':'current_original_macro_alignment_calls=288','actual_selected_B167_IDs':'actual_selected_B169_IDs',
        '27 complete progressive planes,216 macro cases,27 QA plans and19 source-consumer negatives pass;four sheets':'36 complete progressive planes,288 macro cases,36 QA plans and21 source-consumer negatives pass;five sheets',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_bound_profile_and_automatic_native_tools.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),
        dependencies=deps,tools=tools,source36_progressive_FI5_FO2_and_six_static_actors_bound=True,
        native216x64_four_rows_and_shared_pair_guard_metrics_unchanged=True,no_global_profile_or_waiver_change=True,
        no_ROM_registry_ledger_credit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B169 exact source profile and automatic layout/native tools prepared;no credit.')
