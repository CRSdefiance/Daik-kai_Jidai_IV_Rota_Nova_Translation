"""Test the host exit with all original nonspeech setup, effects and cleanup retained."""
from scripts.prepare_maria301_display_fixtures_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    "host_exit=[c for c in opening if c['offset']>=tail_at]":
        "host_exit=[c for c in opening if c['offset']>=first and c['word']!=0x4000]",
    "clean_exit=[c for c in clean_commands if c['offset']>=clean_tail_at]":
        "clean_exit=[c for c in clean_commands if c['offset']>=first and c['word']!=0x4000]",
    "assert host_exit[0]['whole_command_hex']=='4062'\n    assert all(c['word'] in [0x6240,0xA000,0] for c in host_exit) and host_exit[-1]['word']==0":
        """assert host_exit[0]['whole_command_hex']=='51465580'
    assert len(host_exit)==40 and host_exit[-1]['word']==0
    assert all(not c['ancestor_0100_offsets'] and c['word'] in [0x4651,0x2000,0x4620,0x0505,0x4500,0x4684,0x6008,0xA000,0x6340,0x4678,0x6240,0] for c in host_exit)""",
    'source_bound_QA_host_opening_exit=host_exit,':
        'all_original_host_nonspeech_setup_effects_andcleanup_after_first_speech_retained=True,source_bound_QA_host_opening_exit=host_exit,',
})
exec(compile(source, __file__+'::same-source-bound-fixture-keep-all-original-host-nonspeech-commands', 'exec'), globals())
