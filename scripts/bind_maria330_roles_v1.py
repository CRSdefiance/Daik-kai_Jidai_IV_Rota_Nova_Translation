"""Retain the original unassigned role/voice dispatcher for the five Maria330 selectors."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/bind_maria328_roles_v1.py').read_text(encoding='utf-8'),{
    'from scripts.meaning_maria328_clean_v1 import ROOT':'from scripts.meaning_maria330_clean_v1 import ROOT',
    'assert len(records) == 38 and selectors == [207,208,214,215]':'assert len(records) == 37 and selectors == [207,208,209,214,220]',
    'all14_ordinary_and24_physical_style_references_bound':'all2_ordinary_and35_physical_style_references_bound',
    'no_static_actor207_208_214_215_lookup':'no_static_actor207_208_209_214_220_lookup',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-source-owned-native-role-dispatch-guards330','exec'),globals())
