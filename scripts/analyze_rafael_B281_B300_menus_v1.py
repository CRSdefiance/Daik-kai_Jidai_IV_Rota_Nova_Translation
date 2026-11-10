"""Verify both controller menus on the fixture with the qualified Zaganos name."""
from scripts.analyze_rafael_B261_B280_menus_v1 import PARENT, source as previous
from scripts.prepare_rafael_B281_B300_actual_v1 import NAME_PROOF, PROPOSAL
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'arm,_=plan_surnames(': 'arm,_=plan_arm9_name_fields(',
})


if __name__ == '__main__':
    from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
    exec(compile(source, __file__ + '::live-menus-with-verified-Zaganos-field', 'exec'), globals())
