"""Keep the complete SC3 loader/cache and parent-handoff guards for the26-block reconstruction."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/check_maria301_loaders_v1.py').read_text(encoding='utf-8'),{
    'work/Maria_B0_B32_clean_20261109':'work/Maria_B96_B124_clean_20261109',
    "ROOT/'stored_reconstruction_v1/reconstruction.json'":"ROOT/'reconstruction_v2/reconstruction.json'",
    "len(rebuilt['changed_blocks']) == 32":"rebuilt['changed_blocks'] == [96,98,99,100,101,102,103,104,105,106,107,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124]",
    'Maria301-stored-research':'Maria330-stored-research',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-full-native-SC3-load-cache-andparent-guards330','exec'),globals())
