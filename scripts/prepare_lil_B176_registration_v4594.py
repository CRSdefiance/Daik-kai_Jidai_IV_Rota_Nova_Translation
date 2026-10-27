"""Prepare positive and atomic-negative B176 registration after the full V4541 stack."""
import re
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B176_registration_tools_v4594')
assert not ROOT.exists()
source=Path('scripts/register_lil_B175_v4540b.py')
text=source.read_text(encoding='utf-8')
replacements={
    'lil_B175_editorial_v2':'lil_B176_editorial_v2','lil_B175':'lil_B176','B175':'B176',
    'registration_v4540b':'registration_v4594',
    "PROFILE='all-routes-unified-v4541'":"PROFILE='all-routes-unified-v4595'",
    'all_routes_combined_v4496':'all_routes_combined_v4541',
    'reference_checkpoint_v4537':'reference_checkpoint_v4591',
    'all-routes-unified-v4496':'all-routes-unified-v4541',
    'lil_B175_layout_v1':'lil_B176_layout_v4',
    'reference_approval_v4536':'reference_approval_v4590',
    'loader_v4527':'loader_v4581','editorial_handoff_verification_v4538':'editorial_handoff_verification_v4592',
    "len(proof['changed_records'])==32":"len(proof['changed_records'])==10",
    "english='{SPEAKER:02}Hello.'":"english='{SPEAKER:AE}Hello.'",
    'actual_all32_progressive_FE_controls_C200_and_first_end':'actual_all10_progressive_FE_A000_C200_and_single_end',
    'build_integrated_release_v4540b.tmp':'build_integrated_release_v4594.tmp',
    'V4496':'V4541','expected_manifest_batches=551':'expected_manifest_batches=552',
    'positive_records=32':'positive_records=10','expected_batches=551':'expected_batches=552',
}
def mutation(label,new):
    pattern=r"(?m)^        \('"+re.escape(label)+r"',.*\n"
    matches=re.findall(pattern,text)
    assert len(matches)==1,label
    replacements[matches[0]]='        '+new+'\n'
mutation('missing-second-end',"('missing-single-end','reference_map',lambda v:v['blocks'][0]['original_declared_end_word_maps'].pop()),")
mutation('wrong-second-end-map',"('wrong-single-end-map','reference_map',lambda v:v['blocks'][0]['original_declared_end_word_maps'][0].update(target_offset=398)),")
mutation('wrong-resource-boundary',"('wrong-A000-boundary','reference_map',lambda v:next(r for r in v['blocks'][0]['mapped_native_commands'] if r['word']==0xA000).update(new_offset=10)),")
mutation('wrong-C200-offset',"('wrong-C200-offset','relocated_control_proof',lambda v:v['relocated_C200_pairs'][0].update(target_offset=400)),")
mutation('lost-resource-proof',"('lost-A000-uninterpreted-scope','relocated_control_proof',lambda v:v.update(source_A000_packed_operand_semantics_not_inferred=False)),")
mutation('wrong-Camille-name',"('wrong-Owner-role','source_nameplate_consumer_proof',lambda v:v['approved_prose_names'].update({'174':'Queen'})),")
mutation('wrong-Camille-full-name',"('wrong-Cook-catalogue','source_nameplate_consumer_proof',lambda v:v['full_catalogue_values'].update({'175':'Chef'})),")
mutation('lost-owned-name-path',"('invented-readonly-scratch','source_nameplate_consumer_proof',lambda v:next(r for r in v['native_four_consumer_cases']['rows'] if r['actor_ID']==174).update(original_scratch_rings=[{}])),")
mutation('invented-readonly-writes',"('invented-readonly-writes','source_nameplate_consumer_proof',lambda v:next(r for r in v['native_four_consumer_cases']['rows'] if r['actor_ID']==175).update(original_getter_writes=[{}])),")
mutation('natural-event-claim',"('natural-event-claim','representative_proof',lambda v:v.update(actual_selected_B176_source_events=[176])),")
mutation('invented-all-nontext-equal',"('wrong-nontext-count','postscene_native_state_proof',lambda v:v.update(nontext_equal_samples=114)),")
mutation('hide-final-RGB-limit',"('lost-final-RGB-equality','postscene_native_state_proof',lambda v:v.update(whole_RGB_final9001_equal=False)),")
mutation('lost-native-state-equality',"('lost-native-state-equality','postscene_native_state_proof',lambda v:v['postscene9001_native_component_equality'].update(state=False)),")
mutation('lost-second-end-offline-scope',"('lost-actual-source-control-scope','postscene_native_state_proof',lambda v:v.update(source_A0008_C200384_single_end386_actually_executed=False)),")
mutation('wrong-timing-scope',"('wrong-timing-scope','postscene_native_state_proof',lambda v:v['actual_timing_differences'].append({})),")
mutation('wrong-actual-first-end',"('wrong-actual-single-end','actual',lambda v:v['versions'][0]['selected_B22_command_pairs'][-1].update(original_source_offset=400)),")
mutation('wrong-actual-presentation',"('wrong-actual-A000-word','actual',lambda v:v['versions'][0]['source_A000'][0].update(word=0xA001)),")
mutation('wrong-actual-resource',"('wrong-actual-A000-extent','actual',lambda v:v['versions'][0]['source_A000'][0].update(extent=7)),")
mutation('false-actual-claim',"('false-actual-claim','actual',lambda v:v.update(complete_matching_observations=9)),")
# Actual-proof cases are two-tuples in the template; preserve that interface.
for key,value in list(replacements.items()):
    if "'actual',lambda" in value:
        replacements[key]=value.replace("'actual',lambda","lambda")
start=text.index('    mutations.extend([\n        (\'lost-FI\'')
end=text.index('    for label,key,edit in mutations:',start)
replacements[text[start:end]]="""    mutations.extend([
        ('missing-A000-structural-pair','relocated_control_proof',lambda v:v['relocated_A000_structural_pairs'].pop()),
        ('lost-future-world-limit','postscene_native_state_proof',lambda v:v.update(future_world_equivalence_and_full_RAM_equality_not_claimed=False)),
        ('wrong-PRNG-scope','postscene_native_state_proof',lambda v:v.update(postscene9001_PRNG_seeds=[0,0])),
    ])
"""
start=text.index("        description='Full V4496")
end=text.index("        note=",start)
replacements[text[start:end]]="        description='Full V4541 stack plus ten B176 whole-exchange reviews:five revisions/five retentions,nine progressive/one impersonal null-actor FE,no FI/FA/FO,13 commands,one opaque A000,C200,single end. Two9001-frame content boots display all ten panels and reach the end/town return;all115 nontext samples,22 command timings and final native state/PRNG agree.',\n"
tool=derive(source,'scripts/register_lil_B176_v4594.py',replacements)
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,complete_parent_profile='all-routes-unified-v4541',
    new_profile='all-routes-unified-v4595',offset_NUL_index_guards_and_readonly_names_preserved=True,
    no_registry_builder_ROM_ledger_change_yet=True,full_goal_complete=False))
