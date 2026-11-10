"""Recognize the exact B177 legacy inter-label padding only in the current object."""
from types import FunctionType
from dk4tool.dialogue import reviewed_two_choice_object_v1 as strict
from scripts import check_rafael_B177_B180_two_choice_display_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

LEGACY_CURRENT = bytes.fromhex('002100000c005965730020002020202020204e6f0000')


def labels(raw):
    if raw == LEGACY_CURRENT:
        # The original offset table leads to Yes and No. Keep all intervening
        # bytes in the source receipt. The replacement emits strict zero alignment.
        assert raw[6:18] == b'Yes\x00 \x00      ' and raw[18:22] == b'No\x00\x00'
        return [b'Yes', b'No']
    return strict.labels(raw)


compile_choices = FunctionType(strict.compile_choices.__code__, {**vars(strict), 'labels': labels})
compile_choices.__kwdefaults__ = strict.compile_choices.__kwdefaults__

source = checked_text(previous.source, {
    'from dk4tool.dialogue.reviewed_two_choice_object_v1 import compile_choices,labels': '',
    "    target=compile_choices(source,current,rows,require_formatting=False)":
        """    assert source!=LEGACY_CURRENT
    if current==LEGACY_CURRENT:
        assert rows[0]['block']==177 and rows[0]['source_command_offset']==2278
    target=compile_choices(source,current,rows,require_formatting=False)
    assert strict.labels(target)==[row['english'].encode('ascii') for row in rows]""",
    'compiler_owned_zero_alignment_only_no_speech_encoder=True,source_index_andcount_preserved=True,':
        'compiler_owned_zero_alignment_only_no_speech_encoder=True,source_index_andcount_preserved=True,exact_legacy_current_slot_exception=(current==LEGACY_CURRENT),',
})
exec(compile(source, __file__+'::same-native-proofs-with-exact-current-only-padding-binding', 'exec'), globals())
