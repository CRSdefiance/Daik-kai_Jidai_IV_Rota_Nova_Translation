"""Create exact-source variable-selector formatting tools without global edits."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B111_B119_tools_v3226')
PROFILE=Path('dk4tool/dialogue/lil_B111_B119_profile.py')
LAYOUT=Path('dk4tool/dialogue/lil_B111_B119_layout_v1.py')
PARENT=Path('dk4tool/dialogue/lil_shrines_temples_layout_v2.py')
SOURCE=Path('work/analysis/lil_B111_B119_source_v3217b/complete150_reachable_Lil_clean_current_context.json')
CONTROL=Path('work/analysis/lil_B111_B119_controls_v3219/all150_source_current_dispatch_variable_styles_predicates_and_query.json')
VOICES=Path('work/analysis/lil_B111_B119_voices_v3218/current207_catalog_eight_voices_and_CF_D0_D1_D6_D7_DC_roles.json')
TERMS=Path('work/analysis/lil_B111_B119_terms_v3220/clean_current_items_and_native_actor_role_reconciliation.json')
CLASSIFICATION=Path('work/analysis/lil_B115_tail_classification_v3216/source_return0_graph_and_canonical_Maria_copy_classification.json')
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,PROFILE,LAYOUT])
    source,control=map(read,[SOURCE,CONTROL])
    hashes=sorted({b[k] for b in source['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    selectors=sorted({r['source_selector'] for r in source['records']+source['typed_actor_style_records'] if r['source_selector']!=254})
    assert len(hashes)==18 and selectors==[2,4,9,14,19,20,104,137,163,170,179,198,207,208,209,214,215,220]
    deps={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTROL,VOICES,TERMS,CLASSIFICATION,Path(control['registered_catalog_binding'])]}
    text='''"""Exact nine-block Lil prose/FE and five variable actor-style selectors."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA=@ARM@
BLOCKS=frozenset(@HASHES@)
SELECTORS=frozenset(@SELECTORS@)
DEPENDENCIES=@DEPS@
CONTROL=Path(@CONTROL@)
VOICES=Path(@VOICES@)
CLASSIFICATION=Path(@CLASSIFICATION@)
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('B111-B119 requires exact nine clean/current blocks andruntime')
    for p,digest in DEPENDENCIES.items():
        if sha(Path(p).read_bytes())!=digest:raise ValueError('B111-B119 source contract changed:'+p)
    control=json.loads(CONTROL.read_text(encoding='utf-8'))
    voices=json.loads(VOICES.read_text(encoding='utf-8'))
    classification=json.loads(CLASSIFICATION.read_text(encoding='utf-8'))
    if (len(control['speech_and_stored_alternative_dispatch_cases'])!=300
        or len(control['whole_original4100_command_cases'])!=12
        or len(control['all207_actor_style_source_pointer_cases']['cases'])!=2484
        or len(control['current_original_predicate_cases'])!=16
        or len(control['original_event_queries'])!=1
        or control['original_event_queries'][0]['event']!=319
        or not control['one_FE_before_dynamic_fallback208_uses5473C_and24310_null_actor']
        or not voices['all_six_dynamic_selectors_bind_actual_current_original_roles_without_assignment']
        or len(voices['catalog']['rows'])!=207
        or not classification['all12_original_VM_return0_cases_stop_before_cursor_advance']):
        raise ValueError('Complete variable-role/source dispatch/predicate/query/copy contract required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B111-B119-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';exact9blocks/116speech/34actor-stylebodies. VirtualD0/D1/D6/D7/DCprefixmatchesreal4100header andmustnotbestoredinbody;preserve48slots/aliases and20byteheaders. CFcaptain/currentunassignedrolefallback boundwithoutassignment. Unowned32Maria copy excludedfromformatting andpreservedbyteforbyte.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B111-B119-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';oneFE24000goldnotice;originalnullactor24310then5473Cbeforefallback208. Calibrated228x48logical/228x64physical mode1paper,conservative216pxplanning. No inventedname,macro orleadingblankline.')
    raise ValueError('Unknown B111-B119 consumer')
'''
    substitutions={'@ARM@':repr(source['current_ARM9_sha256']),'@HASHES@':repr(hashes),
        '@SELECTORS@':repr(selectors),'@DEPS@':repr(deps),'@CONTROL@':repr(CONTROL.as_posix()),
        '@VOICES@':repr(VOICES.as_posix()),'@CLASSIFICATION@':repr(CLASSIFICATION.as_posix())}
    for old,new in substitutions.items():assert old in text;text=text.replace(old,new)
    planner=PARENT.read_text(encoding='utf-8')
    old="'lil-shrines-temples-progressive-runtime-bound-v1':frozenset({2,9,16,20,139,151,160,177,178,191,207,208})"
    new="'lil-B111-B119-progressive-runtime-bound-v1':frozenset({2,4,9,14,19,20,104,137,163,170,179,198,207,208,209,214,215,220})"
    assert planner.count(old)==1
    planner=planner.replace(old,new).replace('lil-shrines-temples-FE-runtime-bound-v1','lil-B111-B119-FE-runtime-bound-v1').replace('Shrines/Temples','B111-B119')
    anchor='PROTECTED_BOUNDARIES=frozenset({';assert planner.count(anchor)==1
    pairs=[('cargo','hold'),('stone','tablet'),('source','of'),('of','hope'),('gold','coins'),("grandson's",'life')]
    planner=planner.replace(anchor,anchor+','.join(repr(p) for p in pairs)+',')
    compile(text,str(PROFILE),'exec');compile(planner,str(LAYOUT),'exec')
    PROFILE.write_text(text,encoding='utf-8');LAYOUT.write_text(planner,encoding='utf-8')
    ROOT.mkdir(parents=True)
    save(ROOT/'source_bound_tools_provenance.json',dict(profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),
        formatter=str(LAYOUT),formatter_sha256=sha(LAYOUT.read_bytes()),parent_formatter=str(PARENT),
        parent_formatter_sha256=sha(PARENT.read_bytes()),dependencies=deps,source_selectors=selectors,
        actual_virtual_style_prefixes=['d0','d1','d6','d7','dc'],protected_new_source_phrases=pairs,
        no_global_helper_or_previous_profile_modified=True,full_native_planes_and_format_approval_pending=True,
        source_prose_or_completion_credit_added=0,new_emulator_runs=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Exact9block profile/18selectors andnewlocal formatter created;5realvirtualstyleprefixes. Globalhelpers/previousprofiles unchanged.')
