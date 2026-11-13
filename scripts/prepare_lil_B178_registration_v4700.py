"""Prepare guarded B178 registration after the full V4655 cumulative profile."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B178_registration_tools_v4700');assert not ROOT.exists()
source=Path('scripts/register_lil_B177_v4654.py');text=source.read_text(encoding='utf-8')
a=text.index("    promotion=read(");b=text.index("    verified=read(",a)
prior="    prior=read('work/analysis/lil_B178_reference_checkpoint_v4697/checkpoint_receipt.json')['preserved_release_files']\n"
old_description=next(l for l in text.splitlines(True) if l.startswith("        description='Full V4595"))
description="        description='Full V4655 stack plus thirteen B178 whole-exchange reviews:two revisions/eleven justified retentions,twelve progressive/one impersonal FE,three static Lady actors,six read-only names,no macros,16 commands,opaque A000,C200,single end. Paired9001-frame content boots display all thirteen panels and resume the original parent. All115 upper/portrait/name regions,five state components,whole actor/captain2,PRNG3306586022 and final RGB agree;14 command timings/four original A-indicator RGB differences remain disclosed.',\n"
extra="""    mutations.extend([
        ('wrong-third-Lady-name','source_nameplate_consumer_proof',lambda v:v['full_catalogue_values'].update({'168':'Duchess'})),
        ('missing-sixth-name-consumer','source_nameplate_consumer_proof',lambda v:v['native_six_consumer_cases']['rows'].pop()),
        ('missing-final-calendar-component','postscene_native_state_proof',lambda v:v['postscene9001_native_component_equality'].pop('calendar')),
    ])
"""
tool=derive(source,'scripts/register_lil_B178_v4700.py',{
    text[a:b]:prior,old_description:description,
    'lil_B177_editorial_v1':'lil_B178_editorial_v1','lil_B177_layout_v3':'lil_B178_layout_v1',
    'lil_B177_editorial_manuscript_v6':'lil_B178_editorial_manuscript_v4',
    'lil_B177_registration_v4654':'lil_B178_registration_v4700',
    'editorial_handoff_verification_v4652':'editorial_handoff_verification_v4698',
    'lil_B177_reference_approval_v4640':'lil_B178_reference_approval_v4696',
    'lil_B177_loader_v4631':'lil_B178_loader_v4687',
    "PROFILE='all-routes-unified-v4655'":"PROFILE='all-routes-unified-v4701'",
    'all_routes_combined_v4595':'all_routes_combined_v4655',
    "registry['profiles']['all-routes-unified-v4595']":"registry['profiles']['all-routes-unified-v4655']",
    "parent_profile='all-routes-unified-v4595'":"parent_profile='all-routes-unified-v4655'",
    'build_integrated_release_v4654.tmp':'build_integrated_release_v4700.tmp','V4595':'V4655',
    'expected_manifest_batches=553':'expected_manifest_batches=554','expected_batches=553':'expected_batches=554',
    "len(proof['changed_records'])==10":"len(proof['changed_records'])==13",'positive_records=10':'positive_records=13',
    "english='{SPEAKER:AE}Hello.'":"english='{SPEAKER:A6}Hello.'",
    'actual_all10_progressive':'actual_all13_progressive',
    'native_four_consumer_cases':'native_six_consumer_cases',"{'174':'Queen'}":"{'166':'Queen'}","{'175':'Chef'}":"{'167':'Chef'}",
    "r['actor_ID']==174":"r['actor_ID']==166","r['actor_ID']==175":"r['actor_ID']==167",
    'actual_selected_B177_source_events=[177]':'actual_selected_B178_source_events=[178]',
    'source_A0008_C200480_single_end482_actually_executed':'source_A0008_C200488_single_end490_actually_executed',
    'fourteen_following_A_button_indicator_animation_differences_retained_unmasked':'sampled_postscene_whole_RGB_differences_unmasked',
    'fourteen_following_indicator_differences_viewed_in_representative_full_screens_and_retained':'all_four_following_indicator_differences_viewed_in_full_and_retained',
    "('hidden-PRNG-difference','postscene_native_state_proof',lambda v:v.update(PRNG_equality=True))":
        "('lost-PRNG-equality','postscene_native_state_proof',lambda v:v.update(PRNG_equality=False))",
    'whole_RGB_town5290_through5950_and_final9001_equal':'sampled_postscene_whole_RGB_equal_except_four_original_A_indicator_frames',
    'lost-third-fullscreen-sheet':'lost-fourth-fullscreen-sheet',
    '    for label,key,edit in mutations:':extra+'    for label,key,edit in mutations:',
    'lil_B177':'lil_B178','B177':'B178',
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,complete_parent_profile='all-routes-unified-v4655',new_profile='all-routes-unified-v4701',
    promoted_main_V4595_preserved=True,third_actor_sixth_name_and_full_five_state_component_negatives_added=True,
    actual_mutations_must_differ_and_reject_before_any_image_mutation=True,no_registry_builder_ROM_orledger_change_yet=True,full_goal_complete=False))
print('Prepared B178 positive/negative registration after full V4655;554 batches expected,main V4595 preserved.')
