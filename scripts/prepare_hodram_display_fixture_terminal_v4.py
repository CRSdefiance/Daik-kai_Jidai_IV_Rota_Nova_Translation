"""Test the earlier qualified QA end-action command without changing production scenes."""
from scripts import prepare_hodram_B211_B230_fixtures_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "    end = rebuilt['groups'][-1]['all_target_commands'][-1]":
        """    # The full B281-B300 QA sequence used this exact source end-action command.
    clean_image=NdsImage.open('work/clean.nds')
    clean_B300=IlnkContainer.parse(clean_image.read_file(path)).blocks[300]
    clean_commands,_=inventory(clean_image.read_file('/__arm9__.bin'),clean_B300)
    current_commands,_=inventory(arm,bank[300])
    end=clean_commands[-1]
    assert end['whole_command_hex']==current_commands[-1]['whole_command_hex']=='00000080'
    assert end['native_result_hex']==current_commands[-1]['native_result_hex']=='010000000000000000000000000000000000000000000000'
    prior=load('work/Hodram_B281_B300_clean_20261107/focused_fixtures_v1/hodram_royal_ruins_beasts_and_gunpowder_fixture.json')
    prior_image=NdsImage.open(prior['research_ROM'])
    assert sha(Path(prior['research_ROM']).read_bytes())==prior['research_ROM_sha256']
    prior_B42=IlnkContainer.parse(prior_image.read_file(path)).blocks[42]
    prior_commands,_=inventory(arm,prior_B42)
    assert prior_commands[-1]['whole_command_hex']==end['whole_command_hex']
    terminal_source=dict(clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        block=300,clean_block_sha256=sha(clean_B300),clean_command=end,current_command=current_commands[-1],
        earlier_qualified_fixture='work/Hodram_B281_B300_clean_20261107/focused_fixtures_v1/hodram_royal_ruins_beasts_and_gunpowder_fixture.json',
        earlier_qualified_fixture_sha256=sha(Path('work/Hodram_B281_B300_clean_20261107/focused_fixtures_v1/hodram_royal_ruins_beasts_and_gunpowder_fixture.json').read_bytes()))""",
    "            original_initializers=[c for c in opening if c['offset'] < first], menus=menus,":
        """            original_initializers=[c for c in opening if c['offset'] < first], menus=menus,
            QA_only_end_action_command_source=terminal_source,
            original_production_scene_controls_not_changed=True,
            QA_terminal_contract_observation_pending=True,""",
})
exec(compile(source,__file__+'::same-complete-native-commands-source-qualified-QA-terminal-test','exec'),globals())
