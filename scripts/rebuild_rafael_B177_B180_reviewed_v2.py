"""Reuse full native relocation with the qualified B177 legacy current reader."""
from pathlib import Path
from types import FunctionType

from dk4tool.script import reviewed_scene_rebuild_with_fu_andcompounds_v1 as normal
from scripts.check_rafael_B177_B180_two_choice_display_v2 import LEGACY_CURRENT, labels
from scripts.rebuild_rafael_B177_B180_reviewed_v1 import compile_bound_choices, source as previous
from scripts.source_locked_derivation_v5118 import checked_text

TEMPLATE = Path('scripts/rebuild_reviewed_editorial_batch_v4.py')
FIRST_ATTEMPT = Path('scripts/rebuild_rafael_B177_B180_reviewed_v1.py')
original = normal.rebuild_block
verify = original.__globals__['verify_compound']
legacy_verify = FunctionType(verify.__code__, {**verify.__globals__, 'labels': labels})


def verify_compound(word, source, current, target):
    if current != LEGACY_CURRENT:
        return verify(word, source, current, target)
    assert source != LEGACY_CURRENT and target != LEGACY_CURRENT and word == 0x2100
    return legacy_verify(word, source, current, target)


rebuild_bound_block = FunctionType(original.__code__,
    {**original.__globals__, 'verify_compound':verify_compound}, argdefs=original.__defaults__)
source = checked_text(previous, {
    'from dk4tool.script.reviewed_scene_rebuild_with_fu_andcompounds_v1 import rebuild_block': '',
    "        target,proof=rebuild_block(arm,clean,current,records,compiled,inventory,compound)":
        """        legacy=[row for row in compound if bytes.fromhex(row['current_hex'])==LEGACY_CURRENT]
        assert len(legacy)==int(block==177)
        if legacy:
            assert legacy[0]['id']=='B177_C2278_menu' and legacy[0]['offset']==2278
        target,proof=rebuild_bound_block(arm,clean,current,records,compiled,inventory,compound)""",
    'producers={str(p):sha(p.read_bytes()) for p in [TEMPLATE,Path(__file__),':
        'producers={str(p):sha(p.read_bytes()) for p in [TEMPLATE,FIRST_ATTEMPT,Path(__file__),',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::exact-current-only-choice-compatibility','exec'),globals())
