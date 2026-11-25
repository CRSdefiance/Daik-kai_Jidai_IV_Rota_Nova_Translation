"""Select the repaired captions without repeating native provider checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/prepare_maria330_actual_menu_v1.py').read_text(encoding='utf-8'),{
    'scripts.meaning_maria330_clean_v1':'scripts.meaning_maria337_clean_v1',
    'menu_native_v1/menu_provider_and_planes.json':'menu_native_v2/menu_provider_and_planes.json',
    "r['block']==102 and r['source_command_offset']==210":"r['block']==136 and r['source_command_offset']==356",
    'records=rows,blocks=[102]':'records=rows,blocks=[136]',
    'B102 captions':'B136 captions',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-exact-caption-projection-no-provider-replay','exec'),globals())
