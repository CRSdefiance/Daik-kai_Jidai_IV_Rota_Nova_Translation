"""Derive exact same-runtime loader/caller audits for the resized B46 archive."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B46_reference_tools_v7942');assert not root.exists();rows=[]
    rows.append(derive('scripts/verify_Rafael_B45_loaders_v7888.py','scripts/verify_Rafael_B46_loaders_v7942.py',{
        'scripts.create_Rafael_B45_reference_v7887':'scripts.create_Rafael_B46_reference_v7941',
        'Rafael_B45_loaders_v7888':'Rafael_B46_loaders_v7942',
        'Rafael_B45_reference_v7887':'Rafael_B46_reference_v7941',
        'exact_B45_header':'exact_B46_header',
    }))
    rows.append(derive('scripts/verify_Rafael_B45_references_v7889.py','scripts/verify_Rafael_B46_references_v7943.py',{
        'Fresh shipped caller census and exact twenty-four command/five relative maps.':'Fresh shipped caller census andexact37 command/four relative/two-choice maps.',
        'scripts.create_Rafael_B45_reference_v7887':'scripts.create_Rafael_B46_reference_v7941',
        'Rafael_B45_reference_census_v7889':'Rafael_B46_reference_census_v7943',
        'Rafael_B45_current_v7871/all12_complete_source_current_refs_before_new_English_manuscript.json':'Rafael_B46_current_v7927/all24_speeches2_choices_source_current_refs_before_new_English_manuscript.json',
        'Rafael_B45_loaders_v7888':'Rafael_B46_loaders_v7942',
        'Rafael_B45_relocated_controls_v7886/12_stored_dispatches25_relocated_relative_cases_predicate25_seeded_ends.json':'Rafael_B46_relocated_controls_v7940/24_stored_dispatches_two_choices20_relative_cases25_seeded_ends.json',
        'bank[45]':'bank[46]',
        "cg['block']==tg['block']==45":"cg['block']==tg['block']==46",
        "source['word'] not in [0x4000,0x100,0x200,0x300,0x400]":"source['word'] not in [0x4000,0x2100,0x100,0x200,0x300,0x400]",
        "        rows.append(deepcopy(m))":"        if source['word']==0x2100:\n            choice=tg['choice_commands'][0]\n            assert source['whole_command_hex']==choice['clean_hex'] and before['whole_command_hex']==choice['old_hex'] and after['whole_command_hex']==choice['target_hex']\n            assert len(choice['label_references'])==2\n        rows.append(deepcopy(m))",
        'len(rows)==24':'len(rows)==37',
        "len(tg['relative_fixups'])==5 and sum(len(r['cases']) for r in tg['relocated_skip_cases'])==25":"len(tg['relative_fixups'])==4 and sum(len(r['cases']) for r in tg['relocated_skip_cases'])==20",
        "len(controls['final_dispatches'])==12":"len(controls['final_dispatches'])==24",
        'all24_commands_five_relative_sites_EV0_entry_shipped_callers.json':'all37_commands_four_relative_sites_two_choices_EV0_entry_shipped_callers.json',
        "file_path=mapping['file_path'],block=45":"file_path=mapping['file_path'],block=46",
        "all12_text_records=deepcopy(tg['text_records'])":"all24_text_records=deepcopy(tg['text_records']),typed_choice_records=deepcopy(tg['choice_commands'])",
        'all24_source_current_target_commands_and5_relative_sites_bound_to_research_ROM':'all37_source_current_target_commands_four_relative_sites_andtwo_choices_bound_to_research_ROM',
        'all12_sixbyte_preambles_including_source00_FE_andcomplete_fourbyte_end_preserved':'all24_sixbyte_preambles_including_source00_FE_andcomplete_fourbyte_end_preserved',
        'source_event45_action46_empty_explicit_dependencies_not_natural_eligibility':'source_event46_action47_requires38_not_natural_eligibility',
        '24 mapped commands/five relative sites25cases,one original EV0 block entry andfresh shipped caller census pass;343loads686parent modes bound. Actual/policy/registered integration pending.':'37 mapped commands/four relative sites20 cases/two choices,original EV0 entry andfresh shipped caller census pass;343 loads686 parentmodes bound. Actual/policy/release pending.',
    }))
    root.mkdir(parents=True);save(root/'source_locked_derivations.json',rows)
