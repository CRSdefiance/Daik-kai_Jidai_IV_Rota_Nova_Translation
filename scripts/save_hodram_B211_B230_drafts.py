"""Keep the logical-paragraph checks while selecting ordinary speeches separately from styles."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/save_hodram_B191_B210_drafts.py').read_text(encoding='utf-8'),{
    'Hodram_B191_B210_clean_20261104':'Hodram_B211_B230_clean_20261104',
    "r.get('source_selector') is not None":"'source_complete_preamble_hex' in r",
    "            if selector == 254:\n                if block == 202:\n                    speaker = 'Unidentified Namahage voice'\n                elif block == 208:\n                    speaker = \"Jam's letter in FE panel\"\n                elif block == 209:\n                    speaker = 'Parrot or sound effect in FE panel'\n                elif original['source_Japanese'] in ['どさっ！', 'ガタッ', 'パラッパラッ']:\n                    speaker = 'Sound effect in FE panel'":
    "            if selector == 254 and block == 215:\n                speaker = 'Swan call or wing sound in FE panel'",
})
exec(compile(source,__file__+'::same-logical-source-drafts-ordinary-speeches-only','exec'),globals())
