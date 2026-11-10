"""Preserve v1 positive andfreeze explicit original-event andmap-identity guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/maria_story_production_tools_v7775b');assert not root.exists()
    anchor="    require(len(branches['operands_requiring_adjustment_when_resizing'])==20,'all original branch operands')"
    addition=anchor+"""
    require(len(branches['native_cases'])==200 and branches['complete_nested0100_and0200_0300_branch_targets_are_mapped_native_boundaries'],'source/current native branch coverage')
    entry=load(p['source_entry_proof']);sourcepacket=load(p['clean_source_exchanges'])
    require(entry['source_completion_dependency_chain']==[34,108,35] and len(entry['native_predicate_cases'])==10,'source dependency chain/predicate coverage')
    require([(e['event_ID'],e['action_index'],e['script_block'],e['must_be_completed'],e['must_not_be_completed']) for e in entry['selected_source_events']]==[(34,35,34,[],[]),(35,36,35,[108],[]),(108,109,108,[34],[])],'original EV3 actions/prerequisites')
    require(sha(image.read_file('/data/EV3.DK4'))==sourcepacket['EV3_sha256'] and image.read_file('/data/EV3.DK4')==clean.read_file('/data/EV3.DK4'),'original EV3 file')
    require(entry['existing_system_only_unlock_fixture'] and entry['earned_unlock_verified'] is False and entry['no_predicate_completion_flag_actor_roster_orRNG_forcing'],'entry eligibility/unlock limits')
    for group in mapping['groups']:
        cg=next(g for g in census['groups'] if g['block']==group['block'])
        pg=next(g for g in packet['groups'] if g['block']==group['block'])
        require(group['source_header_hex']==pg['current_header_hex'] and group['target_header_hex']==cg['target_header_hex'],'exact source/target header metadata')
        require(group['command_map']==cg['all_command_maps'] and group['relative_fixups']==cg['relative_operand_maps'],'all sealed mapped commands/relatives')
"""
    a=derive('dk4tool/patch/maria_story_editorial_v1.py','dk4tool/patch/maria_story_editorial_v2.py',{
        anchor:addition,
        "    require(doc['records']==approved['records']":"    require(all(g['approved_manuscript']==doc['native_approved_manuscript'] and g['approved_manuscript_sha256']==doc['native_approved_manuscript_sha256'] for g in mapping['groups']),'map approved-manuscript identity')\n    require(doc['records']==approved['records']",
    })
    b=derive('scripts/validate_Maria_story_atomic_v7775.py','scripts/validate_Maria_story_atomic_v7775b.py',{
        'maria_story_editorial_v1':'maria_story_editorial_v2','maria_story_atomic_v7775':'maria_story_atomic_v7775b',
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivations=[a,b],
        original_v1_positive_andall_source_numeric_guards_preserved=True,
        explicit_original_EV3_dependency_actions_predicates_unlock_andmap_header_census_identity_checks_added=True,
        new_credit=0,full_goal_complete=False))
