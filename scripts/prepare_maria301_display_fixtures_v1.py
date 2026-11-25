"""Copy reviewed commands behind Maria's own source-bound initialization and cleanup."""
from scripts import prepare_reviewed_dialogue_fixtures_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    'work/analysis/Rafael_early_tutorial_B42_B43_clean_20261104/ordinary_Rafael_NewGame_inputs_v1.json':
        'work/Maria_current_context_20261109_v1/ordinary_inputs.json',
    "path == '/data/SC0.DK4'": "path == '/data/SC3.DK4'",
    'bank[44]': 'bank[33]',
    'changed[44]': 'changed[33]',
    "first == 40 and len([c for c in opening if c['offset'] < first]) == 10":
        "first == 34 and len([c for c in opening if c['offset'] < first]) == 7",
    "    speeches = [r for r in doc['records']":
        """    clean_image=NdsImage.open('work/clean.nds')
    clean_block=IlnkContainer.parse(clean_image.read_file(path)).blocks[33]
    clean_commands,clean_texts=inventory(clean_image.read_file('/__arm9__.bin'),clean_block)
    assert clean_block[:4]==bank[33][:4] and clean_block[6:first]==bank[33][6:first]
    tail_at=texts[-1]['offset']+texts[-1]['native_extent']
    clean_tail_at=clean_texts[-1]['offset']+clean_texts[-1]['native_extent']
    host_exit=[c for c in opening if c['offset']>=tail_at]
    clean_exit=[c for c in clean_commands if c['offset']>=clean_tail_at]
    assert [c['whole_command_hex'] for c in host_exit]==[c['whole_command_hex'] for c in clean_exit]
    assert host_exit[0]['whole_command_hex']=='4062'
    assert all(c['word'] in [0x6240,0xA000,0] for c in host_exit) and host_exit[-1]['word']==0
    host_exit_bytes=b''.join(bytes.fromhex(c['whole_command_hex']) for c in host_exit)
    speeches = [r for r in doc['records']""",
    "r['expanded_hex'] for r in [*stored['records'],*stored['style_records']]":
        "(r['stored_hex'] if r.get('virtual_prefix_not_stored') else r['expanded_hex']) for r in [*stored['records'],*stored['style_records']]",
    "        logical += bytes.fromhex(end['whole_command_hex'])": '        logical += host_exit_bytes',
    '        block = bytes(logical)+bytes(-len(logical) % 4)':
        "        block = bytes(logical)+bytes(-len(logical) % 4)\n        assert len(block)<=0x2400,('Oversized native QA buffer',spec['name'],len(block))",
    'controls = load(ORDINARY)+': "controls = [r for r in load(ORDINARY) if r['start']<4000]+",
    'no_savestate_battery_RAM_roster_money_RNG_eventflag_orcondition_result_override=True,':
        'no_savestate_RAM_roster_money_RNG_eventflag_orcondition_result_override=True, preexisting_system_only_unlock_required_not_earned=True,',
    '            original_initializers=[c for c in opening if c[\'offset\'] < first], menus=menus,':
        """            original_initializers=[c for c in opening if c['offset'] < first], menus=menus,
            source_bound_QA_host_opening_exit=host_exit,source_bound_QA_host_exit_hex=host_exit_bytes.hex(),
            clean_andregistered_host_prefix_andexit_commands_identical=True,
            padded_QA_block_bytes=len(block),source_bound_QA_block_limit=9216,
            QA_block_inside_original_stack_buffer=True,""",
})
exec(compile(source, __file__+'::same-native-command-fixtures-own-Maria-prefix-tail-andinputs', 'exec'), globals())
