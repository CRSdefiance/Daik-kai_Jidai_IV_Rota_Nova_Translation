"""Prepare source-exact B177 registration and atomic negative controls."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B177_registration_tools_v4654')
assert not ROOT.exists()
source=Path('scripts/register_lil_B176_v4594.py')
text=source.read_text(encoding='utf-8')
oldprior="    prior=read('work/analysis/lil_B176_reference_checkpoint_v4591/checkpoint_receipt.json')['preserved_release_files']"
newprior="""    promotion=read('work/analysis/promotion_v4651b/promotion_receipt.json')
    prior={'translations/release_stack.json':promotion['updated_files']['translations/release_stack.json'],
        'scripts/build_integrated_release.py':read('work/analysis/lil_B177_reference_checkpoint_v4641/checkpoint_receipt.json')['preserved_release_files']['scripts/build_integrated_release.py']}
    verified=read('work/analysis/editorial_handoff_verification_v4652/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']"""
old_description=next(l for l in text.splitlines(True) if l.startswith("        description='Full V4541"))
new_description="        description='Full V4595 stack plus ten B177 whole-exchange reviews:five revisions/five retentions,nine progressive/one impersonal null-actor FE,no FI/FA/FO,13 commands,one opaque A000,C200,single end. Two9001-frame content boots show all ten panels and normal town return. All115 upper/portrait/name samples,five components,whole actor/captain2 and town/final RGB agree;11 command timings,14 A-indicator RGB differences and unequal PRNG seeds remain disclosed.',\n"
extra="""    mutations.extend([
        ('hidden-indicator-difference','postscene_native_state_proof',lambda v:v['fourteen_following_A_button_indicator_animation_differences_retained_unmasked'].pop()),
        ('wrong-indicator-frame','postscene_native_state_proof',lambda v:v['fourteen_following_A_button_indicator_animation_differences_retained_unmasked'][0].update(frame=6011)),
        ('wrong-indicator-bounds','postscene_native_state_proof',lambda v:v['fourteen_following_A_button_indicator_animation_differences_retained_unmasked'][0].update(whole_frame_difference_bbox=[0,0,256,384])),
        ('invented-indicator-equality','postscene_native_state_proof',lambda v:v['fourteen_following_A_button_indicator_animation_differences_retained_unmasked'][0].update(whole_RGB_equal=True)),
        ('lost-indicator-visual-scope','postscene_native_state_proof',lambda v:v.update(fourteen_following_indicator_differences_viewed_in_representative_full_screens_and_retained=False)),
        ('hidden-PRNG-difference','postscene_native_state_proof',lambda v:v.update(PRNG_equality=True)),
        ('invented-PRNG-causal-trace','postscene_native_state_proof',lambda v:v.update(no_new_PRNG_causal_trace=False)),
        ('wrong-timing-counts','postscene_native_state_proof',lambda v:v['exact_timing_difference_counts'].update(speech=8)),
        ('wrong-exact-timing','postscene_native_state_proof',lambda v:v['actual_timing_differences'][0]['source'].update(returned=3335)),
        ('lost-third-fullscreen-sheet','postscene_native_state_proof',lambda v:v['paired_full_screen_views'].pop()),
        ('lost-town-RGB-equality','postscene_native_state_proof',lambda v:v.update(whole_RGB_town5290_through5950_and_final9001_equal=False)),
    ])
"""
tool=derive(source,'scripts/register_lil_B177_v4654.py',{
    oldprior:newprior,old_description:new_description,
    'lil_B176_editorial_v2':'lil_B177_editorial_v1','lil_B176_layout_v4':'lil_B177_layout_v3',
    'lil_B176_editorial_manuscript_v4':'lil_B177_editorial_manuscript_v6',
    'lil_B176_registration_v4594':'lil_B177_registration_v4654',
    'lil_B176_reference_approval_v4590':'lil_B177_reference_approval_v4640',
    'lil_B176_loader_v4581':'lil_B177_loader_v4631',
    'editorial_handoff_verification_v4592':'editorial_handoff_verification_v4652',
    "PROFILE='all-routes-unified-v4595'":"PROFILE='all-routes-unified-v4655'",
    'all_routes_combined_v4541':'all_routes_combined_v4595','all-routes-unified-v4541':'all-routes-unified-v4595',
    'build_integrated_release_v4594.tmp':'build_integrated_release_v4654.tmp',
    "source_A0008_C200384_single_end386_actually_executed":"source_A0008_C200480_single_end482_actually_executed",
    "actual_selected_B176_source_events=[176]":"actual_selected_B177_source_events=[177]",
    'V4541':'V4595','lil_B176':'lil_B177','B176':'B177',
    'expected_manifest_batches=552':'expected_manifest_batches=553','expected_batches=552':'expected_batches=553',
    '    for label,key,edit in mutations:':extra+'    for label,key,edit in mutations:',
    "value=deepcopy(read(path));edit(value);reject(label,positive,{str(Path(path)):value})":
        "value=deepcopy(read(path));initial=deepcopy(value);edit(value);assert value!=initial,label;reject(label,positive,{str(Path(path)):value})",
    "value=deepcopy(read(actual_path));edit(value);reject(label,positive,{str(Path(actual_path)):value})":
        "value=deepcopy(read(actual_path));initial=deepcopy(value);edit(value);assert value!=initial,label;reject(label,positive,{str(Path(actual_path)):value})",
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,complete_parent_profile='all-routes-unified-v4595',
    new_profile='all-routes-unified-v4655',measured11_timings14_indicators_and_unequal_PRNG_negative_controls_added=True,
    all_mutations_must_actually_change_the_test_object=True,offset_NUL_index_and_readonly_name_guards_preserved=True,
    no_registry_builder_ROM_orledger_change_yet=True,full_goal_complete=False))
print('Prepared B177 registration after full V4595;553 batches expected,main V4595 preserved.')
