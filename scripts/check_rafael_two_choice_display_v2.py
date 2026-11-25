"""Read complete provider labels within the supplied native object's own bounds.

The older host diagnostic sampled only32 bytes, truncating a34-byte Japanese
caption despite the original getter returning its correct pointer and width.
Native instructions, provider/return checks, canaries and display limits stay
unchanged. Use this successor only where that concrete limitation was found.
"""
from scripts.check_rafael_two_choice_display import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    "    adapter=load(PRECEDENT)['source_owned_VM_adapter']":
        """    adapter=checked_text(load(PRECEDENT)['source_owned_VM_adapter'], {
        "        label = bytes(cpu.mem_read(pointer, 32)).split(b'\\\\0')[0]":
            "        assert text <= pointer < text + len(object_bytes)\\n        remaining = text + len(object_bytes) - pointer\\n        complete = bytes(cpu.mem_read(pointer, remaining))\\n        assert b'\\\\0' in complete\\n        label = complete.split(b'\\\\0')[0]",
    })""",
})
exec(compile(source, __file__+'::same-native-provider-complete-object-bounded-host-label-read', 'exec'), globals())
