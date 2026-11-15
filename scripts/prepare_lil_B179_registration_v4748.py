"""Prepare B179 registration and atomic negatives after the entire V4701 stack."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B179_registration_tools_v4748')
assert not ROOT.exists()
source=Path('scripts/register_lil_B178_v4700b.py');text=source.read_text(encoding='utf-8')
description=next(l for l in text.splitlines(True) if l.startswith("        description='Full V4655"))
new_description="        description='Full V4701 stack plus14 B179 whole-exchange reviews:8 revisions/6 justified retentions,13 progressive/one impersonal FE,Barkeep/Patron/Sailor and separate catalog Retainer152,six read-only names,no macros,16 commands,A000 and single end,no C200. Paired9001-frame content boots show14 panels and parent return. All115 upper/name/portrait regions,five state components,whole actor/captain2,PRNG403514907 and final RGB agree;8 timings/four original A-indicator differences remain disclosed.',\n"
start=text.index("        ('missing-C200'");end=text.index("        ('lost-A000-uninterpreted-scope'",start)
new_controls="""        ('invented-C200-pair','relocated_control_proof',lambda v:v['relocated_C200_pairs'].append({})),
        ('invented-third-leaf','relocated_control_proof',lambda v:v['all2_source_current_target_nonrelative_nonspeech_leaves'].append({})),
        ('wrong-A000-source-offset','relocated_control_proof',lambda v:v['relocated_A000_structural_pairs'][0].update(source_offset=10)),
        ('lost-A000-structural-guard','relocated_control_proof',lambda v:v['relocated_A000_structural_pairs'][0].update(nondecode_effect_callee_bridged_zero_return_not_body_or_game_state_execution=False)),
"""
extra="""    mutations.extend([
        ('catalog-Sailor-overrides-Retainer','source_nameplate_consumer_proof',lambda v:v['full_catalogue_values'].update({'152':'Sailor'})),
        ('progressive-Retainer-overrides-Sailor','source_nameplate_consumer_proof',lambda v:v['progressive_nameplate_values'].update({'152':'Retainer'})),
        ('individual-progressive-name-path','source_nameplate_consumer_proof',lambda v:next(r for r in v['native_six_consumer_cases']['rows'] if r['actor_ID']==152 and r['consumer']=='progressive-nameplate').update(text='Retainer')),
    ])
"""
tool=derive(source,'scripts/register_lil_B179_v4748.py',{
    description:new_description,text[start:end]:new_controls,
    'lil_B178_editorial_v2':'lil_B179_editorial_v1','lil_B178_layout_v1':'lil_B179_layout_v1',
    'lil_B178_registration_v4700b':'lil_B179_registration_v4748',
    'lil_B178_reference_checkpoint_v4697':'lil_B179_reference_checkpoint_v4745',
    'editorial_handoff_verification_v4698':'editorial_handoff_verification_v4746',
    'lil_B178_reference_approval_v4696':'lil_B179_reference_approval_v4744',
    'lil_B178_loader_v4687':'lil_B179_loader_v4735',
    "PROFILE='all-routes-unified-v4701'":"PROFILE='all-routes-unified-v4749'",
    'all_routes_combined_v4655':'all_routes_combined_v4701',
    "registry['profiles']['all-routes-unified-v4655']":"registry['profiles']['all-routes-unified-v4701']",
    "parent_profile='all-routes-unified-v4655'":"parent_profile='all-routes-unified-v4701'",
    'all-routes-unified-v4595':'all-routes-unified-v4701',
    'build_integrated_release_v4700b.tmp':'build_integrated_release_v4748.tmp','V4655':'V4701',
    'expected_manifest_batches=554':'expected_manifest_batches=555','expected_batches=554':'expected_batches=555',
    "len(proof['changed_records'])==13":"len(proof['changed_records'])==14",'positive_records=13':'positive_records=14',
    "english='{SPEAKER:A6}Hello.'":"english='{SPEAKER:5C}Hello.'",
    "{'166':'Queen'}":"{'92':'Queen'}","{'167':'Chef'}":"{'96':'Chef'}",
    "r['actor_ID']==166":"r['actor_ID']==92","r['actor_ID']==167":"r['actor_ID']==96",
    "{'168':'Duchess'}":"{'152':'Duchess'}",'wrong-third-Lady-name':'wrong-Retainer-catalog-name',
    'actual_selected_B178_source_events=[178]':'actual_selected_B179_source_events=[179]',
    'source_A0008_C200488_single_end490_actually_executed':'source_A0008_single_end508_actually_executed_no_C200',
    "('lost-actual-C200-result',lambda v:v['versions'][0]['source_C200'].update(result_words=[3,1]))":
        "('invented-actual-C200',lambda v:v['versions'][0]['source_C200'].append({}))",
    'actual_all13_progressive_FE_A000_C200_and_single_end.json':'actual_all14_progressive_FE_A000_and_single_end_no_C200.json',
    'lost-fourth-fullscreen-sheet':'lost-fifth-fullscreen-sheet',
    "'postscene_native_state_proof'])":"'postscene_native_state_proof','separate_untranslated_city_alias_lead'])",
    '    for label,key,edit in mutations:':extra+'    for label,key,edit in mutations:',
    'lil_B178':'lil_B179','B178':'B179',
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,complete_parent_profile='all-routes-unified-v4701',new_profile='all-routes-unified-v4749',
    promoted_main_V4701_preserved=True,separate_progressive_and_catalog_name_negatives_added=True,
    source_absent_C200_rejected_instead_of_inherited_C200_tests=True,expected_manifest_batches=555,
    no_registry_builder_ROM_orledger_change_yet=True,full_goal_complete=False))
