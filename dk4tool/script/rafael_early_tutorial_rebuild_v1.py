"""Complete B42/B43 rebuild after the registered sparse Julio glyph relocation."""
import inspect
from dk4tool.script.reviewed_scene_rebuild import rebuild_block as original
from scripts.source_locked_derivation_v5118 import checked_text

SOURCE = checked_text(inspect.getsource(original), {
    '    assert old_end == clean_end and current[:8] == clean[:8]':
        '    assert current[:4] + current[6:8] == clean[:4] + clean[6:8]',
    '    assert len(current) == len(clean) and current[old_end:] == clean[clean_end:]':
        '    assert len(current) == ((old_end+3)&~3) and len(clean) == ((clean_end+3)&~3) and not any(clean[clean_end:])',
    '    patches = []':
        """    assert len(records) in (12,28)
    assert not any(c['word'] in (0x100,0x200,0x300,0x400) for c in before+source_commands)
    source_to_current = {s['offset']:c['offset'] for s,c in zip(source_commands,before,strict=True)}
    assert len(source_to_current)==len(before) and all(s['word']==c['word'] for s,c in zip(source_commands,before,strict=True))
    assert {r['source_reference']['header_offset'] for r in records} == {c['offset'] for c in source_speeches}
    patches = []""",
    '        assert at == source_at and len(previous) == len(original)':
        "        assert source_to_current[source_at-5] == at-5",
    "clean[at - 5:at + 1].hex()": "clean[source_at - 5:source_at + 1].hex()",
    "clean[at:at + len(original) + 1]": "clean[source_at:source_at + len(original) + 1]",
    "        assert command['offset'] == original['offset'] and command['word'] == original['word']":
        "        assert command['offset'] == source_to_current[original['offset']] and command['word'] == original['word']",
    'bytes(inverse) + original[old_end:]':
        'bytes(inverse) + original[clean_end if source_version else old_end:]',
})

env = {**original.__globals__, '__file__': __file__}
exec(compile(SOURCE, __file__ + '::same-complete-inverse-qualified-prior-relocation-zero-relative-scope', 'exec'), env)
rebuild_block = env['rebuild_block']
