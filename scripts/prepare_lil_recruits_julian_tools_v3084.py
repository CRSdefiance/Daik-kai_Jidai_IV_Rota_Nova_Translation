"""Create a new exact five-block profile and local planner; preserve prior modules."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_Recruits_Julian_tools_v3084')
PROFILE=Path('dk4tool/dialogue/lil_recruits_julian_profile.py')
LAYOUT=Path('dk4tool/dialogue/lil_recruits_julian_layout_v1.py')
SOURCE=Path('work/analysis/lil_Recruits_Julian_source_v3072/complete199_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_Recruits_Julian_controls_v3074/source_bound197_preambles_FE_and_original_conditional_predicates.json')
TERMS=Path('work/analysis/lil_Recruits_Julian_terms_v3076/clean_current_crown_Mihwa_alias_and_shipyard_UI_terms.json')
PARENT=Path('dk4tool/dialogue/lil_christina_mivor_layout_v3.py')
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,PROFILE,LAYOUT])
    source,control=map(read,[SOURCE,CONTROL])
    hashes=sorted({b[k] for b in source['blocks'] for k in ['clean_block_sha256','current_block_sha256']});assert len(hashes)==10
    selectors=[2,4,9,12,14,18,20,22,26,41,109,158]
    assert control['ordinary_native_actor_selectors']=={str(k):k for k in selectors}
    text='''"""Exact B75-B79 recruitment/Julian speech and unlabeled FE consumers."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
PROOF=Path(@CONTROL@)
PROOF_SHA=@CONTROL_SHA@
TERMS=Path(@TERMS@)
TERMS_SHA=@TERMS_SHA@
ARM9_SHA=@ARM@
BLOCKS=frozenset(@HASHES@)
SELECTORS=frozenset(@SELECTORS@)

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('Recruits/Julian requires exact reviewed B75-B79 source/runtime')
    if sha(PROOF.read_bytes())!=PROOF_SHA or sha(TERMS.read_bytes())!=TERMS_SHA:
        raise ValueError('Recruits/Julian source-control or approved terminology changed')
    proof=json.loads(PROOF.read_text(encoding='utf-8'));terms=json.loads(TERMS.read_text(encoding='utf-8'))
    if (proof['ARM9_sha256']!=ARM9_SHA or not proof['all197_complete_preambles_and394_historical_dispatch_contexts_pass']
        or len(proof['dispatch_cases'])!=394 or proof['ordinary_native_actor_selectors']!={str(k):k for k in SELECTORS}
        or len(proof['current_original_predicate_cases'])!=16 or proof['original_event_queries']
        or not proof['all1_FE_before_fallback208_use5473C_and_original24310_null_macro_actor']
        or not proof['all1_FE_source_unlabeled_ship_rename_guide_preserved_by_original_dispatcher']
        or terms['approved_item_name']!='Silla Gold Crown'
        or terms['versions'][1]['Mihwa_catalog201']['text']!='Mihwa'):
        raise ValueError('Complete ordinary, unlabeled FE and approved terminology contracts required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-recruits-julian-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+'; exactB75-B79 complete preambles and12 original ordinary54020 selectors. No new individual nameplate or earned recruitment claim; current font/reference/representative/release gates required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-recruits-julian-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+'; exact source FEbeforefallback208and5473C,original24310 null-actor unlabeled ship guide and inherited228x48mode1paper. Conservative216pxplanning; complete currentFEfont/pagination required.')
    raise ValueError('Unknown Recruits/Julian presentation consumer')
'''
    substitutions={'@CONTROL@':repr(CONTROL.as_posix()),'@CONTROL_SHA@':repr(sha(CONTROL.read_bytes())),'@TERMS@':repr(TERMS.as_posix()),'@TERMS_SHA@':repr(sha(TERMS.read_bytes())),'@ARM@':repr(source['current_ARM9_sha256']),'@HASHES@':repr(hashes),'@SELECTORS@':repr(selectors)}
    for old,new in substitutions.items():assert old in text;text=text.replace(old,new)
    assert '@' not in text
    planner=PARENT.read_text(encoding='utf-8')
    old="'lil-christina-mivor-progressive-runtime-bound-v1':frozenset({2,6,7,9,20,79,162,167})"
    new="'lil-recruits-julian-progressive-runtime-bound-v1':frozenset({2,4,9,12,14,18,20,22,26,41,109,158})"
    assert planner.count(old)==1;planner=planner.replace(old,new).replace('lil-christina-mivor-FE-runtime-bound-v1','lil-recruits-julian-FE-runtime-bound-v1').replace('Christina/Mivor','Recruits/Julian')
    anchor="PROTECTED_BOUNDARIES=frozenset({"
    assert planner.count(anchor)==1
    planner=planner.replace(anchor,anchor+"('silla','gold'),('gold','crown'),('janus','pasar'),('charles','jean'),('jean','rochefort'),('dr','charles'),('yukihisa','genjo'),('genjo','shiraki'),('luo','yuli'),('gunpowder','promptly'),('national','academy'),('of','science'),")
    compile(text,str(PROFILE),'exec');compile(planner,str(LAYOUT),'exec')
    PROFILE.write_text(text,encoding='utf-8');LAYOUT.write_text(planner,encoding='utf-8')
    ROOT.mkdir(parents=True);save(ROOT/'new_scoped_tools_provenance.json',dict(profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),layout=str(LAYOUT),layout_sha256=sha(LAYOUT.read_bytes()),
        parent_layout=str(PARENT),parent_layout_sha256=sha(PARENT.read_bytes()),dependencies={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTROL,TERMS,Path(__file__)]},
        exact_five_clean_and_current_blocks=hashes,ordinary_selectors=selectors,unlabeled_FE_selector=254,no_global_or_previous_module_change=True,no_editorial_or_completion_credit=True,full_goal_complete=False))
    print('New exact ten-hash/twelve-selector profile and batch-local planner created; prior modules preserved.')
