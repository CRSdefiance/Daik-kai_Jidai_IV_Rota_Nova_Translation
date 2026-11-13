"""Reuse current catalogue binding for any clean-first batch, retaining typed menus."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/extract_editorial_current.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    "    ap.add_argument('--out', type=Path, required=True)":
    """    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--release', type=Path, required=True)
    ap.add_argument('--startup', type=Path, required=True)""",
    "assert meanings['clean_meanings'] == 144 and meanings['earlier_English_dialogue_unconsulted']":
        "assert meanings['meanings'] == len(meanings['records']) and meanings['earlier_English_unconsulted']",
    "    ctx = RegisteredRuntime('work/analysis/Hodram_Julio_release_verified_20261101/registered_release_verification.json',\n                            'work/analysis/Hodram_Julio_release_verified_20261101/own_registered_startup_verification.json')":
    """    meanings['groups'] = [dict(block=group['block'],records=[row for row in meanings['records']
        if row['block']==group['block']]) for group in packet['groups']]
    ctx = RegisteredRuntime(args.release,args.startup)""",
    "elif source['word'] in (0x100, 0x200, 0x300, 0x400):":
        "elif source['word'] in (0x100, 0x200, 0x300, 0x400, 0x2100):",
    'original_current_catalogue_lookups=144':"original_current_catalogue_lookups=meanings['meanings']",
    "print('144 current stored/effective records bound after complete clean meanings; no new credit.')":
        "print(meanings['meanings'],'current records bound after complete clean meanings;typed menu bodies retained for separate comparison;no credit.')",
})
exec(compile(source,__file__+'::same-native-catalogue-binding','exec'),globals())
