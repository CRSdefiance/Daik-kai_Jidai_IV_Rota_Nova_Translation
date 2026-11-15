"""Keep capacity and initializer guards; resolve compound occurrences by exact source keys."""
from scripts import prepare_hodram_display_fixtures_bounded_v1 as previous
from scripts.source_scoped_fixture_command_v1 import resolve
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    "command=next(c for c in group['all_target_commands'] if c['whole_command_hex']==raw.hex())":
        "command=resolve(group,request['source_command_offset'],0x4100,raw.hex())",
    "command = next(c for c in groups[request['block']]['all_target_commands'] if c['whole_command_hex'] == proof['target_object_hex'])":
        "command = resolve(groups[request['block']],request['source_command_offset'],int.from_bytes(bytes.fromhex(proof['target_object_hex'])[:2],'little'),proof['target_object_hex'])",
})
exec(compile(source, __file__+'::same-source-bound-capacity-guard-and-unambiguous-command-occurrences', 'exec'), globals())
