"""Resolve a compiled compound command by its source key, even when bodies are identical."""
def resolve(group, source_command_offset, word, expected_hex):
    objects = [o for o in group['native_objects'] if o['old_offset'] == source_command_offset and o['word'] == word]
    assert len(objects) == 1
    obj = objects[0]
    commands = [c for c in group['all_target_commands'] if c['offset'] == obj['new_offset'] and c['word'] == word]
    assert len(commands) == 1
    command = commands[0]
    assert command['whole_command_hex'] == obj['compiled_hex'] == expected_hex
    assert command['native_extent'] == len(bytes.fromhex(expected_hex))
    return command
