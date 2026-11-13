"""Retain the QA host opening's source-bound cleanup instead of an unrelated scene exit."""
from scripts import prepare_hodram_B211_B230_fixtures_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "    speeches = [r for r in doc['records']":
        """    host_exit=opening[-2:]
    assert [c['word'] for c in host_exit]==[0xC200,0]
    clean_image=NdsImage.open('work/clean.nds')
    clean_opening=IlnkContainer.parse(clean_image.read_file(path)).blocks[42]
    clean_commands,_=inventory(clean_image.read_file('/__arm9__.bin'),clean_opening)
    assert [c['whole_command_hex'] for c in host_exit]==[c['whole_command_hex'] for c in clean_commands[-2:]]
    assert host_exit[-1]['whole_command_hex']=='00000000'
    host_exit_bytes=b''.join(bytes.fromhex(c['whole_command_hex']) for c in host_exit)
    speeches = [r for r in doc['records']""",
    "        logical += bytes.fromhex(end['whole_command_hex'])":
        "        logical += host_exit_bytes",
    "            original_initializers=[c for c in opening if c['offset'] < first], menus=menus,":
        """            original_initializers=[c for c in opening if c['offset'] < first], menus=menus,
            source_bound_QA_host_opening_exit=host_exit,source_bound_QA_host_exit_hex=host_exit_bytes.hex(),
            clean_andregistered_host_exit_commands_identical=True,
            original_optional_scene_exit_not_relocated_into_QA_host=True,
            exit_transition_requires_fresh_emulator_observation=True,""",
})
exec(compile(source,__file__+'::same-complete-display-commands-with-exact-host-opening-cleanup','exec'),globals())
