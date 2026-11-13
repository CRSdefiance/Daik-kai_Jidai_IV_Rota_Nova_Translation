"""Use Lil's clean-identical B22 setup and complete exit for bounded samples."""
from scripts.prepare_maria270_display_fixtures_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'work/Maria_current_context_20261109_v1/ordinary_inputs.json':
        'work/Lil382_residual_A_clean_20261110/current_context_v1/ordinary_Lil_inputs.json',
    '/data/SC3.DK4': '/data/SC2.DK4',
    'bank[33]': 'bank[22]',
    '.blocks[33]': '.blocks[22]',
    'first == 34 and len([c for c in opening if c[\'offset\'] < first]) == 7':
        'first == 56 and len([c for c in opening if c[\'offset\'] < first]) == 9',
    "host_exit[0]['whole_command_hex']=='51465580'": "host_exit[0]['whole_command_hex']=='2a63'",
    'len(host_exit)==40': 'len(host_exit)==32',
    '[0x4651,0x2000,0x4620,0x0505,0x4500,0x4684,0x6008,0xA000,0x6340,0x4678,0x6240,0]':
        '[0x632a,0x4621,0x2000,0x6314,0x6311,0x4679,0x4635,0x632c,0x4620,0x623d,0x4631,0x6116,0x050a,0x4678,0x600a,0x6312,0x4660,0xA000,0xC200,0]',
    'changed[33] = block': 'changed[22] = block',
    'preexisting_system_only_unlock_required_not_earned=True': 'preexisting_system_only_unlock_required_not_earned=False',
})
exec(compile(source, __file__+'::same-source-commands-roles-allocation-andparent-inverse-guards', 'exec'), globals())
