"""Prepare source-locked2b6 consumers,event binding and the actual B222 control shape."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B222_native_tools_v7038')
if __name__=='__main__':
    assert not ROOT.exists()
    common={
        'B221':'B222',
        'source_v6967/sixteen_clean_current_Crusades_Saladin_context_four_relative_sites_one_choice':'source_v7037/sixteen_clean_current_sunset_Noritsune_exchange_source_references',
        'current_V6956_native_v6966':'current_V7029_native_v7033',
        'Al_Ferid_exact_native_context_v6520':'square_shopkeeper_exact_native_context_v7020'}
    consumers={**common,'v6968':'v7038',
        'all14_clean_speech_glosses_and_two_labels_precede_old_English':'all16_clean_speeches_glossed_together_before_old_English',
        '[2,17,85]':'[2,16]','aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05':'2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a',
        'all_six_original_consumers_and_owned_or_readonly_memory_paths_exact':'all_four_original_consumers_and_owned_or_readonly_memory_paths_exact',
        "len(native['rows'])==6":"len(native['rows'])==4",'len(cases)==28':'len(cases)==32','len(effective)==14':'len(effective)==16',
        'all28_source_current_dispatches':'all32_source_current_dispatches','all14_current_templates':'all16_current_templates',
        'native_six_distinct_name_consumers':'native_four_distinct_name_consumers',
        'fourteen_effective_bodies28_dispatches_three_actors_six_name_consumers':'sixteen_effective_bodies32_dispatches_two_actors_four_name_consumers',
        'bodies=14,dispatches=28':'bodies=16,dispatches=32',
        'Bind three actors,six original name consumers and fourteen effective zero-macro bodies.':'Bind two actors,four original name consumers and sixteen effective zero-macro bodies.',
        '::three-actors':'::two-actors'}
    entry={**common,'v6969':'v7039','in [221]':'in [222]'}
    controls={
        'B221':'B222','v6971':'v7040',
        'source_v6967/sixteen_clean_current_Crusades_Saladin_context_four_relative_sites_one_choice':'source_v7037/sixteen_clean_current_sunset_Noritsune_exchange_source_references',
        "packet['source_relative_sites']==4 and packet['source_typed_commands']==1":"packet['source_relative_sites']==0 and packet['source_typed_commands']==0",
        'blocks[221]':'blocks[222]','1208':'1112','1204':'1108','1196':'1100','len(commands)==21':'len(commands)==18',
        '{0x4000,0x2100,0x100,0x200,0x300,0xA000,0}':'{0x4000,0xA000,0}',
        '00a0ffff47000110':'00a0ffff44000110',
        'two_A000_structural_cases50_normal_seeded_ends_choice_and_relatives_separate':'two_A000_structural_cases50_normal_seeded_ends_no_choices_or_relatives',
        'one_original2100_menu_four_relative_sites_require_separate_binding':'no_original_menu_or_relative_sites',
        'menu/four branches remain separate':'there are no source menus or relative branches',
        'Bind original opaque A000 and complete normal end separately from menu/branch behavior.':'Bind original opaque A000 and complete normal end;no source menu or relative sites.'}
    jobs=[('scripts/prove_lil_B221_consumers_v6968.py','scripts/prove_lil_B222_consumers_v7038.py',consumers),
        ('scripts/prove_lil_B221_entry_v6969.py','scripts/prove_lil_B222_entry_v7039.py',entry),
        ('scripts/prove_lil_B221_controls_v6971.py','scripts/prove_lil_B222_controls_v7040.py',controls)]
    for source,target,mapping in jobs:
        assert not Path(target).exists();checked_text(Path(source).read_text('utf8'),mapping)
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_consumers_entry_controls.json',dict(tools=[derive(*j) for j in jobs],
        exact2b6_current_helpers_required_old_AA5_guards_preserved=True,all_native_address_constants_preserved=True,
        sixteen_speeches_two_actors_no_source_menu_relative_or_C200=True,new_review_credit=0,full_goal_complete=False))
